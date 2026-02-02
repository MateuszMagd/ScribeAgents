# Discord Platform

## ffplay

ffplay is currently used for basic audio playback and debugging during development.  
This is a temporary solution and may be replaced by a more advanced audio processing approach in the future.

## How to start?

1. Create a Discord application and bot  
   Go to <https://discord.com/developers/applications> and create a new application.  
   Enable the Bot feature and copy the bot token.

2. Configure environment variables  
   Create a `.env` file (or copy `.env.example`) and set the Discord bot token.

3. Invite the bot to your server  
   Generate an OAuth2 URL with the following permissions:
   - View Channels
   - Connect
   - Speak

4. Start the bot  
   Run the application with the Discord platform selected:

       python main.py --platform_name discord

5. Join a voice channel  
   Once the bot is running, use a command in a text channel to make the bot join a voice channel and start listening.

## Commands

The following commands are currently supported by the Discord bot:

- `!join`  
  Makes the bot join the voice channel of the user who issued the command.

- `!leave`  
  Makes the bot leave the current voice channel.

- `!start`  
  Starts listening to the voice channel and begins audio processing.

- `!stop`  
  Stops listening and ends the current session.

Command prefix and exact behavior may change as the project evolves.
