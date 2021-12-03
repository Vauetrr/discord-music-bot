# discord-music-bot
A small project to make a discord music bot for a private discord server.

The program uses the discord, os, and youtube_dl libraries, and has dependencies on the asyncio library, pynacl library and ffmpeg.

The project's purpose was to improve skills relating to python and asynchronous programming.

# commands
The bot's commands use the prefix "bt ". The current commands are:

  * play [youtube url | search] - Apply the join command, then play the youtube track requested, or add the track to the playlist (if audio already playing)
  * join - Joins the voice channel of the user who invoked the command, otherwise joins the first voice channel it finds (if any)
  * leave - Leaves the currently joined voice channel (if in a voice channel)
  * pause - Pauses the music being played
  * resume - Resumes music that has been paused
  * stop - Stops the currently playing/paused music
  * skip - Skips the current track and plays the next one in the playlist (if any)
  * insert [youtube url | search] - Insert the youtube track at the top of the playlist
  * shuffle - Shuffle the order of the tracks in the playlist
  * help - Gives the user the list of commands the bot can do
