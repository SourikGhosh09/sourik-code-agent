"""Real model acceptance tasks, with independent tests and restricted command approval.

Not a general sandbox. Approval is limited to the calculator or fixed trusted repair fixtures.
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
from local_agent.resources import detect,preference_profile
from local_agent.storage import Store
from local_agent.context import evidence_for


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



# Fixed trusted fixture variants keep automated approval specific to this task.
# This deliberately tests arithmetic repair across imports, not arbitrary code generation.
INVOICE_FILES = {
    'validation.py': "def validate_quantity(quantity):\n    if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity < 0:\n        raise ValueError('quantity must be a nonnegative integer')\n",
    'line_items.py': "from validation import validate_quantity\n\ndef line_total(unit_cents, quantity):\n    validate_quantity(quantity)\n    if unit_cents < 0:\n        raise ValueError('price must be nonnegative')\n    return unit_cents + quantity\n",
    'invoice.py': "from line_items import line_total\n\ndef invoice_total(items, discount_cents=0):\n    subtotal = sum(line_total(price, quantity) for price, quantity in items)\n    if discount_cents < 0 or discount_cents > subtotal:\n        raise ValueError('discount out of range')\n    return subtotal + discount_cents\n",
    'test_invoice.py': "import unittest\nfrom invoice import invoice_total\nfrom line_items import line_total\n\nclass InvoiceTests(unittest.TestCase):\n    def test_line(self):\n        self.assertEqual(line_total(125, 3), 375)\n    def test_invoice(self):\n        self.assertEqual(invoice_total([(125, 3), (200, 2)], 75), 700)\n    def test_quantity(self):\n        with self.assertRaises(ValueError):\n            line_total(100, -1)\n    def test_discount(self):\n        with self.assertRaises(ValueError):\n            invoice_total([], 1)\n",
    'README.md': 'Invoice amounts use integer cents. Multiply price by quantity; subtract the invoice discount. Keep validation and public functions. No dependencies are needed.\n',
}
INVOICE_FIXED = {
    **INVOICE_FILES,
    'line_items.py': INVOICE_FILES['line_items.py'].replace('unit_cents + quantity', 'unit_cents * quantity'),
    'invoice.py': INVOICE_FILES['invoice.py'].replace('subtotal + discount_cents', 'subtotal - discount_cents'),
}


# Non-arithmetic repair: Unicode normalization and stable deduplication.
TAG_FILES = {
    'validation.py': "def validate_tag(tag):\n    if not isinstance(tag, str) or not tag.strip():\n        raise ValueError('tag must be a nonempty string')\n",
    'normalization.py': "from validation import validate_tag\n\ndef normalize_tag(tag):\n    validate_tag(tag)\n    return tag.strip().lower()\n",
    'catalog.py': "from normalization import normalize_tag\n\ndef unique_tags(tags):\n    normalized = [normalize_tag(tag) for tag in tags]\n    return sorted(set(normalized))\n",
    'test_catalog.py': "import unittest\nfrom normalization import normalize_tag\nfrom catalog import unique_tags\n\nclass CatalogTests(unittest.TestCase):\n    def test_unicode(self):\n        self.assertEqual(normalize_tag(' Stra\u00dfe '), 'strasse')\n    def test_order(self):\n        self.assertEqual(unique_tags(['Zulu', 'alpha', 'Zulu']), ['zulu', 'alpha'])\n    def test_invalid(self):\n        with self.assertRaises(ValueError):\n            unique_tags(['good', '  '])\n    def test_empty(self):\n        self.assertEqual(unique_tags([]), [])\n",
    'README.md': 'Normalize tags by stripping whitespace and Unicode casefolding. Deduplicate normalized tags while preserving first-seen order. Preserve input, validation and public functions. Use existing modules and the standard library only.\n',
}
TAG_FIXED = {
    **TAG_FILES,
    'normalization.py': TAG_FILES['normalization.py'].replace('.lower()', '.casefold()'),
    'catalog.py': TAG_FILES['catalog.py'].replace('sorted(set(normalized))', 'list(dict.fromkeys(normalized))'),
}
TAG_CHECKS = """from normalization import normalize_tag
from catalog import unique_tags
assert normalize_tag(' Stra\u00dfe ') == 'strasse'
assert normalize_tag(' \u03a3 ') == normalize_tag('\u03c2') == '\u03c3'
source = ['Zulu', ' Stra\u00dfe ', 'alpha', 'STRASSE', ' ZULU ']
before = source.copy()
assert unique_tags(source) == ['zulu', 'strasse', 'alpha']
assert source == before
assert unique_tags(iter(['B', 'a', 'b'])) == ['b', 'a']
assert unique_tags([]) == []
for tag in ('', '  ', None, 42, True):
    try: unique_tags(['valid', tag])
    except ValueError: pass
    else: raise AssertionError('invalid tag accepted')
