from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")

db = client["secure_file_sharing"]

users_collection = db["users"]
logs_collection = db["logs"]

print(">>> MongoDB connected: secure_file_sharing <<<")