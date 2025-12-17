import React from 'react';

const ActionList = () => {
  const actions = [
    { name: 'Bike to work', icon: 'https://via.placeholder.com/40' },
    { name: 'Recycle', icon: 'https://via.placeholder.com/40' },
  ];

  return (
    <div style={{ padding: '16px' }}>
      <h2>Eco-friendly actions</h2>

      {actions.map((action, index) => (
        <div
          key={index}
          style={{
            display: 'flex',
            alignItems: 'center',
            marginBottom: '8px',
          }}
        >
          <img
            src={action.icon}
            alt={action.name}
            style={{ marginRight: '8px' }}
          />
          <span>{action.name}</span>
        </div>
      ))}
    </div>
  );
};

export default ActionList;
