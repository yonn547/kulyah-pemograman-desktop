import json, os
from datetime import datetime

DATA_FILE = "tasks.json"

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load()

    def load(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.tasks = json.load(f)
            except Exception:
                self.tasks = []

    def save(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=2, ensure_ascii=False)

    def add(self, title, priority="Normal"):
        self.tasks.append({
            "id": len(self.tasks) + 1,
            "title": title,
            "priority": priority,
            "done": False,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        self.save()

    def toggle(self, idx):
        if 0 <= idx < len(self.tasks):
            self.tasks[idx]["done"] = not self.tasks[idx]["done"]
            self.save()

    def delete(self, idx):
        if 0 <= idx < len(self.tasks):
            self.tasks.pop(idx)
            self.save()

    def stats(self):
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t["done"])
        pending = total - done
        progress = (done / total * 100) if total else 0
        return total, done, pending, progress