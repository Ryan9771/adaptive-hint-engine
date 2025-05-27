from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


class LLM_instance:
    """Singleton Class instance of the LangChain OpenAI llm"""

    @classmethod
    def get_instance(cls):
        return ChatOpenAI(model="gpt-4o", temperature=0.0)
