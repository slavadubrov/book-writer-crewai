from pydantic import BaseModel


class ChapterOutline(BaseModel):
    """
    The outline of a chapter.
    """

    title: str
    description: str


class BookOutline(BaseModel):
    """
    The outline of a book.
    """

    chapters: list[ChapterOutline]


class Chapter(BaseModel):
    """
    A chapter of a book.
    """

    title: str
    content: str
