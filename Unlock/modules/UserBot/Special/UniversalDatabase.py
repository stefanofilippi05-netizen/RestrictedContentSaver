import sys
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

# URL MongoDB
MONGO_URL = os.environ.get(
    "DATABASE_URL", 
    os.environ.get(
        "MONGO_DB_URI", 
        "mongodb+srv://stefano:nkKMhPsyZEl4x9Fw@cluster0.pua77pf.mongodb.net/?appName=Cluster0"
    )
)

# Variabili di configurazione richieste dal bot
channel_id = int(os.environ.get("CHANNEL_ID", "-1000000000000"))
INVITE_LINK = os.environ.get("INVITE_LINK", "https://t.me/")

# Altre variabili globali che il bot si aspetta di importare
rbot = None
ubot = None
DEVELOPER = "CoderX"
SUPPORT = "https://t.me/StarkBotsChat"
UPDATES = "https://t.me/StarkBots"
CX = "https://t.me/CoderX"
UPDATES_LINK = "https://t.me/StarkBots"
REPO_LINK = "https://github.com/StarkBotsIndustries/RestrictedContentSaver"

# Connessione MongoDB
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
