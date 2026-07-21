from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq

from dotenv import load_dotenv
import os
import asyncio

load_dotenv()


async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["mathserver.py"],
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            },
        }
    )

    # Load API Key
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    # Get MCP tools
    tools = await client.get_tools()

    # Create LLM
    model = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0
    )

    # Create ReAct Agent
    agent = create_react_agent(
        model=model,
        tools=tools
    )

    # Math Query
    math_response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What's (3 + 5) * 12?"
                }
            ]
        }
    )

    print("\nMath Response:\n")
    print(math_response["messages"][-1].content)

    # Weather Query
    weather_response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is the weather in Alappuzha?"
                }
            ]
        }
    )

    print("\nWeather Response:\n")
    print(weather_response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())