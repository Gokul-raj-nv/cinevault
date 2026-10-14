import React, { useState } from 'react';

export default function StarRating({ current = 0, onRate, readonly = false }) {
  const [hovered, setHovered] = useState(0);

  return (
    <div style={{ display: 'flex', gap: '4px' }}>
      {[1, 2, 3, 4, 5].map((star) => (
        <span
          key={star}
          style={{
            fontSize: '1.6rem',
            cursor: readonly ? 'default' : 'pointer',
            color: star <= (hovered || current) ? '#f5c518' : '#444',
            transition: 'color 0.15s',
            userSelect: 'none',
          }}
          onMouseEnter={() => !readonly && setHovered(star)}
          onMouseLeave={() => !readonly && setHovered(0)}
          onClick={() => !readonly && onRate && onRate(star)}
        >
          ★
        </span>
      ))}
      {!readonly && current > 0 && (
        <span style={{ color: '#aaa', fontSize: '0.85rem', marginLeft: '8px', alignSelf: 'center' }}>
          Your rating: {current}/5
        </span>
      )}
    </div>
  );
}
