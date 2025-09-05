import os
from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	SerperDevTool,
	ScrapeWebsiteTool,
	WebsiteSearchTool,
	TavilySearchTool,
	GithubSearchTool
)
from comprehensive_curriculum_creator.tools.custom_tool import (
	FileOrganizerTool,
	ZipCreatorTool,
	ContentWriterTool
)
from comprehensive_curriculum_creator.tools.deep_research_tool import DeepResearchTool




@CrewBase
class ComprehensiveCurriculumCreatorCrew:
    """ComprehensiveCurriculumCreator crew"""

    
    @agent
    def curriculum_architect(self) -> Agent:
        
        return Agent(
            config=self.agents_config["curriculum_architect"],
            tools=[
				SerperDevTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o",
                temperature=0.7,
            ),
        )
    
    @agent
    def subject_matter_researcher(self) -> Agent:
        # Build tools list conditionally based on available API keys
        tools = [
            SerperDevTool(),
            ScrapeWebsiteTool(),
            WebsiteSearchTool()
        ]

        # Only add TavilySearchTool if API key is available
        try:
            if os.getenv("TAVILY_API_KEY"):
                tools.append(TavilySearchTool())
        except ImportError:
            pass  # TavilySearchTool not available

        # Only add GitHub tool if token is available
        github_token = os.getenv("GITHUB_TOKEN")
        if github_token:
            tools.append(GithubSearchTool(
                gh_token=github_token,
                content_types=['code', 'repo', 'issue']
            ))

        # Add Deep Research Tool - always available (with graceful fallback)
        try:
            # Check if required API keys are available for deep research
            has_openai = bool(os.getenv("OPENAI_API_KEY"))
            has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))
            has_tavily = bool(os.getenv("TAVILY_API_KEY"))

            if has_openai or has_anthropic:  # At least one LLM provider
                tools.append(DeepResearchTool())
                print("✅ Deep Research Tool added to subject_matter_researcher")
            else:
                print("⚠️  Deep Research Tool not available - missing API keys")
                print("   Required: OPENAI_API_KEY or ANTHROPIC_API_KEY")
        except Exception as e:
            print(f"⚠️  Failed to initialize Deep Research Tool: {e}")
            print("   Continuing with standard research tools")

        return Agent(
            config=self.agents_config["subject_matter_researcher"],
            tools=tools,
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o",
                temperature=0.7,
            ),
        )
    
    @agent
    def learning_content_developer(self) -> Agent:
        
        return Agent(
            config=self.agents_config["learning_content_developer"],
            tools=[

            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o",
                temperature=0.7,
            ),
        )
    
    @agent
    def project_specialist(self) -> Agent:
        # Build tools list conditionally based on available API keys
        tools = [
            SerperDevTool(),
            WebsiteSearchTool()
        ]

        # Only add TavilySearchTool if API key is available
        try:
            if os.getenv("TAVILY_API_KEY"):
                tools.append(TavilySearchTool())
        except ImportError:
            pass  # TavilySearchTool not available

        # Only add GitHub tool if token is available
        github_token = os.getenv("GITHUB_TOKEN")
        if github_token:
            tools.append(GithubSearchTool(
                gh_token=github_token,
                content_types=['code', 'repo', 'issue']
            ))

        return Agent(
            config=self.agents_config["project_specialist"],
            tools=tools,
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o",
                temperature=0.7,
            ),
        )
    
    @agent
    def course_structure_organizer(self) -> Agent:

        return Agent(
            config=self.agents_config["course_structure_organizer"],
            tools=[
				FileOrganizerTool(),
				ZipCreatorTool(),
				ContentWriterTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o",
                temperature=0.7,
            ),
        )
    

    
    @task
    def create_curriculum_outline(self) -> Task:
        return Task(
            config=self.tasks_config["create_curriculum_outline"],
            markdown=False,
        )
    
    @task
    def continue_course_development(self) -> Task:
        return Task(
            config=self.tasks_config["continue_course_development"],
            markdown=False,
        )
    
    @task
    def research_course_content(self) -> Task:
        return Task(
            config=self.tasks_config["research_course_content"],
            markdown=False,
        )
    
    @task
    def design_project_based_activities(self) -> Task:
        return Task(
            config=self.tasks_config["design_project_based_activities"],
            markdown=False,
        )
    
    @task
    def develop_learning_materials(self) -> Task:
        return Task(
            config=self.tasks_config["develop_learning_materials"],
            markdown=False,
        )
    
    @task
    def organize_course_structure(self) -> Task:
        return Task(
            config=self.tasks_config["organize_course_structure"],
            markdown=False,
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the ComprehensiveCurriculumCreator crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
