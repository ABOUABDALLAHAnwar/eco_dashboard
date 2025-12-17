from frontend_agent import FrontendAgent
from pathlib import Path
import json

# Dossier où générer le front
FRONTEND_DIR = Path("../agentic_frontend/src")
FRONTEND_DIR.mkdir(parents=True, exist_ok=True)

# Initialiser l'agent
agent = FrontendAgent(prompt_file='prompts/frontend_prompt.json')

# Composants à générer
user_stories = {
    "Header.js": "Create a responsive header with the app name and navigation links.",
    "CarbonCard.js": "Display a dashboard card showing user's carbon footprint reduction with a progress bar.",
    "ActionList.js": "Display a list of eco-friendly actions completed by the user with icons.",
    "NeighborComparison.js": "Show a chart comparing user's CO2 reduction with neighbors or city average.",
    "Footer.js": "Create a responsive footer with contact info and social media links."
}

# Générer tous les composants
for file_name, story in user_stories.items():
    agent.generate_component(story, FRONTEND_DIR / file_name)
    print(f"{file_name} generated.")

# Générer App.js
app_js = """import React from 'react';
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
"""
with open(FRONTEND_DIR / "App.js", 'w', encoding='utf-8') as f:
    f.write(app_js)

# Générer index.js (CRA entrypoint)
index_js = """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
"""
with open(FRONTEND_DIR / "index.js", 'w', encoding='utf-8') as f:
    f.write(index_js)

print("Front-end generated successfully in agentic_frontend/src")
