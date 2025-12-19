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
        .bindPopup(`${a.name}<br>${a.quartier}<br>CO₂ évité: ${(a.impact_co2_kg/1000).toFixed(1)} t`).addTo(map);
    });

    // Stats CO2
    const totalCO2 = actions.reduce((sum,a)=>sum+a.impact_co2_kg,0);
    document.getElementById('total-co2').innerText = (totalCO2/1000).toFixed(1) + ' TONNES';
    document.getElementById('co2-bar-inner').style.width = Math.min(totalCO2/5000*100,100) + '%';
    const typesCO2 = {};
    actions.forEach(a=>typesCO2[a.type]=(typesCO2[a.type]||0)+a.impact_co2_kg);
    document.getElementById('co2-details').innerHTML = Object.entries(typesCO2).map(([t,v])=>`<div>${t}: ${(v/1000).toFixed(1)} t</div>`).join('');

    // Graphique évolution (mock)
    const evolution = { months:["Jan","Fév","Mar","Avr","Mai"], values:[0,2,0,12,5] };
    Plotly.newPlot('evolution-chart',[{x:evolution.months, y:evolution.values, type:'scatter', mode:'lines+markers', line:{color:'#4a6c59'}}],{margin:{t:30,b:30,l:30,r:30}});

    // Top quartiers
    const quartiers={};
    actions.forEach(a=>quartiers[a.quartier]=(quartiers[a.quartier]||0)+1);
    const top3 = Object.entries(quartiers).sort((a,b)=>b[1]-a[1]).slice(0,3);
    document.getElementById('top-quartiers').innerHTML = top3.map(([q,val],i)=>`<tr><td>${i+1} ${q}</td><td>${val}</td></tr>`).join('');

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
