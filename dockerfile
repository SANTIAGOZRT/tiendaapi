#1. imagen base 
FROM node:18-alpine

#2. crear directorio de la app
WORKDIR /app

#3. copiar package.json y package-lock.json
COPY package*.json ./
RUN npm install

#4. copiar el resto de la app
COPY . .

#5. exponer el puerto
EXPOSE 3000

#6. comando para correr la app
CMD ["node", "index.js"]