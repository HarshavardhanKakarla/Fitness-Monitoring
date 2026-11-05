import time
import pandas as pd
import os

class SessionManager:
    def __init__(self):
        self.active = False
        self.start_time = None
        self.duration = 120  # 2 minutes

    def start(self):
        self.active = True
        self.start_time = time.time()

    def check_end(self):
        if not self.active:
            return False

        if time.time() - self.start_time > self.duration:
            self.active = False
            return True

        return False

    def end(self):
        self.active = False
        return True


def save_session(reps):
    data = []
    date = pd.Timestamp.now()

    for ex, r in reps.items():
        data.append([ex, r, date])

    df = pd.DataFrame(data, columns=["exercise","reps","date"])

    if os.path.exists("workout_log.csv"):
        df.to_csv("workout_log.csv", mode='a', header=False, index=False)
    else:
        df.to_csv("workout_log.csv", index=False)