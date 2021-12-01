# discord-music-bot
A small project to make a discord music bot for a private discord server.

The program uses the discord, os, and youtube_dl libraries, and has dependencies on the pynacl library and ffmpeg.

# commands
The bot's commands use the prefix "bt ". The current commands are:

  * play [youtube url] - Apply the join command, then play the audio of the youtube url
  * join - Joins the voice channel of the user who invoked the command, otherwise joins the first voice channel it finds (if any)
  * leave - Leaves the currently joined voice channel (if in a voice channel)
  * pause - Pauses the music being played
  * resume - Resumes music that has been paused
  * stop - Stops the currently playing/paused music
