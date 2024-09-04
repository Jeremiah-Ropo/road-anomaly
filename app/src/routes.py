from flask import Blueprint, jsonify, request
from bson import ObjectId
from app.src import mongo
from app.src.models import create_user
import os
import pickle
import pandas as pd

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
        if 'email' not in data:
            return jsonify({'error': 'Email is required'}), 400
        if 'password' not in data:
            return jsonify({'error': 'Password is required'}), 400
        # Check if username exists
        existing_user = mongo.db.users.find_one({'email': data['email']})

        if existing_user:
            return jsonify({'error': 'Email already registered'}), 400

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
    model_path = os.path.join(os.path.dirname(__file__), 'finalnorm_model.pkl')
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # List of required fields
        required_fields = ['Latitude', 'Longitude', 
                           'Accel_X', 'Accel_Y', 'Accel_Z', 
                           'Gyro_X', 'Gyro_Y', 'Gyro_Z', 'Vibration_Binary']

        # Check if all required fields are present
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400

        # Convert data to a DataFrame
        input_data = pd.DataFrame([data])
        # Ensure all required fields are converted to float
        try:
            input_data = input_data[required_fields].astype(float)
        except ValueError as e:
            return jsonify({'error': 'All fields must be valid numbers'}), 400
        # Make a prediction using the loaded model
        anomaly_prediction = model.predict(input_data)[0]

        # Add the prediction to the data dictionary
        data['Anomaly'] = int(anomaly_prediction)

        return jsonify({"status": "success", 'data': data}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        # Handle other unexpected errors
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal Server Error', 'message': f'{e}'}), 500


    
    