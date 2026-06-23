from fastapi import FastAPI 
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = FastAPI()
uri = "mongodb+srv://Abdullah_Admin:8434427@aitaskmanager.ecyrgos.mongodb.net/?appName=AITaskMAnager"
client = MongoClient(uri,server_api = ServerApi('1'))
db = client["ai_system"]
tasks_collection = db["tasks"]

class Task(BaseModel):
    title: str
    description: str
    is_done:bool = False
    periority : int
@app.get("/tasks")
def get_all_tasks():
    # 1. تجهيز لستة فاضية هنجمع فيها المهام
    all_tasks = []
    # 2. جلب كل المهام من المونجو (find بدون شروط يعني هات كله)
    cursor = tasks_collection.find()
    # 3. معالجة الداتا (Data Processing)
    for task in cursor:
        # تحويل الـ ObjectId المعقد لنص عادي
        task["_id"] = str(task["_id"])
        # إضافة المهمة للستة بتاعتنا
        all_tasks.append(task)

    # 4. إرسال الرد لليوزر    
    return{"tasks" : all_tasks}

@app.post("/tasks/")
def create_task (task: Task):
    # 1. Serialization: تحويل الداتا من Pydantic Model لـ Dictionary عشان المونجو تفهمه
    task_dict = task.model_dump()

    # 2. Database Execution: إرسال الداتا للخزنة
    result = tasks_collection.insert_one(task_dict)

    # 3. HTTP Response: الرد على اليوزر برسالة نجاح مع الـ ID اللي المونجو عمله أوتوماتيك
    return {"massage" : "task addied successfuly " , "task_id: " : str(result.inserted_id)}