"""


def approve_invoice(root, argv):
    return _approve_fixture(root, argv, INVOICE_FILES, INVOICE_FIXED, ('line_items.py', 'invoice.py'))


def approve_tags(root, argv):
    return _approve_fixture(root, argv, TAG_FILES, TAG_FIXED, ('normalization.py', 'catalog.py'))


def _approve_fixture(root, argv, files, fixed, editable):
    if not argv or argv[0] not in ('python', sys.executable):
        return False
    if argv[1:] not in (['-m', 'unittest', 'discover'], ['-m', 'unittest', 'discover', '-v']):
        return False
    try:
        for name, original in files.items():
            path = root / name
            if path.is_symlink() or path.is_junction() or not path.is_file():
                return False
            actual = path.read_text(encoding='utf-8')
            if name in editable:
                # AST identity allows comments/formatting, but no new executable behavior.
                allowed = {ast.dump(ast.parse(original)), ast.dump(ast.parse(fixed[name]))}
                if ast.dump(ast.parse(actual)) not in allowed:
                    return False
            elif actual != original:
                return False
        for path in root.rglob('*'):
            relative = path.relative_to(root)
            if path.is_symlink() or path.is_junction():
                return False
            if relative.parts[0] == '.agent':
                continue
            if path.is_file() and str(relative) not in files and str(relative) != 'PROJECT_LOG.txt':
                # Reject added modules, bytecode and startup customizations as well.
                return False
    except (OSError, UnicodeError, SyntaxError):
        return False
    return True


def evaluate_multifile(base, model_runtime, model, model_digest, code_digest, suite='invoice'):
    if suite not in ('invoice', 'tags'):
        raise ValueError('Unknown trusted repair suite.')
    files = TAG_FILES if suite == 'tags' else INVOICE_FILES
    approve = approve_tags if suite == 'tags' else approve_invoice
    preserved_names = ('test_catalog.py', 'validation.py', 'README.md') if suite == 'tags' else ('test_invoice.py', 'validation.py', 'README.md')
    results = []
    for repeat in range(1, 3):
        root = base / f'{suite}-{repeat}'
        root.mkdir()
        for name, content in files.items():
            (root / name).write_text(content, encoding='utf-8')
        events = []
        def emit(event):
            events.append(event)
            print(root.name, event['kind'], json.dumps(event['data'])[:1000], flush=True)
        config = preference_profile(detect(root), 'Balanced')
        agent = Agent(root, model_runtime, config, emit, lambda argv: approve(root, argv))
        goal = ('Repair this multi-file invoice project. Inspect its modules and run the existing tests first. '
                'Line totals must multiply integer cents by quantity; invoice totals must subtract the discount. '
                'Preserve validation, public functions, README and existing tests. Reuse the existing modules; '
                'add no files or dependencies. Only python -m unittest discover is approved. '
                'This controlled evaluation accepts only arithmetic-expression repairs to the two existing functions.')
        if suite == 'tags':
            goal = ('Repair this tag catalog project. Inspect its modules and run existing tests first. '
                    'Normalize tags with strip and Unicode casefold, then deduplicate with list(dict.fromkeys(normalized)) '
                    'to preserve first-seen order. Preserve validation, public functions, README and existing tests. '
                    'Reuse existing modules; add no files or dependencies. Only python -m unittest discover is approved. '
                    'This controlled evaluation accepts only these expression repairs in normalization.py and catalog.py.')
        started = time.monotonic()
        state = agent.run(goal)
        approved = approve(root, ['python', '-m', 'unittest', 'discover'])
        independent = False
        if approved:
            # Execute only AST-identical trusted fixture variants, independently of model tests.
            checks = """from invoice import invoice_total
from line_items import line_total
assert line_total(125, 3) == 375
assert line_total(999, 0) == 0
assert invoice_total([(125, 3), (200, 2)], 75) == 700
assert invoice_total([], 0) == 0
assert invoice_total([(25, 4)], 100) == 0
for quantity in (-1, 1.5, True):
    try: line_total(100, quantity)
    except ValueError: pass
    else: raise AssertionError('invalid quantity accepted')
for items, discount in (([], 1), ([(100, 1)], -1), ([(100, 1)], 101)):
    try: invoice_total(items, discount)
    except ValueError: pass
    else: raise AssertionError('invalid discount accepted')
