"""Bounded repository context; evidence is refreshed per task."""
import ast
from pathlib import Path


def repository_map(tools, limit=100):
    result=[]
    for name in tools.files()[:limit]:
        row={'path':name,'language':Path(name).suffix}
        p=tools.path(name)
        if p.suffix=='.py' and p.stat().st_size<100_000:
            try:
                tree=ast.parse(p.read_text(encoding='utf-8'))
                row['symbols']=[n.name for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))][:40]
                row['imports']=[n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)][:20]
            except (SyntaxError,UnicodeError,OSError):
                row['parse']='Read file to inspect syntax or encoding problem.'
        result.append(row)
    return result


def repair_context(tools, error, budget=7000):
    """Refresh evidence after a repeated failure, avoiding stale attempted fixes."""
    files=tools.files()
    files.sort(key=lambda name: (Path(name).name not in error, name))
    result=[]
    for name in files:
        if name == 'PROJECT_LOG.txt' or Path(name).suffix not in ('.py','.js','.ts','.tsx','.jsx','.json','.toml','.html','.css'):
            continue
        try:
            content=tools.execute({'tool':'read','path':name})['content']
        except (OSError,ValueError):
            continue
        excerpt=content[:min(budget,3000)]
        result.append({'path':name,'content':excerpt})
        budget-=len(excerpt)
        if budget<=0 or len(result)>=5:
            break
    return result
