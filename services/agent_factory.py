from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_core.models import ModelInfo, ModelFamily
from autogen_agentchat.agents import AssistantAgent

from config import OLLAMA_MODEL, OLLAMA_BASE_URL
from services.data_provider import get_records,get_record_by_id

def create_business_analyst_agent():
    model_client = OllamaChatCompletionClient(
        model=OLLAMA_MODEL,
        host=OLLAMA_BASE_URL,
        model_info=ModelInfo(
            function_calling=True,
            vision=False,
            json_output=False,
            family=ModelFamily.UNKNOWN
        )
    )
    
    return AssistantAgent(
        name="Motomind",
        model_client=model_client,
        system_message="คุณคือ JR BUDDY เป็นผู้วิเคาะห์ความเสี่ยงข้อมูลของสุขภาพปอดของคุณ",
        tools=[get_records,get_record_by_id],
        reflect_on_tool_use=True
    )