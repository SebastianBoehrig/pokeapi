FROM node:24-alpine AS build

WORKDIR /app

COPY . .
RUN npm install
RUN npm run build

FROM node:20-alpine AS prod

WORKDIR /app
COPY --from=build /app/build ./build
COPY --from=build /app/package.json .

RUN npm install --omit=dev

COPY ./static ./static

EXPOSE 3000

CMD [ "node", "build/index.js" ]
# npm run install
# docker run -d -p 8080:3000 frontend