# backend/utils.py
import json
import os
from pprint import pprint
from openai import OpenAI
from dotenv import load_dotenv
import uuid
def generate_uuid() -> str:
    return str(uuid.uuid4())

uid = generate_uuid()
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DEFAULT_ACTIONS = {
# GITHUB
    "create_repo": {
        "name": "GITHUB_CREATE_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER",
        "params": {"owner": "<owner>", "repo": "<repo>"}
    },
    "star_repo": {
        "name": "GITHUB_STAR_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER",
        "params": {"owner": "<owner>", "repo": "<repo>"}
    },
    "create_issue": {
        "name": "GITHUB_CREATE_AN_ISSUE",
        "params": {"owner": "<owner>", "repo": "<repo>", "title": "<title>", "body": "<body>"}
    },
    "list_repos": {
        "name": "github_list_repositories_for_a_user",
        "params": {"user": "<user>"}
    },
# WEATHER
    "check_weather": {
        "name": "weathermap_weather", 
        "params": {"location": "<location>"}
    }
}

def interpret_command(text: str) -> dict:
    examples = [
# GITHUB
        "'create a repo named xyz and make it public' -> {'intent': 'GITHUB_CREATE_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER', 'params': {'name': 'xyz', 'private': False}}",
        "'star the repo microsoft/vscode' -> {'intent': 'github_star_a_repository_for_the_authenticated_user', 'params': {'owner': 'microsoft', 'repo': 'vscode'}}",
        "'open an issue on facebook/react titled Bug and say it crashes' -> {'intent': 'github_create_an_issue', 'params': {'owner': 'facebook', 'repo': 'react', 'title': 'Bug', 'body': 'it crashes'}}",
        "'list repos for user pantha704' -> {'intent': 'github_list_repositories_for_a_user', 'params': {'user': 'pantha704'}}",
# WEATHER
        "'what's the weather in New York?' -> {'intent': 'weathermap_weather', 'params': {'location': 'New York'}}",
        "'check the weather in London' -> {'intent': 'weathermap_weather', 'params': {'location': 'London'}}",
# NOTION
        "'create a page in my Notion workspace with title My Page' -> {'intent': 'NOTION_CREATE_NOTION_PAGE', 'params': {'name': 'My Page'}}",        
# MULTIAPPS
          "'create fork of vercel/next.js and check the weather in Paris' -> ["
        "  {'intent': 'github_create_a_fork', 'params': {'owner': 'vercel', 'repo': 'next.js'}},"
        "  {'intent': 'weathermap_weather', 'params': {'location': 'Paris'}}",
        "'create fork of vercel/next.js and check the weather in Paris and create an issue on pantha704/basics-recap titled testing and say 1234' -> ["
        "  {'intent': 'github_create_a_fork', 'params': {'owner': 'vercel', 'repo': 'next.js'}},"
        "  {'intent': 'weathermap_weather', 'params': {'location': 'Paris'}}",
    ]

    prompt = (
        "You are an intent parser for GitHub commands. Convert natural language into a JSON object like "
        "{'intent': '...', 'params': {...}}.\n"
        "Examples:\n" +
        "\n".join(examples) +
        "\nIf you don't understand, return {'intent': 'unknown', 'params': {}}.\n\n"
        f"User command: {text}"
    )

    response = client.chat.completions.create(
        model="gpt-4o",  # or "gpt-3.5-turbo" for cheaper alt
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts structured JSON commands."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    # pprint(f"Response from OpenAI: {response}")
    return json.loads(response.choices[0].message.content)
