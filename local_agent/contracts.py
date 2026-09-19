"""State-dependent response shapes shared by model adapters."""

def response_schema(planned, verified):
    if not planned:
        return {'type':'object','properties':{'plan':{'type':'array','items':{'type':'string'},'minItems':1}},'required':['plan'],'additionalProperties':False}
    props={'reason':{'type':'string','description':'One short sentence describing the concrete purpose of this action, addressing the latest error if any.'},'tool':{'type':'string','enum':['list','read','search','write','patch','move','delete','run']}}
    for key in ('path','content','old','new','destination','query'):
        props[key]={'type':'string'}
    props['argv']={'type':'array','items':{'type':'string'}}
    props['verify']={'type':'boolean'}
    for key in ('timeout','start_line','line_count'):
        props[key]={'type':'integer'}
    action={'type':'object','properties':props,'required':['reason','tool'],'additionalProperties':False}
    done={'type':'object','properties':{'done':{'type':'string'}},'required':['done'],'additionalProperties':False}
    return {'anyOf':[action,done]} if verified else action
