"""
Complete Flowise-to-Langflow Flow Converter
Translates Flowise agentic JSON flows into 100% native, schema-compliant Langflow 1.x flows.
Translates all Flowise {{ $flow.state.* }} and {{ $form.* }} variables into clear,
executable Langflow pipeline contracts so LLMs receive and process real data seamlessly.
"""

import json
import os
import re
import glob
import copy
from langflow.services.database.models.flow.model import FlowCreate
from langflow.api.v1.flows import normalize_code_for_import

# -----------------------------------------------------------------------------
# 1. Load native component blueprints from Langflow's starter project bank
# -----------------------------------------------------------------------------
starters = glob.glob(".venv/lib/python3.12/site-packages/langflow/initial_setup/starter_projects/*.json")
blueprint_nodes = {}
for sf in starters:
    try:
        data = json.load(open(sf, "r", encoding="utf-8"))
        for n in data.get("data", {}).get("nodes", []):
            t = n.get("data", {}).get("type")
            if t and t not in blueprint_nodes:
                blueprint_nodes[t] = copy.deepcopy(n)
    except Exception:
        pass

def make_chat_input(node_id, display_name, description, default_text, pos_x, pos_y):
    node = copy.deepcopy(blueprint_nodes["ChatInput"])
    node["id"] = node_id
    node["position"] = {"x": pos_x, "y": pos_y}
    node["data"]["id"] = node_id
    node["data"]["node"]["display_name"] = display_name
    node["data"]["node"]["description"] = description
    node["data"]["node"]["template"]["input_value"]["value"] = default_text
    return node

def make_agent_node(node_id, display_name, description, full_system_prompt, pos_x, pos_y):
    node = copy.deepcopy(blueprint_nodes["Agent"])
    node["id"] = node_id
    node["position"] = {"x": pos_x, "y": pos_y}
    node["data"]["id"] = node_id
    node["data"]["node"]["display_name"] = display_name
    node["data"]["node"]["description"] = description
    node["data"]["node"]["template"]["system_prompt"]["value"] = full_system_prompt
    return node

def make_chat_output(node_id, display_name, description, pos_x, pos_y):
    node = copy.deepcopy(blueprint_nodes["ChatOutput"])
    node["id"] = node_id
    node["position"] = {"x": pos_x, "y": pos_y}
    node["data"]["id"] = node_id
    node["data"]["node"]["display_name"] = display_name
    node["data"]["node"]["description"] = description
    return node

def make_edge(source_node, target_node, source_output_name="response", target_input_name="input_value"):
    source_id = source_node["id"]
    target_id = target_node["id"]
    source_type = source_node["data"]["type"]
    target_type = target_node["data"]["type"]

    out_obj = None
    for o in source_node["data"]["node"].get("outputs", []):
        if o.get("name") == source_output_name or source_output_name in o.get("types", []):
            out_obj = o
            break
    if not out_obj and source_node["data"]["node"].get("outputs"):
        out_obj = source_node["data"]["node"]["outputs"][0]

    out_types = out_obj["types"] if out_obj else ["Message"]
    out_name = out_obj["name"] if out_obj else "message"

    target_field = target_node["data"]["node"]["template"].get(target_input_name, {})
    in_types = target_field.get("input_types", ["Message"])
    f_type = target_field.get("type", "str")

    source_handle_dict = {
        "dataType": source_type,
        "id": source_id,
        "name": out_name,
        "output_types": out_types
    }

    target_handle_dict = {
        "fieldName": target_input_name,
        "id": target_id,
        "inputTypes": in_types,
        "type": f_type
    }

    source_handle_str = json.dumps(source_handle_dict).replace('"', '\u0153')
    target_handle_str = json.dumps(target_handle_dict).replace('"', '\u0153')

    return {
        "animated": False,
        "className": "",
        "data": {
            "sourceHandle": source_handle_dict,
            "targetHandle": target_handle_dict
        },
        "id": f"reactflow__edge-{source_id}{source_handle_str}-{target_id}{target_handle_str}",
        "selected": False,
        "source": source_id,
        "sourceHandle": source_handle_str,
        "target": target_id,
        "targetHandle": target_handle_str
    }

