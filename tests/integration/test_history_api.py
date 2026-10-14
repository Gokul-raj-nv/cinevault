def _create_movie(client, admin_headers, title="History Test Movie"):
    client.post("/genres", json={"name": "Action"}, headers=admin_headers)
    resp = client.post(
        "/movies",
        json={"title": title, "genre_id": 1, "actor_ids": []},
        headers=admin_headers,
    )
    assert resp.status_code == 201
    return resp.json()["id"]


def test_log_watch_event(client, user_headers, admin_headers):
    movie_id = _create_movie(client, admin_headers)
    resp = client.post(
        f"/history/{movie_id}",
        json={"last_position_seconds": 1200},
        headers=user_headers,
    )
    assert resp.status_code == 201


def test_get_watch_history(client, user_headers, admin_headers):
    movie_id = _create_movie(client, admin_headers)
    client.post(
        f"/history/{movie_id}",
        json={"last_position_seconds": 900},
        headers=user_headers,
    )
    resp = client.get("/history", headers=user_headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    assert resp.json()[0]["last_position_seconds"] == 900


def test_watch_history_upserts(client, user_headers, admin_headers):
    """Watching the same movie twice updates the position, not duplicate rows."""
    movie_id = _create_movie(client, admin_headers)
    client.post(f"/history/{movie_id}", json={"last_position_seconds": 500}, headers=user_headers)
    client.post(f"/history/{movie_id}", json={"last_position_seconds": 1500}, headers=user_headers)

    resp = client.get("/history", headers=user_headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    assert resp.json()[0]["last_position_seconds"] == 1500


def test_history_requires_auth(client):
    resp = client.get("/history")
    assert resp.status_code == 401
