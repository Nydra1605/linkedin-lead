"""CrewAI orchestration wiring all tools together."""
from crewai import Agent, Task, Crew, Process
from app.discovery import LinkedInSearchTool
from app.enrichment import EnrichmentTool
from app.scoring import LeadScoringTool
from app.personalization import MessageComposer
from app.sequencer import OutreachScheduler
from app.observability import logger

# -- Instantiate tools -------------------------------------------------------
discovery_tool = LinkedInSearchTool()
enrichment_tool = EnrichmentTool()
scoring_tool   = LeadScoringTool()
composer_tool  = MessageComposer()
scheduler_util = OutreachScheduler()

# -- Agents ------------------------------------------------------------------

discovery_agent = Agent(
    role="Prospect Discovery Specialist",
    goal="Find LinkedIn prospects matching ICP",
    backstory="SEO wizard who speaks fluent Boolean search.",
    tools=[discovery_tool],
)

enrichment_agent = Agent(
    role="Data Enricher",
    goal="Append firmographic & contact details",
    tools=[enrichment_tool],
)

scoring_agent = Agent(
    role="Lead Scorer",
    goal="Score and prioritise leads",
    tools=[scoring_tool],
)

personalisation_agent = Agent(
    role="Copywriter",
    goal="Write personalised, non‑spammy LinkedIn invites",
    tools=[composer_tool],
)

sequencer_agent = Agent(
    role="Sequencer",
    goal="Send messages at optimal times",
    tools=[scheduler_util],
)

# -- Tasks -------------------------------------------------------------------
search_task = Task(
    description="Search LinkedIn for prospects with query: {search_query}",
    agent=discovery_agent,
    output_json={"prospects": "list"},
)

enrich_task = Task(
    description="Enrich each prospect with Clearbit data",
    agent=enrichment_agent,
)

score_task = Task(
    description="Score prospects and select top 20%",
    agent=scoring_agent,
)

message_task = Task(
    description="Compose personalised connection invite for each top prospect",
    agent=personalisation_agent,
)

send_task = Task(
    description="Schedule and send the messages during business hours",
    agent=sequencer_agent,
)

# -- Crew --------------------------------------------------------------------
leadgen_crew = Crew(
    agents=[discovery_agent, enrichment_agent, scoring_agent, personalisation_agent, sequencer_agent],
    tasks=[search_task, enrich_task, score_task, message_task, send_task],
    process=Process.sequential,
)