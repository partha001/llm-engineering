import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@tool
def get_restaurant_recommendations(location: str):
    """Provides a list of top restaurant recommendations for a given location."""
    print("finding recommendations:")
    recommendations = {
        "munich": ["Hofbräuhaus", "Augustiner-Keller", "Tantris"],
        "new york": ["Le Bernardin", "Eleven Madison Park", "Joe's Pizza"],
        "paris": ["Le Meurice", "L'Ambroisie", "Bistrot Paul Bert"],
    }
    return recommendations.get(location.lower(), ["No recommendations available for this location."])


# TODO: Bind the tool to the model
tools = [get_restaurant_recommendations]
llm = ChatOpenAI()
llm_with_tools = llm.bind_tools(tools)


messages = [
    HumanMessage("Recommend some restaurants in Munich.")
]

#TODO: Invoke the llm
llm_output = llm_with_tools.invoke(messages) # the llm_output is of type langchain_core.messages.ai.AIMessage
print(llm_output)

# #program output:
# content='' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 19, 'prompt_tokens': 59, 'total_tokens': 78, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'id': 'chatcmpl-CiRMXK9bNraoHyBLEdS21QmN6CLZY', 'service_tier': 'default', 'finish_reason': 'tool_calls', 'logprobs': None} id='lc_run--42fc705e-2ed7-458f-bd8b-6825cf0c2d4a-0' tool_calls=[{'name': 'get_restaurant_recommendations', 'args': {'location': 'Munich'}, 'id': 'call_2MMlIpHb8Yv9Dk3m7EmuQdPT', 'type': 'tool_call'}] usage_metadata={'input_tokens': 59, 'output_tokens': 19, 'total_tokens': 78, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}




