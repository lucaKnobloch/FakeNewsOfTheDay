# FakeNewsTrackerOfTheDay

The FakeNewsTracker will used crawled classified data to extract their main message and visualize them.

Further information can be find here: [Documentation of this project](./docs/UserGuide.md) or here
<https://lucaknobloch.github.io/FakeNewsOfTheDay/>

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

**The containers of fakenod are locally buildable and the following steps explain how**

1. Container fakenod-back
    - go to the directory Classifier

        `./back-end/Classifier`

    - run the command

        `docker build . -t fakenod-back:latest`

    -> builded the container fakenod-back
        - further information are located here

2. Container Connection Server
    - go to the directory flaskServer

        `./back-end/flaskServer`
    - run the command

        `docker build . -t fakenod-con:latest`

    -> builded the container fakenod-con
        -   further information are located here

3. Container fakenod-front
    - go to the directory FrontEnd

        `./front-end`
    - run the command

        `docker build . -t fakenod-front:latest`

    -> builded the container fakenod-front
        - further information are located here

    After building these 3 containers they are usable with a docker-compose command in the root directory

    `docker-compose-local up`

### Further pulled containers

Either if the pulled containers or the local containers are used the docker-compose file will pull the following containers:

4. Container News scrawler

    The container is pulled from uhhlt/newscrawler dockerhub.
    In general it feeds on a daily basis news articles and scrape them into elasticSearch.
    In this context english articles are hourly feeded and once a day scraped which contain the whole article. Those information will be stored in Elasticsearch.

    Further information can be find on the origin project: <https://github.com/uhh-lt/news-crawler>

5. Container ElasticSearch

   The 5. container is pulled from elasticsearch:7.1.0 from the dockerhub. It is used to for storage and for search within the data.

6. Container Kibana

    The 6. container is pulled from kibana:7.1.0 from the dockerhub. It is used for development purposes and simplifices to get insight over the data in elasticsearch.

An example picture of the working front-end

![Overview](./docs/pictures/Overview.png)

Some ideas for further improvements are already open in the issue section. Further ideas are cordially
 welcome!

* <https://github.com/lucaKnobloch/FakeNewsOfTheDay/issues/1>
* <https://github.com/lucaKnobloch/FakeNewsOfTheDay/issues/2>
* <https://github.com/lucaKnobloch/FakeNewsOfTheDay/issues/3>
