import sys
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

# Cerca la stringa MongoDB nelle variabili d'ambiente.
# Se non trova nulla, usa la tua stringa personalizzata inserita qui sotto.
MONGO_URL = os.environ.get(
    "DATABASE_URL", 
    os.environ.get(
        "MONGO_DB_URI", 
        "mongodb+srv://stefano:nkKMhPsyZEl4x9Fw@cluster0.pua77pf.mongodb.net/?appName=Cluster0"
    )
)

mc = MongoClient(MONGO_URL, server_api=ServerApi('1'))
db = mc["UNIcache"]

class SD:
    """Handles data storage, retrieval, and deletion for cached messages."""
    
    @staticmethod
    def write_data(message_id: int, message_link: str, requested_by: int, data_type: str):
        collection = db["datas"]
        data = {
            "_id": message_id,
            "message_link": message_link,
            "requestedBy": requested_by,
            "dataType": data_type
        }
        collection.insert_one(data)

    @staticmethod
    def read_data(message_link: str):
        collection = db["datas"]
        return collection.find_one({"message_link": message_link})

    @staticmethod
    def delete_data(message_link: str):
        collection = db["datas"]
        collection.delete_one({"message_link": message_link})

class Banned:
    """Handles management of banned users."""
    
    @staticmethod
    def write_data(user_id: int):
        collection = db["banned"]
        collection.insert_one({"_id": user_id})

    @staticmethod
    def read_data(user_id: int):
        collection = db["banned"]
        return collection.find_one({"_id": user_id})

def initialize_database():
    try:
        mc.admin.command('ping')
        print("MongoDB Connected Successfully!")
    except Exception as e:
        print(f"MongoDB Connection Error: {e}")

DEVELOPER = "CoderX"
