from flask import Blueprint, jsonify, request
from bson import ObjectId
from app.src import mongo
from app.src.models import create_user

main = Blueprint('main', __name__)


def serialize_document(document):
    document['_id'] = str(document['_id'])
    return document
##########################################################################################################
#########################################(API-HEALTH)#######################################################
@main.route('/health', methods=['GET'])
def home():
    return jsonify({'message': 'Server is up and running!'})
##########################################################################################################
############################################(GET A USER)####################################################
@main.route('/api/user/<id>', methods=['GET'])
def get_user(id):
    try:
        user = mongo.db.users.find_one({'_id': ObjectId(id)})
        if user:
            return jsonify({ "status": "success", "data": serialize_document(user)}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
##########################################################################################################
#############################################(REGISTER)###################################################
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
        existing_user = list(mongo.db.users.find({
        "$or": [
            {'username': data['username']},
            {'email': data['email']}
        ]
        }))

        if len(existing_user) > 0:
            return jsonify({'error': 'Email or Username already registered'}), 400

        create_user(data)
        return jsonify({ "status": "success", 'data': serialize_document(data)}), 201
    except ValueError as e:
        # Handle specific validation errors
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        # Handle other unexpected errors
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal Server Error', 'message': f'{e}'}), 500
    
##########################################################################################################
#############################################(GET ALL USERs)##############################################
@main.route('/api/users', methods=['GET'])
def get_all_users():
    users = list(mongo.db.users.find({}))
    serialized_users = [serialize_document(user) for user in users]
    return jsonify({ "status": "success", "data": serialized_users}), 200

##########################################################################################################
#############################################(UPDATE USER)##############################################
@main.route('/api/user/<id>', methods=['PUT'])
def update_user(id):
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

        user = mongo.db.users.find_one({'_id': ObjectId(id)})
        if not user:
            return jsonify({'error': 'User not found'}), 404

        mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': data})
        return jsonify({ "status": "success", 'data': serialize_document(data)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

##########################################################################################################
#############################################(DELETE USER)################################################
@main.route('/api/user/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = mongo.db.users.find_one({'_id': ObjectId(id)})
        if not user:
            return jsonify({'error': 'User not found'}), 404

        mongo.db.users.delete_one({'_id': ObjectId(id)})
        return jsonify({ "status": "success", 'message': 'User deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
##########################################################################################################
#############################################(CREATE ROAD ANOMALY)########################################
@main.route('/api/roads', methods=['POST'])
def create_road_anomaly():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # List of required fields
        required_fields = ['Vibration', 'Latitude', 'Longitude', 
                           'Accel_X', 'Accel_Y', 'Accel_Z', 
                           'Gyro_X', 'Gyro_Y', 'Gyro_Z', 
                           'Temperature', 'Anomaly']

        # Check if all required fields are present and convert them to float
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
            
            try:
                data[field] = float(data[field])
            except ValueError:
                return jsonify({'error': f'{field} must be a valid number'}), 400

        # Insert the validated and converted data into the database
        mongo.db.roads.insert_one(data)
        return jsonify({"status": "success", 'data': serialize_document(data)}), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        # Handle other unexpected errors
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal Server Error', 'message': f'{e}'}), 500
    
##########################################################################################################
#############################################(GET ALL ROAD ANOMALIES)#####################################
@main.route('/api/roads', methods=['GET'])
def get_all_roads():
    roads = list(mongo.db.roads.find({}))
    if not roads:
        return jsonify({'error': 'No road anomalies found'}), 404
    serialized_roads = [serialize_document(road) for road in roads]
    return jsonify({ "status": "success", "data": serialized_roads}), 200

##########################################################################################################
#############################################(GET ROAD ANOMALY)###########################################
@main.route('/api/roads/<id>', methods=['GET'])
def get_road_anomaly(id):
    try:
        road = mongo.db.roads.find_one({'_id': ObjectId(id)})
        if road:
            return jsonify({ "status": "success", "data": serialize_document(road)}), 200
        else:
            return jsonify({'error': 'Road anomaly not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
##########################################################################################################
###########################################(PREDICT ROAD ANOMALY)#########################################
@main.route('/api/roads/predict', methods=['POST'])
def predict_road_anomaly():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # List of required fields
        required_fields = ['Vibration', 'Latitude', 'Longitude', 
                           'Accel_X', 'Accel_Y', 'Accel_Z', 
                           'Gyro_X', 'Gyro_Y', 'Gyro_Z', 
                           'Temperature']

        # Check if all required fields are present and convert them to float
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
            
            try:
                data[field] = float(data[field])
            except ValueError:
                return jsonify({'error': f'{field} must be a valid number'}), 400

        # Dummy prediction
        data['Anomaly'] = 1

        return jsonify({ "status": "success", 'data': data}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        # Handle other unexpected errors
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal Server Error', 'message': f'{e}'}), 500


    
    