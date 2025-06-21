# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import TextInput, TextOutput
from utils import interpret_command
from services import create_repo, schedule_event

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hey Render, I'm alive!"}

@app.post("/process_text", response_model=TextOutput)
async def process_text(input: TextInput):
    """Process user text command and return a response."""
    try:
        command = interpret_command(input.text)
        intent = command.get("intent", "").lower()
        params = command.get("params", {})

        if intent == "create_repo":
            name = params.get("name")
            if not name:
                return TextOutput(response="Please specify a repository name.")
            repo_url = create_repo(name)
            return TextOutput(response=f"Repository created: {repo_url}")

        elif intent == "schedule_event":
            summary = params.get("summary")
            time = params.get("time")
            if not summary or not time:
                return TextOutput(response="Please specify event summary and time.")
            event_url = schedule_event(summary, time)
            return TextOutput(response=f"Event scheduled: {event_url}")

        elif intent == "github_create_an_issue":
            from services import create_issue
            owner = params.get("owner")
            repo = params.get("repo")
            title = params.get("title")
            body = params.get("body")
            if not all([owner, repo, title]):
                return TextOutput(response="Please provide owner, repo, and title to create an issue.")
            url = create_issue(owner, repo, title, body)
            return TextOutput(response=f"Issue created: {url}")

        # You can add more intents below:
        # elif intent == "github_star_a_repository_for_the_authenticated_user":
        # elif intent == "github_list_repositories_for_a_user":

        else:
            return TextOutput(response=f"Sorry, I didn’t understand that command.\n(Parsed intent: {intent})")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)