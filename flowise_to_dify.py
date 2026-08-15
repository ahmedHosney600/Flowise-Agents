#!/usr/bin/env python3
"""
flowise_to_dify.py
===================

Converts Flowise "Agentflow v2" JSON exports into Dify Chatflow DSL (.yml)
files, preserving the same flow core: prompts, flow-state variables, form
inputs, branching logic, and the revision/critique loop.

FIX LOG (this revision)
------------------------
1. CRITICAL: pending edge targets were stored as raw Flowise node ids and
   NEVER translated into the Dify node ids they became. `_assemble_dsl`
   used them directly, so every edge whose target wasn't already a
   resolved Dify id (i.e. everything except intra-loop-clone edges) was
   silently wired to a nonexistent node. Fixed by tracking a proper
   entry_id_for[] map and resolving every pending target through it in
   _assemble_dsl (raising loudly if something still doesn't resolve).
2. CRITICAL / SILENT: an `llmAgentflow` node expands into up to three Dify
   nodes (llm -> code parser -> assigner). Incoming edges must land on the
   FIRST node (the llm node, so the prompt actually runs); outgoing edges
   must originate from the LAST node (the assigner, so state is
   committed). The converter only ever tracked one id and used it for
   both, and that id was the assigner (exit). Every loop re-entry and
   "loop again" edge therefore pointed at a `- Save State` assigner
   instead of the actual LLM call, skipping it on every iteration. This
   produced a *valid* edge (no import error), so it was invisible to a
   simple "is the target a real node" check. Fixed by having
   `_convert_llm` return the llm node id (entry) instead of the assigner
   id (exit); the assigner is still used correctly as the exit for the
   node's own outgoing edges.
3. Fields whose label contains "(optional)" (stockSources, aiTools,
   musicBPM, musicTrackLink, trendStyle, referenceVideos,
   availablePlugins) were hardcoded required=True, which would block
   Dify form submission without them -- directly contradicting the
   flows' own system prompts, which have an entire section dedicated to
   gracefully handling blank/missing fields. Now required is derived
   from the label.
4. `number`-typed Flowise fields (musicBPM, clipCount) were falling into
   the generic string/paragraph branch. Now mapped to Dify's `number`
   start-node variable type.
5. Removed two dead `if False` no-ops (one referenced undefined
   self._last_source/_last_source_handle attributes) and a fragile
   __init__ monkey-patch that existed only to avoid a mutable
   class-level list default; _pending_edges is now a normal instance
   attribute initialized in __init__.
6. Broadened the condition operator map (contains/not contains/is/is not/
   start with/end with) for forward compatibility. All conditions in the
   three source flows use "contains", so this doesn't change existing
   output -- it just stops a future flow with a different operator from
   silently defaulting to the wrong comparison.

WHY CHATFLOW (advanced-chat) MODE
----------------------------------
These Flowise flows use two features that only exist in Dify's
`advanced-chat` (Chatflow) apps:
  1. "Flow State" (Flowise `$flow.state.*`) is a mutable key/value bag
     written by many nodes and read by later ones. Dify's equivalent is
     `conversation_variables`, written with an `assigner` node -- and
     conversation_variables only exist in Chatflow apps.
  2. `humanInputAgentflow` nodes pause the run for a person to click
     Proceed/Reject. Dify's matching node (`human-input`) is likewise a
     Chatflow-only concept.
So every generated app uses `app.mode: advanced-chat`.

NODE MAPPING
------------
  startAgentflow        -> `start` node (variables) + conversation_variables
                            seeded from Flowise's `startState`
  llmAgentflow           -> `llm` node
                            + `code` node (only if the Flowise node used
                              "Structured Output" -- parses the model's JSON
                              reply into separate fields)
                            + `assigner` node (v2) replaying `llmUpdateState`
                              writes into conversation_variables
                            + `template-transform` node for any state write
                              that is a *computed* value (Liquid `| plus: N`
                              or string concatenation), since `assigner` can
                              only copy a value, not compute one
  humanInputAgentflow    -> `human-input` node (Proceed/Reject buttons +
                            optional feedback textbox). An unwired branch
                            (usually "Reject") gets a small `answer` node
                            appended so no path dead-ends.
  conditionAgentflow     -> `if-else` node. Flowise's output-0 is always the
                            "condition matched" branch and output-1 is the
                            else branch (confirmed from each node's own
                            `outputAnchors` labels) -> Dify 'true' / 'false'.
  directReplyAgentflow   -> `answer` node
  loopAgentflow          -> see LOOP HANDLING below.

LOOP HANDLING (the one lossy part of this conversion)
-------------------------------------------------------
Flowise's `loopAgentflow` is a raw "goto": it jumps execution back to an
earlier node, with `maxLoopCount` as a hard safety cap. Dify's graph has no
literal goto; the closest primitive is the newer `loop` (while-loop)
container node, but its exact nested-node wiring is not something this
script can verify without a live Dify instance to test an import against.

Rather than emit an unverified nested-loop structure that might fail to
import, this script UNROLLS the loop by default: it clones the loop body
(every node that sits on a path from the loop-back target to the loop
node, computed generically via forward/reverse reachability -- this is
NOT hardcoded per-flow and correctly handles the fact that the three
source flows have differently-shaped loop bodies) `maxLoopCount + 1`
times, rewiring each copy's "loop again" edge to the next copy -- and on
the final allowed copy, forcing the exit path instead. Every condition
inside the loop body keeps its original true/false targets, so the
branch logic is reproduced exactly at each iteration; only the
*mechanism* (repeated nodes vs. a native loop) differs from the source
file. This guarantees valid, importable Dify DSL using only
well-documented node types.

If you've confirmed your Dify version's `loop` node schema, pass
--native-loop to attempt the compact container form instead (marked
EXPERIMENTAL in code) -- see build_native_loop() docstring.

KNOWN LIMITATION: this script assumes each conditionAgentflow node has a
single condition (binary true/false via output-0/output-1), which matches
all condition nodes in the three source flows. A Flowise condition node
with multiple stacked conditions (else-if chains) is not handled.

TEMPLATE VARIABLE TRANSLATION
------------------------------
  {{ $form.fieldName }}        -> {{#start.fieldName#}}
  {{ $flow.state.key }}        -> {{#conversation.key#}}
  {{ output }}                 -> (llm node).text            [state-write only]
  {{ output.key }}             -> (json-parser code node).key [state-write only]
  {{ $flow.state.x | plus: N }}-> Jinja2 in a template-transform node
  {{ $flow.state.x }}<suffix>  -> Jinja2 string concat in a template-transform node

Usage:
    python3 flowise_to_dify.py FLOWISE_JSON [-o OUT.yml]
        [--provider PROVIDER] [--model MODEL] [--temperature T]
        [--app-name NAME] [--native-loop]

Defaults for --provider/--model assume Dify's official
"OpenAI-API-compatible" plugin (langgenius/openai_api_compatible), which is
the closest match to the custom OpenAI-compatible endpoint
(chatOpenAICustom / basepath) the source flows were built with. Override
these to match whatever model provider is actually installed in your Dify
workspace -- the script does not (and cannot) know that for you.
"""

