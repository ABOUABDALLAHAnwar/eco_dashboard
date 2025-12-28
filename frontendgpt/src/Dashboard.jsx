import { useState, useEffect } from 'react';
import L from 'leaflet';
import Header from './components/Header';
import DashboardGrid from './components/DashboardGrid';
import { useActions } from './hooks/useActions';
import { openFormPopup } from './utils/openFormPopup';
import ContributionDonut from './components/ContributionDonut';

export default function Dashboard() {
  const { actions, fetchActions } = useActions();
  const [profile, setProfile] = useState({});
  const [coordinates, setCoordinates] = useState([0,0]);
  const [tco2e, setTco2e] = useState({ tco2e_total:0, monney:0 });
  const [contributions, setContributions] = useState({});
  const [badges, setBadges] = useState({ current_badge: null, next_badge: null, progress_percent: 0 });

  // Récupérations
  useEffect(() => { fetchActions(); }, []);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await fetch("http://localhost:8001/get_user_profile", { credentials: "include" });
        const data = await res.json();
        setProfile(data);
      } catch(err){ console.error(err); }
    };
    fetchProfile();
  }, []);

  useEffect(() => {
    const fetchCoordinates = async () => {
      try {
        const res = await fetch("http://localhost:8001/coordinates", { credentials: "include" });
        const data = await res.json();
        setCoordinates(data);
      } catch(err){ console.error(err); }
    };
    fetchCoordinates();
  }, []);

  useEffect(() => {
    const fetchTco2e = async () => {
      try {
        const res = await fetch("http://localhost:8001/tco2e_total", { credentials: "include" });
        const data = await res.json();
        setTco2e(data);
      } catch(err){ console.error(err); }
    };
    fetchTco2e();
  }, []);

  useEffect(() => {
    const fetchContributions = async () => {
      try {
        const res = await fetch("http://localhost:8001/tco2e_evite_contributions", { credentials: "include" });
        const data = await res.json();
        setContributions(data);
      } catch(err){ console.error(err); }
    };
    fetchContributions();
  }, []);

  useEffect(() => {
    const fetchBadges = async () => {
      try {
        const res = await fetch("http://localhost:8001/users_badges", { credentials: "include" });
        const data = await res.json();
        if(!data.next_badge) data.next_badge = data.current_badge;
        setBadges(data);
      } catch(err){ console.error(err); }
    };
    fetchBadges();
  }, []);

  const openActionPopup = async () => {
    try {
      const res = await fetch("http://localhost:8001/all_actions_names", { credentials: "include" });
      const actionsList = await res.json();

      openFormPopup(
        "Choisir Action",
        [{ name: "action", placeholder: "Sélectionnez l'action", type: "select", options: actionsList }],
        (values, popup) => {
          const selected = values.action;
          if(selected === "reduce_car_use_bicycle" || selected === "reduce_car_use_public_transport") {
            popup.close();
            openFormPopup(
              "Ajouter Action",
              [
                { name: "address_a", placeholder: "Adresse A", type: "text" },
                { name: "address_b", placeholder: "Adresse B", type: "text" },
                { name: "type", placeholder: "Type de voiture", type: "select", options: ["petite","moyenne","grande"] }
              ],
              async (values2, popup2) => {
                try {
                  const res2 = await fetch("http://localhost:8001/add_user_actions", {
                    method:"POST", credentials:"include",
                    headers:{"Content-Type":"application/json"},
                    body:JSON.stringify({name:selected, info:values2})
                  });
                  if(!res2.ok) throw new Error("Erreur ajout action");
                  popup2.close(); fetchActions();
                } catch { alert("Erreur réseau ou non authentifié"); }
              }
            );
          } else {
            alert("Action non développée");
          }
        }
      );
    } catch(err){ console.error(err); alert("Impossible de charger la liste des actions"); }
  };

  const openProfilePopup = () => openFormPopup(
    "Update Profile",
    [
      {name:"name",placeholder:"Nom"},
      {name:"position",placeholder:"Poste"},
      {name:"about",placeholder:"À propos"},
      {name:"age",placeholder:"Âge",type:"number"},
      {name:"country",placeholder:"Pays"},
      {name:"address",placeholder:"Adresse"},
      {name:"phone",placeholder:"Téléphone"}
    ],
    async (values,popup) => {
      try{
        const res = await fetch("http://localhost:8001/initialise_user_profiles", {
          method:"POST", credentials:'include', headers:{"Content-Type":"application/json"},
          body:JSON.stringify(values)
        });
        if(!res.ok) throw new Error("Erreur update profil");
        popup.close(); setProfile(values);
      } catch { alert("Erreur réseau ou non authentifié"); }
    },
    profile
  );

  const handleLogout = () => fetch("http://localhost:8001/logout",{method:"GET",credentials:"include"}).then(()=>window.location.reload()).catch(console.error);

  // Nouvelle fonction pour le bouton Onboarding
  const handleOnboarding = () => {
    alert("Fonctionnalité Onboarding en cours de développement ! 🚀");
    // Tu pourras remplacer ça par un vrai tour guidé, modal, etc.
  };

  // Carte
  useEffect(() => {
    if(!actions.length) return;
    const map = L.map('map',{center:[44.8695,-0.545],zoom:13,scrollWheelZoom:false});
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    actions.forEach(a=>{
      const color = a.impact_co2_kg < 1000 ? 'orange' : a.impact_co2_kg < 2000 ? 'yellowgreen' : 'green';
      L.circle([a.lat,a.lon],{color,fillColor:color,fillOpacity:0.7,radius:(a.impact_co2_kg||0)*5})
        .bindPopup(`${a.name}<br>${a.quartier}<br><strong>CO₂ évité:</strong> ${(a.impact_co2_kg/1000).toFixed(1)} t`).addTo(map);
    });
  },[actions]);

  return (
    <div className="min-h-screen bg-cover bg-center bg-fixed" style={{backgroundImage:"url('https://thumbs.dreamstime.com/b/misty-forest-scene-serene-green-nature-background-ideal-relaxation-documentaries-tones-soft-light-atmosphere-themes-376070078.jpg')"}}>
      <div className="absolute inset-0 bg-black/40"></div>
      <div className="relative z-10 flex flex-col min-h-screen">
        {/* Passage de la nouvelle fonction onboarding au Header */}
        <Header
          onAddAction={openActionPopup}
          onUpdateProfile={openProfilePopup}
          onLogout={handleLogout}
          onOnboarding={handleOnboarding}
        />
        <main className="flex-1 p-6">
          <DashboardGrid>
            {/* Carte */}
            <div id="map" className="card h-96 bg-white/90 backdrop-blur-sm shadow-xl"></div>

            {/* Profil, Badges et Bilan */}
            <div className="card bg-white/90 backdrop-blur-sm shadow-xl p-6 flex flex-col justify-between h-full">
              <div>
                {/* Profil Utilisateur */}
                <h2 className="text-4xl font-extrabold mb-6" style={{color:'olive'}}>Profil Utilisateur</h2>
                <p className="mb-1"><strong>Nom:</strong> {profile.name}</p>
                <p className="mb-1"><strong>Poste:</strong> {profile.position}</p>
                <p className="mb-1"><strong>À propos:</strong> {profile.about}</p>
                <p className="mb-1"><strong>Âge:</strong> {profile.age}</p>
                <p className="mb-1"><strong>Pays:</strong> {profile.country}</p>
                <p className="mb-1"><strong>Adresse:</strong> {profile.address}</p>
                <p className="mb-1"><strong>Téléphone:</strong> {profile.phone}</p>
                <p className="my-4"><strong>Coordonnées:</strong> {coordinates[0]}, {coordinates[1]}</p>

                {/* Badges - Côte à côte + texte en gras dessous */}
                <div className="my-8">
                  <table style={{ margin: "0 auto", borderCollapse: "separate", borderSpacing: "60px 0" }}>
                    <tbody>
                      <tr style={{ textAlign: "center" }}>
                        <td style={{ verticalAlign: "top" }}>
                          <div className="font-semibold mb-2">Badge actuel</div>
                          {badges.current_badge && (
                            <img
                              src={`http://localhost:8001${badges.current_badge.image}`}
                              alt={badges.current_badge.name}
                              style={{ width: "2.5cm", height: "2.5cm", objectFit: "contain" }}
                            />
                          )}
                        </td>
                        <td style={{ verticalAlign: "top" }}>
                          <div className="font-semibold mb-2">Prochain badge</div>
                          {badges.next_badge && (
                            <img
                              src={`http://localhost:8001${badges.next_badge.image}`}
                              alt={badges.next_badge.name}
                              style={{ width: "2.5cm", height: "2.5cm", objectFit: "contain" }}
                            />
                          )}
                        </td>
                      </tr>
                    </tbody>
                  </table>

                  <progress
                    className="w-full h-4 mt-6 block"
                    value={badges.progress_percent}
                    max={100}
                    style={{ accentColor: "olive" }}
                  />
                  <p className="text-center mt-4 font-bold text-lg">
                    {badges.progress_percent.toFixed(1)} % vers le prochain badge
                  </p>
                </div>

                {/* Bilan d'activité */}
                <h2 className="text-4xl font-extrabold mb-6" style={{color:'olive'}}>Bilan d'activité</h2>
                <p className="font-bold text-green-600 mb-4">CO₂ évité: {tco2e.tco2e_total.toFixed(1)} t</p>
                <p className="font-bold mb-4">Récompenses générées: {tco2e.monney.toFixed(2)} €</p>

                {/* Donut des contributions */}
                <div className="flex justify-center mb-6">
                  <ContributionDonut data={contributions} />
                </div>
              </div>

              {/* Citation */}
              <div className="mt-auto">
                <p className="font-bold text-2xl" style={{color:'olive'}}>
                  "Chaque tonne de CO₂ évitée est un pas concret vers un climat plus stable, une biodiversité préservée et un futur où la planète peut respirer. Réduire nos émissions, c’est investir dans la santé et la survie de la Terre."
                  Dr Anwar ABOUABDALLAH, CEO
                </p>
              </div>
            </div>
          </DashboardGrid>
        </main>
      </div>
    </div>
  );
}