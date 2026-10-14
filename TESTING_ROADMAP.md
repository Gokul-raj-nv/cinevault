# 🎬 CineVault — Testing Roadmap

> Complete guide to verify every feature of CineVault from scratch.

---

## Prerequisites — Start Everything First

Open **two terminals** in VS Code (`Ctrl + Shift + \`` to open each one):

**Terminal 1 — Start Docker containers:**
```powershell
docker-compose -f docker/docker-compose.yml up -d
docker ps   # verify both containers show "healthy"
```

**Terminal 2 — Start the backend:**
```powershell
venv\Scripts\activate
uvicorn app.main:app --reload
```

**Terminal 3 — Start the frontend:**
```powershell
cd frontend
npm install    # only needed first time
npm start
```

Wait for:
- `http://localhost:8000` → `{"message": "CineVault API is running 🎬"}`
- `http://localhost:3000` → React app opens in browser

---

## Part 1 — Automated Tests (Backend)

```powershell
# In a terminal (venv must be active, Docker must be running)
pytest tests/ -v
```

### Expected output

```
tests/unit/test_security.py::test_password_hash_round_trip    PASSED
tests/unit/test_security.py::test_access_token_round_trip     PASSED
tests/integration/test_auth_api.py::test_register_login...    PASSED
tests/integration/test_movies_api.py::test_admin_can_create.. PASSED
tests/integration/test_watchlist_api.py::test_watchlist...    PASSED
tests/integration/test_ratings_api.py::test_rate_movie        PASSED
tests/integration/test_ratings_api.py::test_rating_upserts    PASSED
tests/integration/test_ratings_api.py::test_movie_stats       PASSED
tests/integration/test_ratings_api.py::test_rating_auth       PASSED
tests/integration/test_history_api.py::test_log_watch_event   PASSED
tests/integration/test_history_api.py::test_get_watch_history PASSED
tests/integration/test_history_api.py::test_upserts           PASSED
tests/integration/test_history_api.py::test_auth_required     PASSED

========== 13 passed in X.XXs ==========
```

---

## Part 2 — Manual API Testing (Swagger UI)

Open: **http://localhost:8000/docs**

### Step 1 — Register a user

`POST /auth/register`
```json
{ "name": "Bruce Wayne", "email": "bruce@gotham.com", "password": "batman123" }
```
✅ Expected: `201` with your user object

---

### Step 2 — Make yourself admin

In a new terminal:
```powershell
docker exec cinevault_db psql -U cinevault -d cinevault_db -c "UPDATE users SET is_admin = true WHERE email = 'bruce@gotham.com';"
```
✅ Expected: `UPDATE 1`

---

### Step 3 — Login and authorize

`POST /auth/login`
```json
{ "email": "bruce@gotham.com", "password": "batman123" }
```
Copy the `access_token`. Click 🔒 **Authorize** → paste the token → **Authorize**.

---

### Step 4 — Create genres

`POST /genres` (repeat for each):
```json
{ "name": "Action" }
{ "name": "Drama" }
{ "name": "Sci-Fi" }
{ "name": "Comedy" }
```
✅ Expected: `201` each time

---

### Step 5 — Create actors

`POST /actors`:
```json
{ "name": "Christian Bale", "bio": "Welsh actor" }
{ "name": "Heath Ledger", "bio": "Australian actor" }
{ "name": "Cillian Murphy", "bio": "Irish actor" }
```

---

### Step 6 — Create movies

`POST /movies`:
```json
{
  "title": "The Dark Knight",
  "description": "Batman faces the Joker in Gotham City in an epic battle.",
  "release_year": 2008,
  "runtime_minutes": 152,
  "language": "English",
  "genre_id": 1,
  "actor_ids": [1, 2]
}
```

Create 4–5 more movies for a realistic catalog.

---

### Step 7 — Test core features

