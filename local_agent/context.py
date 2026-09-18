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
