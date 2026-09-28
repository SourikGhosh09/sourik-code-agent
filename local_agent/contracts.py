"""State-dependent response shapes shared by model adapters."""

REQUIRED_FIELDS = {
    'list': (), 'read': ('path',), 'search': ('query',),
    'write': ('path', 'content'), 'patch': ('path', 'old', 'new'),
    'move': ('path', 'destination'), 'delete': ('path',), 'run': ('argv',),
}


def validate_action(action):
    tool = action.get('tool')
    if tool not in REQUIRED_FIELDS:
        raise ValueError('Choose a supported tool.')
    missing = [key for key in REQUIRED_FIELDS[tool] if key not in action]
    if missing:
        raise ValueError(f'{tool} requires fields: {", ".join(missing)}. Return a complete action.')
    for key in REQUIRED_FIELDS[tool]:
        if key != 'argv' and not isinstance(action[key], str):
            raise ValueError(f'{tool}.{key} must be a string.')
    if tool == 'patch' and not action['old']:
        raise ValueError('patch.old must contain the exact existing text to replace.')
    if tool == 'patch' and action['old'] == action['new']:
        raise ValueError('Patch old and new are identical; no repair is needed there. Run approved tests on current code to identify any remaining failure before another edit.')


def response_schema(planned, verified, simplicity_required=False):
    plan = {'type':'object','properties':{
        'plan':{'type':'array','items':{'type':'string'},'minItems':1},
        'change_budget':{'type':'object','properties':{**{k:{'type':'integer','minimum':0} for k in ('files','new_files','dependencies')},'complexity':{'type':'string'}},'required':['files','new_files','dependencies','complexity'],'additionalProperties':False}},
        'required':['plan','change_budget'],'additionalProperties':False}
    if not planned:
        return plan
    props={'reason':{'type':'string','description':'One short sentence describing the concrete purpose of this action, addressing the latest error if any.'},'tool':{'type':'string','enum':['list','read','search','write','patch','move','delete','run']}}
    for key in ('path','content','old','new','destination','query','simplicity'):
        props[key]={'type':'string'}
    props['argv']={'type':'array','items':{'type':'string'}}
    props['verify']={'type':'boolean'}
    for key in ('timeout','start_line','line_count'):
        props[key]={'type':'integer'}
    actions = []
    optional = {'read': ('start_line', 'line_count'), 'run': ('verify', 'timeout')}
    for tool, fields in REQUIRED_FIELDS.items():
        keys = ('reason', 'tool', 'simplicity') + fields + optional.get(tool, ())
        tool_props = {key: props[key] for key in keys}
        tool_props['tool'] = {'type': 'string', 'enum': [tool]}
        actions.append({'type': 'object', 'properties': tool_props,
                        'required': ['reason', 'tool', *fields] + (['simplicity'] if simplicity_required and tool in ('write', 'patch', 'move', 'delete') else []),
                        'additionalProperties': False})
    done={'type':'object','properties':{'done':{'type':'string'},'simplicity':{'type':'string'}},'required':['done']+(['simplicity'] if simplicity_required else []),'additionalProperties':False}
    finish = {'type':'object','properties':{'reason':props['reason'], 'tool':{'type':'string','enum':['finish']},
              'content':{'type':'string'}, 'simplicity':{'type':'string'}},
              'required':['reason','tool','content']+(['simplicity'] if simplicity_required else []), 'additionalProperties':False}
    return {'anyOf': ([finish, done] if verified else []) + actions}
