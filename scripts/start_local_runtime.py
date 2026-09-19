"""Start the workspace-local Ollama service without changing system settings."""
import os
from pathlib import Path
import subprocess
import time
import urllib.request

root=Path(__file__).resolve().parents[1]
runtime=root/'.runtime'
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
try:
    with opener.open('http://127.0.0.1:11434/api/tags',timeout=2) as response:
        print('Local model server is already running.')
except OSError:
    exe=runtime/'ollama'/'ollama.exe'
    if not exe.exists():
        raise SystemExit('Portable Ollama is not installed in .runtime/ollama.')
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
