def test_register_login_and_get_profile(client):
    registration = client.post(
        "/auth/register",
        json={"name": "Ada", "email": "ada@example.com", "password": "strong-password"},
    )
    assert registration.status_code == 201
    assert registration.json()["email"] == "ada@example.com"

    login = client.post(
        "/auth/login",
        json={"email": "ada@example.com", "password": "strong-password"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    profile = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert profile.status_code == 200
    assert profile.json()["name"] == "Ada"
