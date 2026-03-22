from google.cloud import aiplatform

def create_agent(
    project_id: str,
    location: str,
    display_name: str,
):
    """Create a new conversational agent using Vertex AI Agent Builder."""
    aiplatform.init(project=project_id, location=location)

    # The agent is created through the Agent Builder interface
    # For programmatic creation, we use the Dialogflow CX API
    from google.cloud.dialogflowcx_v3 import AgentsClient, Agent

    client = AgentsClient()
    parent = f"projects/{project_id}/locations/{location}"

    agent = Agent(
        display_name=display_name,
        default_language_code="en",
        time_zone="America/New_York",
        description="A conversational AI agent for customer support",
        start_flow=None,  # Will use default start flow
        enable_stackdriver_logging=True,
    )

    created_agent = client.create_agent(parent=parent, agent=agent)
    print(f"Agent created: {created_agent.name}")
    return created_agent

# https://oneuptime.com/blog/post/2026-02-17-how-to-build-a-conversational-ai-agent-with-vertex-ai-agent-builder/view
