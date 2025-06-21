try:
    from composio_openai import ComposioToolSet, Action, App
    print("Imports successful!")
except ImportError as e:
    print(f"Import failed: {e}")
from dotenv import load_dotenv
from pprint import pprint
import os
load_dotenv()

# Initialize ToolSet (assuming API key is in env)
toolset = ComposioToolSet()

### FETCHING TOOLS

## BY SINGLE/LIST OF ACTIONS -> RETURNS SINGLE SCHEMA FOR THAT ACTION / LIST OF SCHEMA FOR PROVIDING A LIST OF ACTIONS

# # Fetch only the tool for starring a GitHub repo
# github_star_tool = toolset.get_tools(
#     actions=[Action.GITHUB_STAR_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER]
# )

# pprint(github_star_tool)
# # Output will contain the schema for the specified action.

# --- 

## BY QUERY -> FINDS RELEVANT SET OF ACTIONS SCHEMA 

# # Describe the task
# query = "send a message on general channel in discord on my server"
# # Find relevant action ENUMS (Python-specific helper)
# relevant_actions = toolset.find_actions_by_use_case(
#     use_case=query,
#     apps=[App.DISCORD]
#     advanced=True # Use for complex queries needing multiple tools
# )
# pprint(f"Found relevant actions: {relevant_actions}")
# # Fetch the actual tool schemas for the found actions
# if relevant_actions:
#     github_tools = toolset.get_tools(actions=relevant_actions)
#     print(f"Fetched {len(github_tools)} tool(s) for the use case.")
# else:
#     print("No relevant actions found for the use case.")
# # Use the `notion_tools` in your agent

## BY APP -> PPROVIDES FIRST FEW IMPORTANT ACTIONS SCHEMA

# # Fetch default tools for the connected GitHub app
# github_tools = toolset.get_tools(actions=[Action.GITHUB_CREATE_AN_ISSUE])
# pprint(f"Fetched {(github_tools)} tools for GitHub.")
# # Output contains schemas for 'important' GitHub tools.


### EXECUTING TOOLS

print("Creating GitHub issue directly...")
try:
    result = toolset.execute_action(
        action=Action.GITHUB_CREATE_AN_ISSUE,
        params={
            "owner": "pantha704",  # Replace with actual owner
            "repo": "basics-recap",  # Replace with actual repo
            "title": "Improve UI",
            "body": "This UI literally sucks a 5yo can make better than this",
            # Other optional params like 'assignees', 'labels' can be added here
        },
        # entity_id="your-user-id" # Optional: Specify if not 'default'
    )
    if result.get("successful"):
        print("Successfully created issue!")
        # Issue details are often in result['data']
        print("Issue URL:", result.get("data", {}).get("html_url"))
    else:
        print("Failed to create issue:", result.get("error"))
except Exception as e:
    print(f"An error occurred: {e}")