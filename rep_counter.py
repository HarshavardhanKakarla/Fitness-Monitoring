from typing import Optional

class RepCounter:
    def __init__(self):
        self.stage: dict[str, Optional[str]] = {
            "squat": None,
            "pushup": None,
            "pullup": None
        }

        self.reps = {"squat": 0, "pushup": 0, "pullup": 0}
        self.last_frame = {"squat": None, "pushup": None, "pullup": None}

    def update(self, exercise, angles, frame_id, quality):

        # ---------- SQUAT ----------
        if exercise == "squat":

    # 🔥 use both knees
            knee = (angles[2] + angles[3]) / 2

    # ---------- DOWN ----------
            if knee < 0.75:   # relaxed threshold
              self.stage["squat"] = "down"

    # ---------- UP ----------
            if knee > 0.92 and self.stage["squat"] == "down":

                if self.last_frame["squat"] is None or frame_id - self.last_frame["squat"] > 8:

            # 🔥 TEMP: remove strict filter (debug first)
                   self.reps["squat"] += 1

                   self.stage["squat"] = "up"
                   self.last_frame["squat"] = frame_id
        # ---------- PUSHUP ----------
        elif exercise == "pushup":
            elbow = (angles[0] + angles[1]) / 2

            if elbow < 0.6:
                self.stage["pushup"] = "down"

            if elbow > 0.80 and self.stage["pushup"] == "down":
                if self.last_frame["pushup"] is None or frame_id - self.last_frame["pushup"] > 10:
                    self.reps["pushup"] += 1
                    self.stage["pushup"] = "up"
                    self.last_frame["pushup"] = frame_id

        # ---------- PULLUP ----------
        elif exercise == "pullup":
            elbow = angles[0]

            if elbow < 0.5:
                self.stage["pullup"] = "up"

            if elbow > 0.85 and self.stage["pullup"] == "up":
                if self.last_frame["pullup"] is None or frame_id - self.last_frame["pullup"] > 10:
                    self.reps["pullup"] += 1
                    self.stage["pullup"] = "down"
                    self.last_frame["pullup"] = frame_id

        return self.reps