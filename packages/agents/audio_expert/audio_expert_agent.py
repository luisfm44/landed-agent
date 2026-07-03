from google.adk.agents import Agent

from packages.tools import retrieve_knowledge

audio_expert_agent = Agent(
    name="audio_expert",
    model="gemini-2.5-flash",
    instruction="""
You provide audio product buying guidance for headphones, speakers, DACs, microphones, and related gear.
Always answer in Spanish and explain tradeoffs clearly.
""",
    tools=[retrieve_knowledge],
)
