import sqlite3, json, os
from pathlib import Path
from .models import now
class Database:
    def __init__(self,path=None):
        path=path or os.getenv('JR_DB',str(Path(__file__).resolve().parents[1]/'data'/'missions.sqlite3'))
        Path(path).parent.mkdir(parents=True,exist_ok=True)
        self.conn=sqlite3.connect(path,check_same_thread=False)
        self.conn.row_factory=sqlite3.Row
        self.conn.executescript('''PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS missions(id TEXT PRIMARY KEY,started TEXT,ended TEXT,mode TEXT);
        CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,mission TEXT,type TEXT,timestamp TEXT,source TEXT,mode TEXT,payload TEXT);
        CREATE INDEX IF NOT EXISTS idx_events_mission ON events(mission,id);
        CREATE INDEX IF NOT EXISTS idx_events_type ON events(type,id);
        CREATE TABLE IF NOT EXISTS snapshots(mission TEXT PRIMARY KEY,payload TEXT);''')
    def start(self,id,mode):
        self.conn.execute('INSERT INTO missions VALUES(?,?,NULL,?)',(id,now(),mode)); self.conn.commit()
    def end(self,id):
        self.conn.execute('UPDATE missions SET ended=? WHERE id=?',(now(),id)); self.conn.commit()
    def add(self,mission,e):
        self.conn.execute('INSERT INTO events(mission,type,timestamp,source,mode,payload) VALUES(?,?,?,?,?,?)',(mission,e['type'],e['timestamp'],e['source'],e['data_mode'],json.dumps(e['payload']))); self.conn.commit()
    def save(self,mission,state):
        self.conn.execute('INSERT OR REPLACE INTO snapshots VALUES(?,?)',(mission,json.dumps(state))); self.conn.commit()
    def history(self,mission=None,kind=None,limit=500):
        sql='SELECT * FROM events WHERE 1=1'; args=[]
        if mission: sql+=' AND mission=?';args.append(mission)
        if kind: sql+=' AND type=?';args.append(kind)
        sql+=' ORDER BY id DESC LIMIT ?';args.append(limit)
        return [dict(r)|{'payload':json.loads(r['payload'])} for r in self.conn.execute(sql,args)]
    def missions(self): return [dict(r) for r in self.conn.execute('SELECT * FROM missions ORDER BY started DESC')]
    def snapshot(self,id):
        r=self.conn.execute('SELECT payload FROM snapshots WHERE mission=?',(id,)).fetchone()
        return json.loads(r[0]) if r else None
