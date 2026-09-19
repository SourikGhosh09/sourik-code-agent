"""Real model acceptance tasks, with independent tests and restricted command approval.

Not a general sandbox. Only this tiny calculator evaluation is approved here.
"""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from local_agent.agent import Agent
from local_agent.models import LocalModel
from local_agent.resources import detect,profile


def approve_calculator(root,argv):
    # Evaluation runs only unittest or the specified calculator, after checking
    # imports/calls in every generated Python file. Production always asks user.
    if Path(argv[0]).stem.lower() not in ('python','python3','python314'):
        return False
    if argv[1:] not in (['-m','unittest','discover'],['-m','unittest'],['-m','unittest','discover','-v'],['-m','unittest','-v']):
        return False
    allowed_calls={'add','subtract','multiply','divide','float','int','str','print','len','abs','sum','round','ValueError','ZeroDivisionError','main','assertEqual','assertAlmostEqual','assertRaises','assertTrue','assertFalse','assertIn','assertIsInstance','subTest'}
    for p in root.rglob('*.py'):
        if '.agent' in p.parts:
            continue
        try:
            tree=ast.parse(p.read_text(encoding='utf-8'))
        except (SyntaxError,UnicodeError):
            continue  # Let unittest report syntax failures for the repair loop.
        for node in ast.walk(tree):
            if isinstance(node,ast.Import) and any(a.name not in ('unittest','calculator','math') for a in node.names):
                return False
            if isinstance(node,ast.ImportFrom) and node.module not in ('unittest','calculator','math'):
                return False
            if isinstance(node,ast.Attribute) and node.attr.startswith('__'):
                return False
            if isinstance(node,ast.Call):
                name=node.func.id if isinstance(node.func,ast.Name) else node.func.attr if isinstance(node.func,ast.Attribute) else ''
                if name not in allowed_calls:
                    return False
    return True


def main():
    base=Path(__file__).resolve().parents[1]/'evaluation-results'/time.strftime('%Y%m%d-%H%M%S')
    base.mkdir(parents=True)
    model=sys.argv[1] if len(sys.argv)>1 else 'qwen2.5-coder:3b'
    code_root=Path(__file__).resolve().parents[1]/'local_agent'
    code_digest=hashlib.sha256(b''.join(p.name.encode()+p.read_bytes() for p in sorted(code_root.glob('*.py')))).hexdigest()
    model_runtime=LocalModel(model)
    model_digest=next((m.get('digest') for m in model_runtime.installed_models() if m.get('name')==model),None)
    results=[]
    for power,case in [('Eco','empty'),('Balanced','broken')]:
        root=base/case
        root.mkdir()
        if case=='broken':
            (root/'calculator.py').write_text('def add(a, b):\n    return a - b\n\ndef divide(a, b):\n    return a / b\n',encoding='utf-8')
            (root/'test_calculator.py').write_text('import unittest\nfrom calculator import add, divide\nclass TestCalculator(unittest.TestCase):\n    def test_add(self):\n        self.assertEqual(add(2, 3), 5)\n    def test_divide(self):\n        self.assertEqual(divide(8, 2), 4)\n',encoding='utf-8')
        goal=('Create a small Python calculator in calculator.py with add(a,b), subtract(a,b), multiply(a,b), divide(a,b). Division by zero must raise ZeroDivisionError. Create unittest tests in test_calculator.py and verify them.' if case=='empty' else 'Find and repair the bug in this calculator project. Run the existing tests first to observe the failure, fix the source code rather than weakening tests, then verify again.')
        goal+=' Use only Python standard library. Run tests using exactly python -m unittest discover. No shell commands, dependency installs, or other commands are approved for this evaluation.'
        config=profile(detect(root),power)
        events=[]
        def emit(event):
            events.append(event)
            print(case,event['kind'],json.dumps(event['data'])[:1200],flush=True)
        agent=Agent(root,model_runtime,config,emit,lambda argv:approve_calculator(root,argv))
        start=time.monotonic()
        state=agent.run(goal)
        # Independently inspect source and verify behavior; do not trust model-written tests.
        independent=False
        if (root/'calculator.py').exists() and approve_calculator(root,['python','-m','unittest','discover']):
            assertions='from calculator import add, divide; assert add(2,3)==5; assert add(-3,1)==-2; assert divide(9,3)==3\ntry:\n divide(1,0)\nexcept ZeroDivisionError:\n pass\nelse:\n raise AssertionError("division by zero")\n'
            if case=='empty':
                assertions+='from calculator import subtract, multiply\nassert subtract(7,2)==5\nassert multiply(-2,4)==-8\n'
            check=subprocess.run([sys.executable,'-I','-c','import sys; sys.path.insert(0, '+repr(str(root))+');\n'+assertions],capture_output=True,text=True,timeout=15)
            independent=check.returncode==0
            (root/'independent-check.txt').write_text(check.stdout+check.stderr,encoding='utf-8')
        failed_observation=any(e['kind']=='observation' and isinstance(e['data'],dict) and e['data'].get('exit_code',0)!=0 for e in events)
        result=dict(suite_version='v0-1',model=model,model_digest=model_digest,code_digest=code_digest,case=case,profile=power,config=config,state=state,independent_pass=independent,observed_failure=failed_observation,seconds=round(time.monotonic()-start,2))
        results.append(result)
        (base/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
        print('RESULT',json.dumps(result),flush=True)
    return 0 if all(r['state']=='COMPLETED' and r['independent_pass'] for r in results) and results[1]['observed_failure'] else 1


if __name__=='__main__':
    raise SystemExit(main())
