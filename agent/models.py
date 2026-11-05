from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from constant import GOOGLE_LLM_MODEL_NAME, OPEN_AI_LLM_LUNA_MODEL_NAME

_gemini_llm = ChatGoogleGenerativeAI(model=GOOGLE_LLM_MODEL_NAME)
_luna_llm = ChatOpenAI(model=OPEN_AI_LLM_LUNA_MODEL_NAME)

llm = _luna_llm
