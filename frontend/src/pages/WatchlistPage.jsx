import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getWatchlist, removeFromWatchlist } from '../api/client';
import MovieCard from '../components/MovieCard';

const s = {
  page: { padding: '2rem' },
  title: { fontSize: '2rem', fontWeight: 800, color: '#fff', marginBottom: '0.3rem' },
  sub: { color: '#888', marginBottom: '2rem' },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: '1.2rem' },
  empty: { textAlign: 'center', padding: '4rem', color: '#666' },
  removeBtn: {
    width: '100%', background: 'transparent', color: '#e50914',
    border: '1px solid #e50914', padding: '0.4rem', borderRadius: '4px',
    cursor: 'pointer', fontSize: '0.8rem', marginTop: '0.5rem',
  },
  cardWrap: { position: 'relative' },
};

export default function WatchlistPage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    getWatchlist()
      .then((r) => setItems(r.data))
      .catch(() => navigate('/login'))
      .finally(() => setLoading(false));
  }, [navigate]);

  const handleRemove = (movieId) => {
    removeFromWatchlist(movieId)
      .then(() => setItems((prev) => prev.filter((i) => i.movie_id !== movieId)))
      .catch(() => {});
  };

  if (loading) return <div style={{ textAlign: 'center', padding: '4rem', color: '#888' }}>Loading...</div>;

  return (
    <div style={s.page}>
      <div style={s.title}>📌 My Watchlist</div>
      <div style={s.sub}>{items.length} {items.length === 1 ? 'movie' : 'movies'} saved</div>
      {items.length === 0 ? (
        <div style={s.empty}>
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📭</div>
          <p>Your watchlist is empty. Browse movies and add some!</p>
        </div>
      ) : (
        <div style={s.grid}>
          {items.map((item) => (
            <div key={item.id} style={s.cardWrap}>
              <MovieCard movie={item.movie} />
              <button style={s.removeBtn} onClick={() => handleRemove(item.movie_id)}>
                ✕ Remove
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
