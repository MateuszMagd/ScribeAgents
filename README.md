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

Yes
