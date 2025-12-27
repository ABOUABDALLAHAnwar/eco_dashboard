#!/bin/bash
set -e

echo "📁 Création des dossiers"
mkdir -p src/components src/hooks src/utils

#################################
# Header.jsx
#################################
cat > src/components/Header.jsx << 'EOF'
export default function Header({ onAddAction, onUpdateProfile, onLogout }) {
  return (
    <header className="flex justify-between items-center p-4 bg-gray-900/80 backdrop-blur-sm text-white rounded-b-lg shadow-lg">
      <h1 className="text-2xl font-bold">Dashboard Éco</h1>
      <div className="flex gap-3">
        <button onClick={onAddAction} className="px-5 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg">
          Ajouter Action
        </button>
        <button onClick={onUpdateProfile} className="px-5 py-2 bg-green-600 hover:bg-green-700 rounded-lg">
          Update Profile
        </button>
        <button onClick={onLogout} className="px-5 py-2 bg-red-600 hover:bg-red-700 rounded-lg">
          Logout
        </button>
      </div>
    </header>
  );
}
EOF

#################################
# useActions.js
#################################
cat > src/hooks/useActions.js << 'EOF'
import { useEffect, useState } from "react";

export function useActions() {
  const [actions, setActions] = useState([]);

  const fetchActions = async () => {
    try {
      const res = await fetch("http://localhost:8001/all_actions_templates", {
        credentials: "include",
      });
      if (!res.ok) {
        setActions([]);
        return;
      }
      const data = await res.json();
      setActions(Array.isArray(data) ? data : []);
    } catch {
      setActions([]);
    }
  };

  useEffect(() => {
    fetchActions();
  }, []);

  return { actions, fetchActions };
}
EOF

#################################
# CO2Map.jsx
#################################
cat > src/components/CO2Map.jsx << 'EOF'
import { useEffect } from "react";
import L from "leaflet";

export default function CO2Map({ actions }) {
  useEffect(() => {
    if (!actions.length) return;

    const map = L.map("map", {
      center: [44.8695, -0.545],
      zoom: 13,
      scrollWheelZoom: false,
    });

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);

    actions.forEach((a) => {
      const color =
        a.impact_co2_kg < 1000 ? "orange" :
        a.impact_co2_kg < 2000 ? "yellowgreen" : "green";

      L.circle([a.lat, a.lon], {
        color,
        fillColor: color,
        fillOpacity: 0.7,
        radius: (a.impact_co2_kg || 0) * 5,
      }).addTo(map);
    });

    return () => map.remove();
  }, [actions]);

  return <div id="map" className="card h-96 bg-white/90 shadow-xl" />;
}
EOF

#################################
# CO2Stats.jsx
#################################
cat > src/components/CO2Stats.jsx << 'EOF'
export default function CO2Stats({ actions }) {
  const totalCO2 = actions.reduce((sum, a) => sum + (a.impact_co2_kg || 0), 0);
  const percent = Math.min((totalCO2 / 5000) * 100, 100);

  return (
    <div className="card bg-white/90 backdrop-blur-sm shadow-xl">
      <h3 className="text-xl font-semibold text-gray-800 mb-4">
        Total CO₂ évité
      </h3>
      <div className="text-4xl font-bold text-green-700">
        {(totalCO2 / 1000).toFixed(1)} TONNES
      </div>
      <div className="mt-6 bg-gray-200 rounded-full h-8 overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-yellow-500 to-green-600"
          style={{ width: percent + "%" }}
        />
      </div>
    </div>
  );
}
EOF

#################################
# openFormPopup.js
#################################
cat > src/utils/openFormPopup.js << 'EOF'
export function openFormPopup(title, fields, onSubmit, initialValues = {}) {
  const width = 420;
  const height = 500;
  const left = window.innerWidth / 2 - width / 2;
  const top = window.innerHeight / 2 - height / 2;

  const popup = window.open("", title, `width=${width},height=${height},top=${top},left=${left}`);
  if (!popup) {
    alert("Autorise les pop-ups pour ce site");
    return;
  }

  popup.document.write(`
    <h3>${title}</h3>
    <form id="popupForm">
      ${fields.map(f => `
        <input name="${f.name}" placeholder="${f.placeholder}" value="${initialValues[f.name] || ''}" />
      `).join("")}
      <button type="submit">Envoyer</button>
    </form>
  `);

  popup.document.getElementById("popupForm").onsubmit = (e) => {
    e.preventDefault();
    const values = {};
    fields.forEach(f => values[f.name] = popup.document.forms[0][f.name].value);
    onSubmit(values, popup);
  };
}
EOF

echo "✅ Découpage terminé"
