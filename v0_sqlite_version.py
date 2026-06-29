import sqlite3


class Task:
    def __init__(self, task_id, name, ai_model):
        self.task_id = task_id
        self.name = name
        self.ai_model = ai_model
        self.status = "Pending"  

    def mark_as_completed(self):
        self.status = "Completed"



class TaskManager:
    def __init__(self):
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS ai_tasks(
                task_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                ai_model TEXT NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        self.conn.commit()
        print("System Log: Database Connected and Table is Ready! 💾")
    

    def add_task(self, task):
        self.cursor.execute('''
            INSERT OR REPLACE INTO ai_tasks (task_id, name, ai_model, status)
            VALUES (?, ?, ?, ?)
        ''', (task.task_id, task.name, task.ai_model, task.status))
        
        self.conn.commit()
        print(f"System Log: Task '{task.name}' saved to Database! 📥")
    

    def remove_task(self, task_id):
        self.cursor.execute('DELETE FROM ai_tasks WHERE task_id = ?', (task_id,))
        self.conn.commit()
        print(f"System Log: Task ID [{task_id}] removed successfully! 🗑️")


    def update_task_status(self, task_id, new_status):
        self.cursor.execute('UPDATE ai_tasks SET status = ? WHERE task_id = ?', (new_status, task_id))
        self.conn.commit()
        print(f"System Log: Task ID [{task_id}] is now {new_status}! ✅")


    def display_all_tasks(self):
        print("\n--- 📊 AI Tasks Database Dashboard ---")
        
        self.cursor.execute('SELECT * FROM ai_tasks')
        
        rows = self.cursor.fetchall()
        
        if len(rows) == 0:
            print("No tasks found in Database.")
            
        for row in rows:
            print(f"[{row[0]}] {row[1]} | Model: {row[2]} | Status: {row[3]}")
        print("--------------------------------------\n")


manager = TaskManager()

t1 = Task(1, "Train Vision Model", "YOLOv8")
t2 = Task(2, "Build RAG", "FastAPI")
t3 = Task(3, "Use Multi-Tenant Arc" , "Python")

print("\n--- Executing Operations ---")
manager.add_task(t1)
manager.add_task(t2)
manager.add_task(t3)

manager.remove_task(3)

manager.update_task_status(1, "Completed")

manager.display_all_tasks()