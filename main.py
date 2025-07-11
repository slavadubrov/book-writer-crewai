#!/usr/bin/env python
import asyncio

from crewai.flow.flow import Flow, listen, start
from dotenv import load_dotenv
from pydantic import BaseModel

from book_writer.crews.outline_book_crew.outline_crew import OutlineCrew
from book_writer.crews.write_book_chapter_crew.write_book_chapter_crew import (
    WriteBookChapterCrew,
)
from book_writer.custom_types import Chapter, ChapterOutline

load_dotenv()


class BookState(BaseModel):
    """
    The state of the book flow.
    """

    id: str = ""  # Required by CrewAI Flow
    title: str = "Python Design Patterns for Machine Learning"
    book: list[Chapter] = []
    book_outline: list[ChapterOutline] = []
    topic: str = "Python Design Patterns for Machine Learning"
    goal: str = (
        "The goal of this book is to provide a comprehensive overview with "
        "examples of the most common design patterns used in machine learning. "
        "It will be a practical guide with real-world examples and use cases. "
        "It will be written in a way that is easy to understand and "
        "follow."
    )


class BookFlow(Flow[BookState]):
    """
    The book flow.
    """

    initial_state = BookState

    @start()
    def generate_book_outline(self):
        """
        Generate the book outline.
        """
        print("Kickoff the Book Outline Crew")
        output = (
            OutlineCrew()
            .crew()
            .kickoff(
                inputs={
                    "topic": self.state.topic,
                    "goal": self.state.goal,
                }
            )
        )

        chapters = output["chapters"]
        print("Chapters:", chapters)

        self.state.book_outline = chapters
        return chapters

    @listen(generate_book_outline)
    async def write_chapters(self):
        """
        Write the book chapters.
        """
        print("Writing Book Chapters")
        tasks = []

        async def write_single_chapter(chapter_outline):
            output = (
                WriteBookChapterCrew()
                .crew()
                .kickoff(
                    inputs={
                        "goal": self.state.goal,
                        "topic": self.state.topic,
                        "chapter_title": chapter_outline.title,
                        "chapter_description": chapter_outline.description,
                        "book_outline": [
                            chapter_outline.model_dump_json()
                            for chapter_outline in self.state.book_outline
                        ],
                    }
                )
            )
            title = output["title"]
            content = output["content"]
            chapter = Chapter(title=title, content=content)
            return chapter

        for chapter_outline in self.state.book_outline:
            print(f"Writing Chapter: {chapter_outline.title}")
            print(f"Description: {chapter_outline.description}")
            # Schedule each chapter writing task
            task = asyncio.create_task(write_single_chapter(chapter_outline))
            tasks.append(task)

        # Await all chapter writing tasks concurrently
        chapters = await asyncio.gather(*tasks)
        print("Newly generated chapters:", chapters)
        self.state.book.extend(chapters)

        print("Book Chapters", self.state.book)

    @listen(write_chapters)
    async def join_and_save_chapter(self):
        """
        Join and save the book chapters.
        """
        print("Joining and Saving Book Chapters")
        # Combine all chapters into a single markdown string
        book_content = ""

        for chapter in self.state.book:
            # Add the chapter title as an H1 heading
            book_content += f"# {chapter.title}\n\n"
            # Add the chapter content
            book_content += f"{chapter.content}\n\n"

        # The title of the book from self.state.title
        book_title = self.state.title

        # Create the filename by replacing spaces with underscores and adding .md extension
        filename = f"./{book_title.replace(' ', '_')}.md"

        # Save the combined content into the file
        with open(filename, "w", encoding="utf-8") as file:
            file.write(book_content)

        print(f"Book saved as {filename}")
        return book_content


def kickoff():
    """
    Kickoff the book flow.
    """
    poem_flow = BookFlow()
    poem_flow.kickoff()


def plot():
    """
    Plot the book flow.
    """
    poem_flow = BookFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
