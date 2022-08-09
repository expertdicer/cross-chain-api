import os

class MongoDBConfig:
    MONGODB_HOST = os.environ.get("MONGODB_HOST", '0.0.0.0')
    MONGODB_PORT = os.environ.get("MONGODB_PORT", '27017')
    USERNAME = os.environ.get("MONGODB_USERNAME", 'admin')
    PASSWORD = os.environ.get("MONGODB_PASSWORD", 'dev123')
    CONNECTION_URL = f'mongodb://localhost:27017'