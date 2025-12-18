#!/bin/bash

# Script pour générer la structure du front React pour ton MVP FastAPI
# Usage : bash generate_front.sh

PROJECT_DIR="eco-dashboard-frontend"
SRC_DIR="$PROJECT_DIR/src"

echo "Création de la structure de projet..."
mkdir -p $SRC_DIR/{api,components,pages,types}
mkdir -p $PROJECT_DIR/public

# Fichiers de base
echo "Création des fichiers de configuration..."
cat > $PROJECT_DIR/package.json <<EOL
{
  "name": "eco-dashboard-frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "axios": "^1.6.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "typescript": "^5.2.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build"
  }
}
EOL

cat > $PROJECT_DIR/tsconfig.json <<EOL
{
  "compilerOptions": {
    "target": "ES6",
    "module": "ESNext",
    "jsx": "react-jsx",
    "moduleResolution": "Node",
    "strict": true,
    "esModuleInterop": true
  },
  "include": ["src"]
}
EOL

cat > $PROJECT_DIR/public/index.html <<EOL
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Éco Dashboard</title>
</head>
<body>
  <div id="root"></div>
</body>
</html>
EOL

# src/index.tsx
cat > $SRC_DIR/index.tsx <<EOL
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root')!);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
EOL

# src/App.tsx
cat > $SRC_DIR/App.tsx <<EOL
import React, { useState } from 'react';
import Home from './pages/Home';
import Login from './components/Login';
import Signup from './components/Signup';

export default function App() {
  const [user, setUser] = useState<string | null>(null);

  if (!user) {
    return (
      <div>
        <h1>Éco Dashboard</h1>
        <Login setUser={setUser} />
        <Signup setUser={setUser} />
      </div>
    );
  }

  return <Home user={user} />;
}
EOL

# src/api/axiosClient.ts
cat > $SRC_DIR/api/axiosClient.ts <<EOL
import axios from 'axios';

export const axiosClient = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true,
});
EOL

# src/api/apiClient.ts
cat > $SRC_DIR/api/apiClient.ts <<EOL
import { axiosClient } from './axiosClient';

export const getActionsTemplates = async (act_type: string) => {
  const res = await axiosClient.get(\`/actions_templates?act_type=\${act_type}\`);
  return res.data;
};

export const getAllActionsTemplates = async () => {
  const res = await axiosClient.get('/all_actions_templates');
  return res.data;
};

export const addUserAction = async (action: any) => {
  const res = await axiosClient.post('/add_user_actions', action);
  return res.data;
};

export const signup = async (email: string, password: string) => {
  const res = await axiosClient.post(\`/signup?email=\${email}&password=\${password}\`);
  return res.data;
};

export const login = async (username: string, password: string) => {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);
  const res = await axiosClient.post('/login', formData);
  return res.data;
};
EOL

# src/types/action.ts
cat > $SRC_DIR/types/action.ts <<EOL
export interface Action {
  user: string;
  name: string;
  type: string;
  quartier: string;
}
EOL

# src/components/Login.tsx
cat > $SRC_DIR/components/Login.tsx <<EOL
import React, { useState } from 'react';
import { login } from '../api/apiClient';

export default function Login({ setUser }: { setUser: (user: string) => void }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    try {
      await login(username, password);
      setUser(username);
    } catch (err) {
      alert('Erreur login');
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
      <input placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}
EOL

# src/components/Signup.tsx
cat > $SRC_DIR/components/Signup.tsx <<EOL
import React, { useState } from 'react';
import { signup } from '../api/apiClient';

export default function Signup({ setUser }: { setUser: (user: string) => void }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSignup = async () => {
    try {
      await signup(email, password);
      setUser(email);
    } catch (err) {
      alert('Erreur signup');
    }
  };

  return (
    <div>
      <h2>Signup</h2>
      <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleSignup}>Signup</button>
    </div>
  );
}
EOL

# src/components/ActionsList.tsx
cat > $SRC_DIR/components/ActionsList.tsx <<EOL
import React, { useEffect, useState } from 'react';
import { getAllActionsTemplates } from '../api/apiClient';

export default function ActionsList() {
  const [actions, setActions] = useState<any[]>([]);

  useEffect(() => {
    getAllActionsTemplates().then(setActions);
  }, []);

  return (
    <div>
      <h3>Actions</h3>
      <ul>
        {actions.map((a, i) => (
          <li key={i}>{JSON.stringify(a)}</li>
        ))}
      </ul>
    </div>
  );
}
EOL

# src/components/AddAction.tsx
cat > $SRC_DIR/components/AddAction.tsx <<EOL
import React, { useState } from 'react';
import { addUserAction } from '../api/apiClient';

export default function AddAction() {
  const [name, setName] = useState('');
  const [type, setType] = useState('');
  const [quartier, setQuartier] = useState('');

  const handleAdd = async () => {
    await addUserAction({ name, type, quartier });
    alert('Action ajoutée');
  };

  return (
    <div>
      <h3>Ajouter action</h3>
      <input placeholder="Nom" value={name} onChange={(e) => setName(e.target.value)} />
      <input placeholder="Type" value={type} onChange={(e) => setType(e.target.value)} />
      <input placeholder="Quartier" value={quartier} onChange={(e) => setQuartier(e.target.value)} />
      <button onClick={handleAdd}>Ajouter</button>
    </div>
  );
}
EOL

# src/pages/Home.tsx
cat > $SRC_DIR/pages/Home.tsx <<EOL
import React from 'react';
import ActionsList from '../components/ActionsList';
import AddAction from '../components/AddAction';

export default function Home({ user }: { user: string }) {
  return (
    <div>
      <h1>Bienvenue {user}</h1>
      <AddAction />
      <ActionsList />
    </div>
  );
}
EOL

echo "Structure du front générée dans $PROJECT_DIR"
echo "Pour lancer :"
echo "1) cd $PROJECT_DIR"
echo "2) npm install"
echo "3) npm start"
