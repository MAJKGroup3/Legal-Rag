# app/agents/legalrag_agent.py
from __future__ import annotations

from typing import Any, Dict

from langchain.agents import create_agent
from langchain_aws import ChatBedrock

from app.core.config import Config
from app.agents.tools import rag_query, get_weather


SYSTEM_PROMPT = (
    "You are an AI assistant helping a user understand EULA and Terms of Service documents.\n"
    "Rules:\n"
    "- Use rag_query to fetch relevant excerpts when needed.\n"
    "- Use ONLY excerpts to answer.\n"
    "- If not supported by excerpts, reply exactly: 'I don't know'\n"
    "- Explain legal terms plainly and reference section labels when present.\n"
    "- Use weather_tool only for weather questions.\n"
)


def build_agent():
    # Create a Bedrock chat model instance
    model = ChatBedrock(
        model_id=Config.BEDROCK_MODEL_ID,
        region_name=Config.AWS_REGION,
    )

    tools = [rag_query, get_weather]

    # LangChain v1 agent runtime
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )

    return agent


def extract_agent_text(result: Any) -> str:
    """
    LangChain v1 agents typically return a dict with a 'messages' list.
    This helper extracts the last assistant message content robustly.
    """
    if isinstance(result, dict):
        # Most common: {"messages": [...]} where last is assistant output
        msgs = result.get("messages")
        if isinstance(msgs, list) and msgs:
            last = msgs[-1]
            # messages can be dicts: {"role":"assistant","content":"..."}
            if isinstance(last, dict) and "content" in last:
                return last["content"]
            # or message objects with .content
            if hasattr(last, "content"):
                return last.content

        # Fallbacks some runtimes provide
        if "output" in result and isinstance(result["output"], str):
            return result["output"]
        if "content" in result and isinstance(result["content"], str):
            return result["content"]

    # If it’s already a string, return it
    if isinstance(result, str):
        return result

    return str(result)


def extract_agent_response(result: Any) -> Dict[str, Any]:
    """
    Extracts answer and retrieved chunks from agent result.
    Scans the message history for successful rag_query tool outputs.
    """
    import json
    from langchain_core.messages import ToolMessage
    
    answer = extract_agent_text(result)
    retrieved_chunks = []
    num_chunks = 0
    
    if isinstance(result, dict) and "messages" in result:
        # Iterate through messages to find tool outputs
        # We look for ToolMessage coming from 'rag_query'
        for msg in reversed(result["messages"]):
            if isinstance(msg, ToolMessage) and msg.name == "rag_query":
                try:
                    content = msg.content
                    # Content can be a dictionary or a JSON string
                    if isinstance(content, str):
                        data = json.loads(content)
                    else:
                        data = content
                        
                    if isinstance(data, dict):
                        retrieved_chunks = data.get("retrieved_chunks", [])
                        num_chunks = data.get("num_chunks", 0)
                        # We found the latest RAG query result
                        break
                except Exception:
                    # If parsing fails, just continue
                    continue

    return {
        "answer": answer,
        "retrieved_chunks": retrieved_chunks,
        "num_chunks": num_chunks
    }