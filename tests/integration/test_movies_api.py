def test_admin_can_create_and_browse_a_movie(client, admin_headers):
    genre = client.post("/genres", json={"name": "Science Fiction"}, headers=admin_headers)
    assert genre.status_code == 201

    actor = client.post(
        "/actors",
        json={"name": "Test Actor", "bio": "A test performer."},
        headers=admin_headers,
    )
    assert actor.status_code == 201

    movie = client.post(
        "/movies",
        json={
            "title": "Arrival Test",
            "description": "A linguist encounters an alien language.",
            "release_year": 2016,
            "genre_id": genre.json()["id"],
            "actor_ids": [actor.json()["id"]],
        },
        headers=admin_headers,
    )
    assert movie.status_code == 201
    assert movie.json()["actors"][0]["name"] == "Test Actor"

    listing = client.get("/movies")
    assert listing.status_code == 200
    assert listing.json()["total"] == 1
    assert listing.json()["results"][0]["title"] == "Arrival Test"
