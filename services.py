# backend/services.py
from composio import ComposioToolSet, App, Action
from config import COMPOSIO_API_KEY

# Initialize Composio ToolSet
toolset = ComposioToolSet(api_key=COMPOSIO_API_KEY)
tools = toolset.validate_tools(apps=[App.GITHUB])

def create_repo(name: str) -> str:
    """Create a GitHub repository."""
    try:
        response = toolset.execute_action(
            action="github_create_repository",  # String-based action identifier
            params={"name": name, "private": False}
        )
        return response.get('html_url', 'Error: No URL returned')
    except Exception as e:
        raise Exception(f"Failed to create repository: {str(e)}")

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