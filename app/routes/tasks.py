from fastapi import APIRouter
from app.database.connection import tasks_collection
from app.models.schemas import Task

router = APIRouter()

@router.get("/tasks")
def get_all_tasks():
    all_tasks = []
    cursor = tasks_collection.find()
    for task in cursor:
        task["_id"] = str(task["_id"])
        all_tasks.append(task)
    return {"tasks": all_tasks}

@router.post("/tasks/")
def create_task(task: Task):
    task_dict = task.model_dump()
    result = tasks_collection.insert_one(task_dict)
    # تم تصحيح كلمة massage لـ message
    return {"message": "Task added successfully", "task_id": str(result.inserted_id)}