import os
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()

#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

#llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5, openai_api_key=OPENAI_API_KEY)
llm=ChatGroq(model="llama-3.1-8b-instant", temperature=0.5, groq_api_key=GROQ_API_KEY)

class WaterIntakeAgent:
    def __init__(self):
        self.history=[]
    def analyze_intake(self, intake):
        prompt=f"""
        You are a hydration assisstant.The User has consumed  {intake} ml of water today. 
        provide a hydration status and suggest if they need to drink more water.But keep the response concise and actionable.
        Give a brief analysis of their hydration level based on the intake and provide a recommendation.Give it in a way that user should understand clearly"""
        response=llm.invoke([HumanMessage(content=prompt)])
        return response.content.strip()
if __name__=="__main__":
    agent=WaterIntakeAgent()
    intake=1500
    result=agent.analyze_intake(intake)
    print(f"Hydration Analysis: {result}")
