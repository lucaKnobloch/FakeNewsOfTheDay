# FakeNewsTrackerOfTheDay

The Fake News Tracker Of The day crawls, classifies, abstract and visualizes the data.

Further documentation is located here: [Documentation of this project](./docs/UserGuide.md) or is provided in that online resource. <https://lucaknobloch.github.io/FakeNewsOfTheDay/>

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

    -> built the container fakenod-back
        - further information are located here [Technologie Guide](./docs/TechnologieGuide.md)

    The docker image for this is located here [DockerHub -  Back](https://cloud.docker.com/repository/docker/buecherwurm/fakenod-back)

2. Container Connection Server
    - go to the directory flaskServer

        `./back-end/flaskServer`
    - run the command

        `docker build . -t fakenod-con:latest`

    -> built the container fakenod-con
        -   further information are located here [Technologie Guide](./docs/TechnologieGuide.md)

    The docker image for this is located here [DockerHub - Con](https://cloud.docker.com/repository/docker/buecherwurm/fakenod-con)

3. Container fakenod-front
    - go to the directory FrontEnd

        `./front-end`
    - run the command

        `docker build . -t fakenod-front:latest`

    -> built the container fakenod-front
        - further information are located here [Technologie Guide](./docs/TechnologieGuide.md)

    The docker image for this is located here [DockerHub - Front](https://cloud.docker.com/repository/docker/buecherwurm/fakenod-front)

    After building these 3 containers locally they are usable with a docker-compose command in the root directory.

    `docker-compose-local up`

### Further pulled containers

Either of the docker-compose file will pull the following containers: 

4. Container News scrawler

    The container is pulled from uhhlt/newscrawler [dockerhub](https://hub.docker.com/r/uhhlt/newscrawler).

    In general, it feeds daily news articles and scrapes them into elastic search.
    In the context of the FakeNews project, the English articles are hourly fed and once a day scraped which contain the whole article into elastic search as save it on local storage.

    Further information can be found on the origin project: <https://github.com/uhh-lt/news-crawler>

5. Container ElasticSearch

   The 5. container is pulled from elastic search:7.1.0 from the docker hub. It is used for storage and searches within the data.

6. Container Kibana

    The 6. container is pulled from kibana:7.1.0 from the docker hub. It is used for development purposes and simplifies to get insight over the data in elastic search.

A second branch called "providedData" provides additional crawled data, which can be fed in elastic search.

An example screenshot of the working front-end with successfully complete the pipeline.

![Overview](./docs/pictures/Overview.png)

Some ideas for further improvements are already open in the issue section. Further ideas are cordially welcome!

* <https://github.com/lucaKnobloch/FakeNewsOfTheDay/issues/1>
* <https://github.com/lucaKnobloch/FakeNewsOfTheDay/issues/2>
* <https://github.com/lucaKnobloch/FakeNewsOfTheDay/issues/3>
