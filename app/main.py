from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import (
    actors,
    analytics,
    auth,
    genres,
    history,
    movies,
    ratings,
    recommendations,
    search,
    watchlist,
)
from app.core.logging import configure_logging
from app.middleware.logging_middleware import RequestLoggingMiddleware

configure_logging()

app = FastAPI(
    title="CineVault",
    description="AI-powered streaming platform backend",
    version="1.0.0",
)

app.add_middleware(RequestLoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(genres.router)
app.include_router(actors.router)
app.include_router(ratings.router)
app.include_router(watchlist.router)
app.include_router(history.router)
app.include_router(search.router)
app.include_router(recommendations.router)
app.include_router(analytics.router)


@app.get("/")
def root():
    return {"message": "CineVault API is running 🎬"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
