#!/bin/bash

# Nom du projet frontend
FRONTEND_DIR="frontendgpt"

echo "[*] Création du projet React dans ./$FRONTEND_DIR"
npx create-react-app $FRONTEND_DIR --template javascript

cd $FRONTEND_DIR || exit

echo "[*] Création des composants et pages"

# Supprimer le CSS et App.js existants
rm src/App.css src/App.js src/index.css

# Création du CSS global
cat > src/index.css <<EOL
/* ==== Global ==== */
body { font-family: 'Roboto', sans-serif; margin: 0; background: #f0f2f5; color: #333'; }
h1,h3 { margin: 0; }
p { margin: 5px 0 0 0; color: #666; }
header { background: linear-gradient(90deg, #4a6c59, #2f4f3f); color: white; padding: 20px 40px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
header h1 { font-size: 1.8rem; font-weight: 700; }
header button { background: #6b8b73; border: none; padding: 12px 24px; color: white; border-radius: 8px; cursor: pointer; font-weight: 500; transition: background 0.3s; }
header button:hover { background: #55725a; }
#dashboard { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; padding: 30px 40px; }
.card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 6px 15px rgba(0,0,0,0.08); transition: transform 0.2s; }
.card:hover { transform: translateY(-5px); }
#map { height: 500px; border-radius: 12px; }
#total-co2 { font-size: 2.2rem; font-weight: 700; color: #4a6c59; margin-bottom: 10px; }
#co2-bar { margin-bottom: 15px; height: 25px; background: #e0e0e0; border-radius: 12px; overflow: hidden; }
#co2-bar-inner { height: 100%; width: 0; background: #4a6c59; border-radius: 12px 0 0 12px; transition: width 0.5s ease; }
#co2-details div { margin: 4px 0; font-weight: 500; }
#evolution-chart { height: 250px; }
table { width: 100%; border-collapse: collapse; margin-top: 10px; }
td { padding: 8px 0; font-weight: 500; }
tr td:first-child { color: #4a6c59; }
@media (max-width: 900px) { #dashboard { grid-template-columns: 1fr; } header { flex-direction: column; align-items: flex-start; gap: 10px; } }
EOL

# Création du composant Header
mkdir -p src/components
cat > src/components/Header.jsx <<EOL
export default function Header({onAdd}) {
  return (
    <header>
      <div>
        <h1>Dashboard Carbon Card</h1>
        <p>Suivi et impact CO₂ des initiatives locales</p>
      </div>
      <button onClick={onAdd}>Ajouter une action</button>
    </header>
  );
}
EOL

# Création du composant DashboardGrid
cat > src/components/DashboardGrid.jsx <<EOL
export default function DashboardGrid({children}) {
  return <div id="dashboard">{children}</div>;
}
EOL

# Création de la page Dashboard
cat > src/Dashboard.jsx <<EOL
import { useEffect, useState } from 'react';
import Header from './components/Header';
import DashboardGrid from './components/DashboardGrid';
import L from 'leaflet';
import Plotly from 'plotly.js-dist';

export default function Dashboard() {
  const [actions, setActions] = useState([]);

  useEffect(() => {
    // Fetch des actions depuis l'API
    fetch('http://localhost:8000/all_actions_templates')
      .then(res => res.json())
      .then(data => setActions(data))
      .catch(e => console.error(e));
  }, []);

  useEffect(() => {
    if(actions.length===0) return;

    // Carte
    const map = L.map('map').setView([44.8695, -0.545], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    actions.forEach(a => {
      let color = a.impact_co2_kg < 1000 ? 'orange' : (a.impact_co2_kg < 2000 ? 'yellowgreen' : 'green');
      L.circle([a.lat, a.lon], {color, fillColor: color, fillOpacity:0.6, radius: a.impact_co2_kg})
        .bindPopup(\`\${a.name}<br>\${a.quartier}<br>CO₂ évité: \${(a.impact_co2_kg/1000).toFixed(1)} t\`).addTo(map);
    });

    // Stats CO2
    const totalCO2 = actions.reduce((sum,a)=>sum+a.impact_co2_kg,0);
    document.getElementById('total-co2').innerText = (totalCO2/1000).toFixed(1) + ' TONNES';
    document.getElementById('co2-bar-inner').style.width = Math.min(totalCO2/5000*100,100) + '%';
    const typesCO2 = {};
    actions.forEach(a=>typesCO2[a.type]=(typesCO2[a.type]||0)+a.impact_co2_kg);
    document.getElementById('co2-details').innerHTML = Object.entries(typesCO2).map(([t,v])=>\`<div>\${t}: \${(v/1000).toFixed(1)} t</div>\`).join('');

    // Graphique évolution (mock)
    const evolution = { months:["Jan","Fév","Mar","Avr","Mai"], values:[0,2,0,12,5] };
    Plotly.newPlot('evolution-chart',[{x:evolution.months, y:evolution.values, type:'scatter', mode:'lines+markers', line:{color:'#4a6c59'}}],{margin:{t:30,b:30,l:30,r:30}});

    // Top quartiers
    const quartiers={};
    actions.forEach(a=>quartiers[a.quartier]=(quartiers[a.quartier]||0)+1);
    const top3 = Object.entries(quartiers).sort((a,b)=>b[1]-a[1]).slice(0,3);
    document.getElementById('top-quartiers').innerHTML = top3.map(([q,val],i)=>\`<tr><td>\${i+1} \${q}</td><td>\${val}</td></tr>\`).join('');

  }, [actions]);

  return (
    <div className="min-h-screen">
      <Header onAdd={()=>alert('Ajouter une action')} />
      <DashboardGrid>
        <div className="card" id="map"></div>
        <div className="card">
          <h3>Total CO₂ évité</h3>
          <div id="total-co2">0 t</div>
          <div id="co2-bar"><div id="co2-bar-inner"></div></div>
          <div id="co2-details"></div>
        </div>
        <div className="card" style={{gridColumn:"span 2"}}>
          <h3>Évolution des initiatives</h3>
          <div id="evolution-chart"></div>
        </div>
        <div className="card">
          <h3>Top 3 quartiers</h3>
          <table id="top-quartiers"></table>
        </div>
      </DashboardGrid>
    </div>
  );
}
EOL

# Création de la page Login
cat > src/Login.jsx <<EOL
import { useState } from 'react';

export default function Login({onLogin}) {
  const [email,setEmail]=useState('');
  const [password,setPassword]=useState('');

  const handleSubmit=(e)=>{
    e.preventDefault();
    fetch('http://localhost:8000/login',{
      method:'POST',
      headers:{'Content-Type':'application/x-www-form-urlencoded'},
      body:new URLSearchParams({username:email,password})
    })
    .then(res=>res.json())
    .then(data=>onLogin(data))
    .catch(err=>alert('Erreur login'));
  }

  return (
    <div style={{display:'flex',justifyContent:'center',alignItems:'center',height:'100vh'}}>
      <form onSubmit={handleSubmit} style={{background:'white',padding:30,borderRadius:12,boxShadow:'0 6px 15px rgba(0,0,0,0.1)'}}>
        <h1>Connexion</h1>
        <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} style={{display:'block',margin:'10px 0',padding:'10px',width:200}} />
        <input placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} style={{display:'block',margin:'10px 0',padding:'10px',width:200}} />
        <button type="submit" style={{padding:'10px 20px',background:'#4a6c59',color:'white',border:'none',borderRadius:6,cursor:'pointer'}}>Login</button>
      </form>
    </div>
  );
}
EOL

# Création du fichier App.js
cat > src/App.js <<EOL
import { useState } from 'react';
import Dashboard from './Dashboard';
import Login from './Login';

function App() {
  const [user,setUser] = useState(null);

  return user ? <Dashboard /> : <Login onLogin={data=>setUser(data)} />;
}

export default App;
EOL

echo "[*] Frontend React prêt dans ./$FRONTEND_DIR"
echo "[*] Pour lancer : cd $FRONTEND_DIR && npm start"
