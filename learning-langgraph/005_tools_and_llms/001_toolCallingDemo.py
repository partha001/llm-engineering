import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@tool
def get_restaurant_recommendation(location: str):
    """Provides a list of top restaurant recommendation for a given location."""
    recommendations = {
        "munich": ["Hofbrauhauss", "Augustiner-Keller", "Tantris"],
        "new york": ["Le Bernardin","Eleven Madison Park", "Joe's Pizza"],
        "paris": ["Le Meurice", "L'Ambroisie","Bistrot Paul Bert"]
    }
    return recommendations.get(location.lower(), ["No recommendations available for this location"])

#binding the tool with the model
tools = [get_restaurant_recommendation]
llm = ChatOpenAI(model = "gpt-4o", api_key=OPENAI_API_KEY)
llm_with_tools = llm.bind_tools(tools)

messages = [
    HumanMessage("Recommend some restaurants in Munich")
]


llm_output = llm_with_tools.invoke(messages)
print(llm_output)

# #this gives the below output
# content='' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 19, 'prompt_tokens': 58, 'total_tokens': 77, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_689bad8e9a', 'id': 'chatcmpl-Chyyx1ihAF71wiWlosg2HPO17Rw5G', 'service_tier': 'default', 'finish_reason': 'tool_calls', 'logprobs': None} id='lc_run--21dfc4e0-487b-421d-bebb-a35f3d911af1-0' tool_calls=[{'name': 'get_restaurant_recommendation', 'args': {'location': 'Munich'}, 'id': 'call_yxI8svyCDP4gnHsXyd9KGW2x', 'type': 'tool_call'}] usage_metadata={'input_tokens': 58, 'output_tokens': 19, 'total_tokens': 77, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}