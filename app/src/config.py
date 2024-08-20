from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Access environment variables
secret_key = os.getenv("SECRET_KEY")
database_url = os.getenv("MONGO_URI")
debug_mode = os.getenv("DEBUG")

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGO_URI = os.getenv('MONGO_URI')

# class DevelopmentConfig(Config):
#     MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/devdatabase')

# class TestingConfig(Config):
#     TESTING = True
#     MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/testdatabase')

# class ProductionConfig(Config):
#     MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/proddatabase')
