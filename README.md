# ScribeAgents — What is it?

ScribeAgents is a project focused on building an AI Scribe that listens to conversations on a channel and automatically generates a text file containing the complete dialogue from a session. The resulting transcript can be reviewed later, edited, annotated, or used to refine and extract important parts of the conversation.

## Setup

## Prerequisites

- Python 3.10+
- Discord Bot Token (<https://discord.com/developers/applications>)

## Installation (basic)

1. Clone the repository:

```bash
    git clone https://github.com/MateuszMagd/ScribeAgents.git
    cd ScribeAgents
```

2. Create and activate a virtual environment:

```bash
    python -m venv .venv

    # Windows:
    .venv\Scripts\activate

    # Linux / macOS:
    source .venv/bin/activate
```

3. Install dependencies:

```bash
    pip install -r requirements.txt
```

4. Configure environment variables:

Edit the .env file and add your Discord bot token.

```bash
    cp .env.example .env
```

5. Run the bot:

```bash
    python main.py --platform_name discord --save_audio
```

## Running Bots

Each platform has its own documentation available in the /docs directory.

- Discord: ./docs/discord.md

## Command-line Flags

--platform_name  
Specifies which platform bot should be launched.

Currently supported platforms:
- discord

Example:

```bash
    python main.py --platform_name discord
```

--save_audio  
Enables saving the raw audio from the session to a file.

## Roadmap

### Stage 1 - Validation / Feasibility

The goal of this stage is to validate whether the idea is technically feasible, even on a single platform (starting with Discord).

This stage focuses on:

- early experiments, ✅

- proof-of-concept implementations, ✅

- minimal, often non-production-ready code. ✅

The scope is intentionally limited and not fully designed.

Result:
It has been confirmed that building such a bot is feasible on Discord, so the project can move forward to Stage 2

### Stage 2 - Basic System

Stage 2 – Core System

This stage introduces the actual foundation of the system.
The goal is to build a clean, testable, and extensible core that future platforms and features can rely on.

Core Features
1. Session Manager

The heart of the system. Responsible for managing recording and transcription sessions.

Responsibilities:

- creating and closing sessions,

- assigning unique session IDs,

- tracking session metadata (platform, users, timestamps, etc.),

- coordinating audio and transcript writers,

- providing a single entry point for saving and retrieving session data.

2. Audio Writer

Responsible for handling raw audio data.

Responsibilities:

- saving audio streams to disk,

- organizing audio files by session,

- supporting different audio formats (initially one, extensible later),

- optional buffering / chunking for long sessions.

3. Transcript Writer

Responsible for persisting text output.

Responsibilities:

- saving transcriptions to files,

- supporting different formats (e.g. .txt, .json, later .md),

- preserving timestamps and speaker information,

- appending or updating transcripts during an active session.

4. Platform Adapter (Core-level abstraction)

A thin abstraction layer between the core system and external platforms (Discord, later others).

Responsibilities:

- - normalizing platform-specific events (join, leave, audio start/stop),

providing a unified interface for the Session Manager,

- isolating Discord-specific logic from the core.

- Even if Discord is the only platform for now, this abstraction will prevent core pollution later.

5. Configuration System

Centralized configuration handling.

Responsibilities:

- loading configuration from files / environment variables,

- managing paths, audio settings, feature flags,

- providing typed and validated access to config values.

6. Logging & Diagnostics

Essential for debugging audio pipelines and long-running sessions.

Responsibilities:

- structured logging (per session),

- debug vs production log levels,

- optional session-scoped logs.

#### Testing Requirements

All core components must include tests:

- unit tests for each class,

- mocked platform adapters,

- file system operations tested in isolation,

- clear separation between pure logic and I/O.
