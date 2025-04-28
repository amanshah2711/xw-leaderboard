
FROM node:23.6.1-slim

WORKDIR /app

COPY package.json vite.config.js ./

RUN yarn install 

COPY . .

EXPOSE 5173

CMD [ "yarn", "build" ]

