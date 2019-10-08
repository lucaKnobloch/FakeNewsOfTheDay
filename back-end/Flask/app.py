from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from datetime import datetime
from elasticsearch import Elasticsearch
from healthcheck import HealthCheck
import json

# configuration
DEBUG = True

# loads the config file
with open('config.json') as config_file:
	config = json.load(config_file)

# instantiate the app
es = Elasticsearch(config['prod']+':9200')

# default needs to be modified because Vue.js uses the variables with / 
class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  
        variable_end_string='%%'
    ))
app = CustomFlask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)


@app.route('/elasticIndexCheck', methods=['GET'])
def elasticCheckIndex():
	results = es.get(index='failures-english', id='/_search')
	return jsonify(results['hits'])

@app.route("/search/<date>/<label>", methods=["POST", "OPTIONS"])
def search(date, label):
	if request.method == "OPTIONS": # CORS preflight
		return _build_cors_prelight_response()
	elif request.method == "POST": # The actual request following the preflight
		print(date)
		body = {
			"size": 500,
			"query": {
				"bool": {
				"must": [
					{"match": {"label": label}},
					{"match": {"date": date}}
				]
			}
		}
		}
		res = es.search(index='labeled-news-english', body=body)
		return _corsify_actual_response(jsonify(res['hits']['hits']))
	else:
		raise RuntimeError("Wierd - don't know how to handle method {}".format(request.method))

def _build_cors_prelight_response():
	response = make_response()
	response.headers.add("Access-Control-Allow-Origin", "*")
	response.headers.add('Access-Control-Allow-Headers', "*")
	response.headers.add('Access-Control-Allow-Methods', "*")
	return response

def _corsify_actual_response(response):
	response.headers.add("Access-Control-Allow-Origin", "*")
	return response

@app.route('/search', methods=['POST'])
def test():
	data = json.loads(request.data)
	label = data["label"]
	date = data["date"]
	body = {
		"size": 30,
		"query": {
			"bool": {
				"must": [
					{"match": {"label": label}},
					{"match": {"date": date}}
				]
			}
		}
	}
	res = es.search(index='labeled-news-english', body=body)
	return json.dumps(res['hits']['hits'])

@app.route('/singleSearch', methods=['POST'])
def searchPost():
	data = request.json
	print(data)
	body = {
		"query": {
			"match": request.json
		}
	}
	res = es.search(index='test', body=body)
	return jsonify(res['hits']['hits'])


@app.route('/updateEntry', methods=['GET'])
def info():
	body = {
		'id': 8,
		'labeled1': 'FALSE',
		'entity': 'LUCA',
		'headline': 'LORUM LARUM',
		'content': 'LIROUM LARUM PASDPASDPASPD',
		'date1': '1-9-2019'
	}
	res = es.index(index='test', id=8, body=body)
	return jsonify(res)


@app.route('/searchAbsolute', methods=['GET'])
def searchTest():
	body = {
		"query": {
			"match": {
				'date': '30-8-2019',
				'label': 'true'
			}
		}
	}
	res = es.search(index='news-english', body=body)
	return jsonify(res['hits']['hits'])


@app.route('/deleteEntry', methods=['GET'])
def deleteEntry():
	res = es.delete(index='test', id=3)
	return jsonify(res)


@app.route('/insertData', methods=['POST'])
def insert_data():
	article_id = request.form['id']
	label = request.form['label']
	entity = request.form['entity']
	headline = request.form['headline']
	content = request.form['content']
	date = request.form['date']

	body = {
		'id': article_id,
		'label': label,
		'entity': entity,
		'headline': headline,
		'content': content,
		'date': date
	}
	result = es.index(index='contents', id=article_id, doc_type='label', body=body)
	return jsonify(result)


@app.route('/elasticCheck', methods=['GET'])
def elasticCheck():
	res = es.info()
	return jsonify(res, {'message': 'response ok'}), 200


health = HealthCheck(app, "/healthcheck")

BOOKS = [
	{
		'title': 'On the Road',
		'author': 'Jack Kerouac',
		'read': True
	},
	{
		'title': 'Harry Potter and the Philosopher\'s Stone',
		'author': 'J. K. Rowling',
		'read': False
	},
	{
		'title': 'Green Eggs and Ham',
		'author': 'Dr. Seuss',
		'read': True
	}
]


@app.route('/books', methods=['GET'])
def all_books():
	return jsonify({
		'status': 'success',
		'books': BOOKS
	})

if __name__ == '__main__':
	# use the config file to get host and parameters
	with open('config.json') as config_file:
		config = json.load(config_file)
	app.run(host=config['host'], debug=True)