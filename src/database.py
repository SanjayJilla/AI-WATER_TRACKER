import sqlite3
from datetime import datetime, timedelta

DB_NAME = 'watertracker.db'

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS water_intake (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            intake_ml INTEGER,
            date TEXT 
        )
    """)
    conn.commit()
    conn.close()

def log_intake(user_id, intake_ml):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    date_today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("INSERT INTO water_intake(user_id, intake_ml, date) VALUES (?, ?, ?)",
                   (user_id, intake_ml, date_today))
    conn.commit()
    conn.close()

def get_intake_history(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT date, intake_ml FROM water_intake WHERE user_id=? ORDER BY date ASC", (user_id,))
    results = cursor.fetchall()

    conn.close()
    return results

def get_daily_totals(user_id):
    """Returns a dict mapping date strings ('YYYY-MM-DD') to total ml for the user."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT date, intake_ml FROM water_intake WHERE user_id=?", (user_id,))
    rows = cursor.fetchall()
    conn.close()

    daily_totals = {}
    for date_str, intake in rows:
        day_key = date_str[:10]  # Extract 'YYYY-MM-DD'
        daily_totals[day_key] = daily_totals.get(day_key, 0) + intake
    return daily_totals

def get_weekly_stats(user_id, days=7):
    """Calculates daily breakdown and average intake over the past `days` days."""
    daily_totals = get_daily_totals(user_id)
    today = datetime.today().date()
    
    history_last_n = []
    for i in range(days - 1, -1, -1):
        day = today - timedelta(days=i)
        day_str = day.strftime('%Y-%m-%d')
        total_ml = daily_totals.get(day_str, 0)
        history_last_n.append({"date": day_str, "day_name": day.strftime('%a'), "intake_ml": total_ml})
    
    total_intake = sum(item["intake_ml"] for item in history_last_n)
    weekly_avg = round(total_intake / days) if days > 0 else 0
    return history_last_n, weekly_avg

def get_gentle_streak(user_id, daily_goal=2500, min_threshold_ratio=0.8):
    """
    Computes a 'Gentle Streak':
    - Qualifies days where intake >= 80% of goal (or at least logged).
    - Today is treated as in-progress (does not break streak if not yet reached).
    - Allows 1 Grace Day protection so a single missed day doesn't immediately wipe your hard work.
    """
    daily_totals = get_daily_totals(user_id)
    if not daily_totals:
        return {
            "streak": 0,
            "today_met": False,
            "grace_used": False,
            "badge": "🌱 Beginner",
            "message": "Start logging your water today to begin your streak!"
        }

    target_ml = daily_goal * min_threshold_ratio
    today_str = datetime.today().strftime('%Y-%m-%d')
    today_intake = daily_totals.get(today_str, 0)
    today_met = today_intake >= target_ml

    streak = 0
    grace_used = False
    
    # Check backwards starting from yesterday
    current_date = datetime.today().date() - timedelta(days=1)
    
    while True:
        day_str = current_date.strftime('%Y-%m-%d')
        day_intake = daily_totals.get(day_str, 0)
        
        if day_intake >= target_ml:
            streak += 1
            current_date -= timedelta(days=1)
        elif not grace_used and streak > 0:
            # 1 Grace day protection
            grace_used = True
            current_date -= timedelta(days=1)
        else:
            break

    # If today is already completed, add today to streak
    if today_met:
        streak += 1

    # Badges and gentle messaging
    if streak >= 14:
        badge = "🏆 Hydration Legend"
    elif streak >= 7:
        badge = "🌊 Wave Master"
    elif streak >= 3:
        badge = "💧 Flowing Well"
    elif streak >= 1:
        badge = "🌱 Fresh Sprout"
    else:
        badge = "✨ Ready to Start"

    if streak > 0 and grace_used:
        message = f"Protected by a Grace Day 🛡️! Keep hydrating today to maintain your {streak}-day streak."
    elif streak > 0:
        message = f"Awesome consistency! You're on a {streak}-day hydration streak! 🔥"
    else:
        message = "Drink water today to start your streak!"

    return {
        "streak": streak,
        "today_met": today_met,
        "grace_used": grace_used,
        "badge": badge,
        "message": message
    }

create_tables()


