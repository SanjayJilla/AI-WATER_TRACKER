# 💧 AI Water Tracker

An intelligent hydration companion built to track daily water intake, provide AI-powered feedback, and build sustainable habits.

---

### Tools & Stack
The application is built with **Streamlit** for the interactive dashboard UI, **Python** and **Pandas** for data aggregation and visualization, **SQLite** for lightweight relational persistence, and the **Groq API** (`openai/gpt-oss-20b` via `WaterIntakeAgent`) configured with `python-dotenv` for real-time, actionable hydration insights.

### What the Memory Does
The memory layer is powered by a local SQLite database (`watertracker.db`) storing timestamped intake logs per user. This persistent memory allows the system to aggregate daily intake totals, generate 7-day rolling intake charts, calculate weekly averages, and power a "Gentle Streak" algorithm that preserves user habit momentum across sessions with a 1-day grace buffer.

### Honest Failure & Resolution
During initial integration, missing `GROQ_API_KEY` configurations and transient API timeouts caused unhandled exceptions that crashed the logging workflow. To resolve this, graceful fallback handling was implemented in `src/agent.py`: if the API key is missing or the network call fails, the database log completes uninterrupted and the UI renders a clear offline status message rather than breaking the application.

---

## 🚀 Getting Started

### 1. Installation
Clone the repository and install the dependencies:
```bash
pip install -r requirements.txt
```

### 2. Environment Configuration
Create a `.env` file in the project root and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```
*(Note: The app will continue to work for logging and tracking even without an API key).*

### 3. Run the Dashboard
Launch the Streamlit app:
```bash
streamlit run dashboard.py
```

---

## 📁 Project Structure
```text
WATER TRACKER/
├── assets/             # Media and static images
├── src/
│   ├── agent.py        # Groq-powered AI Hydration Agent
│   └── database.py     # SQLite persistence & streak calculation
├── dashboard.py        # Streamlit user interface
├── requirements.txt    # Project dependencies
├── .env                # Environment variables (API keys)
└── README.md           # Project documentation
```
