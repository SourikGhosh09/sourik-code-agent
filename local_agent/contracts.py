"""State-dependent response shapes shared by model adapters."""

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
    action={'type':'object','properties':props,'required':['reason','tool']+(['simplicity'] if simplicity_required else []),'additionalProperties':False}
    done={'type':'object','properties':{'done':{'type':'string'},'simplicity':{'type':'string'}},'required':['done']+(['simplicity'] if simplicity_required else []),'additionalProperties':False}
    return {'anyOf':[action,done]} if verified else action
