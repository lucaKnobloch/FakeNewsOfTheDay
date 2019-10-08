# Front-end

The front-end is developed with VueJs and connects via Flask-server to the backend. REST-Calls are used.
The front-end can also be started in developmet mode. For easier front-end purposes the docker-compose can be configured to be started without the front-end. In that case the front-end is supposed to be installed and run locally.

## Install the dependencies 
```
npm install
```

## Compiles and runs the application 
```
npm run serve
```


### Compiles and minifies for production
```
npm run build
```
The build process creates a dist folder which will be used to deploy within the docker container.

