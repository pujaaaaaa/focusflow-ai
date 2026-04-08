import pandas as pd

class WorkdayEnv:
    def __init__(self):
        self.energy = 100
        self.productivity = 0
        self.time_elapsed = 0
        self.history = []
        self.log = [] # Finalized actions
        self.pending_tasks = [] # Selection buffer
        self._record_history("Start")

    def add_to_plan(self, task_name):
        self.pending_tasks.append(task_name)

    def remove_from_plan(self, index):
        if 0 <= index < len(self.pending_tasks):
            self.pending_tasks.pop(index)

    def execute_plan(self):
        for task in self.pending_tasks:
            if self.time_elapsed >= 8: break
            
            if task == "Break":
                self.energy = min(100, self.energy + 25)
                self.log.append(f"Hour {self.time_elapsed+1}: ☕ Restored Energy")
            else:
                drain = 20 if task == "Deep Work" else 10
                gain = 30 if task == "Deep Work" else 15
                if self.energy >= drain:
                    self.energy -= drain
                    self.productivity += gain
                    self.log.append(f"Hour {self.time_elapsed+1}: ✅ {task}")
                else:
                    self.log.append(f"Hour {self.time_elapsed+1}: ❌ Failed {task} (No Energy)")
            
            self.time_elapsed += 1
            self._record_history(task)
        
        self.pending_tasks = [] # Clear plan after execution

    def _record_history(self, action):
        self.history.append({
            "Time": self.time_elapsed, "Energy": self.energy,
            "Productivity": self.productivity, "Action": action
        })

    def get_history_df(self):
        return pd.DataFrame(self.history)
