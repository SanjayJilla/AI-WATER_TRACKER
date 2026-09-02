import streamlit as st
import pandas as pd
from datetime import datetime
from src.agent import WaterIntakeAgent
from src.database import get_intake_history, log_intake, get_weekly_stats, get_gentle_streak

st.set_page_config(
    page_title="AI Water Tracker",
    page_icon="💧",
    layout="wide"
)

col1, col2 = st.columns([1, 3])
with col1:
    try:
        st.image("assets/waterprog.webp", width=180)
    except Exception:
        st.markdown("# 💧")

with col2:
    st.title("💧 Smart Water Intake Tracker")
    st.markdown("Track your hydration, get AI feedback, and build healthy habits with a gentle streak.")

if "tracker_started" not in st.session_state:
    st.session_state.tracker_started = False

# Welcome section
if not st.session_state.tracker_started:
    st.markdown("""
    Welcome to the **AI Water Tracker**!
    Track your daily hydration with the help of an AI assistant, monitor your weekly average, maintain a gentle streak, and stay healthy effortlessly.
    """)
    if st.button("🚀 Start Tracking"):
        st.session_state.tracker_started = True
        st.rerun()

if st.session_state.tracker_started:
    # Sidebar: Intake input & Goal settings
    st.sidebar.header("Log Your Water Intake")
    user_id = st.sidebar.text_input("User ID", value="SAMPLE USER", help="Enter your unique user ID")
    intake_ml = st.sidebar.number_input("Intake (ml)", min_value=0, value=250, step=50)

    daily_goal = st.sidebar.slider(
        "Set your daily goal (ml)",
        min_value=1000,
        max_value=5000,
        value=2500,
        step=100
    )

    if st.sidebar.button("Log Intake"):
        log_intake(user_id, intake_ml)
        st.sidebar.success(f"Logged {intake_ml} ml for {user_id}")

        agent = WaterIntakeAgent()
        analysis = agent.analyze_intake(intake_ml)
        st.info(f"💡 **AI Hydration Analysis:** {analysis}")

    # Fetch stats
    history = get_intake_history(user_id)
    weekly_breakdown, weekly_avg = get_weekly_stats(user_id, days=7)
    streak_info = get_gentle_streak(user_id, daily_goal=daily_goal)

    today_total = sum(
        row[1] for row in history
        if str(row[0])[:10] == datetime.today().strftime('%Y-%m-%d')
    ) if history else 0

    progress = min(today_total / daily_goal, 1.0) if daily_goal > 0 else 0

    # Top KPI Metrics Cards
    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="💧 Today's Intake", value=f"{today_total} ml", delta=f"{today_total - daily_goal} ml vs goal")
    with m2:
        st.metric(label="🎯 Daily Goal", value=f"{daily_goal} ml")
    with m3:
        st.metric(label="📊 7-Day Average", value=f"{weekly_avg} ml/day")
    with m4:
        st.metric(label="🔥 Gentle Streak", value=f"{streak_info['streak']} Days", delta=streak_info['badge'])

    # Gentle Streak Notice
    if streak_info['streak'] > 0:
        st.success(f"**{streak_info['badge']}**: {streak_info['message']}")
    else:
        st.info(f"🌱 {streak_info['message']}")

    # Daily Progress Bar
    st.subheader("Today's Hydration Progress")
    st.progress(progress)
    st.caption(f"**{today_total} ml** logged of **{daily_goal} ml** daily target ({int(progress * 100)}%)")

    remaining = max(daily_goal - today_total, 0)
    if remaining > 0:
        st.warning(f"You need **{remaining} ml** more to reach today's goal.")
    else:
        st.balloons()
        st.success("🎉 You've reached your daily hydration goal!")

    # 7-Day Weekly Breakdown Chart
    st.markdown("---")
    st.subheader("📅 Past 7 Days Hydration Trend")
    weekly_df = pd.DataFrame(weekly_breakdown)
    weekly_df.rename(columns={"day_name": "Day", "intake_ml": "Intake (ml)", "date": "Date"}, inplace=True)
    st.bar_chart(weekly_df.set_index("Day")["Intake (ml)"])

    # Full Intake History
    st.markdown("---")
    st.subheader("📋 Your Water Intake History")
    if history:
        dates = [str(row[0]) for row in history]
        values = [row[1] for row in history]
        df = pd.DataFrame({"Timestamp": dates, "Intake (ml)": values})
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No intake history recorded yet for this user. Log your first glass in the sidebar!")



        
        



