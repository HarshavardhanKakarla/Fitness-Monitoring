import numpy as np
import joblib
from tensorflow.keras.models import load_model
from collections import deque

LABELS = ["squat", "pushup", "pullup", "idle"]


class ExerciseClassifier:
    def __init__(self):
        self.model = load_model("model/exercise_model.h5", compile=False)
        self.scaler = joblib.load("model/scaler.pkl")

        self.seq = []
        self.window = deque(maxlen=10)   # smoother than before

    def predict(self, f):

        # ---------- BUILD SEQUENCE ----------
        self.seq.append(f)

        if len(self.seq) < 30:
            return "collecting", 0

        if len(self.seq) > 30:
            self.seq.pop(0)

        # ---------- PREPROCESS ----------
        seq = np.array(self.seq)
        seq = self.scaler.transform(seq)
        seq = np.expand_dims(seq, axis=0)

        # ---------- MODEL PREDICTION ----------
        pred = self.model.predict(seq, verbose=0)[0]
        cls = np.argmax(pred)
        conf = pred[cls]

        label = LABELS[cls]

        # =====================================================
        # 🔥 INTELLIGENT POST-FILTERING (KEY FIX)
        # =====================================================

        # ---------- MOTION GATE ----------
        # Squat requires movement → prevent idle misclassification
        if label == "squat":
            motion_energy = f[-2]   # index of motion_energy

            if motion_energy < 0.01:
                return "idle", conf

        # ---------- KNEE GUARD ----------
        # Fully straight leg ≠ squat
        if label == "squat":
            knee = f[-4]   # knee_mean

            if knee > 0.85:
                return "idle", conf
            
        #--- PUSHUP FIX -----#
        if label == "pushup":
            motion_energy = f[-2]   # index of motion_energy

            if motion_energy < 0.005:
                return "idle", conf

        # =====================================================
        # ---------- TEMPORAL SMOOTHING ----------
        # =====================================================
        self.window=deque(maxlen=12)  # reset window for new exercise
        self.window.append(cls)
        # weighted voting (recent frames matter more)
        weights = np.arange(1, len(self.window) + 1)
        scores = {}

        for i, c in enumerate(self.window):
            scores[c] = scores.get(c, 0) + weights[i]

        final_cls = max(scores, key=scores.get)

        return LABELS[final_cls], conf