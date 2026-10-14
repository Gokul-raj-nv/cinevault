def _create_movie(client, admin_headers):
    genre = client.post("/genres", json={"name": "Drama"}, headers=admin_headers)
    movie = client.post(
        "/movies",
        json={"title": "Watchlist Test", "genre_id": genre.json()["id"]},
        headers=admin_headers,
    )
    return movie.json()["id"]


def test_watchlist_rating_and_history(client, admin_headers, user_headers):
    movie_id = _create_movie(client, admin_headers)

    assert client.post(f"/watchlist/{movie_id}", headers=user_headers).status_code == 201
    watchlist = client.get("/watchlist", headers=user_headers)
    assert watchlist.status_code == 200
    assert watchlist.json()[0]["movie_id"] == movie_id

    rating = client.post("/ratings", json={"movie_id": movie_id, "rating": 5}, headers=user_headers)
    assert rating.status_code == 201
    assert rating.json()["rating"] == 5

    history = client.post(
        f"/history/{movie_id}",
        json={"last_position_seconds": 120},
        headers=user_headers,
    )
    assert history.status_code == 201
    assert client.get("/history", headers=user_headers).json()[0]["last_position_seconds"] == 120
