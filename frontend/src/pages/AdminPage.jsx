import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getGenres, getActors, createGenre, createActor, createMovie } from '../api/client';
import { useAuth } from '../context/AuthContext';

const s = {
  page: { padding: '2rem', maxWidth: '800px', margin: '0 auto' },
  title: { fontSize: '2rem', fontWeight: 800, color: '#fff', marginBottom: '0.3rem' },
  sub: { color: '#888', marginBottom: '2rem' },
  tabs: { display: 'flex', gap: '0.5rem', marginBottom: '2rem', borderBottom: '1px solid #2a2a4a', paddingBottom: '0' },
  tab: (active) => ({
    background: 'transparent', border: 'none', color: active ? '#e50914' : '#888',
    padding: '0.7rem 1.5rem', cursor: 'pointer', fontWeight: active ? 700 : 400,
    fontSize: '0.95rem', borderBottom: active ? '2px solid #e50914' : '2px solid transparent',
    marginBottom: '-1px', transition: 'color 0.2s',
  }),
  card: { background: '#1a1a2e', border: '1px solid #2a2a4a', borderRadius: '10px', padding: '1.5rem', marginBottom: '1.5rem' },
  cardTitle: { color: '#fff', fontWeight: 700, marginBottom: '1rem', fontSize: '1.1rem' },
  row: { display: 'flex', gap: '0.8rem', flexWrap: 'wrap', alignItems: 'flex-end' },
  group: { display: 'flex', flexDirection: 'column', gap: '0.3rem', flex: 1, minWidth: '150px' },
  label: { color: '#aaa', fontSize: '0.8rem' },
  input: { background: '#0f0f1a', border: '1px solid #2a2a4a', color: '#fff', padding: '0.6rem 0.9rem', borderRadius: '6px', fontSize: '0.9rem', outline: 'none' },
  select: { background: '#0f0f1a', border: '1px solid #2a2a4a', color: '#fff', padding: '0.6rem 0.9rem', borderRadius: '6px', fontSize: '0.9rem', outline: 'none', cursor: 'pointer' },
  btn: { background: '#e50914', color: '#fff', border: 'none', padding: '0.6rem 1.4rem', borderRadius: '6px', cursor: 'pointer', fontWeight: 700, whiteSpace: 'nowrap' },
  success: { color: '#2ecc71', fontSize: '0.85rem', marginTop: '0.5rem' },
  error: { color: '#e50914', fontSize: '0.85rem', marginTop: '0.5rem' },
  chips: { display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginTop: '0.8rem' },
  chip: { background: '#2a2a4a', color: '#ccc', padding: '3px 12px', borderRadius: '16px', fontSize: '0.8rem' },
};

