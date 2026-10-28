from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from constant import GOOGLE_LLM_MODEL_NAME

llm = ChatGoogleGenerativeAI(model=GOOGLE_LLM_MODEL_NAME)


