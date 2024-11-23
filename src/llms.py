from crewai import LLM
import os

coding_question = LLM(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key=os.environ.get("OPENAI_API_KEY"),
)