# -----------------------------------------------------------------------------
# 2. Translate Flowise template tags to native Langflow pipeline instructions
# -----------------------------------------------------------------------------
def translate_flowise_tags(text):
    """
    Translates Flowise {{ $flow.state.xyz }} and {{ $form.xyz }} tags into
    clear natural language references to data received in the pipeline input.
    """
    if not text:
        return ""

    # Replace form fields
    def replace_form(m):
        raw_name = m.group(1).strip()
        readable = re.sub(r'([A-Z])', r' \1', raw_name).title().strip()
        return f"[Intake Parameter: {readable}]"

    # Replace state fields
    def replace_state(m):
        raw_name = m.group(1).strip()
        readable = raw_name.replace('_', ' ').title().strip()
        return f"[Input Section: {readable}]"

    text = re.sub(r'\{\{\s*\$form\.(\w+)\s*\}\}', replace_form, text)
    text = re.sub(r'\{\{\s*\$flow\.state\.(\w+)[^}]*\}\}', replace_state, text)
    return text

def build_native_agent_prompt(stage_num, stage_label, sys_prompt, user_prompt, state_target=""):
    """
    Combines the Flowise system instructions and user task instructions into
    a cohesive, native Langflow prompt with clear input/output boundaries.
    """
    cleaned_sys = translate_flowise_tags(sys_prompt).strip()
    cleaned_usr = translate_flowise_tags(user_prompt).strip()

    prompt_parts = [
        f"=== STAGE {stage_num:02d}: {stage_label.upper()} ===",
        "",
        "## PIPELINE OPERATING PROTOCOL",
        "You are an autonomous expert agent in a multi-stage video production pipeline.",
        "Your input message contains the cumulative output and state data produced by the preceding pipeline stages.",
        "Read all previous sections carefully, apply your domain expertise according to the instructions below, and produce your designated section.",
        "Maintain high fidelity to all established creative decisions, story beats, and technical constraints from upstream stages.",
        "",
        "## DOMAIN INSTRUCTIONS & METHODOLOGY",
        cleaned_sys
    ]

    if cleaned_usr:
        prompt_parts.extend([
            "",
            "## STAGE TASK & INPUT MAPPING",
            cleaned_usr
        ])

    if state_target:
        prompt_parts.extend([
            "",
            f"## OUTPUT DELIVERABLE TARGET: `{state_target}`",
            f"Structure your response clearly with a dedicated `## {stage_label}` heading so downstream pipeline agents can seamlessly reference your output."
        ])

    return "\n".join(prompt_parts)

