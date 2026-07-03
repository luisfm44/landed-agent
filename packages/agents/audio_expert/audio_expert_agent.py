from google.adk.agents import Agent

from packages.agents.audio_expert.prompts import AUDIO_EXPERT_INSTRUCTIONS
from packages.shared.config import REASONING_AGENT_MODEL
from packages.tools import retrieve_knowledge

audio_expert_agent = Agent(
    name="audio_expert",
    model=REASONING_AGENT_MODEL,
    instruction=AUDIO_EXPERT_INSTRUCTIONS,
    tools=[retrieve_knowledge],
)
