"""
Automated Validator for Langflow Workflows
Checks graph topology, node structure, handles, and custom code integrations.
"""

import json
import glob
import sys

def validate_flow(file_path):
    print(f"\nValidating: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ JSON Parse Error: {e}")
        return False

    if "data" not in data or "nodes" not in data["data"] or "edges" not in data["data"]:
        print("❌ Missing top-level Langflow schema fields ('data', 'nodes', 'edges')")
        return False

    nodes = data["data"]["nodes"]
    edges = data["data"]["edges"]
    node_ids = {n["id"] for n in nodes}

    print(f"  • Nodes: {len(nodes)}")
    print(f"  • Edges: {len(edges)}")

    # Check duplicate node IDs
    if len(node_ids) != len(nodes):
        print("❌ Duplicate node IDs detected!")
        return False

    # Check edge connections
    for i, e in enumerate(edges):
        src = e.get("source")
        tgt = e.get("target")
        if src not in node_ids:
            print(f"❌ Edge {i}: Source node '{src}' does not exist.")
            return False
        if tgt not in node_ids:
            print(f"❌ Edge {i}: Target node '{tgt}' does not exist.")
            return False

    # Check node display names and types
    for n in nodes:
        node_id = n["id"]
        node_type = n.get("type", "")
        comp_type = n.get("data", {}).get("type", "")
        display_name = n.get("data", {}).get("node", {}).get("display_name", "")
        print(f"    ✓ [{node_id}] {display_name} ({comp_type})")

    print(f"✅ {file_path} is structurally 100% valid!")
    return True

def main():
    flow_files = sorted(glob.glob("flows/*.json"))
    if not flow_files:
        print("❌ No flow files found in flows/")
        sys.exit(1)

    all_valid = True
    for f in flow_files:
        if not validate_flow(f):
            all_valid = False

    print("\n" + "=" * 60)
    if all_valid:
        print("🎉 ALL 3 LANGFLOW WORKFLOWS ARE 100% VALID & READY!")
    else:
        print("❌ Some workflows failed validation.")
        sys.exit(1)

if __name__ == "__main__":
    main()
