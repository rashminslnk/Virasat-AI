import os
import logging
import google.cloud.logging
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext
# IMPORTING FunctionTool IS REQUIRED
from google.adk.tools import FunctionTool
from google.adk.tools.langchain_tool import LangchainTool

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from google.cloud import datastore

# --- Setup Logging and Environment ---
cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()
load_dotenv()

model_name = os.getenv("MODEL")
PROJECT_ID = os.getenv("PROJECT_ID")
DB_ID = "genrash"

# --- Custom Heritage Tools ---

def add_prompt_to_state(tool_context: ToolContext, prompt: str) -> dict[str, str]:
    """Saves the user's heritage site request to the system state."""
    tool_context.state["PROMPT"] = prompt
    return {"status": "success"}

def manage_to_visit_list(tool_context: ToolContext, site_name: str) -> dict[str, str]:
    """Adds a heritage site to the persistent 'To-Visit' list in the database."""
    try:
        client = datastore.Client(project=PROJECT_ID, database=DB_ID)
        key = client.key("HeritageSite", site_name.strip().title())
        entity = datastore.Entity(key=key)
        entity.update({
            "site_name": site_name,
            "status": "Planned",
            "added_at": datastore.helpers.datetime.datetime.now()
        })
        client.put(entity)
        return {"status": "success", "message": f"Saved {site_name} to your list."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def view_to_visit_list(tool_context: ToolContext) -> dict:
    """Retrieves and lists all heritage sites saved in the user's 'To-Visit' list."""
    try:
        client = datastore.Client(project=PROJECT_ID, database=DB_ID)
        query = client.query(kind="HeritageSite")
        results = list(query.fetch())
        if not results:
            return {"status": "success", "message": "Your list is empty."}
        sites = [entity["site_name"] for entity in results]
        return {"status": "success", "sites": sites}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Wikipedia Research Tool
wikipedia_tool = LangchainTool(tool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()))

# --- Multi-Agent Architecture ---

historian = Agent(
    name="heritage_historian",
    model=model_name,
    description="Researches historical facts.",
    instruction="Research the site in { PROMPT } using Wikipedia and summarize the history.",
    tools=[wikipedia_tool],
    output_key="historical_research"
)

itinerary_manager = Agent(
    name="itinerary_manager",
    model=model_name,
    description="Saves data to the database.",
    instruction="Save the site from { PROMPT } using manage_to_visit_list.",
    tools=[FunctionTool(manage_to_visit_list)], # Wrapped in FunctionTool
    output_key="db_confirmation"
)

heritage_workflow = SequentialAgent(
    name="heritage_workflow",
    sub_agents=[historian, itinerary_manager]
)

root_agent = Agent(
    name="virasat_guide",
    model=model_name,
    description="Virasat AI Entry Point.",
    instruction="""
    Welcome the user. 
    - If they want to SEE their list, use 'view_to_visit_list'. 
    - If they want to explore a site, use 'add_prompt_to_state' then heritage_workflow.
    """,
    # BOTH TOOLS WRAPPED CORRECTLY
    tools=[FunctionTool(add_prompt_to_state), FunctionTool(view_to_visit_list)],
    sub_agents=[heritage_workflow]
)