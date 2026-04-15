FROM node:22-alpine
WORKDIR /app

# Копируем только package.json для установки зависимостей
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем остальные файлы (но они будут перезаписаны volume)
COPY . .

# Запускаем dev сервер
CMD ["npm", "run", "dev", "--", "--host"]