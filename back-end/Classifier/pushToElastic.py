import pandas as pd
from elasticsearch import Elasticsearch, TransportError
import time
import spacy
from collections import Counter
from spacy.cli.download import download
from spacy import displacy
import logging
import numpy as np
from elasticsearch import Elasticsearch
import json

# Connect to the elastic cluster
def connect_elasticsearch():
	_es = None
	# another way of writting the command
	# _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
	
	# reads the config file
	with open("./config.json") as config_file:
		config = json.load(config_file)

	_es = Elasticsearch(config['prod'] + ':9200')
	# returns that the connection is working
	if _es.ping():
		print('Yay Connect')
	# otherwise gives the error message that it is not connected
	else:
		print('Awww it could not connect!')
	return _es

# pushes the updated information back to elasticSearch
def push_data(es_object, index_name, data, entities):
	# checkes if the index already exist
	if es_object.indices.exists(index_name):
		# gets the amount of already existing entries in the index
		i = es.count(index=index_name, doc_type='article', body={ "query": {"match_all" : { }}})
		# sets the index for the additonal created entries
		indexer = i['count']
	# if the index is not created before it will start with 0
	else: 
		indexer = 0
	
	for index, row in data.iterrows():
		# empty lists to save elements
		list_entities = []
		list_content = []
		# for each entity which is saved within the 
		for i in range(len(entities[index])):
			iter_entites = entities[index][i][0]
			list_entities.append(iter_entites)
			# gets the occurance of the entitites
			list_content.append(entities[index][i][3])
		# connects all the information together to be saved in elasticSearch
		body = {
			"title": row['title'],
			"text": row['text'],
			"label": row['label'],
			"url": row['url'],
			"published": row['published'],
			"date": time.strftime("%d-%m-%Y"),
			"entities": list_entities,
			"occurance": list_content
		}
		try:
			# indexes new entries
			es_object.index(index=index_name, doc_type='article', id=index, body=body)
			indexer += 1
			print(indexer, "entites pushed")
		except TransportError as e:
			print(e.info)

# reads the csv file and loads the data 
def get_labeled_data(path):
	return pd.read_csv(path)

# frees storage 
def delete_file_content(path):
	# Open a file
	fo = open(path, "w")
	# Now truncate remaining file.
	fo.truncate()
	# closses the file again
	fo.close()

# creates entites from the dataset 
def NER_spacy(dataset, amount_of_entities, char_length):
	# creates a dict to save the entities for the articles 
	relations = {}
	# 
	for index, row in dataset.iterrows():
		
		# can either create the entities from the headline of from the content
		## title = row['title'],
		# saves the content of the article
		text = row['text'],
		
		# applies the spacy approach to use the previous loaded corpus to apply tools of spacy 

		doc = nlp(str(text))
		
		# approach to display the entities 
		# html = displacy.render(doc, style="ent")
		
		# creates empty lists
		info = []
		entities = []

		# loops through all the entities of the text
		for ent in doc.ents:
			
			# every entity the text, the starting and end char is saved 
			info.extend([ent.text, ent.start_char, ent.end_char])
			
			# saves the text of the entity
			entities.append(ent.text)

		# finds of the article the most common articles and saves them 		
		mostCommon = Counter(entities).most_common(amount_of_entities)

		# creates a props list
		props = []
		# goes through every entity in the most common onces
		for i in range(len(mostCommon)):
			# ensures that the most common one is not empty 
			if mostCommon != []:
				# when the entitiy is also in the list of the entities which where created before
				if mostCommon[i][0] in info:
					# finds the beginning and the end of the entity and the entity itself
					indexer = info.index(mostCommon[i][0])
					start = info[indexer + 1]
					end = info[indexer + 2]
					# saves the snippet of the text where the entity appeared 
					text_extended = text[0][start - char_length:end + char_length]
					# saves entity name, start and ending char position plus the snippets of the text
					prop = mostCommon[i][0], start, end, text_extended
				# the entities are saved 
				props.append(prop)
		# returns the most common entites with their starting and ending point
		relations[index] = np.array(props)
	return relations


# creates an new indextemplate in elasticsearch
def create_index(es_object, index_name):
	created = False
	# index settings
	settings = {
		"settings": {
			"number_of_shards": 1,
			"number_of_replicas": 0
		},
		# specifies the attributes in the index 
		"mappings": {
			"article":{
			"properties": {
				"id": {
					"type": "integer"
				},
				"title": {
					"type": "text"
				},
				"content": {
					"type": "text"
				},
				"label": {
					"type": "text"
				},
				"url": {
					"type": "text"
				},
				"published": {
					"type": "text"
				},
				"date":{
					"type": "text"
				},
				"entities": {
					"type": "text"
				},
				"occurance": {
					"type": "text"
				}
			}
		}
	}
	}
	try:
		if not es_object.indices.exists(index_name):
			# Ignore 400 means to ignore "Index Already Exist" error.
			# creates a new index 
			es_object.indices.create(index=index_name, ignore=400, body=settings)
			print('Created Index')
		created = True
	except Exception as ex:
		# returns the exception
		print(str(ex))
	finally:
		return created


if __name__ == '__main__':

	# Hyperparameter 
	## to set the amount of entities which should be saved to for each article
	amount_of_entities = 3
	# Name of the csv file with the data
	PATH_LABELED_DATA = './data_files/labeled_data.csv'
	PATH_UNLABELED_DATA = './data_files/data.csv'
	# Indexname for elasticSearch
	INDEX = 'labeled-news-english'
	# lenght of char around the entitiy
	char_length= 20
	
	# logging.basicConfig(level=logging.ERROR)

	# checks if the corpus is in the container and if needed downloaded it 
	download('en_core_web_sm')
	# loads the spacy corpus  
	nlp = spacy.load('en_core_web_sm')

	# connects to elasticsearch 
	es = connect_elasticsearch()

	# ensures that an connection is successfull before perfom the following steps
	if es is not None:
		
		# loads the data set from which the entities shoudl be taken
		dataset = get_labeled_data(PATH_LABELED_DATA)
		
		# creates the amount of entities of each article 
		entities = NER_spacy(dataset, amount_of_entities, char_length)
		
		# creates an index with a mapping 
		# if the index is already created before the function will not create a second one
		result = create_index(es, INDEX)
		
		# pushes the labeled data with the entites + occurances back to elasticSearch
		push_data(es, INDEX, dataset, entities)
		print("finished pushing data")

		# cleans the files, to free storage 
		delete_file_content(PATH_UNLABELED_DATA)
		delete_file_content(PATH_LABELED_DATA)



