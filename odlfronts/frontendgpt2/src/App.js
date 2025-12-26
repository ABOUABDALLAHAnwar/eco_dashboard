import { useState } from 'react';
import Dashboard from './Dashboard';
import Login from './Login';

function App() {
  const [user,setUser] = useState(null);

  return user ? <Dashboard /> : <Login onLogin={data=>setUser(data)} />;
}

export default App;
