# Feed data manually

The idea to feed data manually into elastic search can be provided. This branch contains data from over 100 crawled days.

## Copy json-files into docker container

Each of the json files contains urls of the articles. Each json file needs to be scrapped in combination with the news-crawler docker container provided by the UHH-LT.
The recommended version is to use the docker container and copy the json file into the docker container. This can be done with the following command:

`docker cp <filelocation> <containerName>:/app/out/feeds/english`

filelocation needs to be replaced with the location of the json file and the containerName needs to replaced with the Name of the current docker container of the news-crawler.

## Scrape the articles into elasticsearch

After the new json file is within the docker container the data needs to be scraped into elastic search. Therefor a running instance of elastic search needs to be active. The following command will use all the URLs which are located in the specified .json file and will download the Html file of the article. Furthermore, it feeds the content into elastic search with the index of news-english. This command needs to be executed within the docker container.
`news-crawler scrape /app/out/feeds/english/<date>.json --lang english`
The parameter <date> needs to be replaced with the json file name which should be fed into elastic search.

## Classify the data

When the articles are stored in elasticsearch, the classification needs to be done. The classification can be done with the provided docker container. <https://cloud.docker.com/repository/docker/buecherwurm/fakenod-back>
The image needs to be running addional to the elasticsearch instance.
The steps which need to be performed are described in section Classifier [here](./docs/TechnologGuide.md).
Warning the loadFromElastic.py file will load only the files from yesterday. This paramter needs to be adjusted.

