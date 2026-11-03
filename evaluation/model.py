from deepeval.models import GeminiModel
from dotenv import load_dotenv

load_dotenv()

llm = GeminiModel("gemini-3.5-flash-lite")
