import streamlit as st
import cv2, time, os
import pandas as pd
import mediapipe as mp

from feature_extractor import FeatureExtractor
from classifier import ExerciseClassifier
from rep_counter import RepCounter
from form_analyzer import FormAnalyzer
from pose_draw import draw_pose

st.set_page_config(layout="centered")

st.markdown(
    "<h1 style='text-align: center;'>🏋️ AI Fitness Trainer</h1>",
    unsafe_allow_html=True
)

# ---------- SESSION STATE ----------
if "running" not in st.session_state:
    st.session_state.running = False
    st.session_state.start_time = None
    st.session_state.end_time = None
    st.session_state.reps = {"squat": 0, "pushup": 0, "pullup": 0}
    st.session_state.session_done = False
    st.session_state.exercise_counts = {"squat":0,"pushup":0,"pullup":0}

# ---------- TABS ----------
tab1, tab2 = st.tabs(["Session", "Data"])

# =====================================================
# SESSION TAB
# =====================================================
with tab1:
    

    col1, col2, col3 = st.columns(3)

    if col1.button("Start"):
        st.session_state.running = True
        st.session_state.start_time = time.time()
        st.session_state.reps = {"squat": 0, "pushup": 0, "pullup": 0}
        st.session_state.exercise_counts = {"squat":0,"pushup":0,"pullup":0}
        st.session_state.session_done = False

    if col2.button("Stop",type="primary"):
        if st.session_state.running:
            st.session_state.running = False
            st.session_state.end_time = time.time()
            st.session_state.session_done = True

    if col3.button("Cancel"):
        st.session_state.running = False
        st.session_state.session_done = False
        st.session_state.reps = {"squat": 0, "pushup": 0, "pullup": 0}

    frame_window = st.empty()

    cap = cv2.VideoCapture(0)
    pose = mp.solutions.pose.Pose()

    extractor = FeatureExtractor()
    classifier = ExerciseClassifier()
    counter = RepCounter()
    analyzer = FormAnalyzer()

    frame_id = 0

    if st.session_state.running:

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_id += 1
            frame = cv2.resize(frame, (640, 480))

            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            res = pose.process(img)

            if res.pose_landmarks:

                f, _, angles = extractor.extract(res.pose_landmarks.landmark)
                exercise, conf = classifier.predict(f)

                # track dominant exercise
                if exercise in st.session_state.exercise_counts:
                    st.session_state.exercise_counts[exercise] += 1

                feedback, quality = ("", "good")
                if exercise == "squat":
                    feedback, quality = analyzer.analyze_squat(angles)

                reps = counter.update(exercise, angles, frame_id, quality)
                st.session_state.reps = reps

                frame = draw_pose(frame, res.pose_landmarks.landmark, angles)

                cv2.putText(frame, f"{exercise} ({conf:.2f})",
                            (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                cv2.putText(frame, f"S:{reps['squat']} P:{reps['pushup']} PU:{reps['pullup']}",
                            (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)

                cv2.putText(frame, feedback,
                            (10, 110),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            frame_window.image(frame,channels="BGR", use_column_width=True)

            if not st.session_state.running:
                break

        cap.release()

    # ---------- SUMMARY ----------
    if st.session_state.session_done:

        duration = int(st.session_state.end_time - st.session_state.start_time)

        main_exercise = max(
            st.session_state.exercise_counts,
            key=st.session_state.exercise_counts.get
        )

        st.subheader("Session Summary")

        st.write(f"⏱ Duration: {duration} sec")
        st.write(f"Squat: {st.session_state.reps['squat']}")
        st.write(f"Pushup: {st.session_state.reps['pushup']}")
        st.write(f"Pullup: {st.session_state.reps['pullup']}")

        col1, col2 = st.columns(2)

        if col1.button("💾 Save Session"):

            data = {
                "time": time.strftime("%Y-%m-%d %H:%M"),
                "duration": duration,
                "squat": st.session_state.reps["squat"],
                "pushup": st.session_state.reps["pushup"],
                "pullup": st.session_state.reps["pullup"]
            }

            df = pd.DataFrame([data])

            if os.path.exists("sessions.csv"):
                df.to_csv("sessions.csv", mode="a", header=False, index=False)
            else:
                df.to_csv("sessions.csv", index=False)

            st.success("Session Saved")
            st.session_state.session_done = False

        if col2.button("Discard"):
            st.session_state.session_done = False
            st.session_state.reps = {"squat": 0, "pushup": 0, "pullup": 0}

# =====================================================
# DATA TAB
# =====================================================
with tab2:

    st.subheader("📊 Previous Sessions")

    if os.path.exists("sessions.csv"):
        df = pd.read_csv("sessions.csv")
        
        st.dataframe(df, use_container_width=True,height=400)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Sessions", len(df))
        col2.metric("Avg Duration", int(df["duration"].mean()))
        col3.metric("Total Reps", int(df[["squat","pushup","pullup"]].sum().sum()))

        st.line_chart(df[["squat","pushup","pullup"]])

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download CSV",
            data=csv,
            file_name="sessions.csv",
            mime="text/csv"
        )

    else:
        st.info("No data yet")