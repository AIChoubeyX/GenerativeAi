# from dotenv import load_dotenv
# load_dotenv()

# import os
# import requests

# from langchain_mistralai import ChatMistralAI
# from langchain.tools import tool
# from langchain_core.messages import HumanMessage, ToolMessage
# from tavily import TavilyClient

# # now lets create some tools
# # Weather tool

# @tool
# def get_weather(city : str) -> str:
#     """Get the current weather for a given city."""
#     API_KEY = os.getenv("OPENWEATHER_API_KEY")
#     url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
#     response = requests.get(url)
#     data = response.json()
    
#     print("DEBUG:", data)
    
#     if str(data.get("cod")) != "200":
#         return f"Error: {data.get('message', 'Unable to fetch weather data.')}"
    
#     temp = data["main"]["temp"]
#     desc = data["weather"][0]["description"]
    
#     return f"The current temperature in {city} is {temp}°C with {desc}."
    
# # tavily news tool

# tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# @tool
# def get_news(city :str) -> str:
#     """ Get latest news of the city"""
    
#     response = tavily_client.search (
#         query=f"latest news in {city}",
#         search_depth= "basic",
#         max_results=5
#     )
    
#     results = response.get("results", [])
#     if not results:
#         return f"No news found for {city}."
    
#     news_list =[]
    
#     for r in results :
#         title = r.get("title", "No title")
#         url = r.get("url", "")
#         snippet = r.get("content", "")
        
#         news_list.append(f"{title}\n{snippet}\nRead more: {url}")
    
#     return f"Latest news in {city}:\n\n" + "\n\n".join(news_list)  


# # llm creation

# llm = ChatMistralAI(model="mistral-small-2506")

# tools = {
#     "get_weather": get_weather,
#     "get_news": get_news
# }
# llm_with_tools = llm.bind_tools([get_weather, get_news])

# # agent loop - very imp

# messages = []

# print("Welcome to the City Info Agent! Ask me about the weather or news in any city.")
# print("Type 'exit' to quit.")

# while True:
#     user_input = input("You: ")
#     if user_input.lower() == "exit":
#         print("Goodbye!")
#         break
#     messages.append(HumanMessage(content=user_input))
    
#     while True:
#         result = llm_with_tools.invoke(messages)
#         messages.append(result)
        
#         # if tool is required
#         if result.tool_calls:
#             for tool_call in result.tool_calls:
#                 tool_name = tool_call['name']
#                 # human in the loop to execute the tool
#                 confirm = input(f"Do you want to execute the tool '{tool_name}'? (yes/no): ")
                
#                 if confirm.lower() == "no":
#                     print("Tool execution skipped.")
#                     break
#                 #excute tool
                
#                 tool_result = tools[tool_name].invoke(tool_call)
                
#                 messages.append(ToolMessage(
#                     content=tool_result,
#                     tool_call_id=tool_call['id']
#                 ))
#         continue
#     else:
#         print(f"Agent: {result.content}")
       
             
             
             
             # ==========================================
# STEP 1 : LOAD ENVIRONMENT VARIABLES
# ==========================================

from dotenv import load_dotenv
load_dotenv()

import os
import requests

# ==========================================
# STEP 2 : IMPORT LANGCHAIN + MISTRAL
# ==========================================

from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import (
    HumanMessage,
    ToolMessage
)

# Tavily for news search
from tavily import TavilyClient


# ==========================================
# STEP 3 : CREATE WEATHER TOOL
# ==========================================

@tool
def get_weather(city: str) -> str:
    """
    Get current weather of a city
    """

    API_KEY = os.getenv("OPENWEATHER_API_KEY")

    url = (
        f"http://api.openweathermap.org/data/2.5/weather?"
        f"q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)

    data = response.json()

    # Debugging response
    print("DEBUG WEATHER:", data)

    # Error handling
    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Unable to fetch weather')}"

    # Extract information
    temperature = data["main"]["temp"]
    description = data["weather"][0]["description"]

    return (
        f"The current temperature in {city} "
        f"is {temperature}°C with {description}."
    )


# ==========================================
# STEP 4 : CREATE NEWS TOOL
# ==========================================

# Tavily client setup
tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


@tool
def get_news(city: str) -> str:
    """
    Get latest news of a city
    """

    response = tavily_client.search(
        query=f"Latest news in {city}",
        search_depth="basic",
        max_results=5
    )

    results = response.get("results", [])

    if not results:
        return f"No news found for {city}"

    news_list = []

    for r in results:

        title = r.get("title", "No title")
        content = r.get("content", "")
        url = r.get("url", "")

        news_list.append(
            f"Title: {title}\n"
            f"Summary: {content}\n"
            f"Read More: {url}"
        )

    return "\n\n".join(news_list)


# ==========================================
# STEP 5 : CREATE LLM
# ==========================================

llm = ChatMistralAI(
    model="mistral-small-2506"
)


# ==========================================
# STEP 6 : BIND TOOLS TO LLM
# ==========================================

tools = {
    "get_weather": get_weather,
    "get_news": get_news
}

llm_with_tools = llm.bind_tools(
    [get_weather, get_news]
)


# ==========================================
# STEP 7 : START AGENT LOOP
# ==========================================

messages = []

print("\n===================================")
print("CITY INFO AI AGENT")
print("Ask weather or news of any city")
print("Type 'exit' to quit")
print("===================================\n")


while True:

    # --------------------------------------
    # USER INPUT
    # --------------------------------------

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    # Add user message to chat history
    messages.append(
        HumanMessage(content=user_input)
    )

    # --------------------------------------
    # AGENT THINKING LOOP
    # --------------------------------------

    while True:

        # LLM generates response
        result = llm_with_tools.invoke(messages)

        # Save AI response
        messages.append(result)

        # ----------------------------------
        # IF TOOL CALL IS NEEDED
        # ----------------------------------

        if result.tool_calls:

            for tool_call in result.tool_calls:

                tool_name = tool_call["name"]

                # Ask user permission
                confirm = input(
                    f"\nDo you want to execute "
                    f"'{tool_name}' ? (yes/no): "
                )

                if confirm.lower() != "yes":

                    print("Tool execution skipped.")

                    messages.append(
                        ToolMessage(
                            content="Tool execution denied by user.",
                            tool_call_id=tool_call["id"]
                        )
                    )

                    continue

                # ----------------------------------
                # EXECUTE TOOL
                # ----------------------------------

                print(f"\nExecuting {tool_name}...\n")

                tool_result = tools[tool_name].invoke(
                    tool_call["args"]
                )

                # Add tool result to messages
                messages.append(
                    ToolMessage(
                        content=tool_result,
                        tool_call_id=tool_call["id"]
                    )
                )

            # Continue loop so LLM can read tool output
            continue

        # ----------------------------------
        # FINAL RESPONSE
        # ----------------------------------

        print(f"\nAgent: {result.content}\n")

        break
    
    
