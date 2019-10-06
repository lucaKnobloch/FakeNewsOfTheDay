# FakeNewsTrackerOfTheDay

The FakeNewsTracker will used crawled classified data to extract their main message and visualize them.

## Install

build 3 Docker container

    1. Container
        go to the directory
            ./BackEnd/Classifier
        run the command 
            docker build . -t classifier:latest

        -> build a local docker container which is able to load data from ElasticSearch - Classifiy - NER - push data back 

    2. Container
        go to the directory flaskServer
            ./BackEnd/flaskServer
        run the command
            docker build . -t flask-server:latest

        -> build a local docker container which connects the backend with the frontend 
    
    3. Container
        go to the directory FrontEnd
            ./FrontEnd
        run the command
            docker build . -f Dockerfile-prod -t front-end:prod
        
        -> build a local docker container which enables to visualuze the frontend

    After building these 3 Containers you can run the docker-compose file in the root directory 
        docker-compose up 
