import os
import pymongo as mongo

from dotenv import load_dotenv

env = lambda key: os.getenv(key)

# Environment variables
load_dotenv("././.env")

# Connection string
db_uri = f"mongodb://{env('DATABASE_USER')}:{env('DATABASE_PASSWORD')}@localhost:{env('DATABASE_PORT')}"

# Test connection to mongodb
try:
  client = mongo.MongoClient(db_uri, serverSelectionTimeoutMS=2000)
  client.admin.command('ping')
except Exception as e:
  print(f"ERROR: Connecting to the database: {e}") 
  exit(1)

# Get collection
db         = client[os.getenv('DATABASE_NAME')]
collection = db[os.getenv('DATABASE_COLLECTION')]

documents = list(collection.find({}))