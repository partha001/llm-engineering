import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@tool
def get_restaurant_recommendations(location: str):
    """Provides a list of top restaurant recommendations for a given location."""
    recommendations = {
        "munich": ["Hofbräuhaus", "Augustiner-Keller", "Tantris"],
        "new york": ["Le Bernardin", "Eleven Madison Park", "Joe's Pizza"],
        "paris": ["Le Meurice", "L'Ambroisie", "Bistrot Paul Bert"],
    }
    return recommendations.get(location.lower(), ["No recommendations available for this location."])


# Bind tool to model
tools = [get_restaurant_recommendations]
llm = ChatOpenAI(model="gpt-4o-mini")  # or gpt-3.5-turbo-0125
llm_with_tools = llm.bind_tools(tools)

# Send user message
messages = [HumanMessage("Recommend some restaurants in Munich.")]
llm_output = llm_with_tools.invoke(messages)

print("LLM raw output:", llm_output)

# Handle tool call
tool_calls = llm_output.tool_calls

if tool_calls:
    tool_call = tool_calls[0]
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    print("\nRunning tool:", tool_name)
    print("With args:", tool_args)

    # Execute tool
    result = get_restaurant_recommendations.invoke(tool_args)
    print("\nTool result:", result)

    # Send back result to LLM
    tool_msg = ToolMessage(
        content=str(result),
        tool_call_id=tool_call["id"]
    )

    final_response = llm_with_tools.invoke([llm_output, tool_msg])

    print("\nFinal LLM response:")
    print(final_response.content)
else:
    # If the model directly responded without using a tool
    print("Direct LLM response:", llm_output.content)
