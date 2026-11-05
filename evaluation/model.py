from deepeval.models import GeminiModel, OpenAIModel
from dotenv import load_dotenv
from agent.constant import GOOGLE_LLM_MODEL_NAME, OPEN_AI_LLM_LUNA_MODEL_NAME

load_dotenv()

_gemini_llm = GeminiModel(GOOGLE_LLM_MODEL_NAME)
_luna_llm = OpenAIModel(OPEN_AI_LLM_LUNA_MODEL_NAME)
llm = _luna_llm
