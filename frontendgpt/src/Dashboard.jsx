import { useState, useEffect } from 'react';
import L from 'leaflet';
import Header from './components/Header';
import DashboardGrid from './components/DashboardGrid';
import { useActions } from './hooks/useActions';
import { openFormPopup } from './utils/openFormPopup';

export default function Dashboard() {
  const { actions, fetchActions } = useActions();
  const [profile, setProfile] = useState({
    name:'', position:'', about:'', age:'', country:'', address:'', phone:''
  });

  useEffect(() => { fetchActions(); }, []);

  const openActionPopup = async () => {
    try {
      const res = await fetch("http://localhost:8001/all_actions_names", { credentials: "include" });
      const actionsList = await res.json();

      openFormPopup(
        "Choisir Action",
        [{ name: "action", placeholder: "Sélectionnez l'action", type: "select", options: actionsList }],
        (values, popup) => {
          const selected = values.action;

          if (selected === "reduce_car_use_bicycle") {
            popup.close();

            openFormPopup(
              "Ajouter Action",
              [
                { name: "distance", placeholder: "Distance", type: "number" },
                { name: "type", placeholder: "Type de voiture", type: "select", options: ["petite","moyenne","grande"] }
              ],
              async (values2, popup2) => {
                try {
                  const res2 = await fetch("http://localhost:8001/add_user_actions", {
                    method: "POST",
                    credentials: "include",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ name: selected, info: { distance: Number(values2.distance), type: values2.type } })
                  });
                  if (!res2.ok) throw new Error("Erreur ajout action");
                  popup2.close();
                  fetchActions();
                } catch {
                  alert("Erreur réseau ou non authentifié");
                }
              }
            );
          } else {
            alert("Action non développée");
          }
        }
      );
    } catch (err) {
      console.error(err);
      alert("Impossible de charger la liste des actions");
    }
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
      {name:"phone",placeholder:"Téléphone"},
    ],
    async (values,popup)=>{
      try{
        const res = await fetch("http://localhost:8001/initialise_user_profiles", {
          method:"POST", credentials:'include', headers:{"Content-Type":"application/json"},
          body:JSON.stringify(values)
        });
        if(!res.ok) throw new Error("Erreur update profil");
        popup.close(); setProfile(values);
      }catch{ alert("Erreur réseau ou non authentifié"); }
    },
    profile
  );

  const handleLogout = () => fetch("http://localhost:8001/logout",{method:"GET",credentials:"include"}).then(()=>window.location.reload()).catch(console.error);

  useEffect(() => {
    if(!actions.length) return;
    const map = L.map('map',{center:[44.8695,-0.545],zoom:13,scrollWheelZoom:false});
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    actions.forEach(a=>{
      const color=a.impact_co2_kg<1000?'orange':a.impact_co2_kg<2000?'yellowgreen':'green';
      L.circle([a.lat,a.lon],{color,fillColor:color,fillOpacity:0.7,radius:(a.impact_co2_kg||0)*5})
          .bindPopup(`${a.name}<br>${a.quartier}<br><strong>CO\u2082 évité:</strong> ${(a.impact_co2_kg/1000).toFixed(1)} t`).addTo(map);
    });
    const totalCO2 = actions.reduce((s,a)=>s+(a.impact_co2_kg||0),0);
    const totalEl = document.getElementById('total-co2');
    const barEl = document.getElementById('co2-bar-inner');
    if(totalEl) totalEl.innerText=(totalCO2/1000).toFixed(1)+' TONNES';
    if(barEl) barEl.style.width=Math.min((totalCO2/5000)*100,100)+'%';
  },[actions]);

  return (
    <div className="min-h-screen bg-cover bg-center bg-fixed" style={{backgroundImage:"url('https://thumbs.dreamstime.com/b/misty-forest-scene-serene-green-nature-background-ideal-relaxation-documentaries-tones-soft-light-atmosphere-themes-376070078.jpg')"}}>
      <div className="absolute inset-0 bg-black/40"></div>
      <div className="relative z-10 flex flex-col min-h-screen">
        <Header onAddAction={openActionPopup} onUpdateProfile={openProfilePopup} onLogout={handleLogout} />
        <main className="flex-1 p-6">
          <DashboardGrid>
            <div className="card h-96 bg-white/90 backdrop-blur-sm shadow-xl" id="map"></div>
            <div className="card bg-white/90 backdrop-blur-sm shadow-xl">
              <h3 className="text-xl font-semibold text-gray-800 mb-4">Total CO₂ évité</h3>
              <div id="total-co2" className="text-4xl font-bold text-green-700">0 TONNES</div>
              <div className="mt-6 bg-gray-200 rounded-full h-8 overflow-hidden">
                <div id="co2-bar-inner" className="h-full bg-gradient-to-r from-yellow-500 to-green-600 transition-all duration-1000" style={{width:'0%'}}></div>
              </div>
            </div>
          </DashboardGrid>
        </main>
      </div>
    </div>
  );
}
