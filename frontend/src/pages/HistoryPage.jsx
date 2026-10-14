import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getHistory } from '../api/client';
import MovieCard from '../components/MovieCard';

const s = {
  page: { padding: '2rem' },
  title: { fontSize: '2rem', fontWeight: 800, color: '#fff', marginBottom: '0.3rem' },
  sub: { color: '#888', marginBottom: '2rem' },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: '1.2rem' },
  empty: { textAlign: 'center', padding: '4rem', color: '#666' },
  timestamp: { color: '#666', fontSize: '0.75rem', marginTop: '0.4rem', textAlign: 'center' },
  progress: {
    background: '#2a2a4a', borderRadius: '4px', height: '4px',
    marginTop: '0.5rem', overflow: 'hidden',
  },
  progressBar: { background: '#e50914', height: '100%', transition: 'width 0.3s' },
};

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('en-IN', {
    day: 'numeric', month: 'short', year: 'numeric',
  });
}

export default function HistoryPage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    getHistory()
      .then((r) => setItems(r.data))
      .catch(() => navigate('/login'))
      .finally(() => setLoading(false));
  }, [navigate]);

  if (loading) return <div style={{ textAlign: 'center', padding: '4rem', color: '#888' }}>Loading...</div>;

  return (
    <div style={s.page}>
      <div style={s.title}>🕐 Watch History</div>
      <div style={s.sub}>{items.length} {items.length === 1 ? 'movie' : 'movies'} watched</div>
      {items.length === 0 ? (
        <div style={s.empty}>
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📺</div>
          <p>No watch history yet. Start watching some movies!</p>
        </div>
      ) : (
        <div style={s.grid}>
          {items.map((item) => {
            const runtime = item.movie?.runtime_minutes;
            const position = item.last_position_seconds;
            const pct = runtime ? Math.min(100, Math.round((position / (runtime * 60)) * 100)) : 0;
            return (
              <div key={item.id}>
                <MovieCard movie={item.movie} />
                {runtime > 0 && (
                  <div style={s.progress}>
                    <div style={{ ...s.progressBar, width: `${pct}%` }} />
                  </div>
                )}
                <div style={s.timestamp}>
                  {pct > 0 ? `${pct}% watched · ` : ''}{formatDate(item.watched_at)}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