| Test | Endpoint | Expected |
|------|----------|----------|
| Browse movies | `GET /movies` | Paginated list |
| Filter by genre | `GET /movies?genre_id=1` | Only Action movies |
| Search title | `GET /movies?search=dark` | Matching movies |
| Movie detail | `GET /movies/1` | Full movie with actors |
| Trending | `GET /movies/trending` | Most rated movies |
| Rate a movie | `POST /ratings` `{"movie_id":1,"rating":5}` | `201` with rating |
| Duplicate rating | Same request again | Rating **updated**, not duplicated |
| Movie stats | `GET /ratings/movie/1` | `{"average_rating":5.0,"total_ratings":1}` |
| Add to watchlist | `POST /watchlist/1` | `{"message":"Added to watchlist"}` |
| Add again | Same request | `400 Already in watchlist` |
| View watchlist | `GET /watchlist` | Your movie appears |
| Check status | `GET /watchlist/status/1` | `{"in_watchlist":true}` |
| Log watch | `POST /history` `{"movie_id":1,"last_position_seconds":3600}` | `201` |
| Watch history | `GET /history` | Shows movie with position |
| Recommendations | `GET /recommendations` | Personalised list |
| Remove watchlist | `DELETE /watchlist/1` | `{"message":"Removed"}` |

---

### Step 8 — Test auth protection

| Test | How | Expected |
|------|-----|----------|
| No token on protected route | Click 🔓 Logout in Swagger, then `POST /ratings` | `403 Forbidden` |
| Non-admin on admin route | Login as regular user, `POST /genres` | `403 Forbidden` |

---

## Part 3 — Frontend Testing

Open: **http://localhost:3000**

### Checklist

- [ ] **Home page** loads with feature cards
- [ ] **Browse movies** shows all movies in a grid
- [ ] **Search** — type in search box, results filter with debounce
- [ ] **Genre filter** — dropdown filters by genre
- [ ] **Movie detail** — click a card, opens detail page
- [ ] **Register** — create a new account via `/register`
- [ ] **Login** — sign in, see name in Navbar
- [ ] **Rate** a movie with star rating on detail page
- [ ] **Add to watchlist** — button turns green
- [ ] **Watchlist page** — `/watchlist` shows saved movies, remove works
- [ ] **History page** — `/history` shows watched movies with progress bar
- [ ] **Admin panel** — `/admin` (admin only) — create genre, actor, movie
- [ ] **Logout** — click Logout, protected pages redirect to login

---

## Part 4 — Analytics (Admin only)

`GET /analytics/summary` via Swagger with admin token.

✅ Expected: Top genres, most active users, most watched movies.

---

## Part 5 — GitHub Push

```powershell
# In project root (cinevault/)
git add .
git commit -m "feat: complete CineVault backend + React frontend"

# Create repo on github.com first, then:
git remote add origin https://github.com/YOUR_USERNAME/cinevault.git
git branch -M main
git push -u origin main
```

> ⚠️ Make sure `.env` is in `.gitignore` — it contains your secret key!

---

## Quick Reference — Startup Commands

Every time you open your laptop:

```powershell
# Step 1 — Start Docker (or it auto-starts if Docker Desktop is set to)
docker-compose -f docker/docker-compose.yml up -d

# Step 2 — Start backend (Terminal 1)
cd C:\Users\91963\Cinevault
venv\Scripts\activate
uvicorn app.main:app --reload

# Step 3 — Start frontend (Terminal 2)
cd C:\Users\91963\Cinevault\frontend
npm start
```

| Service | URL |
|---------|-----|
| React frontend | http://localhost:3000 |
| FastAPI backend | http://localhost:8000 |
| Swagger API docs | http://localhost:8000/docs |
| pgAdmin (optional) | connect to localhost:5432 |

---

## Interview Talking Points

> "CineVault is a production-grade backend for a streaming platform. I built it with FastAPI using a layered architecture — routes, services, and repositories — keeping concerns cleanly separated. The database is PostgreSQL with SQLAlchemy ORM and Alembic for migrations. Redis caches trending movies and genres for sub-millisecond reads. Semantic search converts movie descriptions into vector embeddings using Sentence Transformers stored in pgvector, enabling natural-language queries like 'dark detective thriller'. The project is containerised with Docker Compose, tested with Pytest, and has a CI pipeline on GitHub Actions."
