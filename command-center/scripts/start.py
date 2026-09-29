"""Cross-platform launcher for the prebuilt local application."""
from pathlib import Path
import os, sys, subprocess, venv, webbrowser, threading, urllib.request, time
ROOT=Path(__file__).resolve().parents[1]
def main():
    if sys.version_info<(3,10):raise SystemExit('Install Python 3.10 or newer, then run again.')
    env=ROOT/'.venv'
    python=env/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
    if not python.exists():
        print('Creating local Python environment…',flush=True);venv.create(env,with_pip=True)
    check=subprocess.run([str(python),'-c','import fastapi,uvicorn,pydantic'],capture_output=True)
    if check.returncode:
        print('First-run setup: installing Python dependencies (internet required once).',flush=True)
        subprocess.run([str(python),'-m','pip','install','-r',str(ROOT/'backend/requirements.txt')],check=True)
    if not (ROOT/'frontend/dist/index.html').exists():
        raise SystemExit('Prebuilt frontend missing. Run: cd frontend && npm ci && npm run build')
    url='http://127.0.0.1:8000'
    try:
        with urllib.request.urlopen(url+'/api/health',timeout=1) as r:
            if r.status==200:
                print('A service already uses port 8000. Stop it before starting a second instance.')
                return
    except Exception:pass
    def open_ui():
        for _ in range(40):
            try:
                with urllib.request.urlopen(url+'/api/health',timeout=1) as r:
                    if r.status==200:webbrowser.open(url);return
            except Exception:time.sleep(.5)
    threading.Thread(target=open_ui,daemon=True).start()
    print('
JEEVANRAKSHAK — local command center
'+url+'
Ctrl+C to shut down.
',flush=True)
    try:subprocess.run([str(python),'-m','uvicorn','app.main:app','--host','127.0.0.1','--port','8000'],cwd=ROOT/'backend')
    except KeyboardInterrupt:pass
if __name__=='__main__':main()
