import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getTrending, getMovies } from '../api/client';
import MovieCard from '../components/MovieCard';

const styles = {
  hero: {
    background: 'linear-gradient(135deg, #0f0f1a 0%, #1a0a2e 50%, #0f0f1a 100%)',
    padding: '5rem 2rem',
    textAlign: 'center',
    borderBottom: '1px solid #1e1e3a',
  },
  heroTitle: {
    fontSize: '3.5rem',
    fontWeight: 900,
    color: '#fff',
    marginBottom: '1rem',
    lineHeight: 1.1,
  },
  accent: { color: '#e50914' },
  heroSub: { color: '#aaa', fontSize: '1.15rem', marginBottom: '2rem' },
  heroBtns: { display: 'flex', gap: '1rem', justifyContent: 'center' },
  btnPrimary: {
    background: '#e50914',
    color: '#fff',
    border: 'none',
    padding: '0.8rem 2rem',
    borderRadius: '6px',
    fontSize: '1rem',
    fontWeight: 700,
    cursor: 'pointer',
    textDecoration: 'none',
  },
  btnSecondary: {
    background: 'transparent',
    color: '#fff',
    border: '2px solid #333',
    padding: '0.8rem 2rem',
    borderRadius: '6px',
    fontSize: '1rem',
    fontWeight: 700,
    cursor: 'pointer',
    textDecoration: 'none',
  },
  section: { padding: '3rem 2rem' },
  sectionTitle: {
    fontSize: '1.5rem',
    fontWeight: 700,
    color: '#fff',
    marginBottom: '1.5rem',
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))',
    gap: '1.2rem',
  },
  features: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
    gap: '1.5rem',
    padding: '3rem 2rem',
    background: '#12121f',
    borderTop: '1px solid #1e1e3a',
  },
  featureCard: {
    background: '#1a1a2e',
    border: '1px solid #1e1e3a',
    borderRadius: '10px',
    padding: '1.5rem',
    textAlign: 'center',
  },
  featureIcon: { fontSize: '2.5rem', marginBottom: '0.8rem' },
  featureTitle: { color: '#fff', fontWeight: 700, marginBottom: '0.5rem' },
  featureDesc: { color: '#888', fontSize: '0.875rem', lineHeight: 1.5 },
};

export default function HomePage() {
  const [trending, setTrending] = useState([]);
  const [recent, setRecent] = useState([]);

  useEffect(() => {
    getTrending().then((r) => setTrending(r.data.slice(0, 6))).catch(() => {});
    getMovies({ page: 1, page_size: 6 }).then((r) => setRecent(r.data.results)).catch(() => {});
  }, []);

  return (
    <div>
      {/* Hero */}
      <div style={styles.hero}>
        <div style={styles.heroTitle}>
          Your <span style={styles.accent}>Streaming</span> Backend<br />
          Built Like Netflix
        </div>
        <p style={styles.heroSub}>
          AI-powered movie discovery · Semantic search · Personalized recommendations
        </p>
        <div style={styles.heroBtns}>
          <Link to="/movies" style={styles.btnPrimary}>Browse Movies</Link>
          <Link to="/register" style={styles.btnSecondary}>Get Started</Link>
        </div>
      </div>

      {/* Features */}
      <div style={styles.features}>
        {[
          { icon: '🔍', title: 'Semantic Search', desc: 'Search with natural language — "dark detective thriller" finds Batman' },
          { icon: '🤖', title: 'AI Recommendations', desc: 'Personalised picks based on your ratings and watch history' },
          { icon: '⚡', title: 'Redis Caching', desc: 'Trending and genres served in under 1ms from cache' },
          { icon: '🔐', title: 'JWT Auth', desc: 'Secure authentication with role-based access control' },
        ].map((f) => (
          <div key={f.title} style={styles.featureCard}>
            <div style={styles.featureIcon}>{f.icon}</div>
            <div style={styles.featureTitle}>{f.title}</div>
            <div style={styles.featureDesc}>{f.desc}</div>
          </div>
        ))}
      </div>

      {/* Trending */}
      {trending.length > 0 && (
        <div style={styles.section}>
          <div style={styles.sectionTitle}>🔥 Trending Now</div>
          <div style={styles.grid}>
            {trending.map((m) => <MovieCard key={m.id} movie={m} />)}
          </div>
        </div>
      )}

      {/* Recently Added */}
      {recent.length > 0 && (
        <div style={{ ...styles.section, paddingTop: 0 }}>
          <div style={styles.sectionTitle}>🆕 Recently Added</div>
          <div style={styles.grid}>
            {recent.map((m) => <MovieCard key={m.id} movie={m} />)}
          </div>
          <div style={{ textAlign: 'center', marginTop: '2rem' }}>
            <Link to="/movies" style={styles.btnPrimary}>View All Movies →</Link>
          </div>
        </div>
      )}

      {trending.length === 0 && recent.length === 0 && (
        <div style={{ textAlign: 'center', padding: '4rem', color: '#666' }}>
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🎬</div>
          <p>No movies yet. <Link to="/admin" style={{ color: '#e50914' }}>Add some as admin →</Link></p>
        </div>
      )}
    </div>
  );
}