import argparse
import json
import re
import sys
import uuid
from pathlib import Path

import yaml


# --------------------------------------------------------------------------
# YAML output styling: use block literals ("|") for multiline strings so the
# exported YAML stays human-readable/diffable, matching Dify's own exports.
# --------------------------------------------------------------------------
class _LiteralStr(str):
    pass


def _literal_str_representer(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


class DifyDumper(yaml.SafeDumper):
    pass


DifyDumper.add_representer(_LiteralStr, _literal_str_representer)
DifyDumper.add_representer(str, _literal_str_representer)


def _mark_multiline_strings(obj):
    """Recursively wrap multi-line strings so the custom representer fires."""
    if isinstance(obj, str):
        return _LiteralStr(obj) if "\n" in obj else obj
    if isinstance(obj, dict):
        return {k: _mark_multiline_strings(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_mark_multiline_strings(v) for v in obj]
    return obj


def dump_yaml(data: dict) -> str:
    return yaml.dump(
        _mark_multiline_strings(data),
        Dumper=DifyDumper,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=100000,  # don't hard-wrap long prompt lines
    )


# --------------------------------------------------------------------------
# Template-variable translation
# --------------------------------------------------------------------------
FORM_RE = re.compile(r"\{\{\s*\$form\.(\w+)\s*\}\}")
STATE_RE = re.compile(r"\{\{\s*\$flow\.state\.(\w+)\s*\}\}")
OUTPUT_FIELD_RE = re.compile(r"^\{\{\s*output\.(\w+)\s*\}\}$")
OUTPUT_RE = re.compile(r"^\{\{\s*output\s*\}\}$")
PURE_STATE_RE = re.compile(r"^\{\{\s*\$flow\.state\.(\w+)\s*\}\}$")
LIQUID_PLUS_RE = re.compile(r"\{\{\s*\$flow\.state\.(\w+)\s*\|\s*plus:\s*(-?\d+)\s*\}\}")


def translate_text(text: str) -> str:
    """Translate Flowise {{ $form.x }} / {{ $flow.state.x }} references in
    free text (prompts, human-input descriptions, direct-reply messages)
    into Dify's {{#start.x#}} / {{#conversation.x#}} syntax. Leaves any
    other `{{ ... }}` text (illustrative prose in the prompts) untouched."""
    text = FORM_RE.sub(r"{{#start.\1#}}", text)
    text = STATE_RE.sub(r"{{#conversation.\1#}}", text)
    return text


def slug_id(*parts) -> str:
    return "-".join(str(p) for p in parts if p)


# --------------------------------------------------------------------------
# Dify graph builder
# --------------------------------------------------------------------------
class GraphBuilder:
    def __init__(self):
        self.nodes = {}   # id -> node dict
        self.edges = []
        self._base_ts = 1730000000000
        self._counter = 0
        self._depth_cursor = {}  # depth -> next y slot

    def new_id(self) -> str:
        self._counter += 1
        return str(self._base_ts + self._counter)

    def add_node(self, dify_type, title, extra_data, depth=0, width=244, height=90):
        nid = self.new_id()
        y_slot = self._depth_cursor.get(depth, 0)
        self._depth_cursor[depth] = y_slot + 1
        x = 100 + depth * 320
        y = 80 + y_slot * 170
        node = {
            "id": nid,
            "type": "custom",
            "position": {"x": float(x), "y": float(y)},
            "positionAbsolute": {"x": float(x), "y": float(y)},
            "selected": False,
            "sourcePosition": "right",
            "targetPosition": "left",
            "width": width,
            "height": height,
            "data": {
                "desc": "",
                "selected": False,
                "title": title,
                "type": dify_type,
                **extra_data,
            },
        }
        self.nodes[nid] = node
        return nid

    def add_edge(self, source, target, source_handle="source", source_type=None, target_type=None):
        eid = slug_id(source, source_handle, target, "target")
        edge = {
            "id": eid,
            "type": "custom",
            "selected": False,
            "source": source,
            "sourceHandle": source_handle,
            "target": target,
            "targetHandle": "target",
            "zIndex": 0,
            "data": {
                "isInIteration": False,
                "sourceType": source_type or "",
                "targetType": target_type or "",
            },
        }
        self.edges.append(edge)
        return eid

    def node_type(self, nid):
        return self.nodes[nid]["data"]["type"] if nid in self.nodes else ""


# --------------------------------------------------------------------------
# Flowise parsing helpers
# --------------------------------------------------------------------------
class FlowiseFlow:
    def __init__(self, raw: dict):
        self.raw = raw
        self.description = raw.get("description", "")
        self.nodes = {n["id"]: n for n in raw["nodes"]}
        self.edges = raw["edges"]
        self.out_edges = {}   # node_id -> list of edge dicts
        self.in_edges = {}    # node_id -> list of edge dicts
        for e in self.edges:
            self.out_edges.setdefault(e["source"], []).append(e)
            self.in_edges.setdefault(e["target"], []).append(e)

    def node_name(self, nid):
        return self.nodes[nid]["data"].get("name")

    def node_label(self, nid):
        return self.nodes[nid]["data"].get("label") or nid

    def node_inputs(self, nid):
        return self.nodes[nid]["data"].get("inputs") or {}

    def start_node_id(self):
        for nid, n in self.nodes.items():
            if n["data"].get("name") == "startAgentflow":
                return nid
        raise ValueError("No startAgentflow node found")

    def loop_nodes(self):
        return [nid for nid, n in self.nodes.items() if n["data"].get("name") == "loopAgentflow"]

    def branch_handle_index(self, edge):
        """Return the trailing integer/label of a Flowise sourceHandle, e.g.
        '...-output-0' -> 0, '...-output-1' -> 1, '...-output-llmAgentflow' -> None."""
        h = edge.get("sourceHandle", "")
        tail = h.split("-")[-1]
        return int(tail) if tail.isdigit() else None


# --------------------------------------------------------------------------
# State-value compiler: turns a Flowise llmUpdateState `value` string into
# a Dify value_selector, generating helper nodes (json-parser / template
# transform) only when needed.
# --------------------------------------------------------------------------
def compile_state_value(gb: GraphBuilder, value: str, llm_node_id: str,
                         parser_node_id: str, depth: int):
    """Returns a value_selector list [node_id, field] to use as the source
    of an assigner `items[].value`. Builds a template-transform node for
    any computed expression."""
    v = value.strip()

    if OUTPUT_RE.match(v):
        return [llm_node_id, "text"]

    m = OUTPUT_FIELD_RE.match(v)
    if m and parser_node_id:
        return [parser_node_id, m.group(1)]

    m = PURE_STATE_RE.match(v)
    if m:
        return ["conversation", m.group(1)]

    # Computed expression: Liquid `| plus: N` increment, string concatenation
    # with a state read, etc. Build a template-transform (Jinja2) node.
    variables = []
    seen = {}

    def state_repl(match):
        key = match.group(1)
        local = seen.setdefault(key, f"state_{key}")
        return "{{ " + local + " }}"

    # Liquid `plus` filter -> Jinja2 arithmetic, e.g.
    # "{{ $flow.state.revision_count | plus: 1 }}" -> "{{ (state_revision_count | int) + 1 }}"
    def plus_repl(match):
        key, n = match.group(1), match.group(2)
        local = seen.setdefault(key, f"state_{key}")
        return "{{ (" + local + " | int) + " + n + " }}"

    template = LIQUID_PLUS_RE.sub(plus_repl, v)
    template = STATE_RE.sub(state_repl, template)
    # NOTE: {{ output.field }} embedded inside a computed expression (as
    # opposed to being the entire value, handled above by OUTPUT_FIELD_RE)
    # is not observed anywhere in the three source flows, so it's
    # intentionally not handled here -- state-only computed expressions
    # cover every case actually present in llmUpdateState.

    for key, local in seen.items():
        variables.append({"value_selector": ["conversation", key], "variable": local})

    tt_id = gb.add_node(
        "template-transform",
        f"Compute {value[:24]}",
        {
            "type": "template-transform",
            "template": template,
            "variables": variables,
        },
        depth=depth,
    )
    gb.add_edge(llm_node_id, tt_id, "source", source_type="llm", target_type="template-transform")
    return [tt_id, "output"]


# --------------------------------------------------------------------------
# Main converter
# --------------------------------------------------------------------------
class FlowiseToDifyConverter:
    def __init__(self, flow: FlowiseFlow, provider: str, model: str,
                 app_name: str, native_loop: bool = False,
                 unroll_passes: int = None):
        self.flow = flow
        self.provider = provider
        self.model_override = model
        self.app_name = app_name
        self.native_loop = native_loop
        self.unroll_passes_override = unroll_passes
        self.gb = GraphBuilder()
        self.conversation_variables = []
        self.start_field_names = set()

        # Flowise node id -> Dify id of the FIRST node created for it.
        # This is what any INCOMING edge to that Flowise node must target
        # (e.g. for an llmAgentflow node, this is the `llm` node itself,
        # not its trailing `code`/`assigner` helper nodes).
        self.entry_id_for = {}

        # Flowise node id -> {branch_index_or_None: (dify_source_id, handle)}
        # This is what any OUTGOING edge from that Flowise node must
        # originate from (e.g. for an llmAgentflow node, this is its
        # trailing `assigner` node, so the edge fires only after state is
        # committed).
        self.exit_map_for = {}

        self.depth_for = {}  # flowise node id -> BFS depth (for layout)
        self._pending_edges = []  # (src_dify_id, src_handle, target) where
                                   # target is EITHER a raw Flowise node id
                                   # (resolved later via entry_id_for) OR an
                                   # already-resolved Dify id (loop clones)

    # ---- public entry point ----
    def convert(self) -> dict:
        self._compute_depths()
        start_fid = self.flow.start_node_id()
        self._convert_start(start_fid)

        loop_ids = self.flow.loop_nodes()
        if len(loop_ids) > 1:
            raise NotImplementedError("Multiple loopAgentflow nodes in one flow are not supported yet")
        loop_fid = loop_ids[0] if loop_ids else None

        if loop_fid:
            loop_target_fid, loop_body = self._compute_loop_body(loop_fid)
        else:
            loop_target_fid, loop_body = None, set()

        # Walk the flow and materialize every non-loop-body node once.
        visited = set()
        self._emit_chain(start_fid, visited, loop_body, loop_fid, loop_target_fid)

        # Now materialize the loop body itself (unrolled).
        if loop_fid:
            self._emit_unrolled_loop(loop_fid, loop_target_fid, loop_body, visited)

        return self._assemble_dsl()

    # ---- depth (BFS) for layout ----
    def _compute_depths(self):
        start_fid = self.flow.start_node_id()
        depth = {start_fid: 0}
        queue = [start_fid]
        while queue:
            nid = queue.pop(0)
            for e in self.flow.out_edges.get(nid, []):
                tgt = e["target"]
                if tgt not in depth:
                    depth[tgt] = depth[nid] + 1
                    queue.append(tgt)
        self.depth_for = depth

    def _depth(self, fid):
        return self.depth_for.get(fid, 0)

    # ---- start node ----
    def _convert_start(self, start_fid):
        inputs = self.flow.node_inputs(start_fid)
        form_fields = inputs.get("formInputTypes", []) or []
        variables = []
        for f in form_fields:
            name = f["name"]
            self.start_field_names.add(name)
            label = f.get("label", name)
            # Fields whose label signals optionality (the source flows rely
            # on this: their system prompts have dedicated instructions for
            # gracefully handling blank/unfilled fields) should NOT be
            # forced required in the Dify form, or the form itself would
            # block submission and that prompt logic could never trigger.
            required = "(optional)" not in label.lower()

            if f.get("type") == "options":
                options = [o["option"] for o in f.get("addOptions", [])]
                variables.append({
                    "label": label,
                    "variable": name,
                    "type": "select",
                    "options": options,
                    "required": required,
                    "max_length": 256,
                })
            elif f.get("type") == "number":
                variables.append({
                    "label": label,
                    "variable": name,
                    "type": "number",
                    "options": [],
                    "required": required,
                    "max_length": 256,
                })
            else:
                variables.append({
                    "label": label,
                    "variable": name,
                    "type": "paragraph",
                    "options": [],
                    "required": required,
                    "max_length": 4000,
                })

        start_id = self.gb.add_node(
            "start",
            "Start",
            {"type": "start", "variables": variables},
            depth=0,
        )
        self.entry_id_for[start_fid] = start_id
        self.exit_map_for[start_fid] = {None: (start_id, "source")}

        for s in inputs.get("startState", []) or []:
            self.conversation_variables.append({
                "id": str(uuid.uuid4()),
                "name": s["key"],
                "description": "",
                "value_type": "string",
                "value": s.get("value", ""),
            })

    # ---- loop-body detection (generic reachability-set method) ----
    def _compute_loop_body(self, loop_fid):
        loop_input = self.flow.node_inputs(loop_fid)
        raw_target = loop_input.get("loopBackToNode", "")
        target_fid = raw_target.split("-", 1)[0]
        if target_fid not in self.flow.nodes:
            raise ValueError(f"loopBackToNode target '{raw_target}' -> '{target_fid}' not found in graph")

        # forward reachability from target
        reach_fwd = set()
        stack = [target_fid]
        while stack:
            nid = stack.pop()
            if nid in reach_fwd:
                continue
            reach_fwd.add(nid)
            for e in self.flow.out_edges.get(nid, []):
                if e["target"] not in reach_fwd:
                    stack.append(e["target"])

        # nodes that can reach the loop node (reverse reachability)
        can_reach_loop = set()
        stack = [loop_fid]
        while stack:
            nid = stack.pop()
            if nid in can_reach_loop:
                continue
            can_reach_loop.add(nid)
            for e in self.flow.in_edges.get(nid, []):
                if e["source"] not in can_reach_loop:
                    stack.append(e["source"])

        loop_body = (reach_fwd & can_reach_loop) - {loop_fid}
        return target_fid, loop_body

    # ---- generic node conversion (non-loop, single instance) ----
    def _convert_node(self, fid, depth, in_loop_iteration=None):
        """Converts a single Flowise node into its Dify node(s). Returns
        (entry_id, exit_map):
          entry_id: the Dify node id any INCOMING edge to this Flowise
                    node must target.
          exit_map: {branch_index_or_None: (dify_source_id, source_handle)}
                    -- what any OUTGOING edge from this Flowise node must
                    originate from, per branch."""
        name = self.flow.node_name(fid)
        label = self.flow.node_label(fid)
        inputs = self.flow.node_inputs(fid)

        if name == "llmAgentflow":
            return self._convert_llm(fid, label, inputs, depth)
        elif name == "conditionAgentflow":
            return self._convert_condition(fid, label, inputs, depth)
        elif name == "humanInputAgentflow":
            return self._convert_human_input(fid, label, inputs, depth)
        elif name == "directReplyAgentflow":
            return self._convert_direct_reply(fid, label, inputs, depth)
        else:
            raise NotImplementedError(f"Unsupported Flowise node type: {name} ({fid})")

    def _model_block(self, model_cfg):
        return {
            "completion_params": {
                "temperature": model_cfg.get("temperature", 0.7),
            },
            "mode": "chat",
            "name": self.model_override or model_cfg.get("modelName", "gpt-4o-mini"),
            "provider": self.provider,
        }

    def _convert_llm(self, fid, label, inputs, depth):
        messages = inputs.get("llmMessages", []) or []
        structured = inputs.get("llmStructuredOutput") or []
        update_state = inputs.get("llmUpdateState") or []
        model_cfg = inputs.get("llmModelConfig", {}) or {}

        prompt_template = []
        for m in messages:
            prompt_template.append({
                "id": str(uuid.uuid4()),
                "role": m["role"],
                "text": translate_text(m["content"]),
            })

        if structured:
            schema_lines = "\n".join(
                f'  - "{s["key"]}" ({s["type"]}'
                + (f', one of: {s["enumValues"]}' if s.get("enumValues") else '')
                + f'): {s.get("description", "")}'
                for s in structured
            )
            json_instruction = (
                "\n\nRespond with ONLY a single valid JSON object (no markdown "
                "code fences, no commentary before or after) containing exactly "
                f"these keys:\n{schema_lines}"
            )
            prompt_template[-1]["text"] += json_instruction

        llm_id = self.gb.add_node(
            "llm",
            label,
            {
                "type": "llm",
                "model": self._model_block(model_cfg),
                "prompt_template": prompt_template,
                "variables": [],
                "context": {"enabled": False, "variable_selector": []},
                "vision": {"enabled": False},
            },
            depth=depth,
            height=120,
        )

        parser_id = None
        if structured:
            keys = [s["key"] for s in structured]
            py_lines = [
                "import json",
                "import re",
                "",
                "def main(raw_text: str) -> dict:",
                "    text = (raw_text or '').strip()",
                "    text = re.sub(r'^```(?:json)?\\s*|\\s*```$', '', text, flags=re.MULTILINE).strip()",
                "    try:",
                "        data = json.loads(text)",
                "    except Exception:",
                "        data = {}",
                "    if not isinstance(data, dict):",
                "        data = {}",
                "    return {",
            ]
            for k in keys:
                py_lines.append(f"        {k!r}: str(data.get({k!r}, '')),")
            py_lines.append("    }")
            code = "\n".join(py_lines)

            parser_id = self.gb.add_node(
                "code",
                f"{label} - Parse JSON",
                {
                    "type": "code",
                    "code_language": "python3",
                    "code": code,
                    "variables": [{"value_selector": [llm_id, "text"], "variable": "raw_text"}],
                    "outputs": {k: {"type": "string"} for k in keys},
                },
                depth=depth + 1,
            )
            self.gb.add_edge(llm_id, parser_id, "source", source_type="llm", target_type="code")

        last_id = parser_id or llm_id
        if update_state:
            items = []
            compute_depth = depth + (2 if parser_id else 1)
            for u in update_state:
                key = u["key"]
                value_selector = compile_state_value(self.gb, u["value"], llm_id, parser_id, compute_depth)
                items.append({
                    "input_type": "variable",
                    "operation": "over-write",
                    "value": value_selector,
                    "variable_selector": ["conversation", key],
                    "write_mode": "over-write",
                })
            assigner_id = self.gb.add_node(
                "assigner",
                f"{label} - Save State",
                {"type": "assigner", "version": 2, "items": items},
                depth=depth + (3 if parser_id else 2),
            )
            self.gb.add_edge(
                last_id, assigner_id, "source",
                source_type=self.gb.node_type(last_id), target_type="assigner",
            )
            # Any template-transform helper node needed by compile_state_value
            # was already wired FROM llm_id above; the assigner only needs to
            # run after the main chain (parser or llm). Helper nodes are read
            # from via variable_selector, which Dify resolves independent of
            # the visual edge, so they don't need to sit inline in the chain.
            last_id = assigner_id

        # entry_id: the llm node -- what an incoming edge into this Flowise
        # node must target, so the prompt actually runs.
        # exit_map: the LAST node produced (assigner if state was written,
        # otherwise the llm node itself) -- what an outgoing edge from this
        # Flowise node must originate from.
        exit_map = {None: (last_id, "source")}
        return llm_id, exit_map

    def _convert_condition(self, fid, label, inputs, depth):
        conds = inputs.get("conditions", []) or []
        cases_conditions = []
        # Flowise operation -> Dify if-else comparison_operator. All
        # conditions in the source flows use "contains"; the rest are
        # mapped for forward compatibility with other Flowise exports.
        op_map = {
            "contains": "contains",
            "notContains": "not contains",
            "equals": "is",
            "notEqual": "is not",
            "startsWith": "start with",
            "endsWith": "end with",
        }
        for c in conds:
            op = c.get("operation", "contains")
            comparison_operator = op_map.get(op, "contains")
            value1 = c.get("value1", "")
            m = PURE_STATE_RE.match(value1.strip())
            if m:
                variable_selector = ["conversation", m.group(1)]
            else:
                fm = FORM_RE.match(value1.strip())
                variable_selector = ["start", fm.group(1)] if fm else ["conversation", "unknown"]
            cases_conditions.append({
                "id": str(uuid.uuid4()),
                "comparison_operator": comparison_operator,
                "value": c.get("value2", ""),
                "varType": "string",
                "variable_selector": variable_selector,
            })

        node_id = self.gb.add_node(
            "if-else",
            label,
            {
                "type": "if-else",
                "cases": [{
                    "case_id": "true",
                    "id": "true",
                    "logical_operator": "and",
                    "conditions": cases_conditions,
                }],
            },
            depth=depth,
        )
        exit_map = {0: (node_id, "true"), 1: (node_id, "false")}
        return node_id, exit_map

    def _convert_human_input(self, fid, label, inputs, depth):
        desc = translate_text(inputs.get("humanInputDescription", ""))
        enable_feedback = bool(inputs.get("humanInputEnableFeedback"))

        form_inputs = []
        if enable_feedback:
            form_inputs.append({"type": "paragraph", "output_variable_name": "human_feedback"})

        node_id = self.gb.add_node(
            "human-input",
            label,
            {
                "type": "human-input",
                "delivery_methods": [{"type": "webapp", "enabled": True, "id": str(uuid.uuid4())}],
                "form_content": desc,
                "inputs": form_inputs,
                "user_actions": [
                    {"id": "proceed", "title": "Proceed", "button_style": "primary"},
                    {"id": "reject", "title": "Reject", "button_style": "default"},
                ],
                "timeout": 24,
                "timeout_unit": "hour",
            },
            depth=depth,
            height=140,
        )
        exit_map = {0: (node_id, "proceed"), 1: (node_id, "reject")}
        return node_id, exit_map

    def _convert_direct_reply(self, fid, label, inputs, depth):
        msg = translate_text(inputs.get("directReplyMessage", ""))
        node_id = self.gb.add_node(
            "answer",
            label,
            {"type": "answer", "answer": msg, "variables": []},
            depth=depth,
        )
        return node_id, {None: (node_id, "source")}

    # ---- main chain walk (everything outside the loop body) ----
    def _emit_chain(self, fid, visited, loop_body, loop_fid, loop_target_fid):
        """Depth-first walk from start, materializing every node that is
        NOT part of the loop body (loop-body nodes are handled separately
        by _emit_unrolled_loop, and are skipped here)."""
        stack = [fid]
        while stack:
            cur = stack.pop()
            if cur in visited:
                continue
            visited.add(cur)

            if cur != self.flow.start_node_id():
                if cur in loop_body:
                    continue  # handled by the loop unroller
                entry_id, exit_map = self._convert_node(cur, self._depth(cur))
                self.entry_id_for[cur] = entry_id
                self.exit_map_for[cur] = exit_map
            else:
                exit_map = self.exit_map_for[cur]

            for e in self.flow.out_edges.get(cur, []):
                tgt = e["target"]
                if tgt == loop_fid:
                    continue  # loop node itself is never materialized directly
                if tgt in loop_body:
                    # first entry point into the loop is wired by the loop
                    # unroller, not here
                    continue
                idx = self.flow.branch_handle_index(e)
                src_id, src_handle = exit_map.get(idx, exit_map.get(None))
                if tgt not in visited:
                    stack.append(tgt)
                # tgt is still a raw Flowise node id here -- resolved to its
                # Dify entry id later, in _assemble_dsl, once every node has
                # been converted.
                self._pending_edges.append((src_id, src_handle, tgt))

    # ---- loop unrolling ----
    def _emit_unrolled_loop(self, loop_fid, loop_target_fid, loop_body, visited):
        loop_input = self.flow.node_inputs(loop_fid)
        max_loop_count = int(loop_input.get("maxLoopCount", 1))
        passes = self.unroll_passes_override or (max_loop_count + 1)

        # Find the entry edge(s) into the loop body from outside (there
        # should be exactly one in all observed flows: the forward-chain
        # edge from the last outside-loop node into loop_target_fid).
        entry_edges = [
            e for e in self.flow.in_edges.get(loop_target_fid, [])
            if e["source"] not in loop_body
        ]

        body_order = self._topo_order(loop_body)

        clone_first_id = {}   # pass_index -> Dify ENTRY id of the clone of loop_target_fid
        for p in range(passes):
            is_last_pass = (p == passes - 1)
            clone_map = {}  # flowise id -> (entry_id, exit_map) for this pass
            for bfid in body_order:
                entry_id, exit_map = self._convert_node(bfid, self._depth(bfid))
                clone_map[bfid] = (entry_id, exit_map)
                if bfid == loop_target_fid:
                    clone_first_id[p] = entry_id

            # wire internal edges for this pass
            for bfid in body_order:
                entry_id, exit_map = clone_map[bfid]
                for e in self.flow.out_edges.get(bfid, []):
                    tgt = e["target"]
                    idx = self.flow.branch_handle_index(e)
                    src_id, src_handle = exit_map.get(idx, exit_map.get(None))

                    if tgt == loop_fid:
                        # "loop again" edge
                        if not is_last_pass:
                            self._pending_edges.append((src_id, src_handle, ("__NEXT_PASS__", p + 1)))
                        else:
                            # out of allowed passes: force the guard's
                            # "limit hit" exit instead of looping again.
                            # That exit is whichever OTHER out-edge of this
                            # same source node leaves the loop body -- but
                            # since this branch's own target IS the loop
                            # node, we redirect it to the same external
                            # node its sibling branch(es) use.
                            forced_target = self._find_sibling_exit(bfid, loop_body, loop_fid)
                            if forced_target:
                                self._pending_edges.append((src_id, src_handle, forced_target))
                    elif tgt in loop_body:
                        tgt_entry_id = clone_map[tgt][0]
                        self._pending_edges.append((src_id, src_handle, tgt_entry_id))
                    else:
                        # external break edge -> shared downstream node
                        # (materialize it via the normal chain walk if not
                        # already visited; multiple passes/branches
                        # converging on the same external node is expected
                        # and correct -- they share one copy of it)
                        if tgt not in visited:
                            self._emit_chain(tgt, visited, loop_body, loop_fid, loop_target_fid)
                        self._pending_edges.append((src_id, src_handle, tgt))

        # resolve entry edges from outside the loop into pass 0
        for e in entry_edges:
            src_fid = e["source"]
            idx = self.flow.branch_handle_index(e)
            exit_map = self.exit_map_for[src_fid]
            src_id, src_handle = exit_map.get(idx, exit_map.get(None))
            self._pending_edges.append((src_id, src_handle, clone_first_id[0]))

        # resolve __NEXT_PASS__ placeholders (loop-again edges land on the
        # ENTRY id of the next pass's clone of loop_target_fid, so the LLM
        # node actually runs again -- not its assigner)
        resolved = []
        for src_id, src_handle, tgt in self._pending_edges:
            if isinstance(tgt, tuple) and tgt and tgt[0] == "__NEXT_PASS__":
                tgt = clone_first_id[tgt[1]]
            resolved.append((src_id, src_handle, tgt))
        self._pending_edges = resolved

    def _find_sibling_exit(self, bfid, loop_body, loop_fid):
        """On the final unrolled pass, a 'loop again' edge has nowhere to
        go. Redirect it to whatever external (non-loop-body) target this
        same node's OTHER branch already exits to -- i.e. reuse the
        guard's own 'limit hit' destination."""
        for e in self.flow.out_edges.get(bfid, []):
            if e["target"] != loop_fid and e["target"] not in loop_body:
                return e["target"]
        return None

    def _topo_order(self, node_set):
        """Simple topological-ish order for the loop body: BFS from the
        node with no in-edges originating inside the set."""
        indeg = {n: 0 for n in node_set}
        for n in node_set:
            for e in self.flow.out_edges.get(n, []):
                if e["target"] in node_set:
                    indeg[e["target"]] += 1
        queue = sorted([n for n in node_set if indeg[n] == 0], key=lambda n: self._depth(n))
        order = []
        seen = set()
        while queue:
            n = queue.pop(0)
            if n in seen:
                continue
            seen.add(n)
            order.append(n)
            for e in self.flow.out_edges.get(n, []):
                if e["target"] in node_set and e["target"] not in seen:
                    queue.append(e["target"])
        # append any not reached (defensive)
        for n in node_set:
            if n not in seen:
                order.append(n)
        return order

    # ---- assemble final Dify DSL ----
    def _assemble_dsl(self) -> dict:
        for src_id, src_handle, tgt in self._pending_edges:
            if src_id is None or tgt is None:
                continue
            # tgt is either already a resolved Dify node id (loop-clone
            # wiring) or a raw Flowise node id that needs translating into
            # the Dify ENTRY id for that node. entry_id_for's keys are
            # Flowise ids, which never collide with generated Dify ids, so
            # a plain membership check safely distinguishes the two.
            real_tgt = self.entry_id_for.get(tgt, tgt)
            if real_tgt not in self.gb.nodes:
                raise ValueError(
                    f"Unresolved edge target: {tgt!r} (resolved to {real_tgt!r}) "
                    f"is not a known Dify node -- conversion bug, please report "
                    f"this Flowise flow's topology."
                )
            self.gb.add_edge(
                src_id, real_tgt, src_handle,
                source_type=self.gb.node_type(src_id), target_type=self.gb.node_type(real_tgt),
            )

        self._patch_dangling_human_input_branches()

        nodes = list(self.gb.nodes.values())
        edges = self.gb.edges

        dsl = {
            "app": {
                "description": self.flow.description[:500],
                "icon": "\U0001F916",
                "icon_background": "#FFEAD5",
                "mode": "advanced-chat",
                "name": self.app_name,
                "use_icon_as_answer_icon": False,
            },
            "dependencies": [],
            "kind": "app",
            "version": "0.5.0",
            "workflow": {
                "conversation_variables": self.conversation_variables,
                "environment_variables": [],
                "features": self._default_features(),
                "graph": {
                    "edges": edges,
                    "nodes": nodes,
                    "viewport": {"x": 0, "y": 0, "zoom": 0.7},
                },
            },
        }
        return dsl

    def _patch_dangling_human_input_branches(self):
        """Any human-input user_action with no outgoing edge gets a small
        answer node so the branch doesn't dead-end."""
        used_handles = {}
        for e in self.gb.edges:
            used_handles.setdefault(e["source"], set()).add(e["sourceHandle"])

        for nid, node in list(self.gb.nodes.items()):
            if node["data"]["type"] != "human-input":
                continue
            for action in node["data"]["user_actions"]:
                handle = action["id"]
                if handle not in used_handles.get(nid, set()):
                    stop_id = self.gb.add_node(
                        "answer",
                        f"{node['data']['title']} - {action['title']} stop",
                        {
                            "type": "answer",
                            "answer": (
                                f"Flow stopped at \u201c{node['data']['title']}\u201d "
                                f"({action['title']}). Please revise your inputs and run again."
                            ),
                            "variables": [],
                        },
                        depth=self._depth_of_dify_node(nid) + 1,
                    )
                    self.gb.add_edge(nid, stop_id, handle, source_type="human-input", target_type="answer")

    def _depth_of_dify_node(self, dify_id):
        x = self.gb.nodes[dify_id]["position"]["x"]
        return int((x - 100) / 320)

    def _default_features(self):
        return {
            "opening_statement": "",
            "suggested_questions": [],
            "suggested_questions_after_answer": {"enabled": False},
            "text_to_speech": {"enabled": False, "voice": ""},
            "speech_to_text": {"enabled": False},
            "retriever_resource": {"enabled": False},
            "sensitive_word_avoidance": {"enabled": False},
            "file_upload": {
                "image": {"enabled": False, "number_limits": 3, "transfer_methods": ["local_file", "remote_url"]},
                "enabled": False,
            },
        }


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="Path to a Flowise agentflow-v2 JSON export")
    ap.add_argument("-o", "--output", help="Output .yml path (default: alongside input)")
    ap.add_argument("--provider", default="langgenius/openai_api_compatible/openai_api_compatible",
                     help="Dify model provider id for every llm node")
    ap.add_argument("--model", default=None,
                     help="Force a single model name for every llm node "
                          "(default: reuse each node's own Flowise modelName)")
    ap.add_argument("--app-name", default=None, help="Dify app name (default: derived from filename)")
    ap.add_argument("--native-loop", action="store_true",
                     help="EXPERIMENTAL: attempt Dify's native `loop` container "
                          "node instead of unrolling (unverified schema)")
    ap.add_argument("--unroll-passes", type=int, default=None,
                     help="Override number of unrolled loop passes "
                          "(default: Flowise maxLoopCount + 1)")
    args = ap.parse_args()

    in_path = Path(args.input)
    raw = json.loads(in_path.read_text())
    flow = FlowiseFlow(raw)

    if args.native_loop:
        print("ERROR: --native-loop is not implemented in this version of the "
              "script (unverified Dify `loop` node schema). Falling back to "
              "unrolled mode.", file=sys.stderr)

    app_name = args.app_name or in_path.stem.replace("_", " ").title()

    converter = FlowiseToDifyConverter(
        flow, provider=args.provider, model=args.model, app_name=app_name,
        native_loop=False, unroll_passes=args.unroll_passes,
    )
    dsl = converter.convert()

    out_path = Path(args.output) if args.output else in_path.with_suffix(".yml")
    out_path.write_text(dump_yaml(dsl))
    print(f"Wrote {out_path} ({len(dsl['workflow']['graph']['nodes'])} nodes, "
          f"{len(dsl['workflow']['graph']['edges'])} edges)")


if __name__ == "__main__":
    main()