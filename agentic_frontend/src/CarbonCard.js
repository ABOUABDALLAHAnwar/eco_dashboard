import React from 'react';

const CarbonCard = () => {
  const carbonFootprintReduction = 42;

  return (
    <div style={{ border: '1px solid #ccc', padding: '16px', margin: '16px' }}>
      <h2>Carbon Footprint Reduction</h2>
      <p>{carbonFootprintReduction}%</p>

      <div style={{ background: '#eee', height: '20px', width: '100%' }}>
        <div
          style={{
            background: 'green',
            height: '100%',
            width: `${carbonFootprintReduction}%`,
          }}
        />
      </div>
    </div>
  );
};

export default CarbonCard;
