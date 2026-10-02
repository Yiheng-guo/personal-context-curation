#!/usr/bin/env python3
"""Local structured-input helper. Semantic judgments must be supplied or reviewed by a human/agent."""
import argparse, json, sys, math
from pathlib import Path
from datetime import date

def need(condition, message):
    if not condition: raise ValueError(message)
def ids(rows, label):
    seen=set()
    for row in rows:
        value=row.get('id'); need(isinstance(value,str) and value.strip(),label+' requires nonempty id')
        need(value not in seen,label+' duplicate id: '+value);seen.add(value)
    return seen
def number(value, label):
    need(not isinstance(value,bool) and isinstance(value,(int,float)) and math.isfinite(value),label+' must be finite number');return value

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path); parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    try:
        need(not args.output.exists(),'refusing to overwrite output')
        data=json.loads(args.input.read_text(encoding='utf-8'));need(isinstance(data,dict),'input must be object')
        result=process(data)
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open('x',encoding='utf-8') as f: json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
        print(json.dumps({'output':str(args.output),'status':result.get('status','completed')},ensure_ascii=False))
        return 0 if result.get('status') not in ('blocked','failed') else 2
    except (ValueError,KeyError,TypeError,OSError) as e: print('error: '+str(e),file=sys.stderr);return 2

def process(d):
    memories=d['memories'];ids(memories,'memories');today=date.fromisoformat(d['as_of']);proposals=[];bykey={}
    for m in memories:
        for f in ('subject','key','value','kind','source','observed_at'):need(m.get(f),'missing context '+f)
        need(m['kind'] in ('fact','inference','unknown'),'invalid kind');date.fromisoformat(m['observed_at'])
        reasons=[]
        if m['subject']!='user':reasons.append('third_party_subject')
        if m.get('sensitive'):reasons.append('sensitive')
        if m.get('consent') is not True:reasons.append('no_explicit_retention_consent')
        if m['kind']!='fact':reasons.append('not_fact')
        if m.get('valid_until') and date.fromisoformat(m['valid_until'])<today:reasons.append('expired')
        if m.get('superseded_by'):reasons.append('superseded')
        proposal={**m,'action':'exclude' if reasons else 'candidate','reasons':reasons};proposals.append(proposal)
        if not reasons:bykey.setdefault(m['key'],[]).append(proposal)
    for key,rs in bykey.items():
        if len({json.dumps(r['value'],sort_keys=True,ensure_ascii=False) for r in rs})>1:
            for r in rs:r['action']='needs_correction';r['reasons'].append('conflict')
    return {'status':'proposal_only','proposals':proposals,'candidate_context':[r for r in proposals if r['action']=='candidate'],'writes_performed':False,'limits':'Does not write platform memory. Apply approved changes through its authorized memory mechanism; deletion must cover copies and retrieval indexes.'}

if __name__ == "__main__": raise SystemExit(main())
