# ScribeAgents - What is that?
An open-source system of multiple scribe agents that listen to and document conversations on platforms like Discord.

# Setup

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



# Roadmap

