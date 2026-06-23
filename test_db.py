from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://Abdullah_Admin:8434427@aitaskmanager.ecyrgos.mongodb.net/?appName=AITaskMAnager"
client = MongoClient(uri,server_api = ServerApi('1'))

try:
    client.admin.command('ping')
    print("🚀 System Response: 200 OK - Successfully connected to MongoDB Atlas!")

except Exception as e : 
    print(f"❌ Connection Failed: {e}")