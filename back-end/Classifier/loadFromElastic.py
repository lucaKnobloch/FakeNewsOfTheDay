import json
import logging
import pandas
import numpy as np
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta

# Connect to the elastic cluster
def connect_elasticsearch():
	_es = None

	# reads the config file
	with open("./config.json") as config_file:
		config = json.load(config_file)

	_es = Elasticsearch(config['dev'] + ':9200')
	# returns that the connection is working
	if _es.ping():
		print('Yay Connect')
	# otherwise gives the error message that it is not connected
	else:
		print('Awww it could not connect!')
	return _es

# defines the search method in elasticSearch
def search(es_object, index_name, search):
	res = es_object.search(index=index_name, body=search)
	return res

if __name__ == '__main__':
	# enables logging
	logging.basicConfig(level=logging.ERROR)
	# connects to elasticsearch
	es = connect_elasticsearch()
	# get the date of yesterday
	yesterday = datetime.now() - timedelta(days=1)
	# get the date of today
	today = datetime.now()
	# creates the indexname for Yesterday / Today
	INDEX_YESTERDAY = str(yesterday.year) + "-" + str(yesterday.month) + "-" + str(yesterday.day)
	# saves the char at a specific postion to check if the date is saved in the right format
	check1 = INDEX_YESTERDAY[7]
	# checks the right format for the day
	if check1 == "-":
		SEARCH_DAY = INDEX_YESTERDAY[:8] + "0" + INDEX_YESTERDAY[8:]
	# checks that the month has the right format as well 
	check2 = SEARCH_DAY[6]
	if check2 == "-":
		SEARCH_DAY = SEARCH_DAY[:5] + "0" + SEARCH_DAY[5:]
	INDEX_TODAY = "labeled_data" + "_" + str(today.year) + "-" + str(today.month) + "-" + str(today.day)

	if es is not None:
		# search for article which are published between today and yesterday 
		# returns maximal 1000 article
		# gte Greater than or equal to
		# lt = Less than
		# search_object = {
  		# 	"size": 1000,
  		# 	"query": {
   		# 		"range": {
     	# 			"published": {
        # 				"gte": "now-1d/d",
       	# 				"lt": "now/d"
      	# 			}
    	# 		}
  		# 	}
		# }
		search_object={"size": 1000,"query":{"match_phrase":{"published":SEARCH_DAY}}}
		# do the actual search with converting the body in the json format
		rs = search(es, 'news-english', json.dumps(search_object))
		rows = []
		i = 0
		# goes trough every document of the result 
		for doc in rs['hits']['hits']:
			# saves the conentent and perfom preprocessing steps
			# saves the title and deletes the leading whitespaces
			title = doc['_source']['title'].strip()
			# saves the title, deletes the leading whitespaces, replaces "\n\n" with a whitespace
			content = doc['_source']['content'].strip().replace("\n\n", " ")
			# saves the url of the origin article
			url = doc['_source']['url']
			# saves the time when article was published
			published = doc['_source']['published']
			# adds an empty string for the label / entites which will be overwritten after classification 
			# will be created by indexing the article 
			label = ""
			entities = ""
			# when the content is emtpy the article is not usable so it is filtert out
			if content != "":
				# it puts all the saved information together to one array
				row = np.array([i, title, content, label, url, published, entities])
				# adds the row to a list of rows 
				rows.append(row)
				# lets the user see that the programm is working
				i += 1
				print(i, "amount of Elements")

		# creates a pandas DataFrame with the created rows
		df = pandas.DataFrame(rows, columns=['id', 'title', 'text', 'label', 'url', 'published', 'entities'])

		# saves the DataFrame to a csv file to be easily readable by the classifier
		df.to_csv("./data_files/data.csv", index=False)
		print('Saved the elements to the file')
