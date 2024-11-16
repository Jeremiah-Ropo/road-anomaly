# import os
# import pickle
# import random
# import pandas as pd
# from bson import ObjectId
# from app.src import mongo
# from datetime import datetime
# import schedule
# import time
# from pymongo import InsertOne, UpdateOne



# # Load the ML model once
# model_path = os.path.join(os.path.dirname(__file__), 'final_norm_model.pkl')
# with open(model_path, 'rb') as model_file:
#     model = pickle.load(model_file)


# def batch_predict_road_anomalies(batch_size=1000):

#     try:
#         # To fetch batch by batch
#         data_cursor = mongo.db.sensor_data.find({"Predicted": {"$exists": False}, 
#                                                  "Latitude": {"$ne": 0}, 
#                                                  "Longitude": {"$ne": 0}}).limit(batch_size)
#         data_batch = list(data_cursor)

#         if not data_batch:
#             print("No new data to process.")
#             return

#         # List of required fields
#         required_fields = ['Accel_X', 'Accel_Y', 'Accel_Z', 
#                            'Gyro_X', 'Gyro_Y', 'Gyro_Z', 
#                            'Latitude', 'Longitude', 'Speed', 
#                            'Vibration', 'Temperature']

#         update_sensor_data = []
#         predictions = []
#         for data in data_batch:
#             if data.get('Latitude') == 0 or data.get('Longitude') == 0:
#                 continue

#             if data.get('Temperature') is None:
#                 data['Temperature'] = round(32.00 + (33.00 - 32.00) * random.random(), 2)
#             if data.get('Speed') is None:
#                 data['Speed'] = round(0.00 + (10.88 - 0.00) * random.random(), 2)

#             # Convert to DataFrame and ensure data type
#             input_data = pd.DataFrame([{field: data.get(field, None) for field in required_fields}])
#             try:
#                 input_data = input_data.astype(float)
#             except ValueError as e:
#                 print(f"Skipping invalid data: {e}")
#                 continue
            
#             # Make prediction
#             anomaly_prediction = model.predict(input_data)[0]

#             # Add the prediction to the result collection 
#             data['Anomaly'] = int(anomaly_prediction)
            
#             predictions.append(InsertOne(
#                 {

#                     "Latitude": float(data['Latitude']),
#                     "Longitude": float(data['Longitude']),
#                     "Anomaly": data['Anomaly'],
#                     "createdAt": datetime.now()

#                 }
#             ))

#             update_sensor_data.append(UpdateOne(
#                 {"_id": data["_id"]},
#                 {"$set": {"Predicted": True}}
#             ))

#         if update_sensor_data:
#             update_result = mongo.db.sensor_data.bulk_write(update_sensor_data)
#             print(f"Updated {update_result.modified_count} documents in sensor_data collection.")

#         # Perform bulk write to update the predictions in MongoDB
#         if predictions:
#             result = mongo.db.result.bulk_write(predictions)
#             print(f"Inserted {len(predictions)} documents in result collection.")

#     except Exception as e:
#         print(f"Error during batch prediction: {e}")

# def main():
#     # scheduling for 20secs for testing purpose
#     schedule.every(60).seconds.do(batch_predict_road_anomalies)

#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# if __name__ == "__main__":
#     main()
