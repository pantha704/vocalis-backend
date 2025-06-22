# backend/services.py
from composio import ComposioToolSet, App, Action
from config import COMPOSIO_API_KEY
import uuid

# Initialize Composio ToolSet
toolset = ComposioToolSet(api_key=COMPOSIO_API_KEY)
tools = toolset.validate_tools(apps=[App.GITHUB])

def generate_uuid() -> str:
    """Generate a new UUID string."""
    return str(uuid.uuid4())

def create_repo(name: str, private: bool) -> str:
    """Create a GitHub repository."""
    try:
        response = toolset.execute_action(
            action="GITHUB_CREATE_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER",  # String-based action identifier
            params={"name": name, "private": private or False}
        )
        return response.get('html_url', 'Error: No URL returned')
    except Exception as e:
        raise Exception(f"Failed to create repository: {str(e)}")

def list_repositories(user: str) -> str:
    """List GitHub repositories for a user."""
    try:
        response = toolset.execute_action(
            action="github_list_repositories_for_a_user",
            params={"user": user}
        )
        repos = response.get('data', [])
        if not repos:
            return f"No repositories found for user {user}."
        return "\n".join([f"{repo['name']}: {repo['html_url']}" for repo in repos])
    except Exception as e:
        raise Exception(f"Failed to list repositories: {str(e)}")
    
    
def create_issue(owner: str, repo: str, title: str, body: str) -> str:
    try:
        print("Calling Composio with:", owner, repo, title, body)
        response = toolset.execute_action(
            action=Action.GITHUB_CREATE_AN_ISSUE,
            params={
                "owner": owner,
                "repo": repo,
                "title": title,
                "body": body
            }
        )
    except Exception as e:
        return f"Failed to create issue: {str(e)}"
    
    if not response.get("successful"):
        return f"Issue creation failed: {response.get('error', 'Unknown error')}"

    issue_url = response.get("data", {}).get("html_url")
    if issue_url:
        return f"Issue created successfully: {issue_url}"
    else:
        return "Issue created but no URL returned (weird af 🤔)"


def schedule_event(summary: str, time: str) -> str:
    """Schedule a Google Calendar event."""
    try:
        response = toolset.execute_action(
            action="googlecalendar_create_event",
            params={
                "summary": summary,
                "start_time": time,
                "end_time": time
            }
        )
        return response.get('html_url', 'Error: No URL returned')
    except Exception as e:
        raise Exception(f"Failed to schedule event: {str(e)}")
    
def check_weather(location: str) -> str:
    """Check the weather for a given location."""
    try:
        response = toolset.execute_action(
            action="weathermap_weather",
            params={"location": location}
        )
        return response.get('data', {}).get('weather', 'No weather data available')
    except Exception as e:
        raise Exception(f"Failed to check weather: {str(e)}")
    
def multi_app_action(actions: list) -> str:
    """Execute multiple actions in a single call."""
    try:
        responses = []
        for action in actions:
            response = toolset.execute_action(
                action=action['name'],
                params=action['params']
            )
            responses.append(response)
        return responses
    except Exception as e:
        raise Exception(f"Failed to execute multi-app actions: {str(e)}")
    
def notion_create_page(name: str) -> str:
    """Create a page in Notion."""
    print(generate_uuid())
    try:
        response = toolset.execute_action(
            action="NOTION_CREATE_NOTION_PAGE",
            params={
                "name": name,
                "parent_id": generate_uuid()  # Assuming you want to create it under a new parent ID
            }
        )
        return response.get('data', {}).get('url', 'Error: No URL returned')
    except Exception as e:
        raise Exception(f"Failed to create Notion page: {str(e)}")