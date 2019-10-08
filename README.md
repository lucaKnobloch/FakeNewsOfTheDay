# FakeNewsTrackerOfTheDay

The FakeNewsTracker will used crawled classified data to extract their main message and visualize them.

## Docker Compose

1. `git clone https://github.com/lucaKnobloch/FakeNewsOfTheDay.git`
2. `cd FakeNewsOfTheDay`
3. `docker-compose up`
4. `open localhost:8080`

This will pull and run 6 containers:

- Elasticsearch
- Kibana
- News-Crawler
- fakenod-back
- fakenod-front
- fakenod-con

## Build Docker locally

### The containers of fakenod can be build locally. The following steps explain how

1. Container fakenod-back
    - go to the directory Classifier
        `./BackEnd/Classifier`
    - run the command
        `docker build . -t fakenod-back:latest`

    -> builded the container fakenod-back
        - further information are located here

2. Container Connection Server
    - go to the directory flaskServer
        `./BackEnd/flaskServer`
    - run the command
        `docker build . -t fakenod-con:latest`

    -> builded the container fakenod-con
        -   further information are located here

3. Container fakenod-front
    - go to the directory FrontEnd
        `./FrontEnd`
    - run the command
        `docker build . -t fakenod-front:latest`

    -> builded the container fakenod-front
        - further information are located here

    After building these 3 containers they are usable with a docker-compose command in the root directory
        `docker-compose-local up`

### Furhter pulled containers

    Either if the pulled containers or the local containers are used the docker-compose file will pull the following containers:

4. Container News scrawler
    is pulled from uhhlt/newscrawler
    in general it feeds on a daily basis news articles which are customizable. 
    in this application english articles are feeded and once a day scraped with the whole article stored into elasticsearch
    further information can be find on the origin project:
    https://github.com/uhh-lt/news-crawler

5. Container ElasticSearch
    is pulled from elasticsearch:7.1.0
    is used for storage and search for the data

6. Container Kibana
    for develop purposes in combination with elasticsearch
