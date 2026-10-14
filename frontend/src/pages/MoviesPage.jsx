import React, { useEffect, useState } from 'react';
import { getMovies, getGenres } from '../api/client';
import MovieCard from '../components/MovieCard';

const styles = {
  page: { padding: '2rem' },
  header: { marginBottom: '2rem' },
  title: { fontSize: '2rem', fontWeight: 800, color: '#fff', marginBottom: '0.3rem' },
  subtitle: { color: '#888' },
  controls: {
    display: 'flex',
    gap: '1rem',
    marginBottom: '2rem',
    flexWrap: 'wrap',
    alignItems: 'center',
  },
  searchInput: {
    background: '#1a1a2e',
    border: '1px solid #2a2a4a',
    color: '#fff',
    padding: '0.6rem 1rem',
    borderRadius: '6px',
    fontSize: '0.95rem',
    flex: '1',
    minWidth: '200px',
    outline: 'none',
  },
  select: {
    background: '#1a1a2e',
    border: '1px solid #2a2a4a',
    color: '#aaa',
    padding: '0.6rem 1rem',
    borderRadius: '6px',
    fontSize: '0.95rem',
    cursor: 'pointer',
    outline: 'none',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))',
    gap: '1.2rem',
  },
  pagination: {
    display: 'flex',
    gap: '1rem',
    justifyContent: 'center',
    marginTop: '2.5rem',
    alignItems: 'center',
  },
  pageBtn: {
    background: '#1a1a2e',
    border: '1px solid #2a2a4a',
    color: '#fff',
    padding: '0.5rem 1.2rem',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '0.9rem',
  },
  pageInfo: { color: '#888', fontSize: '0.9rem' },
  empty: { textAlign: 'center', padding: '4rem', color: '#666' },
  loader: { textAlign: 'center', padding: '4rem', color: '#888' },
};

export default function MoviesPage() {
  const [movies, setMovies] = useState([]);
  const [genres, setGenres] = useState([]);
  const [search, setSearch] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [genreId, setGenreId] = useState('');
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const pageSize = 20;

  // Debounce search
  useEffect(() => {
    const t = setTimeout(() => setDebouncedSearch(search), 500);
    return () => clearTimeout(t);
  }, [search]);

  useEffect(() => { getGenres().then((r) => setGenres(r.data)).catch(() => {}); }, []);

  useEffect(() => {
    setLoading(true);
    const params = { page, page_size: pageSize };
    if (debouncedSearch) params.search = debouncedSearch;
    if (genreId) params.genre_id = genreId;

    getMovies(params)
      .then((r) => { setMovies(r.data.results); setTotal(r.data.total); })
      .catch(() => setMovies([]))
      .finally(() => setLoading(false));
  }, [page, debouncedSearch, genreId]);

  const totalPages = Math.ceil(total / pageSize);

  return (
    <div style={styles.page}>
      <div style={styles.header}>
        <div style={styles.title}>🎬 All Movies</div>
        <div style={styles.subtitle}>{total} movies in catalog</div>
      </div>

      <div style={styles.controls}>
        <input
          style={styles.searchInput}
          placeholder="🔍 Search by title..."
          value={search}
          onChange={(e) => { setSearch(e.target.value); setPage(1); }}
        />
        <select
          style={styles.select}
          value={genreId}
          onChange={(e) => { setGenreId(e.target.value); setPage(1); }}
        >
          <option value="">All Genres</option>
          {genres.map((g) => <option key={g.id} value={g.id}>{g.name}</option>)}
        </select>
        {(search || genreId) && (
          <button
            style={{ ...styles.pageBtn, color: '#e50914', borderColor: '#e50914' }}
            onClick={() => { setSearch(''); setGenreId(''); setPage(1); }}
          >
            ✕ Clear
          </button>
        )}
      </div>

      {loading ? (
        <div style={styles.loader}>Loading movies...</div>
      ) : movies.length === 0 ? (
        <div style={styles.empty}>
          <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🎬</div>
          <p>No movies found. Try a different search.</p>
        </div>
      ) : (
        <>
          <div style={styles.grid}>
            {movies.map((m) => <MovieCard key={m.id} movie={m} />)}
          </div>
          {totalPages > 1 && (
            <div style={styles.pagination}>
              <button
                style={styles.pageBtn}
                disabled={page === 1}
                onClick={() => setPage(p => p - 1)}
              >← Prev</button>
              <span style={styles.pageInfo}>Page {page} of {totalPages}</span>
              <button
                style={styles.pageBtn}
                disabled={page === totalPages}
                onClick={() => setPage(p => p + 1)}
              >Next →</button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
