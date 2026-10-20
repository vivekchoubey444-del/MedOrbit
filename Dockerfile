FROM node:20-alpine
ENV NODE_ENV=production
WORKDIR /app
COPY package.json ./
COPY index.html ./
COPY assets ./assets
COPY auth ./auth
COPY education ./education
COPY career ./career
COPY pages ./pages
COPY backend ./backend
COPY config ./config
EXPOSE 3000
USER node
CMD ["node","backend/server.js"]
