from flask import jsonify, request
from .mongo import mongo

@app.route('/')

def home():
    return "Welcome to the Flask API!"

@app.route('/api/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'World')
    return jsonify({'message': f'Hello, {name}!'})

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.json
    mongo.db.data.insert_one(data)
    return jsonify({'received': data}), 201

@app.route('/api/data', methods=['GET'])
def get_data():
    data = mongo.db.data.find()
    data_list = [{'id': str(item['_id']), **item} for item in data]
    return jsonify(data_list)
