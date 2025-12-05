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
print("LLM raw output:", llm_output)


# Build a lookup dictionary for dynamic tool invocation
tool_map = {t.name: t for t in tools}
tool_calls = llm_output.tool_calls

if tool_calls:
    tool_call = tool_calls[0]
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    print("\nRunning tool:", tool_name)
    print("With args:", tool_args)

    # ✅ Dynamically invoke the correct tool
    if tool_name in tool_map:
        tool_fn = tool_map[tool_name]
        result = tool_fn.invoke(tool_args)
    else:
        raise ValueError(f"Tool '{tool_name}' not found among registered tools.")

    print("\nTool result:", result)
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