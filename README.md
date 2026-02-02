# ScribeAgents - What is that?

This project aims to build an AI Scribe that listens to conversations on a channel and automatically creates a text file containing the full dialogue from a session. The generated transcript can later be reviewed, edited, annotated, or used to refine important parts of the conversation.

## Setup

## Prerequisites

- Python 3.10+
- Discord Bot Token ([How to get one](https://discord.com/developers/applications))

## Installation

1. Clone the repository:

```bash
git clone https://github.com/MateuszMagd/ScribeAgents.git
cd ScribeAgents
```

2. Create and activate virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables:

```bash
# Copy the example file
cp .env.example .env
# Edit .env and add your Discord bot token
```

5. Run the bot:

```bash
python main.py --platform_name discord --save_audio
```

## Flags

--platform_name - This flag run corresponding to platform_name bot - for example discord run discord bot.
Current options:

1. discord

--save_audio - saves audio file.

## Roadmap

Yes
