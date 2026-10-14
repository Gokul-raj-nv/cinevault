import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { register, login, getMe } from '../api/client';
import { useAuth } from '../context/AuthContext';

const s = {
  page: { minHeight: '80vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2rem' },
  card: { background: '#1a1a2e', border: '1px solid #2a2a4a', borderRadius: '12px', padding: '2.5rem', width: '100%', maxWidth: '400px' },
  title: { fontSize: '1.8rem', fontWeight: 800, color: '#fff', marginBottom: '0.3rem' },
  sub: { color: '#888', marginBottom: '2rem', fontSize: '0.9rem' },
  group: { marginBottom: '1.2rem' },
  label: { color: '#aaa', fontSize: '0.85rem', marginBottom: '0.4rem', display: 'block' },
  input: { width: '100%', background: '#0f0f1a', border: '1px solid #2a2a4a', color: '#fff', padding: '0.7rem 1rem', borderRadius: '6px', fontSize: '0.95rem', outline: 'none', boxSizing: 'border-box' },
  btn: { width: '100%', background: '#e50914', color: '#fff', border: 'none', padding: '0.8rem', borderRadius: '6px', fontSize: '1rem', fontWeight: 700, cursor: 'pointer', marginTop: '0.5rem' },
  err: { background: '#e5091422', color: '#e50914', border: '1px solid #e5091444', borderRadius: '6px', padding: '0.7rem 1rem', marginBottom: '1rem', fontSize: '0.9rem' },
  footer: { textAlign: 'center', marginTop: '1.5rem', color: '#888', fontSize: '0.9rem' },
  link: { color: '#e50914', textDecoration: 'none', fontWeight: 600 },
};

export default function RegisterPage() {
  const [form, setForm] = useState({ name: '', email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { loginUser } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await register(form);
      const res = await login({ email: form.email, password: form.password });
      const me = await getMe();
      loginUser(res.data.access_token, me.data);
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={s.page}>
      <div style={s.card}>
        <div style={s.title}>Create Account 🎬</div>
        <div style={s.sub}>Join CineVault and start discovering movies</div>
        {error && <div style={s.err}>{error}</div>}
        <form onSubmit={handleSubmit}>
          <div style={s.group}>
            <label style={s.label}>Name</label>
            <input
              style={s.input} type="text" required
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              placeholder="Your name"
            />
          </div>
          <div style={s.group}>
            <label style={s.label}>Email</label>
            <input
              style={s.input} type="email" required
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              placeholder="you@example.com"
            />
          </div>
          <div style={s.group}>
            <label style={s.label}>Password</label>
            <input
              style={s.input} type="password" required minLength={6}
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              placeholder="Min 6 characters"
            />
          </div>
          <button style={s.btn} type="submit" disabled={loading}>
            {loading ? 'Creating account...' : 'Create Account'}
          </button>
        </form>
        <div style={s.footer}>
          Already have an account? <Link to="/login" style={s.link}>Sign In</Link>
        </div>
      </div>
    </div>
  );
}
