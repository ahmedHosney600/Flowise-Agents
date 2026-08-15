import json
import yaml
import re
import os
import glob

def create_dify_workflow(json_path, yaml_path, name):
    with open(json_path, 'r') as f:
        data = json.load(f)
        
    nodes = data.get('nodes', [])
    edges = data.get('edges', [])
    
    # We will build a dictionary of nodes keyed by ID for easy access
    node_dict = {n['id']: n for n in nodes}
    
    dify = {
        'app': {
            'description': 'Imported from Flowise',
            'icon': '🤖',
            'icon_background': '#FFEAD5',
            'icon_type': 'emoji',
            'mode': 'workflow',
            'name': name,
            'use_icon_as_answer_icon': False
        },
        'kind': 'app',
        'version': '0.1.0',
        'workflow': {
            'conversation_variables': [],
            'environment_variables': [],
            'features': {},
            'graph': {
                'edges': [],
                'nodes': []
            }
        }
    }
    
    state_to_node = {} # tracks which node outputs which state variable
    
    # 1. Map Start Node
    start_node_id = None
    for nd in nodes:
        node_name = nd.get('data', {}).get('name')
        if node_name == 'startAgentflow':
            start_node_id = nd['id']
            inputs_data = nd.get('data', {}).get('inputs', {})
            variables = []
            for inp in inputs_data.get('formInputTypes', []):
                var_name = inp['name']
                v_type = 'text-input' if inp['type'] == 'string' else 'select' if inp['type'] == 'options' else 'text-input'
                opts = [o['option'] for o in inp.get('addOptions', [])] if v_type == 'select' else []
                variables.append({
                    'variable': var_name,
                    'label': inp.get('label', var_name),
                    'type': v_type,
                    'required': False,
                    'options': opts,
                    'default': ''
                })
                state_to_node[f"$form.{var_name}"] = f"{{{{#{start_node_id}.{var_name}#}}}}"
                
            for state_var in inputs_data.get('startState', []):
                state_to_node[f"$flow.state.{state_var['key']}"] = state_var['value'] # literal default initially, or later node ref
                
            dify['workflow']['graph']['nodes'].append({
                'id': start_node_id,
                'type': 'custom',
                'data': {
                    'title': nd.get('data', {}).get('label', 'Start'),
                    'type': 'start',
                    'variables': variables
                },
                'position': {'x': 100, 'y': 100}
            })
            break

    # Helper to resolve references
    def resolve_refs(text):
        if not isinstance(text, str):
            return text
        # Replace {{ $form.videoTopic }} with {{#startAgentflow_0.videoTopic#}}
        # Replace {{ $flow.state.project_brief }} with {{#llmAgentflow_0.text#}}
        def repl(match):
            key = match.group(1).strip()
            if key in state_to_node:
                val = state_to_node[key]
                return val if val.startswith('{{#') else f"{{{val}}}"
            return match.group(0)
        return re.sub(r'\{\{\s*(.*?)\s*\}\}', repl, text)

    # Topological layout logic simple layout
    x, y = 300, 100
    
    # 2. Map other nodes
    for nd in nodes:
        nid = nd['id']
        if nid == start_node_id:
            continue
            
        node_name = nd.get('data', {}).get('name')
        data_inputs = nd.get('data', {}).get('inputs', {})
        
        dify_node = {
            'id': nid,
            'type': 'custom',
            'position': {'x': x, 'y': y},
            'data': {
                'title': nd.get('data', {}).get('label', nid),
            }
        }
        x += 300
        
        if node_name == 'llmAgentflow':
            dify_node['data']['type'] = 'llm'
            dify_node['data']['model'] = {
                'provider': 'openai',
                'name': 'gpt-4o-mini',
                'mode': 'chat',
                'completion_params': {'temperature': 0.7}
            }
            pts = []
            for m in data_inputs.get('llmMessages', []):
                pts.append({
                    'role': m['role'],
                    'text': resolve_refs(m['content'])
                })
            dify_node['data']['prompt_template'] = pts
            
            # Update state registry for subsequent nodes
            for state_update in data_inputs.get('llmUpdateState', []):
                key = state_update['key']
                state_to_node[f"$flow.state.{key}"] = f"{{{{#{nid}.text#}}}}"
                
        elif node_name == 'conditionAgentflow':
            dify_node['data']['type'] = 'if-else'
            # Dify conditions structure is complex, we just put an empty block for parsing
            dify_node['data']['conditions'] = []
            
        elif node_name == 'humanInputAgentflow':
            dify_node['data']['type'] = 'question-classifier'
            dify_node['data']['classes'] = [{'id': '1', 'name': 'Continue'}]
            
        elif node_name == 'directReplyAgentflow':
            dify_node['data']['type'] = 'end'
            dify_node['data']['outputs'] = [
                {
                    'variable': 'final_output',
                    'value_selector': [start_node_id, 'videoTopic'] if start_node_id else []
                }
            ]
            
        elif node_name == 'loopAgentflow':
            dify_node['data']['type'] = 'code' # Placeholder for loop, as dify doesn't have loops easily
            dify_node['data']['code'] = 'def main(arg1):\n    return {"result": arg1}'
            
        else:
            dify_node['data']['type'] = 'code'
            
        dify['workflow']['graph']['nodes'].append(dify_node)
        
    # 3. Map Edges
    for edge in edges:
        source = edge['source']
        target = edge['target']
        dify['workflow']['graph']['edges'].append({
            'id': edge['id'],
            'source': source,
            'target': target,
            'sourceHandle': 'source',
            'targetHandle': 'target',
            'type': 'custom',
            'data': {'sourceType': 'llm', 'targetType': 'llm'}
        })
        
    os.makedirs(os.path.dirname(yaml_path), exist_ok=True)
    with open(yaml_path, 'w') as f:
        yaml.dump(dify, f, sort_keys=False, default_flow_style=False)
        
    print(f"Successfully converted {os.path.basename(json_path)} to {os.path.basename(yaml_path)}")

def main():
    flowise_dir = 'flowise_flows'
    dify_dir = 'dify_workflows'
    
    json_files = glob.glob(os.path.join(flowise_dir, '*.json'))
    
    for j_path in json_files:
        basename = os.path.basename(j_path)
        name, _ = os.path.splitext(basename)
        y_path = os.path.join(dify_dir, f"{name}.yml")
        create_dify_workflow(j_path, y_path, name)

if __name__ == '__main__':
    main()
