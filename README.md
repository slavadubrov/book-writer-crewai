# book-writer-crewai

This is a simple example project written to demonstrate the use of the CrewAI framework together with a server search agent framework.

## Overview

**book-writer-crewai** orchestrates autonomous AI agents to outline and write book chapters. It leverages CrewAI for building collaborative agent workflows and [uv](https://github.com/astral-sh/uv) for fast, modern Python dependency management.

- **CrewAI**: A framework for orchestrating role-playing, autonomous AI agents. It enables agents to work together seamlessly, tackling complex tasks like outlining and writing book content.
- **uv**: An extremely fast Python package and project manager, written in Rust. It replaces tools like pip and poetry, offering 10-100x faster performance for dependency management and virtual environments.

## Features

- Define and run collaborative agent crews for outlining and writing books
- YAML-based configuration for agents and tasks
- Fast, reproducible Python environments with uv

## Quick Start

1. **Install dependencies** (requires Python >=3.13):

   ```sh
   uv sync
   ```

2. **Configure environment variables**:

   Copy `.env-example` to `.env` and fill in your OpenAI and Serper API keys:

   ```sh
   cp .env-example .env
   # Edit .env and provide your keys
   ```

   The `.env` file should look like:

   ```env
   OPENAI_API_KEY=YOUR_OPENAI_API_KEY
   SERPER_API_KEY=YOUR_SERPER_API_KEY
   ```

3. **Run the main script**:

   ```sh
   uv run main.py
   ```

4. **Project structure**:
   - `book_writer/crews/outline_book_crew/` – Crew and config for outlining the book
   - `book_writer/crews/write_book_chapter_crew/` – Crew and config for writing chapters

## Pre-commit Hooks

This project uses [pre-commit](https://pre-commit.com/) to ensure code quality and consistency. To set up pre-commit hooks, run:

```sh
pre-commit install
```

This will automatically check and format your code on every commit, including checks for trailing whitespace, YAML/JSON validity, code formatting (ruff, isort), and more.

## References

- [CrewAI Documentation](https://github.com/crewaiinc/crewai)
- [uv Documentation](https://github.com/astral-sh/uv)
