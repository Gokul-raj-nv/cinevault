from app.models.genre import Genre
from app.models.actor import Actor
from app.models.user import User
from app.models.movie import Movie
from app.models.movie_actor import movie_actors
from app.models.rating import Rating
from app.models.watchlist import Watchlist
from app.models.watch_history import WatchHistory

__all__ = [
    "Genre",
    "Actor",
    "User",
    "Movie",
    "movie_actors",
    "Rating",
    "Watchlist",
    "WatchHistory",
]
