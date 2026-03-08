import base64

import streamlit as st
import pandas as pd
from datetime import datetime
from src.agent import WaterIntakeAgent
from src.database import get_intake_history, log_intake


from PIL import Image
import streamlit as st
col1, col2 = st.columns([1,2])

with col1:
    st.image("assets/waterprog.webp", width=250)

with col2:
    st.title("💧 Smart Water Intake Tracker")
    st.markdown("Track your hydration, get AI feedback, and stay healthy.")

if "tracker_started" not in st.session_state:
    st.session_state.tracker_started = False

#Welcome section
if not st.session_state.tracker_started:
    st.set_page_config(
    page_title="AI Water Tracker",
    page_icon="💧",
    layout="wide"
)
    st.markdown("""
                Track your daily hydration with help of AI assisstant.
                log your intake, get smart feedback and stay healthy effortlessly""")
    if st.button("Start Tracking"):
        st.session_state.tracker_started = True
        st.rerun()
if st.session_state.tracker_started:
        st.subheader("Welcome to AI WATER TRACKER")

        #sidebar :Intake input
        st.sidebar.header("Log Your Water Intake")
        user_id=st.sidebar.text_input("User ID",value="SAMPLE USER",help="Enter your unique user ID")
        intake_ml=st.sidebar.number_input("Intake (ml)",min_value=0,value=250,step=50)
        if st.sidebar.button("Log Intake"):
            log_intake(user_id,intake_ml)
            st.sidebar.success(f"Logged {intake_ml} ml for {user_id}")

            agent=WaterIntakeAgent()
            analysis=agent.analyze_intake(intake_ml)
            st.info(f"Hydration Analysis: {analysis}")

        st.markdown("---")
        st.header("Your WaterIntake History")

        history=get_intake_history(user_id)
        if history:
                dates=[datetime.fromisoformat(row[0]) for row in history]
                values=[row[1] for row in history]
                df=pd.DataFrame({"Date":dates,"Intake (ml)":values})

                st.dataframe(df)
                st.line_chart(df.set_index("Date")["Intake (ml)"],width=700,height=400)

        st.sidebar.subheader("Daily Water Goal")

        daily_goal = st.sidebar.slider(
            "Set your daily goal (ml)",
            min_value=1000,
            max_value=5000,
            value=2500,
            step=100
        )
        today_total = sum(
            row[1] for row in history
            if datetime.fromisoformat(row[0]).date() == datetime.today().date()
        )

        progress = min(today_total / daily_goal, 1.0)

        st.subheader("Daily Hydration Progress")

        st.progress(progress)

        st.write(f"{today_total} ml / {daily_goal} ml")

        remaining = max(daily_goal - today_total, 0)

        if remaining > 0:
            st.warning(f"You still need {remaining} ml more to reach your daily goal!")

            if remaining <= 500:
                st.info("You're close to your goal! Consider drinking a glass of water soon.")  
        else:
            st.success("Congratulations! You've reached your daily hydration goal!")

        
        



