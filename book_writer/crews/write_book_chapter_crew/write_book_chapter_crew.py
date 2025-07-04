"""
Write Book Chapter Crew
"""

import os

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from book_writer.constants import WRITE_BOOK_CHAPTER_MODEL_NAME as MODEL_NAME
from book_writer.custom_types import Chapter

load_dotenv()


@CrewBase
class WriteBookChapterCrew:
    """Write Book Chapter Crew"""

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
        )

    @agent
    def writer(self) -> Agent:
        """
        The writer agent.
        """
        return Agent(
            config=self.agents_config["writer"],
            llm=self.llm,
        )

    @task
    def research_chapter(self) -> Task:
        """
        The research chapter task.
        """
        return Task(
            config=self.tasks_config["research_chapter"],
        )

    @task
    def write_chapter(self) -> Task:
        """
        The write chapter task.
        """
        return Task(config=self.tasks_config["write_chapter"], output_pydantic=Chapter)

    @crew
    def crew(self) -> Crew:
        """Creates the Write Book Chapter Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
