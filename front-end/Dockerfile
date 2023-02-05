FROM node:latest as build-stage
WORKDIR /app
COPY package*.json ./
# builds all the necessary dependecies
RUN npm install
COPY ./ .
# builds the dist folder which can be deployed
RUN npm run build

FROM nginx:1.23 as production-stage
RUN mkdir /app
# copies the dist folder of the upper process into the app folder
COPY --from=build-stage /app/dist /app/
# uses the nginx conf to deploy the services
COPY nginx.conf /etc/nginx/nginx.conf