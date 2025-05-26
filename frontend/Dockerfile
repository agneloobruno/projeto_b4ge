FROM node:18

WORKDIR /app

COPY package*.json ./

# Instala dependências para plataforma Linux
RUN npm install --platform=linux --force

# Rebuild necessário para pacotes nativos como lightningcss
RUN npm rebuild

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
