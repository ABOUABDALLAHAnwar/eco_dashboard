#!/bin/bash

rm -r agentic_frontend
# Créer le projet si nécessaire
mkdir -p agentic_frontend
mkdir agentic_frontend/src

cd agentic_frontend


# Initialiser npm
npm init -y

# Installer React + Vite
npm install react react-dom
npm install -D vite

# Installer Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Créer index.css avec Tailwind
echo "@tailwind base;\n@tailwind components;\n@tailwind utilities;" > src/index.css

echo "Installation done. You can now run: npm run dev"
