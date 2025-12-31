FROM node:20-alpine

WORKDIR /app

# On précise bien qu'on cherche les fichiers DANS le dossier frontend/
COPY frontend/package*.json ./
RUN npm install

# On copie tout le contenu du dossier frontend vers le dossier de travail /app
COPY frontend/ .

EXPOSE 3000

# Pour éviter que Docker ne se coupe tout seul en mode dev
ENV CI=true
ENV WDS_SOCKET_PORT=0

CMD ["npm", "start"]