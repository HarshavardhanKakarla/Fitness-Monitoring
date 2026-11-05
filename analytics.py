import pandas as pd
import streamlit as st

def show_analytics():
    try:
        df = pd.read_csv("workout_log.csv")

        st.subheader("Workout History")
        st.dataframe(df)

        st.subheader("Total Reps per Exercise")
        summary = df.groupby("exercise")["reps"].sum()
        st.bar_chart(summary)

    except:
        st.warning("No data available")