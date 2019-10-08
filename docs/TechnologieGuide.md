# Technologies

The introduces tools can also be used locally but come with additional dependencies so it is not recommended.

But still within the docker-containers can be looked and trigger processes manually.

## ElasticSearch

Elasticsearch enables the user to index documents easily and fast. Besides, elastic search is one of the most used technologies for searching within the data storage.
The running elastic search instance will have two indices. Once the indices created by the scraper who feeds the articles once a day which is called news-english. At the same time when there are failures at the process of scrapping another index is created with all the failed articles.
The first main index - mapping is looking like this:
`{
  "news-english" : {
    "mappings" : {
      "properties" : {
        "content" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "guid" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "published" : {
          "type" : "date"
        },
        "title" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "url" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        }
      }
    }
  }
}`
In case a user has articles which are in this format it can be added to the index. Afterwards the pipeline can be triggered manually to get the further information to get the second mapping. The tool can extract the information out of this base of information.

The second main index is created after the classification. The mapping gets added by occurrence, label, entities, and date.
{
  "labeled-news-english" : {
    "mappings" : {
      "properties" : {
        "date" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "entities" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "label" : {
          "type" : "boolean"
        },
        "occurance" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "published" : {
          "type" : "date"
        },
        "text" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "title" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "url" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        }
      }
    }
  }
}

In case a user wants to add own articles into the elastic search storage the mapping from above needs to apply.

## Flask

Flask is used as a connection server between the API calls of the frontend and retrieving the data from ElasticSearch. Several Endpoints are established.
The flask container based on the [uwsgi-nginx](https://github.com/tiangolo/uwsgi-nginx-flask-docker) container by tiangolo.

### Endpoint to check if the flask-server is reachable

`GET http://localhost:5000/books`
-> the expected result is supposed to look like the following:
{
  "books": [
    {
      "author": "Jack Kerouac", 
      "read": true, 
      "title": "On the Road"
    }, 
    {
      "author": "J. K. Rowling", 
      "read": false, 
      "title": "Harry Potter and the Philosopher's Stone"
    }, 
    {
      "author": "Dr. Seuss", 
      "read": true, 
      "title": "Green Eggs and Ham"
    }
  ], 
  "status": "success"
}
The endpoint returns static elements which represents a successfull connection.

### Endpoint to check if ElasticSearch is reachable from the flask-server

`GET http://localhost:5000/elasticCheck`
-> the expected result is supposed to look similar to the following:
[
  {
    "cluster_name": "docker-cluster",
    "cluster_uuid": "HevWfahjSa-BEBp7rrHf6A",
    "name": "elasticsearch_node",
    "tagline": "You Know, for Search",
    "version": {
      "build_date": "2019-05-16T00:43:15.323135Z",
      "build_flavor": "default",
      "build_hash": "606a173",
      "build_snapshot": false,
      "build_type": "docker",
      "lucene_version": "8.0.0",
      "minimum_index_compatibility_version": "6.0.0-beta1",
      "minimum_wire_compatibility_version": "6.8.0",
      "number": "7.1.0"
    }
  },
  {
    "message": "response ok"
  }
]

The elasticCheck endpoint connects to the elastic search instance and returns the status. At the lower bound of the responds message, says responds ok, which means the connection was successful. A similar check can be done with the endpoint of:
`localhost:5000/healthcheck`

## Classifier

The classifier takes triggered by the cronjob which is configured in the entrypoint.sh file in combination with the docker file. The logs of the classifier can be seen within the docker container. The user needs to connect to the running container with the command:
`docker exec -it <name of the container> sh`

The logs can be seen in the /var/logs folder. They are called:

- load.log
- classify.log
- push.log

The files which can be triggered within the docker container are located at /root location.
The user can change the directory by:
`cd /root`

Running the command:
`python3 loadFromElastic.py`
will download the articles which are tagged with the date of yesterday. The data is saved within the datafiles - data.csv
Warning: The file loadFromElastic.py has a hyperparameter that is automatically produced to retrieves the articles of yesterday. If the file is used for other porpuses, the parameter needs to be adjusted to get the data that is wanted.

`python3 classifier.py`
will binary classify the data which are loaded from the file - data.csv. The trained model will be loaded from the folder trained_model. The classified data will be saved into the file labeled_data.csv

`python3 pushToElastic.py`
will load the labeled data and apply the named entity recognizer to generate the entities. The entities with the context information will be pushed to the index of labeled-news-english back to elastic search.

The used frameworks for the classification model is Keras and Tensorflow. The Named Entity Extraction is applied within the help of the spacy framework.

## front-end

The front-end is built in the VueJs. This language increases their popularity with the attributes of easy to get started, with a flexible structure and generates a smooth development feeling.

How to use the frontend can be found here [Front-end Documentation](./front-end/README.md)
