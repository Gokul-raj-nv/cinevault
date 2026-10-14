<div align="center">

# 🎬 CineVault

### A full-stack movie discovery platform with semantic search and personalised recommendations

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=111827)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL%20%2B%20pgvector-16-4169E1?logo=postgresql&logoColor=white)](https://github.com/pgvector/pgvector)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)](https://redis.io/)

</div>

## ✨ Overview

CineVault is a production-minded movie discovery application. It pairs a React experience for browsing, ratings, watchlists, and viewing history with a FastAPI service that supports secure access, catalogue management, analytics, semantic search, and personalised recommendations.

Natural-language queries such as `dark detective movie` are matched by meaning—not just by title—using Sentence Transformers and PostgreSQL's `pgvector` extension.

## 🚀 Highlights

| Area | What CineVault provides |
| --- | --- |
| **Discovery** | Paginated browsing, title/language/genre filters, trending titles, and semantic search |
| **Personal experience** | Star ratings, watchlists, watch-progress history, and genre-weighted recommendations |
| **Admin tools** | Movie, genre, and actor management plus catalogue and audience analytics |
| **Performance** | Redis caching for genres, movie detail, trending titles, and recommendations |
| **Security** | JWT authentication, bcrypt password hashing, and role-based admin permissions |
| **Quality** | Alembic migrations, integration tests, and GitHub Actions CI |

## 🧭 How it works

```text
React client
    │
    ▼
FastAPI routes ──► Services ──► Repositories ──► PostgreSQL + pgvector
    │                 │
    │                 ├── Sentence Transformer embeddings
    │                 └── Redis cache
    │
    └── JWT authentication and role-based access
```

## 🛠️ Technology stack

- **Frontend:** React 18, React Router, Axios
- **API:** FastAPI, Pydantic, Uvicorn
- **Data:** PostgreSQL 16, SQLAlchemy 2, Alembic, pgvector
- **Intelligence:** Sentence Transformers (`all-MiniLM-L6-v2`)
- **Caching:** Redis 7
- **Testing & automation:** Pytest, HTTPX, GitHub Actions
- **Local infrastructure:** Docker Compose

## 📁 Project structure

```text
CineVault/
├── app/
│   ├── api/v1/              # FastAPI route modules
│   ├── core/                # Configuration, security, cache, dependencies
│   ├── models/              # SQLAlchemy database models
│   ├── repositories/        # Database access layer
│   ├── schemas/             # Request and response contracts
│   ├── services/            # Business logic, search, recommendations
│   └── main.py              # Application entry point
├── alembic/                 # Database migrations
├── docker/                  # PostgreSQL/pgvector and Redis services
├── frontend/
│   └── src/                 # React pages, components, API client, auth state
├── scripts/
│   └── create_admin.py      # Creates an initial administrator
├── tests/                   # Unit and integration tests
├── .env.example             # Backend configuration template
└── requirements.txt         # Python dependencies
```

## ⚡ Quick start

### Prerequisites

- Python 3.11 or newer
- Node.js 18 or newer
- Docker Desktop

### 1. Configure and start the backend

Run the following from the project root in PowerShell:

```powershell
Copy-Item .env.example .env
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

docker compose -f docker/docker-compose.yml up -d
alembic upgrade head
python scripts/create_admin.py --name "Your Name" --email "you@example.com"
uvicorn app.main:app --reload
```

The API is now available at:

- API root: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Interactive documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Health check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

> If `python` is not recognised on Windows, reopen PowerShell after installing Python or use `py -3.11` in its place.

### 2. Start the React client

Open another terminal while the API remains running:

```powershell
Set-Location frontend
npm install
npm start
```

Open [http://localhost:3000](http://localhost:3000). The client uses `http://localhost:8000` by default; set `REACT_APP_API_URL` in `frontend/.env` to point it at another API instance.

## 🧠 Semantic search

CineVault embeds movie content with `all-MiniLM-L6-v2` and stores the 384-dimensional vectors in PostgreSQL. This makes meaning-based discovery possible:

```http
GET /search?q=dark+detective+movie
```

The model downloads when semantic search is first used (or when the first movie is created), so internet access is needed once. Existing catalogue entries can be indexed through the admin-only endpoint:

```http
POST /search/reindex
```

Set `SEMANTIC_SEARCH_ENABLED=false` in `.env` if the feature needs to be disabled temporarily.

## 📡 API at a glance

| Domain | Key endpoints |
| --- | --- |
| **Authentication** | `POST /auth/register`, `POST /auth/login`, `GET /auth/me` |
| **Movies** | `GET /movies`, `GET /movies/{id}`, `GET /movies/trending` |
| **Catalogue administration** | `POST /movies`, `PUT/DELETE /movies/{id}`, `GET/POST /genres`, `GET/POST /actors` |
| **Your library** | `POST /ratings`, `GET /ratings/movie/{id}`, `GET /watchlist`, `POST/DELETE /watchlist/{movie_id}`, `GET /history`, `POST /history/{movie_id}` |
| **Discovery** | `GET /search?q=…`, `GET /recommendations` |
| **Analytics** | `GET /analytics/top-genres`, `GET /analytics/active-users`, `GET /analytics/most-watched`, `GET /analytics/average-ratings` |

Protected endpoints accept a bearer token. In Swagger UI, first call `/auth/login`, then select **Authorize** and paste the returned access token.

## 🗄️ Database migrations

Run migrations after the Docker services are healthy:

```powershell
alembic upgrade head
```

The initial migration enables `vector`, creates the application tables, adds the 384-dimensional movie embedding column, and applies safe delete behaviour. For a later schema change:

```powershell
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

## 🧪 Testing

With PostgreSQL and Redis running, execute:

```powershell
.\venv\Scripts\python.exe -m pytest tests -v
```

The CI workflow runs the same test suite against PostgreSQL with pgvector and Redis for every push and pull request.

## 🔐 Configuration and security

Copy `.env.example` to `.env` before running the API. It documents database access, JWT, cache, and semantic-search settings.

For any non-local environment, replace `SECRET_KEY` with a long, unique secret and use secure database credentials. Keep `.env` out of source control.

---

<div align="center">
  Built for discovering the next great watch. 🍿
</div>
