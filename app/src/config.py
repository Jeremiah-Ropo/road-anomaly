import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'you-should-change-this')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/mydatabase')

class DevelopmentConfig(Config):
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/devdatabase')

class TestingConfig(Config):
    TESTING = True
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/testdatabase')

class ProductionConfig(Config):
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/proddatabase')
