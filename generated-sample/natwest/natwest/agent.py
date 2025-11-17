# Agent Generated code
from google.adk.agents.llm_agent import Agent
from .tools import tool_list

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    tools=tool_list
)
        