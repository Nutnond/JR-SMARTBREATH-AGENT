from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_core.models import ModelInfo, ModelFamily
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config import OLLAMA_MODEL, OLLAMA_BASE_URL,OPEN_AI_API_KEY
from services.data_provider import get_records,get_record_by_id

def create_business_analyst_agent():
    # model_client = OllamaChatCompletionClient(
    #     model=OLLAMA_MODEL,
    #     host=OLLAMA_BASE_URL,
    #     model_info=ModelInfo(
    #         function_calling=True,
    #         vision=False,
    #         json_output=False,
    #         family=ModelFamily.UNKNOWN
    #     )
    # )

    model_client = OpenAIChatCompletionClient(
        model="gpt-5-mini",
        api_key=OPEN_AI_API_KEY,
    )
    
    return AssistantAgent(
        name="JR_BUDDY",
        model_client=model_client,
        system_message="คุณคือ JR BUDDY เป็นผู้วิเคาะห์ความเสี่ยงข้อมูลของสุขภาพปอดของคุณ",
        tools=[get_records,get_record_by_id],
        reflect_on_tool_use=True
    )