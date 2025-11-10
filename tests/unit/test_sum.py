def test_ok(client):
    resp = client.get("/sum?left=5&right=3")
    assert resp.status_code == 200
    assert resp.get_json() == {"sum": 8}

def test_negative(client):
    resp = client.get("/sum?left=-2&right=-4")
    assert resp.status_code == 200
    assert resp.get_json() == {"sum": -6}

def test_missing_params(client):
    resp = client.get("/sum?left=5")
    assert resp.status_code == 400
    assert "error" in resp.get_json()

def test_invalid_params(client):
    resp = client.get("/sum?left=a&right=2")
    assert resp.status_code == 400
    assert "error" in resp.get_json()

def test_healthz(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("status") == "ok"