try: line_total(-1, 1)
except ValueError: pass
else: raise AssertionError('negative price accepted')
"""
            if suite == 'tags':
                checks = TAG_CHECKS
            check = subprocess.run([sys.executable, '-I', '-B', '-c',
                'import sys; sys.path.insert(0, ' + repr(str(root)) + ');\n' + checks],
                capture_output=True, text=True, timeout=15)
            independent = check.returncode == 0
            (base / f'{suite}-{repeat}-independent.txt').write_text(check.stdout + check.stderr, encoding='utf-8')
        changed = [name for name, original in files.items()
                   if not (root / name).exists() or (root / name).read_text(encoding='utf-8') != original]
        preserved = all((root / name).exists() and (root / name).read_text(encoding='utf-8') == files[name]
                        for name in preserved_names)
        observed = any(e['kind'] == 'observation' and isinstance(e['data'], dict)
                       and e['data'].get('exit_code', 0) != 0 for e in events)
        reviews = sum(e['kind'] == 'simplicity' and e['data'].get('phase') == 'review' for e in events)
        passed = state == 'COMPLETED' and independent and preserved and observed and reviews > 0 and approved
        result = dict(suite_version='tags-1' if suite == 'tags' else 'multifile-1', case=root.name, model=model, model_digest=model_digest,
                      code_digest=code_digest, evaluator_digest=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      state=state, passed=passed, independent_pass=independent, tests_and_validation_preserved=preserved,
                      observed_failure=observed, simplicity_reviews=reviews, changed_files=changed,
                      trusted_fixture_only=approved, config=config, seconds=round(time.monotonic()-started, 2))
        results.append(result)
        (base / 'results.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
        print('RESULT', json.dumps(result), flush=True)
    return 0 if all(r['passed'] for r in results) else 1


def main():
    base=Path(__file__).resolve().parents[1]/'evaluation-results'/time.strftime('%Y%m%d-%H%M%S')
    base.mkdir(parents=True)
    model=sys.argv[1] if len(sys.argv)>1 else 'qwen2.5-coder:3b'
    code_root=Path(__file__).resolve().parents[1]/'local_agent'
    code_digest=hashlib.sha256(b''.join(p.name.encode()+p.read_bytes() for p in sorted(code_root.glob('*.py')))).hexdigest()
    model_runtime=LocalModel(model)
    model_digest=next((m.get('digest') for m in model_runtime.installed_models() if m.get('name')==model),None)
    if '--tags' in sys.argv:
        return evaluate_multifile(base, model_runtime, model, model_digest, code_digest, suite='tags')
    if '--multifile' in sys.argv:
        return evaluate_multifile(base, model_runtime, model, model_digest, code_digest)
    results=[]
    cases = [('Eco','empty'),('Balanced','broken'),('Balanced','indexed')]
    if '--simplicity' in sys.argv:
        cases.append(('Balanced','satisfied'))
    for power,case in cases:
        root=base/case
        root.mkdir()
        if case!='empty':
            (root/'calculator.py').write_text('def add(a, b):\n    return a - b\n\ndef divide(a, b):\n    return a / b\n',encoding='utf-8')
            (root/'test_calculator.py').write_text('import unittest\nfrom calculator import add, divide\nclass TestCalculator(unittest.TestCase):\n    def test_add(self):\n        self.assertEqual(add(2, 3), 5)\n    def test_divide(self):\n        self.assertEqual(divide(8, 2), 4)\n',encoding='utf-8')
        if case == 'satisfied':
            source = root/'calculator.py'
            source.write_text(source.read_text(encoding='utf-8').replace('a - b','a + b'),encoding='utf-8')
        original_source = (root/'calculator.py').read_bytes() if case == 'satisfied' else None
        original_tests = (root/'test_calculator.py').read_bytes() if case != 'empty' else None
        if case == 'indexed':
            for index in range(110):
                (root/f'a_filler_{index:03}.py').write_text(f'VALUE = {index}\n',encoding='utf-8')
            memory = Store(root)
            memory.add_memory('verified_task','Addition must subtract numbers; all tests previously passed.','stale-fixture',{'calculator.py':'outdated-fingerprint'})
            memory.add_memory('note','Keep the existing public calculator functions and test cases.')
            memory.close()
        goal=('Create a small Python calculator in calculator.py with add(a,b), subtract(a,b), multiply(a,b), divide(a,b). Division by zero must raise ZeroDivisionError. Create unittest tests in test_calculator.py and verify them.' if case=='empty' else 'Find and repair the bug in this calculator project. Run the existing tests first to observe the failure, fix the source code rather than weakening tests, then verify again.')
        if case == 'satisfied':
            goal = 'Ensure calculator.add adds numbers and calculator.divide divides numbers and raises ZeroDivisionError for zero. Inspect and test existing behavior. If already correct, make no code changes and add no dependencies or files.'
        goal+=' Use only Python standard library. Run tests using exactly python -m unittest discover. No shell commands, dependency installs, or other commands are approved for this evaluation.'
        config=preference_profile(detect(root),power)
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
        tests_preserved = original_tests is None or (root/'test_calculator.py').read_bytes() == original_tests
        minimal_noop = case != 'satisfied' or (original_source == (root/'calculator.py').read_bytes() and not agent.tools.diff())
        reviews = sum(e['kind']=='simplicity' and e['data'].get('phase')=='review' for e in events)
        result=dict(suite_version='simplicity-1',minimal_noop=minimal_noop,simplicity_reviews=reviews,tests_preserved=tests_preserved,model=model,model_digest=model_digest,code_digest=code_digest,case=case,profile=power,config=config,state=state,independent_pass=independent,observed_failure=failed_observation,seconds=round(time.monotonic()-start,2))
        results.append(result)
        (base/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
        print('RESULT',json.dumps(result),flush=True)
    return 0 if all(r['state']=='COMPLETED' and r['independent_pass'] and r['tests_preserved'] and r['minimal_noop'] and r['simplicity_reviews'] for r in results) and results[1]['observed_failure'] else 1


if __name__=='__main__':
    raise SystemExit(main())
