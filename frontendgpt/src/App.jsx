import React, { useEffect, useState } from "react";
import Header from "./components/Header";
import DashboardGrid from "./components/DashboardGrid";
import { getAllActions } from "./services/api";
import L from "leaflet";
import Plotly from "plotly.js-dist";
import "./App.css";

function App() {
  const [actions, setActions] = useState([]);

  useEffect(() => {
    const fetchActions = async () => {
      const data = await getAllActions();
      setActions(data);
      initMap(data);
      initChart(data);
    };
    fetchActions();
  }, []);

  const initMap = (actions) => {
    const map = L.map("map").setView([44.8695, -0.545], 13);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);
  };

  const initChart = (actions) => {
    Plotly.newPlot("evolution-chart", [{
      x: ["Type1","Type2"],
      y: [1,2],
      type:"bar"
    }]);
  };

  return (
    <div>
      <Header />
      <DashboardGrid>
        <div id="map" style={{ height:"400px", background:"#ddd" }}>Carte ici</div>
        <div>Stats CO2 ici</div>
        <div id="evolution-chart" style={{ height:"300px" }}>Graphiques ici</div>
        <div>Top quartiers ici</div>
      </DashboardGrid>
    </div>
  );
}

export default App;
