from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_mongoengine import MongoEngine
from flask_elasticsearch import FlaskElasticsearch
app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['chat_database']
cache = db['search_cache']
db = MongoEngine(app)
app.config['MONGODB_SETTINGS'] = {
    'db': 'chat_database',
    'host': 'localhost',    
}
app.config['ELASTICSEARCH_URL'] = 'http://localhost:9200'
es = FlaskElasticsearch(app)
app.config
class Message(db.Document):
    sender = db.StringField(required=True)
    content = db.StringField(required=True)
    timestamp = db.DateTimeField()
@app.route('/messages', methods = ['GET' , 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.objects().to_json()
        return jsonify(messages), 200
    elif request.method == ' POST':
        data = request.json
        new_message =Message(sender=data['sender'],
                       content=data['content']
                       )
        new_message.save()
        return jsonify(new_message), 201 
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    res =es.search(index='pdf_index', body={"query": {"match": {"text": query}}})
    hits = res['hits']['hits']
    results = [{'title': hit['_source']['title'], 'snippet': hit['_source']['snippet']} for hit in hits]
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True)