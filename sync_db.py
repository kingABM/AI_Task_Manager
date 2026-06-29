import os
from dotenv import load_dotenv
from pymongo import MongoClient
import chromadb
from sentence_transformers import SentenceTransformer
import certifi

load_dotenv()
mongo_url = os.getenv("MONGODB_URL")

print("System Booting: Initializing Encoders and Databases...")

embed_model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

mongo_client = MongoClient(mongo_url, tlsCAFile=certifi.where())
db = mongo_client["ai_system"]
collection = db["tasks"]

chroma_client = chromadb.PersistentClient(path="./chroma_db")
vector_collection = chroma_client.get_or_create_collection("tasks_vectors")

print("Extracting tasks from MongoDB...")
tasks = list(collection.find({}))
if not tasks:
    print("System Alert: No tasks found in MongoDB. Add some tasks first!")
else:
    print(f"Found {len(tasks)} tasks. Vectorizing and Syncing to ChromaDB...")

    for task in tasks:
        task_id = str(task['_id'])
        task_title = task.get('title' , '')
        task_desc = task.get('description', '')
        full_text = f"Task: {task_title} - Description: {task_desc}"
        
        # الترجمة الرياضية وتحويلها لقائمة أرقام
        vector = embed_model.encode(full_text).tolist()

        # الحقن في قاعدة البيانات المتجهة
        vector_collection.upsert(
            ids=[task_id],
            embeddings=[vector],
            documents=[full_text],
            metadatas=[{"status" : task.get("status" , "pending")}]
        )

print("🟢 System Sync Complete! ChromaDB is now loaded with your tasks.")


