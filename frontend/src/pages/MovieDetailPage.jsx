import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  getMovie, getMovieRating, getMyRating,
  rateMovie, addToWatchlist, removeFromWatchlist,
  checkWatchlistStatus, logWatch,
} from '../api/client';
import { useAuth } from '../context/AuthContext';
import StarRating from '../components/StarRating';

const s = {
  page: { padding: '2rem', maxWidth: '900px', margin: '0 auto' },
  back: { color: '#888', cursor: 'pointer', marginBottom: '1.5rem', fontSize: '0.9rem' },
  layout: { display: 'flex', gap: '2.5rem', flexWrap: 'wrap' },
  poster: {
    width: '260px', minWidth: '200px', height: '380px',
    background: '#1a1a2e', borderRadius: '10px',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    fontSize: '6rem', border: '1px solid #2a2a4a', overflow: 'hidden', flexShrink: 0,
  },
  info: { flex: 1 },
  title: { fontSize: '2.2rem', fontWeight: 800, color: '#fff', marginBottom: '0.5rem' },
  badges: { display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '1rem' },
  badge: { background: '#2a2a4a', color: '#aaa', padding: '4px 12px', borderRadius: '16px', fontSize: '0.8rem' },
  genre: { background: '#e5091422', color: '#e50914', padding: '4px 12px', borderRadius: '16px', fontSize: '0.8rem', fontWeight: 600 },
  desc: { color: '#bbb', lineHeight: 1.7, marginBottom: '1.5rem' },
  section: { marginBottom: '1.5rem' },
  sectionLabel: { color: '#888', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '1px', marginBottom: '0.5rem' },
  actors: { display: 'flex', gap: '0.5rem', flexWrap: 'wrap' },
  actorChip: { background: '#1a1a2e', border: '1px solid #2a2a4a', color: '#ccc', padding: '4px 12px', borderRadius: '16px', fontSize: '0.85rem' },
  actions: { display: 'flex', gap: '1rem', flexWrap: 'wrap', marginTop: '1.5rem' },
  btnRed: { background: '#e50914', color: '#fff', border: 'none', padding: '0.65rem 1.5rem', borderRadius: '6px', cursor: 'pointer', fontWeight: 700, fontSize: '0.95rem' },
  btnOutline: { background: 'transparent', color: '#fff', border: '2px solid #333', padding: '0.65rem 1.5rem', borderRadius: '6px', cursor: 'pointer', fontWeight: 700, fontSize: '0.95rem' },
  btnGreen: { background: '#2ecc71', color: '#fff', border: 'none', padding: '0.65rem 1.5rem', borderRadius: '6px', cursor: 'pointer', fontWeight: 700, fontSize: '0.95rem' },
  ratingBox: { background: '#1a1a2e', border: '1px solid #2a2a4a', borderRadius: '8px', padding: '1rem', marginBottom: '1rem' },
  avgRating: { fontSize: '1.1rem', color: '#f5c518', fontWeight: 700 },
  msg: { padding: '0.5rem 0', fontSize: '0.9rem', color: '#2ecc71' },
  err: { padding: '0.5rem 0', fontSize: '0.9rem', color: '#e50914' },
  loader: { textAlign: 'center', padding: '4rem', color: '#888' },
};

export default function MovieDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  const [movie, setMovie] = useState(null);
  const [ratingStats, setRatingStats] = useState(null);
  const [myRating, setMyRating] = useState(0);
  const [inWatchlist, setInWatchlist] = useState(false);
  const [msg, setMsg] = useState('');
  const [err, setErr] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    Promise.all([
      getMovie(id),
      getMovieRating(id),
    ]).then(([mr, rr]) => {
      setMovie(mr.data);
      setRatingStats(rr.data);
    }).catch(() => navigate('/movies'))
      .finally(() => setLoading(false));

    if (user) {
      getMyRating(id).then((r) => setMyRating(r.data.rating)).catch(() => {});
      checkWatchlistStatus(id).then((r) => setInWatchlist(r.data.in_watchlist)).catch(() => {});
    }
  }, [id, user, navigate]);

  const flash = (text, isErr = false) => {
    if (isErr) setErr(text); else setMsg(text);
    setTimeout(() => { setMsg(''); setErr(''); }, 3000);
  };

  const handleRate = (stars) => {
    if (!user) return flash('Login to rate movies', true);
    rateMovie({ movie_id: Number(id), rating: stars })
      .then(() => {
        setMyRating(stars);
        flash(`Rated ${stars}/5 ⭐`);
        getMovieRating(id).then((r) => setRatingStats(r.data));
      })
      .catch(() => flash('Rating failed', true));
  };

  const handleWatchlist = () => {
    if (!user) return flash('Login to use watchlist', true);
    const action = inWatchlist ? removeFromWatchlist(id) : addToWatchlist(id);
    action.then(() => {
      setInWatchlist(!inWatchlist);
      flash(inWatchlist ? 'Removed from watchlist' : 'Added to watchlist ✅');
    }).catch(() => flash('Action failed', true));
  };

  const handleWatch = () => {
    if (user) logWatch(Number(id), { last_position_seconds: 0 }).catch(() => {});
    flash('Started watching! 🎬');
  };

  if (loading) return <div style={s.loader}>Loading movie...</div>;
  if (!movie) return null;

  return (
    <div style={s.page}>
      <div style={s.back} onClick={() => navigate(-1)}>← Back</div>
      <div style={s.layout}>
        <div style={s.poster}>
          {movie.poster_url
            ? <img src={movie.poster_url} alt={movie.title} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            : '🎬'}
        </div>
        <div style={s.info}>
          <div style={s.title}>{movie.title}</div>
          <div style={s.badges}>
            {movie.genre && <span style={s.genre}>{movie.genre.name}</span>}
            {movie.release_year && <span style={s.badge}>📅 {movie.release_year}</span>}
            {movie.runtime_minutes && <span style={s.badge}>⏱ {movie.runtime_minutes} min</span>}
            {movie.language && <span style={s.badge}>🌐 {movie.language}</span>}
          </div>

          {movie.description && <p style={s.desc}>{movie.description}</p>}

          {movie.actors?.length > 0 && (
            <div style={s.section}>
              <div style={s.sectionLabel}>Cast</div>
              <div style={s.actors}>
                {movie.actors.map((a) => <span key={a.id} style={s.actorChip}>👤 {a.name}</span>)}
              </div>
            </div>
          )}

          {/* Rating */}
          <div style={s.ratingBox}>
            <div style={s.sectionLabel}>Community Rating</div>
            {ratingStats?.average_rating ? (
              <div style={s.avgRating}>⭐ {ratingStats.average_rating} / 5 &nbsp;
                <span style={{ color: '#888', fontWeight: 400, fontSize: '0.9rem' }}>({ratingStats.total_ratings} ratings)</span>
              </div>
            ) : <div style={{ color: '#666' }}>No ratings yet</div>}

            <div style={{ marginTop: '1rem' }}>
              <div style={s.sectionLabel}>Your Rating</div>
              <StarRating current={myRating} onRate={handleRate} />
            </div>
          </div>

          {msg && <div style={s.msg}>{msg}</div>}
          {err && <div style={s.err}>{err}</div>}

          <div style={s.actions}>
            <button style={s.btnRed} onClick={handleWatch}>▶ Watch Now</button>
            <button
              style={inWatchlist ? s.btnGreen : s.btnOutline}
              onClick={handleWatchlist}
            >
              {inWatchlist ? '✓ In Watchlist' : '+ Watchlist'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
