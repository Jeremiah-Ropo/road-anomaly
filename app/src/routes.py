from flask import Blueprint, jsonify, request
from app.src import mongo
from app.src.models import create_user, get_users

main = Blueprint('main', __name__)


def serialize_document(doc):
    """Convert MongoDB document to serializable format."""
    doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
    return doc

@main.route('/health', methods=['GET'])
def home():
    return jsonify({'message': 'Server is up and running!'})

@main.route('/api/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'World')
    return jsonify({'message': f'Hello, {name}!'})

@main.route('/api/register', methods=['POST'])
def register_data():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        if 'username' not in data:
            return jsonify({'error': 'Username is required'}), 400
        if 'email' not in data:
            return jsonify({'error': 'Email is required'}), 400
        if 'password' not in data:
            return jsonify({'error': 'Password is required'}), 400
        # Check if username exists
        existing_user = list(mongo.db.users.find({'username': data['username'], 'email': data['email']}))
        if len(existing_user) > 0:
            return jsonify({'error': 'User already exists'}), 400
        print(f"data: {data}")
        
        created = create_user(data)
        print(f"Created user: {created}")
        return jsonify({'data': serialize_document(data)}), 201
    except ValueError as e:
        # Handle specific validation errors
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        # Handle other unexpected errors
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal Server Error', 'message': f'{e}'}), 500

@main.route('/api/users', methods=['GET'])
def get_data():
    data = mongo.db.data.find()
    data_list = [{'id': str(item['_id']), **item} for item in data]
    return jsonify(data_list)
