import importlib
import os
import pytest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if SRC.is_dir():
    sys.path.insert(0, str(SRC))


PKG = os.getenv("PKG", "tirreno_tracker")
pkg = importlib.import_module(PKG)

Tracker = getattr(pkg, "Tracker")
Event = getattr(pkg, "Event")
Payload = getattr(pkg, "Payload")


@pytest.fixture
def TrackerCls(): return Tracker


@pytest.fixture
def EventCls(): return Event


@pytest.fixture
def PayloadCls(): return Payload


@pytest.fixture
def fake_post(monkeypatch):
    calls = {}

    class Resp:
        def __init__(self, status_code=200): self.status_code = status_code

    def _fake(url=None, data=None, headers=None, timeout=None, **kw):
        calls.update(url=url, data=data, headers=headers, timeout=timeout, kw=kw)
        return Resp(200)

    tracking_mod_name = f"{PKG}.tracking"
    import importlib as _il
    _il.import_module(tracking_mod_name)
    monkeypatch.setattr(f"{tracking_mod_name}.requests", "post", _fake)
    return calls
