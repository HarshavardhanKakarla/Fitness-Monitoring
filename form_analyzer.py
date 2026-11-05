class FormAnalyzer:
    def analyze_squat(self,angles):

        knee=angles[2]
        shoulder=angles[6]

        feedback=[]
        quality="good"

        if knee>0.6:
            feedback.append("Go deeper")
            quality="bad"

        if shoulder<0.3:
            feedback.append("Chest up")
            quality="bad"

        if not feedback:
            feedback=["Good form"]

        return ", ".join(feedback),quality