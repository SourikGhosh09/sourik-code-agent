"""Bounded, task-ranked repository intelligence backed by a disposable index."""
import ast
import hashlib
import json
from pathlib import Path
import re
from .tools import redact


def tokens(text):
    return set(re.findall(r'[a-z][a-z0-9_]{2,}', text.lower()))


def describe(name, content):
    row = {'path': name, 'language': Path(name).suffix, 'symbols': [], 'imports': []}
    try:
        if name.endswith('.py'):
            tree = ast.parse(content)
            row['symbols'] = [n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))][:40]
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    row['imports'].extend(a.name for a in node.names)
                elif isinstance(node, ast.ImportFrom):
                    row['imports'].append(node.module or '')
        elif Path(name).suffix in ('.js', '.jsx', '.ts', '.tsx'):
            row['symbols'] = re.findall(r'\b(?:function|class|interface|type|const)\s+(\w+)', content)[:40]
            row['imports'] = re.findall(r'''(?:from\s*|require\(\s*)['"]([^'"]+)''', content)[:20]
        if Path(name).name == 'package.json':
            data = json.loads(content)
            row['dependencies'] = list(data.get('dependencies', {}))[:40]
            row['scripts'] = list(data.get('scripts', {}))[:20]
        elif Path(name).name == 'pyproject.toml':
            import tomllib
            data = tomllib.loads(content)
            row['dependencies'] = data.get('project', {}).get('dependencies', [])[:40]
        row['imports'] = row['imports'][:20]
    except (SyntaxError, ValueError, TypeError, AttributeError):
        row['parse'] = 'Read this file to inspect its syntax or format.'
    return row


def repository_map(tools, limit=100, goal='', store=None):
    old = store.index_rows() if store else {}
    rows = {}
    for name in tools.files():
        try:
            path = tools.path(name)
            if path.stat().st_size > 100_000:
                row, digest = {'path':name, 'language':path.suffix, 'large':True}, ''
            else:
                raw = path.read_bytes()
                digest = hashlib.sha256(raw).hexdigest()
                row = old[name][1] if name in old and old[name][0] == digest else describe(name, redact(raw.decode('utf-8')))
            rows[name] = (digest, row)
        except (OSError, ValueError, UnicodeError):
            continue
    if store:
        store.save_index(rows)
    query = tokens(goal)
    def score(row):
        name = row['path']
        words = tokens(name + ' ' + ' '.join(row.get('symbols', [])))
        return 5*len(query & words) + (2 if Path(name).name in ('pyproject.toml','package.json','README.md') else 0)
    ranked = sorted((row for _, row in rows.values()), key=lambda r: (-score(r), r['path']))
    imports = {part for row in ranked[:8] if score(row)>0 for imp in row.get('imports',[]) for part in re.split(r'[./]',imp)}
    ranked.sort(key=lambda r: (-(score(r)+(2 if Path(r['path']).stem in imports else 0)),r['path']))
    result, used = [], 0
    for row in ranked[:limit]:
        length = len(json.dumps(row))
        if used+length > 12000:
            break
        result.append(row)
        used += length
    return result


def evidence_for(tools):
    evidence = {}
    for name in tools.files():
        try:
            p = tools.path(name)
            if p.stat().st_size <= 200_000:
                evidence[name] = hashlib.sha256(p.read_bytes()).hexdigest()
        except (OSError, ValueError):
            continue
    return evidence


def relevant_memory(store, tools, goal, budget=2000):
    current = evidence_for(tools)
    result = []
    query = tokens(goal)
    records = sorted(store.memory_records(), key=lambda r: -len(tokens(r['value']) & query))
    for record in records:
        if record['kind'] == 'verified_task' and (not record['evidence'] or record['evidence'] != current):
            continue
        text = record['value'][:budget]
        if not text:
            break
        result.append({'kind':record['kind'], 'value':text, 'source_task':record['task']})
        budget -= len(text)
        if len(result) >= 5:
            break
    return result


def repair_context(tools, error, budget=7000):
    files = tools.files()
    files.sort(key=lambda name: (Path(name).name not in error, name))
    result = []
    for name in files:
        if Path(name).suffix not in ('.py','.js','.ts','.tsx','.jsx','.json','.toml','.html','.css'):
            continue
        try:
            content = tools.execute({'tool':'read','path':name})['content']
        except (OSError, ValueError):
            continue
        excerpt = content[:min(budget,3000)]
        result.append({'path':name,'content':excerpt})
        budget -= len(excerpt)
        if budget <= 0 or len(result) >= 5:
            break
    return result
