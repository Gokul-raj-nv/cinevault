import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
});

// Attach JWT token to every request automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth
export const register = (data) => api.post('/auth/register', data);
export const login = (data) => api.post('/auth/login', data);
export const getMe = () => api.get('/auth/me');

// Movies
export const getMovies = (params) => api.get('/movies', { params });
export const getMovie = (id) => api.get(`/movies/${id}`);
export const getTrending = () => api.get('/movies/trending');
export const createMovie = (data) => api.post('/movies', data);
export const updateMovie = (id, data) => api.put(`/movies/${id}`, data);
export const deleteMovie = (id) => api.delete(`/movies/${id}`);

// Genres
export const getGenres = () => api.get('/genres');
export const createGenre = (data) => api.post('/genres', data);

// Actors
export const getActors = () => api.get('/actors');
export const createActor = (data) => api.post('/actors', data);

// Ratings
export const rateMovie = (data) => api.post('/ratings', data);
export const getMovieRating = (movieId) => api.get(`/ratings/movie/${movieId}`);
export const getMyRating = (movieId) => api.get(`/ratings/my/${movieId}`);

// Watchlist
export const getWatchlist = () => api.get('/watchlist');
export const addToWatchlist = (movieId) => api.post(`/watchlist/${movieId}`);
export const removeFromWatchlist = (movieId) => api.delete(`/watchlist/${movieId}`);
export const checkWatchlistStatus = (movieId) => api.get(`/watchlist/status/${movieId}`);

// History
export const getHistory = () => api.get('/history');
export const logWatch = (movieId, data) => api.post(`/history/${movieId}`, data);

// Recommendations
export const getRecommendations = () => api.get('/recommendations');

// Analytics
export const getAnalytics = () => api.get('/analytics/summary');

export default api;
