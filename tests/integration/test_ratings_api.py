import pytest


def test_rate_movie(client, user_headers, admin_headers):
    # Create genre and movie first
    client.post("/genres", json={"name": "Action"}, headers=admin_headers)
    movie_resp = client.post(
        "/movies",
        json={"title": "Test Movie", "genre_id": 1, "actor_ids": []},
        headers=admin_headers,
    )
    assert movie_resp.status_code == 201
    movie_id = movie_resp.json()["id"]

    # Rate the movie
    resp = client.post(
        "/ratings",
        json={"movie_id": movie_id, "rating": 5},
        headers=user_headers,
    )
    assert resp.status_code == 201
    assert resp.json()["rating"] == 5


def test_rating_updates_not_duplicates(client, user_headers, admin_headers):
    client.post("/genres", json={"name": "Drama"}, headers=admin_headers)
    movie_resp = client.post(
        "/movies",
        json={"title": "Drama Movie", "genre_id": 1, "actor_ids": []},
        headers=admin_headers,
    )
    movie_id = movie_resp.json()["id"]

    # Rate twice — second should update, not create a new row
    client.post("/ratings", json={"movie_id": movie_id, "rating": 3}, headers=user_headers)
    resp = client.post("/ratings", json={"movie_id": movie_id, "rating": 5}, headers=user_headers)
    assert resp.status_code == 201
    assert resp.json()["rating"] == 5

    # Stats should show 1 rating, not 2
    stats = client.get(f"/ratings/movie/{movie_id}")
    assert stats.json()["total_ratings"] == 1
    assert stats.json()["average_rating"] == 5.0


def test_get_movie_rating_stats(client, user_headers, admin_headers):
    client.post("/genres", json={"name": "Sci-Fi"}, headers=admin_headers)
    movie_resp = client.post(
        "/movies",
        json={"title": "Sci-Fi Movie", "genre_id": 1, "actor_ids": []},
        headers=admin_headers,
    )
    movie_id = movie_resp.json()["id"]

    resp = client.get(f"/ratings/movie/{movie_id}")
    assert resp.status_code == 200
    assert resp.json()["total_ratings"] == 0
    assert resp.json()["average_rating"] is None


def test_rating_requires_auth(client, admin_headers):
    client.post("/genres", json={"name": "Comedy"}, headers=admin_headers)
    client.post(
        "/movies",
        json={"title": "Comedy Movie", "genre_id": 1, "actor_ids": []},
        headers=admin_headers,
    )
    resp = client.post("/ratings", json={"movie_id": 1, "rating": 4})
    assert resp.status_code == 401
