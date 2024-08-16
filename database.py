import os
from pymongo import mongo_client, MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_CONNECTION_URL = os.environ.get("MONGO_DB_CONNECTION_URL")


client = mongo_client.MongoClient(MONGO_DB_CONNECTION_URL)
print ("Connected to MongoDB")

# Get or Create Collection

movies_collection = client["Movie_app"]["movies"]
users_collection = client["Movie_app"]["users"]
comments_collection = client["Movie_app"]["comments"]
ratings_collection = client["Movie_app"]["ratings"]


