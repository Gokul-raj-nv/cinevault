import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const styles = {
  nav: {
    background: '#12121f',
    borderBottom: '1px solid #1e1e3a',
    padding: '0 2rem',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    height: '64px',
    position: 'sticky',
    top: 0,
    zIndex: 100,
  },
  logo: {
    color: '#e50914',
    fontWeight: 800,
    fontSize: '1.5rem',
    textDecoration: 'none',
    letterSpacing: '1px',
  },
  links: { display: 'flex', gap: '1.5rem', alignItems: 'center' },
  link: {
    color: '#ccc',
    textDecoration: 'none',
    fontSize: '0.95rem',
    transition: 'color 0.2s',
  },
  btn: {
    background: '#e50914',
    color: '#fff',
    border: 'none',
    padding: '0.4rem 1.2rem',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '0.9rem',
    fontWeight: 600,
  },
  user: { color: '#aaa', fontSize: '0.85rem' },
};

export default function Navbar() {
  const { user, logoutUser } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logoutUser();
    navigate('/login');
  };

  return (
    <nav style={styles.nav}>
      <Link to="/" style={styles.logo}>🎬 CineVault</Link>
      <div style={styles.links}>
        <Link to="/movies" style={styles.link}>Browse</Link>
        {user && <Link to="/watchlist" style={styles.link}>Watchlist</Link>}
        {user && <Link to="/history" style={styles.link}>History</Link>}
        {user?.is_admin && <Link to="/admin" style={styles.link}>Admin</Link>}
        {user ? (
          <>
            <span style={styles.user}>👤 {user.name}</span>
            <button style={styles.btn} onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" style={styles.link}>Login</Link>
            <Link to="/register">
              <button style={styles.btn}>Sign Up</button>
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}
