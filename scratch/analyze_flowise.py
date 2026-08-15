import json
import sys

def dump_node_details(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)

    nodes = data.get('nodes', [])
    edges = data.get('edges', [])
    
    flow_info = {
        'nodes': {},
        'edges': edges
    }

    for node in nodes:
        node_id = node.get('id')
        data_inputs = node.get('data', {}).get('inputs', {})
        node_type = node.get('type')
        node_name = node.get('data', {}).get('name')
        
        node_data = {
            'type': node_type,
            'name': node_name,
            'label': node.get('data', {}).get('label')
        }
        
        if node_name == 'startAgentflow':
            node_data['formInputs'] = data_inputs.get('formInputTypes', [])
            node_data['startState'] = data_inputs.get('startState', [])
        
        elif node_name == 'llmAgentflow':
            node_data['llmMessages'] = data_inputs.get('llmMessages', [])
            node_data['llmUpdateState'] = data_inputs.get('llmUpdateState', [])
            node_data['llmStructuredOutput'] = data_inputs.get('llmStructuredOutput', {})
            
        elif node_name == 'conditionAgentflow':
            node_data['conditions'] = data_inputs.get('conditions', [])
            
        elif node_name == 'humanInputAgentflow':
            node_data['question'] = data_inputs.get('question', '')
            node_data['questionMessage'] = data_inputs.get('questionMessage', '')
            node_data['humanUpdateState'] = data_inputs.get('humanUpdateState', [])
            
        elif node_name == 'loopAgentflow':
            node_data['loopTo'] = data_inputs.get('loopTo', '')
            
        elif node_name == 'directReplyAgentflow':
            node_data['replyMessage'] = data_inputs.get('replyMessage', '')
            node_data['responseSource'] = data_inputs.get('responseSource', '')
            
        flow_info['nodes'][node_id] = node_data
        
    with open('scratch/flow_dump2.json', 'w') as f:
        json.dump(flow_info, f, indent=2)

if __name__ == '__main__':
    dump_node_details(sys.argv[1])
