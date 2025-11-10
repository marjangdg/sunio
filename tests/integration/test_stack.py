import os
import time
import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")

def wait_for_health(timeout=60):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(f"{BASE_URL}/healthz", timeout=2)
            if r.status_code == 200:
                return
        except Exception:
            pass
        time.sleep(2)
    raise RuntimeError("Service did not become healthy in time")

def test_stack_ok():
    wait_for_health()
    r = requests.get(f"{BASE_URL}/sum", params={"left": 5, "right": 3}, timeout=5)
    assert r.status_code == 200
    assert r.json() == {"sum": 8}

def test_stack_negative():
    wait_for_health()
    r = requests.get(f"{BASE_URL}/sum", params={"left": -2, "right": -4}, timeout=5)
    assert r.status_code == 200
    assert r.json() == {"sum": -6}
