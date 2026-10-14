import React from 'react';
import { useNavigate } from 'react-router-dom';

const styles = {
  card: {
    background: '#1a1a2e',
    borderRadius: '10px',
    overflow: 'hidden',
    cursor: 'pointer',
    transition: 'transform 0.2s, box-shadow 0.2s',
    border: '1px solid #1e1e3a',
  },
  poster: {
    width: '100%',
    height: '220px',
    objectFit: 'cover',
    background: '#2a2a4a',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '4rem',
  },
  body: { padding: '0.85rem' },
  title: {
    fontWeight: 700,
    fontSize: '0.95rem',
    color: '#fff',
    marginBottom: '0.3rem',
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },
  meta: { display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginTop: '0.4rem' },
  badge: {
    background: '#2a2a4a',
    color: '#aaa',
    padding: '2px 8px',
    borderRadius: '12px',
    fontSize: '0.75rem',
  },
  genre: {
    background: '#e5091422',
    color: '#e50914',
    padding: '2px 8px',
    borderRadius: '12px',
    fontSize: '0.75rem',
    fontWeight: 600,
  },
};

export default function MovieCard({ movie }) {
  const navigate = useNavigate();

  return (
    <div
      style={styles.card}
      onClick={() => navigate(`/movies/${movie.id}`)}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = 'translateY(-4px)';
        e.currentTarget.style.boxShadow = '0 8px 24px rgba(229,9,20,0.2)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = 'translateY(0)';
        e.currentTarget.style.boxShadow = 'none';
      }}
    >
      <div style={styles.poster}>
        {movie.poster_url ? (
          <img src={movie.poster_url} alt={movie.title} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        ) : (
          '🎬'
        )}
      </div>
      <div style={styles.body}>
        <div style={styles.title}>{movie.title}</div>
        <div style={styles.meta}>
          {movie.genre && <span style={styles.genre}>{movie.genre.name}</span>}
          {movie.release_year && <span style={styles.badge}>{movie.release_year}</span>}
          {movie.runtime_minutes && <span style={styles.badge}>{movie.runtime_minutes}m</span>}
          {movie.language && movie.language !== 'English' && (
            <span style={styles.badge}>{movie.language}</span>
          )}
        </div>
      </div>
    </div>
  );
}
