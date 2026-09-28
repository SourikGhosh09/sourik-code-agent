"""Start portable Ollama, or check local setup without starting a server."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
import time
import urllib.request

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from local_agent.models import LocalModel, NoRedirect


def check_setup(root):
    """Report the default Ollama setup; never download, start inference or save settings."""
    ready = sys.version_info >= (3, 12)
    print(('OK' if ready else 'MISSING') + ': Python 3.12 or newer (running ' + sys.version.split()[0] + ').')
    try:
        import tkinter
        window = tkinter.Tk()
        try:
            window.withdraw()
            window.update_idletasks()
        finally:
            window.destroy()
        print('OK: Tk desktop window can be created. Manual accessibility checks are separate.')
    except Exception as exc:
        ready = False
        print('MISSING: Tk cannot open a desktop window. Install Python with Tk and run python -m tkinter in a desktop session. ' + str(exc))
    portable = root / '.runtime' / 'ollama' / 'ollama.exe'
    print('Portable runtime: ' + ('present' if portable.is_file() else 'absent (optional with a separately running server)') + '.')
    try:
        models = LocalModel('').installed_models()
        names = [item['name'] for item in models if isinstance(item, dict) and isinstance(item.get('name'), str) and item['name'].strip()]
        if not names:
            ready = False
            print('MISSING: No installed Ollama models. Install a coding model separately, then rerun this check.')
        else:
            print('OK: Ollama at http://127.0.0.1:11434; installed models: ' + ', '.join(names))
    except (OSError, ValueError, TypeError, AttributeError, KeyError) as exc:
        ready = False
        print('UNAVAILABLE: Cannot discover local Ollama models. Start Ollama, then rerun this check. ' + str(exc))
    print('This check uses the default Ollama endpoint; custom UI endpoints/backends are not checked.')
    print('Setup check passed; run python -m local_agent.' if ready else 'Setup needs attention. See docs/operations/DEPLOYMENT.md.')
    return 0 if ready else 1


def main(argv=None, root=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='check Python, Tk and the default Ollama server/models without starting a server or inference')
    args = parser.parse_args(argv)
    root = Path(root) if root is not None else Path(__file__).resolve().parents[1]
    if args.check:
        return check_setup(root)
    runtime=root/'.runtime'
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
    try:
        with opener.open('http://127.0.0.1:11434/api/tags',timeout=2) as response:
            print('Local model server is already running.')
    except OSError:
        exe=runtime/'ollama'/'ollama.exe'
        if not exe.exists():
            raise SystemExit('No running Ollama server or portable runtime was found. Start your separately installed Ollama server, then try again. Run python scripts/start_local_runtime.py --check for setup details. See docs/operations/DEPLOYMENT.md.')
        env=os.environ.copy()
        home=runtime/'home'
        home.mkdir(exist_ok=True)
        env.update(OLLAMA_MODELS=str(runtime/'models'),OLLAMA_HOST='127.0.0.1:11434',OLLAMA_NUM_PARALLEL='1',OLLAMA_MAX_LOADED_MODELS='1',USERPROFILE=str(home))
        with (runtime/'server.log').open('ab') as log:
            proc=subprocess.Popen([str(exe),'serve'],env=env,stdout=log,stderr=log,creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS)
        (runtime/'server.pid').write_text(str(proc.pid))
        print('Starting local model server...',flush=True)
        deadline=time.monotonic()+45
        while time.monotonic()<deadline:
            try:
                with opener.open('http://127.0.0.1:11434/api/tags',timeout=2) as response:
                    if response.status==200:
                        print('Local model server is ready:',proc.pid)
                        break
            except OSError:
                time.sleep(.5)
        else:
            raise SystemExit('The local model server did not become ready. See .runtime/server.log for details.')


if __name__ == '__main__':
    raise SystemExit(main())
