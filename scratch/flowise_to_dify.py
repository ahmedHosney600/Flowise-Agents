import json
import yaml
import re

def create_dify_workflow():
    with open('scratch/flow_dump2.json', 'r') as f:
        data = json.load(f)
        
    nodes = data['nodes']
    edges = data['edges']
    
    dify = {
        'app': {
            'description': 'Imported from Flowise',
            'icon': '🤖',
            'icon_background': '#FFEAD5',
            'icon_type': 'emoji',
            'mode': 'workflow',
            'name': '00_flowise_video_preplanning_flow',
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
    for nid, nd in nodes.items():
        if nd['name'] == 'startAgentflow':
            start_node_id = nid
            variables = []
            for inp in nd.get('formInputs', []):
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
                state_to_node[f"$form.{var_name}"] = f"{{{{#{nid}.{var_name}#}}}}"
                
            for state_var in nd.get('startState', []):
                state_to_node[f"$flow.state.{state_var['key']}"] = state_var['value'] # literal default initially, or later node ref
                
            dify['workflow']['graph']['nodes'].append({
                'id': nid,
                'type': 'custom',
                'data': {
                    'title': nd.get('label', 'Start'),
                    'type': 'start',
                    'variables': variables
                },
                'position': {'x': 100, 'y': 100}
            })
            break

    # Helper to resolve references
    def resolve_refs(text):
        # Replace {{ $form.videoTopic }} with {{#startAgentflow_0.videoTopic#}}
        # Replace {{ $flow.state.project_brief }} with {{#llmAgentflow_0.text#}}
        def repl(match):
            key = match.group(1).strip()
            if key in state_to_node:
                val = state_to_node[key]
                return val if val.startswith('{{#') else f"{{{val}}}"
            return match.group(0)
        return re.sub(r'\{\{\s*(.*?)\s*\}\}', repl, text)

    # Topological or sequential layout logic: just lay them out simply
    x, y = 300, 100
    
    # 2. Map other nodes
    for nid, nd in nodes.items():
        if nid == start_node_id:
            continue
            
        dify_node = {
            'id': nid,
            'type': 'custom',
            'position': {'x': x, 'y': y},
            'data': {
                'title': nd.get('label', nid),
            }
        }
        x += 300
        
        if nd['name'] == 'llmAgentflow':
            dify_node['data']['type'] = 'llm'
            dify_node['data']['model'] = {
                'provider': 'openai',
                'name': 'gpt-4o-mini',
                'mode': 'chat',
                'completion_params': {'temperature': 0.7}
            }
            pts = []
            for m in nd.get('llmMessages', []):
                pts.append({
                    'role': m['role'],
                    'text': resolve_refs(m['content'])
                })
            dify_node['data']['prompt_template'] = pts
            
            # Update state registry for subsequent nodes
            for state_update in nd.get('llmUpdateState', []):
                key = state_update['key']
                state_to_node[f"$flow.state.{key}"] = f"{{{{#{nid}.text#}}}}"
                
        elif nd['name'] == 'conditionAgentflow':
            dify_node['data']['type'] = 'if-else'
            # simplified condition, dify conditions are complex, we'll just put a dummy true condition for parsing
            dify_node['data']['conditions'] = []
            
        elif nd['name'] == 'humanInputAgentflow':
            dify_node['data']['type'] = 'question-classifier' # Dify doesn't have human input in workflows normally, maybe parameter extractor or question classifier
            dify_node['data']['classes'] = [{'id': '1', 'name': 'Continue'}]
            
        elif nd['name'] == 'directReplyAgentflow':
            dify_node['data']['type'] = 'end'
            dify_node['data']['outputs'] = [
                {
                    'variable': 'final_output',
                    'value_selector': ['startAgentflow_0', 'videoTopic'] # placeholder
                }
            ]
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
        
    with open('dify_workflows/00_flowise_video_preplanning_flow.yml', 'w') as f:
        yaml.dump(dify, f, sort_keys=False, default_flow_style=False)

if __name__ == '__main__':
    create_dify_workflow()
