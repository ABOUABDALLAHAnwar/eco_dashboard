import React from 'react';
import Header from './Header';
import CarbonCard from './CarbonCard';
import ActionList from './ActionList';
import NeighborComparison from './NeighborComparison';
import Footer from './Footer';

function App() {
  return (
    <div className="App">
      <Header />
      <CarbonCard />
      <ActionList />
      <NeighborComparison />
      <Footer />
    </div>
  );
}

export default App;
