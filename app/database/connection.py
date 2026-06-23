from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# إعدادات الاتصال بقاعدة البيانات
uri = "mongodb+srv://Abdullah_Admin:8434427@aitaskmanager.ecyrgos.mongodb.net/?appName=AITaskMAnager"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["ai_system"]
tasks_collection = db["tasks"]