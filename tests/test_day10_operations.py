from pathlib import Path
import json
import sqlite3
import pytest
from exercises.day10_db import copy_database, inspect_database
from exercises.day10_observe import lifecycle_lines
from exercises import day10_verify_cleanup as cleanup


@pytest.fixture
def live(tmp_path):
    p=tmp_path/'original.db'
    c=sqlite3.connect(p)
    c.execute('PRAGMA journal_mode=WAL')
    c.execute('PRAGMA wal_autocheckpoint=0')
    c.execute('CREATE TABLE tasks(id INTEGER PRIMARY KEY, title TEXT NOT NULL)')
    c.execute("INSERT INTO tasks(title) VALUES('A')");c.commit()
    yield p,c
    c.close()


def test_checkpoint_reads_committed_wal_and_restore_preserves_original(live,tmp_path):
    p,c=live
    assert Path(str(p)+'-wal').stat().st_size>0
    checkpoint=tmp_path/'checkpoint.db';restored=tmp_path/'restored.db'
    r=copy_database(p,checkpoint)
    c.execute("INSERT INTO tasks(title) VALUES('B')");c.commit()
    copy_database(checkpoint,restored,'restore')
    assert inspect_database(p)['task_ids']==[1,2]
    assert inspect_database(restored)['task_ids']==[1]
    assert r['integrity']=='ok' and len(r['sha256'])==64
    assert json.loads(Path(str(checkpoint)+'.record.json').read_text())['task_ids']==[1]


def test_existing_target_is_never_overwritten(live,tmp_path):
    p,_=live; target=tmp_path/'keep.db'; target.write_bytes(b'KEEP')
    with pytest.raises(ValueError):copy_database(p,target)
    assert target.read_bytes()==b'KEEP'


def test_same_source_refused(live):
    p,_=live
    with pytest.raises(ValueError):copy_database(p,p)
    assert inspect_database(p)['task_ids']==[1]


def test_missing_source_does_not_create_database(tmp_path):
    source=tmp_path/'missing.db'
    with pytest.raises(FileNotFoundError):copy_database(source,tmp_path/'copy.db')
    assert not source.exists()


def test_existing_sidecar_refused(live,tmp_path):
    p,_=live;target=tmp_path/'new.db';sidecar=Path(str(target)+'-wal');sidecar.write_bytes(b'KEEP')
    with pytest.raises(ValueError):copy_database(p,target)
    assert sidecar.read_bytes()==b'KEEP' and not target.exists()


def test_symlink_target_refused(live,tmp_path):
    p,_=live;target=tmp_path/'link.db'
    try:target.symlink_to(p)
    except (OSError,NotImplementedError):pytest.skip('Symlinks unavailable on this platform')
    with pytest.raises(ValueError):copy_database(p,target)
    assert inspect_database(p)['task_ids']==[1]


def test_invalid_sqlite_source_leaves_no_target(tmp_path):
    p=tmp_path/'bad.db';p.write_bytes(b'not sqlite');t=tmp_path/'new.db'
    with pytest.raises(sqlite3.Error):copy_database(p,t)
    assert not t.exists()


def test_log_allowlist_excludes_secret_like_and_arbitrary_lines():
    raw='2026-11-20T10:00:00Z INFO: Application startup complete.\n2026-11-20T10:01:00Z INFO: password=fictional-secret\n2026-11-20T10:02:00Z INFO: Application shutdown complete. EXTRA'
    assert lifecycle_lines(raw)==[{'docker_timestamp':'2026-11-20T10:00:00Z','message':'Application startup complete.'}]


def test_cleanup_access_denied_is_unknown(monkeypatch):
    def denied(*args):raise cleanup.QueryError('AccessDeniedException')
    monkeypatch.setattr(cleanup,'aws',denied)
    assert cleanup.check_resource('eu-north-1',{'type':'volume','id':'vol-00000000000000001'})[0]=='Unknown'


def test_cleanup_not_found_is_removed(monkeypatch):
    def missing(*args):raise cleanup.QueryError('InvalidVolume.NotFound')
    monkeypatch.setattr(cleanup,'aws',missing)
    assert cleanup.check_resource('eu-north-1',{'type':'volume','id':'vol-00000000000000001'})[0]=='Removed'


def test_cleanup_stopped_is_not_removed(monkeypatch):
    monkeypatch.setattr(cleanup,'aws',lambda *args:{'Reservations':[{'Instances':[{'State':{'Name':'stopped'}}]}]})
    assert cleanup.check_resource('eu-north-1',{'type':'instance','id':'i-00000000000000001'})[0]=='Remaining'


def test_cleanup_wrong_account_stops_before_resource_queries(monkeypatch):
    calls=[]
    def wrong(*args):calls.append(args);return {'Account':'222222222222'}
    monkeypatch.setattr(cleanup,'aws',wrong)
    with pytest.raises(ValueError):cleanup.verify({'account':'111111111111','region':'eu-north-1','resources':[{'type':'volume','id':'vol-00000000000000001','owner':'test'}]})
    assert len(calls)==1


def test_cleanup_prefix_sibling_does_not_count_as_exact_log_group(monkeypatch):
    monkeypatch.setattr(cleanup,'aws',lambda *args:{'logGroups':[{'logGroupName':'/taskflow/team/day10-other'}]})
    assert cleanup.check_resource('eu-north-1',{'type':'log_group','id':'/taskflow/team/day10'})[0]=='Removed'
