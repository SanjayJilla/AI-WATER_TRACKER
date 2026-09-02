import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class WaterIntakeAgent:
    def __init__(self, model="openai/gpt-oss-20b"):
        self.history = []
        self.api_key = GROQ_API_KEY or os.getenv("GROQ_API_KEY")
        self.model = model
        self.client = Groq(api_key=self.api_key) if self.api_key else None

    def analyze_intake(self, intake):
        if not self.client:
            return f"Hydration Status: You logged {intake} ml. Please configure GROQ_API_KEY in your .env file for AI insights."

        prompt = f"""You are a hydration assistant. The user has consumed {intake} ml of water today.
Provide a concise, actionable hydration status and suggest if they need to drink more water."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=250
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Logged {intake} ml. (AI analysis unavailable: {str(e)})"

if __name__ == "__main__":
    agent = WaterIntakeAgent()
    intake = 1500
    result = agent.analyze_intake(intake)
    print(f"Hydration Analysis:\n{result}")