import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '$Jeremiah59@')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://Jeremiah_Ropo:$Jeremiah59@cluster0.uuj49.mongodb.net/road-anomalies?retryWrites=true&w=majority')

# class DevelopmentConfig(Config):
#     MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/devdatabase')

# class TestingConfig(Config):
#     TESTING = True
#     MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/testdatabase')

# class ProductionConfig(Config):
#     MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/proddatabase')