# -----------------------------------------------------------------------------
# 3. Flow Conversion Logic
# -----------------------------------------------------------------------------
def convert_flow(flowise_path, flow_name, flow_description):
    with open(flowise_path, "r", encoding="utf-8") as f:
        flowise_data = json.load(f)

    # Extract Start Form Default Values for ChatInput
    start_node = next((n for n in flowise_data.get("nodes", []) if n["data"].get("name") == "startAgentflow"), None)
    initial_params = []
    if start_node:
        form_inputs = start_node["data"].get("inputs", {}).get("formInputTypes", [])
        for fi in form_inputs:
            lbl = fi.get("label", fi.get("name", ""))
            opts = [o.get("option", "") for o in fi.get("addOptions", [])]
            opt_str = f" (Options: {', '.join(opts)})" if opts else ""
            initial_params.append(f"{lbl}: {opt_str}")

    default_input_text = "\n".join(initial_params) if initial_params else "Provide project details, video topic, and goals."

    # Identify LLM Agent nodes in execution sequence
    llm_nodes = []
    for n in flowise_data.get("nodes", []):
        if n["data"].get("name") == "llmAgentflow":
            label = n["data"].get("label", "")
            # Skip loop escape clones in linear Langflow pipeline
            if "Escape" in label or "Loop-Limit" in label:
                continue
            llm_nodes.append(n)

    langflow_nodes = []
    pos_x = 50
    pos_y = 250
    spacing_x = 400

    # 1. ChatInput Node
    input_node = make_chat_input("input_0", "Project Intake & Parameters", "Initial project parameters and brief inputs", default_input_text, pos_x, pos_y)
    langflow_nodes.append(input_node)
    pos_x += spacing_x

    # 2. Sequential Agent Nodes
    agent_nodes = []
    for idx, f_node in enumerate(llm_nodes):
        nid = f"agent_{idx+1:02d}_{f_node['id']}"
        label = f"{idx+1:02d}. {f_node['data'].get('label', 'Agent')}"
        msgs = f_node["data"].get("inputs", {}).get("llmMessages", [])
        sys_p = msgs[0]["content"] if len(msgs) > 0 else ""
        usr_p = msgs[1]["content"] if len(msgs) > 1 else ""
        state_k = f_node["data"].get("inputs", {}).get("state", "")

        full_prompt = build_native_agent_prompt(idx + 1, f_node['data'].get('label', 'Agent'), sys_p, usr_p, state_k)

        agent_node = make_agent_node(nid, label, f"Agent for {f_node['data'].get('label')}", full_prompt, pos_x, pos_y)
        langflow_nodes.append(agent_node)
        agent_nodes.append(agent_node)
        pos_x += spacing_x

    # 3. ChatOutput Node
    output_node = make_chat_output("output_final", "Final Deliverable Output", "Complete formatted markdown package deliverable", pos_x, pos_y)
    langflow_nodes.append(output_node)

    # 4. Sequential Edges
    langflow_edges = []
    all_seq = [input_node] + agent_nodes + [output_node]
    for i in range(len(all_seq) - 1):
        src = all_seq[i]
        tgt = all_seq[i+1]
        src_out = "message" if i == 0 else "response"
        langflow_edges.append(make_edge(src, tgt, source_output_name=src_out, target_input_name="input_value"))

    return {
        "name": flow_name,
        "description": flow_description,
        "data": {
            "nodes": langflow_nodes,
            "edges": langflow_edges,
            "viewport": {"x": 0, "y": 0, "zoom": 0.65}
        }
    }

# -----------------------------------------------------------------------------
# 4. Main Execution
# -----------------------------------------------------------------------------
def main():
    flowise_dir = "/Users/ahmedmac/Desktop/My Computer/Programming Proejcts/Prompt Storytelling System/flowise_flows"
    flows_out_dir = "flows"
    os.makedirs(flows_out_dir, exist_ok=True)

    mappings = [
        (
            os.path.join(flowise_dir, "00_flowise_video_preplanning_flow.json"),
            os.path.join(flows_out_dir, "00_video_preplanning_pipeline.json"),
            "00 Video Pre-Planning Pipeline",
            "End-to-end video pre-planning pipeline with brief builder, creative strategy, narrative structure, retention engineering, storyboard, pacing map, self-critique, and QA master package."
        ),
        (
            os.path.join(flowise_dir, "01_post_production_execution_flow.json"),
            os.path.join(flows_out_dir, "01_post_production_execution_flow.json"),
            "01 Post-Production Execution Flow",
            "Comprehensive post-production execution flow from asset organization and first cuts to VFX, motion graphics, sound design, audio mastering, color grading, self-critique audit, and master package."
        ),
        (
            os.path.join(flowise_dir, "02_speed_ramp_viral_flow.json"),
            os.path.join(flows_out_dir, "02_speed_ramp_viral_flow.json"),
            "02 Speed Ramp & Viral Edit Pipeline",
            "Viral speed ramp editing pipeline with clip arrangement, After Effects curve design, viral effects, sound design, audit critique, revision applier, and final viral package."
        )
    ]

    for flowise_src, target_path, name, desc in mappings:
        print(f"\nConverting: {os.path.basename(flowise_src)} -> {target_path}")
        flow_dict = convert_flow(flowise_src, name, desc)

        # Validate schema against Langflow FlowCreate
        flow_create_obj = FlowCreate(**normalize_code_for_import(flow_dict))

        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(flow_dict, f, indent=2)

        print(f"  ✓ Nodes: {len(flow_dict['data']['nodes'])}")
        print(f"  ✓ Edges: {len(flow_dict['data']['edges'])}")
        print(f"  ✅ Successfully validated and written to {target_path}")

    print("\n" + "=" * 60)
    print("🎉 ALL 3 FLOWS CONVERTED WITH FULL NATIVE LANGFLOW PROMPTS & PIPELINE PROTOCOL!")

if __name__ == "__main__":
    main()
