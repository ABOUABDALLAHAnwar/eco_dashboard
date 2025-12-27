import { useEffect, useState } from 'react';
import L from 'leaflet';
import DashboardGrid from './components/DashboardGrid';

// Header avec boutons
function Header({ onAddAction, onUpdateProfile, onLogout }) {
  return (
    <header className="flex justify-between items-center p-4 bg-gray-900/80 backdrop-blur-sm text-white rounded-b-lg shadow-lg">
      <h1 className="text-2xl font-bold">Dashboard Éco</h1>
      <div className="flex gap-3">
        <button
          onClick={onAddAction}
          className="px-5 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition"
        >
          Ajouter Action
        </button>
        <button
          onClick={onUpdateProfile}
          className="px-5 py-2 bg-green-600 hover:bg-green-700 rounded-lg transition"
        >
          Update Profile
        </button>
        <button
          onClick={onLogout}
          className="px-5 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition"
        >
          Logout
        </button>
      </div>
    </header>
  );
}

export default function Dashboard() {
  const [actions, setActions] = useState([]);
  const [profile, setProfile] = useState({
    name: '',
    position: '',
    about: '',
    age: '',
    country: '',
    address: '',
    phone: '',
  });

  const openActionPopup = () =>
    openFormPopup(
      "Ajouter Action",
      [
        { name: "name", placeholder: "Nom action" },
        { name: "distance", placeholder: "Distance", type: "number" },
        { name: "type", placeholder: "Type" },
      ],
      async (formValues, popupWindow) => {
        try {
          const response = await fetch("http://localhost:8001/add_user_actions", {
            method: "POST",
            credentials: 'include', // Envoie les cookies de session
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              name: formValues.name,
              info: {
                distance: Number(formValues.distance),
                type: formValues.type,
              },
            }),
          });

          if (!response.ok) {
            console.error("Erreur lors de l'ajout de l'action :", response.status);
            alert("Erreur : impossible d'ajouter l'action (non authentifié ?)");
            return;
          }

          popupWindow.close();
          fetchActions(); // Rafraîchir la liste
        } catch (err) {
          console.error("Erreur réseau :", err);
          alert("Erreur de connexion au serveur");
        }
      }
    );


  const openProfilePopup = () =>
    openFormPopup(
      "Update Profile",
      [
        { name: "name", placeholder: "Nom" },
        { name: "position", placeholder: "Poste" },
        { name: "about", placeholder: "À propos" },
        { name: "age", placeholder: "Âge", type: "number" },
        { name: "country", placeholder: "Pays" },
        { name: "address", placeholder: "Adresse" },
        { name: "phone", placeholder: "Téléphone" },
      ],
      async (formValues, popupWindow) => {
        try {
          const response = await fetch("http://localhost:8001/initialise_user_profiles", {
            method: "POST",
            credentials: 'include', // Très important
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(formValues),
          });

          if (!response.ok) {
            console.error("Erreur lors de la mise à jour du profil :", response.status);
            alert("Erreur : impossible de mettre à jour le profil");
            return;
          }

          popupWindow.close();
        } catch (err) {
          console.error("Erreur réseau :", err);
          alert("Erreur de connexion au serveur");
        }
      },
      profile
    );

  // Fonction générique pour pop-up formulaire (inchangée, juste un peu plus stylée)
  const openFormPopup = (title, fields, onSubmit, initialValues = {}) => {
    const width = 420;
    const height = 500;
    const left = window.innerWidth / 2 - width / 2;
    const top = window.innerHeight / 2 - height / 2;

    const newWindow = window.open(
      "",
      title,
      `width=${width},height=${height},top=${top},left=${left}`
    );

    if (!newWindow) {
      alert("Autorise les pop-ups pour ce site !");
      return;
    }

    newWindow.document.write(`
      <style>
        body { font-family: Arial, sans-serif; padding: 20px; background: #f9fafb; }
        h3 { margin-bottom: 20px; text-align: center; color: #1f2937; }
        form { display: flex; flex-direction: column; gap: 12px; }
        input { padding: 10px; border: 1px solid #ccc; border-radius: 6px; font-size: 14px; }
        .buttons { display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px; }
        button { padding: 10px 20px; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; }
        #cancelBtn { background: #e5e7eb; color: #374151; }
        #cancelBtn:hover { background: #d1d5db; }
        button[type="submit"] { background: #10b981; color: white; }
        button[type="submit"]:hover { background: #059669; }
      </style>
      <h3>${title}</h3>
      <form id="popupForm">
        ${fields
          .map(
            (f) => `
          <input
            name="${f.name}"
            placeholder="${f.placeholder}"
            type="${f.type || 'text'}"
            value="${initialValues[f.name] || ''}"
          />`
          )
          .join('')}
        <div class="buttons">
          <button type="button" id="cancelBtn">Annuler</button>
          <button type="submit">Envoyer</button>
        </div>
      </form>
    `);

    const form = newWindow.document.getElementById("popupForm");
    const cancelBtn = newWindow.document.getElementById("cancelBtn");

    cancelBtn.addEventListener("click", () => newWindow.close());

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const formValues = {};
      fields.forEach((f) => {
        formValues[f.name] = form[f.name].value;
      });
      onSubmit(formValues, newWindow);
    });
  };

  const handleLogout = () => {
    fetch("http://localhost:8001/logout", {
      method: "GET",
      credentials: "include"
    })
      .then(() => window.location.reload())
      .catch((err) => console.error("Erreur logout :", err));
  };

  const fetchActions = async () => {
    try {
      const response = await fetch('http://localhost:8001/all_actions_templates', {
        credentials: 'include', // Indispensable
      });

      if (!response.ok) {
        console.error("Erreur fetch actions :", response.status);
        setActions([]);
        return;
      }

      const data = await response.json();
      setActions(Array.isArray(data) ? data : []);
    } catch (e) {
      console.error("Erreur réseau lors du fetch des actions :", e);
      setActions([]);
    }
  };

  useEffect(() => {
    fetchActions();
  }, []);

  useEffect(() => {
    if (!Array.isArray(actions) || actions.length === 0) return;

    const map = L.map('map').setView([44.8695, -0.545], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

    actions.forEach((a) => {
      const color =
        a.impact_co2_kg < 1000
          ? 'orange'
          : a.impact_co2_kg < 2000
          ? 'yellowgreen'
          : 'green';

      L.circle([a.lat, a.lon], {
        color,
        fillColor: color,
        fillOpacity: 0.7,
        radius: a.impact_co2_kg * 5,
      })
        .bindPopup(
          `${a.name}<br>${a.quartier}<br><strong>CO₂ évité :</strong> ${(a.impact_co2_kg / 1000).toFixed(1)} tonnes`
        )
        .addTo(map);
    });

    const totalCO2 = actions.reduce((sum, a) => sum + (a.impact_co2_kg || 0), 0);
    const totalElement = document.getElementById('total-co2');
    const barInner = document.getElementById('co2-bar-inner');

    if (totalElement) {
      totalElement.innerText = (totalCO2 / 1000).toFixed(1) + ' TONNES';
    }
    if (barInner) {
      barInner.style.width = Math.min((totalCO2 / 5000) * 100, 100) + '%';
    }
  }, [actions]);

  return (
    <div
      className="min-h-screen bg-cover bg-center bg-fixed"
      style={{
        backgroundImage:
          "url('https://thumbs.dreamstime.com/b/misty-forest-scene-serene-green-nature-background-ideal-relaxation-documentaries-tones-soft-light-atmosphere-themes-376070078.jpg')",
      }}
    >
      <div className="absolute inset-0 bg-black/40"></div>

      <div className="relative z-10 flex flex-col min-h-screen">
        <Header
          onAddAction={openActionPopup}
          onUpdateProfile={openProfilePopup}
          onLogout={handleLogout}
        />

        <main className="flex-1 p-6">
          <DashboardGrid>
            <div className="card h-96 bg-white/90 backdrop-blur-sm shadow-xl" id="map"></div>

            <div className="card bg-white/90 backdrop-blur-sm shadow-xl">
              <h3 className="text-xl font-semibold text-gray-800 mb-4">
                Total CO₂ évité
              </h3>
              <div id="total-co2" className="text-4xl font-bold text-green-700">
                0 TONNES
              </div>
              <div className="mt-6 bg-gray-200 rounded-full h-8 overflow-hidden">
                <div
                  id="co2-bar-inner"
                  className="h-full bg-gradient-to-r from-yellow-500 to-green-600 transition-all duration-1000"
                  style={{ width: '0%' }}
                ></div>
              </div>
            </div>
          </DashboardGrid>
        </main>
      </div>
    </div>
  );
}