export default function AdminPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [tab, setTab] = useState('movie');
  const [genres, setGenres] = useState([]);
  const [actors, setActors] = useState([]);
  const [msg, setMsg] = useState('');
  const [err, setErr] = useState('');

  // Forms
  const [genreForm, setGenreForm] = useState({ name: '' });
  const [actorForm, setActorForm] = useState({ name: '', bio: '' });
  const [movieForm, setMovieForm] = useState({
    title: '', description: '', release_year: '', runtime_minutes: '',
    language: 'English', poster_url: '', genre_id: '', actor_ids: [],
  });

  useEffect(() => {
    if (!user?.is_admin) { navigate('/'); return; }
    getGenres().then((r) => setGenres(r.data)).catch(() => {});
    getActors().then((r) => setActors(r.data)).catch(() => {});
  }, [user, navigate]);

  const flash = (text, isErr = false) => {
    if (isErr) setErr(text); else setMsg(text);
    setTimeout(() => { setMsg(''); setErr(''); }, 3000);
  };

  const handleGenre = async (e) => {
    e.preventDefault();
    try {
      const res = await createGenre(genreForm);
      setGenres((g) => [...g, res.data]);
      setGenreForm({ name: '' });
      flash('Genre created ✅');
    } catch (ex) { flash(ex.response?.data?.detail || 'Failed', true); }
  };

  const handleActor = async (e) => {
    e.preventDefault();
    try {
      const res = await createActor(actorForm);
      setActors((a) => [...a, res.data]);
      setActorForm({ name: '', bio: '' });
      flash('Actor created ✅');
    } catch (ex) { flash(ex.response?.data?.detail || 'Failed', true); }
  };

  const handleMovie = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        ...movieForm,
        release_year: movieForm.release_year ? Number(movieForm.release_year) : null,
        runtime_minutes: movieForm.runtime_minutes ? Number(movieForm.runtime_minutes) : null,
        genre_id: movieForm.genre_id ? Number(movieForm.genre_id) : null,
        actor_ids: movieForm.actor_ids.map(Number),
      };
      await createMovie(payload);
      setMovieForm({ title: '', description: '', release_year: '', runtime_minutes: '', language: 'English', poster_url: '', genre_id: '', actor_ids: [] });
      flash('Movie created ✅');
    } catch (ex) { flash(ex.response?.data?.detail || 'Failed', true); }
  };

  const toggleActor = (id) => {
    setMovieForm((f) => ({
      ...f,
      actor_ids: f.actor_ids.includes(String(id))
        ? f.actor_ids.filter((a) => a !== String(id))
        : [...f.actor_ids, String(id)],
    }));
  };

  return (
    <div style={s.page}>
      <div style={s.title}>⚙️ Admin Panel</div>
      <div style={s.sub}>Create and manage content</div>

      <div style={s.tabs}>
        {['movie', 'genre', 'actor'].map((t) => (
          <button key={t} style={s.tab(tab === t)} onClick={() => setTab(t)}>
            {t === 'movie' ? '🎬 Movie' : t === 'genre' ? '🏷 Genre' : '👤 Actor'}
          </button>
        ))}
      </div>

      {msg && <div style={s.success}>{msg}</div>}
      {err && <div style={s.error}>{err}</div>}

      {/* Create Genre */}
      {tab === 'genre' && (
        <div style={s.card}>
          <div style={s.cardTitle}>Create Genre</div>
          <form onSubmit={handleGenre}>
            <div style={s.row}>
              <div style={s.group}>
                <label style={s.label}>Genre Name</label>
                <input style={s.input} required value={genreForm.name}
                  onChange={(e) => setGenreForm({ name: e.target.value })} placeholder="e.g. Action" />
              </div>
              <button style={s.btn} type="submit">Create</button>
            </div>
          </form>
          {genres.length > 0 && (
            <div style={s.chips}>{genres.map((g) => <span key={g.id} style={s.chip}>{g.name}</span>)}</div>
          )}
        </div>
      )}

      {/* Create Actor */}
      {tab === 'actor' && (
        <div style={s.card}>
          <div style={s.cardTitle}>Create Actor</div>
          <form onSubmit={handleActor}>
            <div style={s.row}>
              <div style={s.group}>
                <label style={s.label}>Actor Name</label>
                <input style={s.input} required value={actorForm.name}
                  onChange={(e) => setActorForm({ ...actorForm, name: e.target.value })} placeholder="e.g. Christian Bale" />
              </div>
              <div style={s.group}>
                <label style={s.label}>Bio (optional)</label>
                <input style={s.input} value={actorForm.bio}
                  onChange={(e) => setActorForm({ ...actorForm, bio: e.target.value })} placeholder="Short bio..." />
              </div>
              <button style={s.btn} type="submit">Create</button>
            </div>
          </form>
          {actors.length > 0 && (
            <div style={s.chips}>{actors.map((a) => <span key={a.id} style={s.chip}>{a.name}</span>)}</div>
          )}
        </div>
      )}

      {/* Create Movie */}
      {tab === 'movie' && (
        <div style={s.card}>
          <div style={s.cardTitle}>Create Movie</div>
          <form onSubmit={handleMovie}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.9rem' }}>
              <div style={s.group}>
                <label style={s.label}>Title *</label>
                <input style={s.input} required value={movieForm.title}
                  onChange={(e) => setMovieForm({ ...movieForm, title: e.target.value })} placeholder="Movie title" />
              </div>
              <div style={s.group}>
                <label style={s.label}>Description</label>
                <textarea style={{ ...s.input, height: '80px', resize: 'vertical' }}
                  value={movieForm.description}
                  onChange={(e) => setMovieForm({ ...movieForm, description: e.target.value })}
                  placeholder="Short plot summary..." />
              </div>
              <div style={s.row}>
                <div style={s.group}>
                  <label style={s.label}>Release Year</label>
                  <input style={s.input} type="number" min="1900" max="2100"
                    value={movieForm.release_year}
                    onChange={(e) => setMovieForm({ ...movieForm, release_year: e.target.value })} placeholder="2024" />
                </div>
                <div style={s.group}>
                  <label style={s.label}>Runtime (minutes)</label>
                  <input style={s.input} type="number" min="1"
                    value={movieForm.runtime_minutes}
                    onChange={(e) => setMovieForm({ ...movieForm, runtime_minutes: e.target.value })} placeholder="120" />
                </div>
                <div style={s.group}>
                  <label style={s.label}>Language</label>
                  <input style={s.input} value={movieForm.language}
                    onChange={(e) => setMovieForm({ ...movieForm, language: e.target.value })} />
                </div>
              </div>
              <div style={s.row}>
                <div style={s.group}>
                  <label style={s.label}>Genre</label>
                  <select style={s.select} value={movieForm.genre_id}
                    onChange={(e) => setMovieForm({ ...movieForm, genre_id: e.target.value })}>
                    <option value="">Select genre...</option>
                    {genres.map((g) => <option key={g.id} value={g.id}>{g.name}</option>)}
                  </select>
                </div>
                <div style={s.group}>
                  <label style={s.label}>Poster URL (optional)</label>
                  <input style={s.input} value={movieForm.poster_url}
                    onChange={(e) => setMovieForm({ ...movieForm, poster_url: e.target.value })} placeholder="https://..." />
                </div>
              </div>
              {actors.length > 0 && (
                <div>
                  <label style={s.label}>Cast (click to select)</label>
                  <div style={s.chips}>
                    {actors.map((a) => (
                      <span key={a.id}
                        style={{
                          ...s.chip,
                          cursor: 'pointer',
                          background: movieForm.actor_ids.includes(String(a.id)) ? '#e50914' : '#2a2a4a',
                          color: movieForm.actor_ids.includes(String(a.id)) ? '#fff' : '#ccc',
                        }}
                        onClick={() => toggleActor(a.id)}>{a.name}</span>
                    ))}
                  </div>
                </div>
              )}
              <button style={{ ...s.btn, width: '100%', padding: '0.8rem' }} type="submit">
                🎬 Create Movie
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}
