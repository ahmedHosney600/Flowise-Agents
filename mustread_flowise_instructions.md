# Flowise AgentFlow V2 — Rules for AI Coding Assistants

Drop this file into your repo so any AI model editing or generating Flowise flow
JSON in this IDE reads it first. Rename per tool convention if needed:
`CLAUDE.md` (Claude Code), `.cursorrules` / `.cursor/rules/flowise.mdc` (Cursor),
`AGENTS.md` (Codex/other agents), `.github/copilot-instructions.md` (Copilot).

---

## Rule 1 (critical): Never let 2+ Condition or Human Input nodes fan into the same node

**The bug:** In Flowise AgentFlow V2, if a node receives incoming edges from
**two or more Condition nodes** (or a Condition + Human Input node), execution
silently stalls at the Condition node the moment it fires. No error is thrown,
the run still reports "completed," but nothing downstream ever executes —
including the final output node, so the chat shows nothing.

This is a confirmed, open bug in Flowise itself, not a modeling mistake:
- https://github.com/FlowiseAI/Flowise/issues/4660
- https://github.com/FlowiseAI/Flowise/issues/5358
- https://github.com/FlowiseAI/Flowise/issues/5501

Fan-in from two plain LLM/Agent/Tool nodes into one shared node is **fine**.
The bug is specifically about the *upstream* node type being Condition or
Human Input.

**MUST, when creating or editing any flow:**
- Before finishing any edit that touches edges, condition nodes, or loop
  nodes, check every node's incoming edges. If 2+ of them originate from a
  `Condition` or `HumanInput` node type, that is a bug, not a valid pattern —
  fix it before considering the task done.
- When a design naturally wants two branches (e.g. a "pass" branch and a
  "loop-exceeded/escape" branch) to converge on the same next step (e.g. a
  final packaging/output node), **duplicate that downstream node** — one copy
  per Condition-branch — and let both copies fan into whatever comes *after*
  them instead. That later fan-in (LLM → LLM/DirectReply) is safe.
- Give each duplicate a distinct `id`, a distinct `label` that says which
  branch it serves (e.g. `"X (Loop Escape Path)"`), and unique
  `outputAnchors[].id` values (rename any `<oldId>` substring inside them to
  the new node id). Keep the prompt/logic and state-write keys identical
  unless the branches genuinely need different behavior.
- Reposition the duplicate on the canvas (don't leave it stacked exactly on
  top of another node) — offset x/y so it doesn't visually overlap.

**Validation script — run this after any edit and treat any output as a
blocking issue:**

```python
import json, sys
from collections import defaultdict

path = sys.argv[1] if len(sys.argv) > 1 else "flow.json"
data = json.load(open(path))
node_map = {n["id"]: n for n in data["nodes"]}
incoming = defaultdict(list)
for e in data["edges"]:
    incoming[e["target"]].append(e)

problems = []
for target, edges in incoming.items():
    cond_sources = [e for e in edges
                    if node_map[e["source"]]["data"]["type"] in ("Condition", "HumanInput")]
    if len(cond_sources) >= 2:
        problems.append((target, [e["source"] for e in cond_sources]))

if problems:
    print("BLOCKING: Condition/HumanInput fan-in bug found:")
    for target, sources in problems:
        label = node_map[target]["data"]["label"]
        print(f"  '{label}' ({target}) is fed by multiple Condition/HumanInput nodes: {sources}")
    sys.exit(1)
print("OK: no Condition/HumanInput fan-in detected.")
```

---

## Rule 2: Never build a numeric counter with string concatenation

Update State fields that increment a counter must produce a real number
sequence ("0" → "1" → "2"), not string concatenation like
`"{{ $flow.state.count }}1"` (which produces "0" → "01" → "011"...). This
silently breaks any downstream `contains`/`equals` check on that counter.
Prefer a Custom JS node doing `Number(state.count) + 1` if you're not certain
the templating engine supports arithmetic filters (e.g. `| plus: 1`) — verify
by checking whether an existing filter usage elsewhere in the flow actually
renders as a number, not literal template text.

## Rule 3: Every `$flow.state.X` read must have a writer somewhere upstream

Before finishing, diff the set of state keys referenced via `$flow.state.X`
(or `{{$flow.state.X}}`) against the set of keys any node's `Update State` /
`llmUpdateState` actually writes, plus keys given non-empty defaults in the
Start node. Any read-only key with an empty default will silently render
blank sections in later output — flag it rather than assume it's intentional.

## Rule 4: Every branch must terminate — no dead ends

Every output anchor on every Condition, Human Input, or Loop node must be
connected to something that eventually reaches an End/DirectReply node. An
unconnected branch (e.g. a Human Input "Reject" path with no edge) isn't a
crash — it's a silent hang the first time that branch fires. Check for
unconnected `outputAnchors` on every branching node before finishing.

## Rule 5: Full structural validation before calling it done

Run this after every edit, in addition to Rule 1's script:

```python
import json, sys
from collections import defaultdict

path = sys.argv[1] if len(sys.argv) > 1 else "flow.json"
data = json.load(open(path))
node_ids = [n["id"] for n in data["nodes"]]
node_map = {n["id"]: n for n in data["nodes"]}

# duplicate ids
dupes = {x for x in node_ids if node_ids.count(x) > 1}
assert not dupes, f"Duplicate node ids: {dupes}"

# dangling edges / bad handles
for e in data["edges"]:
    assert e["source"] in node_map, f"Edge source missing: {e['source']}"
    assert e["target"] in node_map, f"Edge target missing: {e['target']}"
    anchors = [a["id"] for a in node_map[e["source"]]["data"].get("outputAnchors", [])]
    if anchors:
        assert e["sourceHandle"] in anchors, f"Bad sourceHandle {e['sourceHandle']} on {e['source']}"

# every node reachable from Start (account for Loop nodes' implicit loop-back)
edges_by_source = defaultdict(list)
for e in data["edges"]:
    edges_by_source[e["source"]].append(e["target"])
for n in data["nodes"]:
    if n["data"]["type"] == "Loop":
        back_to = n["data"]["inputs"].get("loopBackToNode", "")
        target_id = back_to.split("-")[0] if back_to else None
        if target_id in node_map:
            edges_by_source[n["id"]].append(target_id)

start_id = next(n["id"] for n in data["nodes"] if n["data"]["type"] == "Start")
visited, stack = set(), [start_id]
while stack:
    cur = stack.pop()
    if cur in visited:
        continue
    visited.add(cur)
    stack.extend(edges_by_source.get(cur, []))
unreached = set(node_ids) - visited
assert not unreached, f"Unreachable nodes: {unreached}"

print("OK: structurally valid.")
```

## Rule 6: Flag fragile external dependencies, don't silently trust them

If any node's `llmModelConfig.basepath` points at `localhost` or another
custom/self-hosted endpoint, note it explicitly in your summary to the user —
it's a common silent-failure point (timeouts, dropped streams), especially
on whichever node sends the largest prompt/expects the largest response in
the flow (e.g. a final aggregation/compile step). Recommend the user confirm
`maxTokens`/timeout settings are generous enough for that specific node if
the option is available.

---

## Workflow for any Flowise task

1. Read/generate the flow.
2. Run the Rule 1 script and the Rule 5 script. Both must pass clean.
3. Manually check Rules 2–4 against the diff you just made.
4. Only then report the task as complete, and mention any Rule 6 flags.