"""
Outline Crew
"""

import os

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from book_writer.constants import OUTLINE_BOOK_MODEL_NAME as MODEL_NAME
from book_writer.custom_types import BookOutline

load_dotenv()


@CrewBase
class OutlineCrew:
    """Book Outline Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    llm = ChatOpenAI(model=MODEL_NAME)

    @agent
    def researcher(self) -> Agent:
        """
        The researcher agent.
        """
        serper_api_key = os.getenv("SERPER_API_KEY")
        search_tool = (
            SerperDevTool(api_key=serper_api_key) if serper_api_key else SerperDevTool()
        )
        return Agent(
            config=self.agents_config["researcher"],
            tools=[search_tool],
            llm=self.llm,
            verbose=True,
        )

    @agent
    def outliner(self) -> Agent:
        """
        The outliner agent.
        """
        return Agent(
            config=self.agents_config["outliner"],
            llm=self.llm,
            verbose=True,
        )

    @task
    def research_topic(self) -> Task:
        """
        The research topic task.
        """
        return Task(
            config=self.tasks_config["research_topic"],
        )

    @task
    def generate_outline(self) -> Task:
        """
        The generate outline task.
        """
        return Task(
            config=self.tasks_config["generate_outline"], output_pydantic=BookOutline
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Book Outline Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
