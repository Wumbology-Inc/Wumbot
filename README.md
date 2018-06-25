# Wumbot
Python bot for the Wumbology Discord server!

## Commands
Commands are prefixed with `~`

### ver
Replies with the current version number provided by the most recent tag on the `master` branch.

Example:
```
[13:37] ELA: ~ver
[13:37] Wumbot: Current Version: v0.2.1
```

**NOTE:** This command utilizes GitPython's `git.describe()`, which will throw an exception if there are no tags present. This exception is handled:

```
[13:37] ELA: ~ver
[13:37] Wumbot: No tags found on current branch
```

To fix this error, ensure that the tags are being pulled or fetched on deployment.

### uptime
Replies with Wumbot's current uptime.

Example:
```
[13:37] ELA: ~uptime
[13:37] Wumbot: Wumbot has been up for: 1d 2h 13m 37s
```

### kill
Disconnects Wumbot from the server.

This command is only enabled for the server owner via DM.

Example:
```
[13:37] ELA: ~kill
[13:37] Wumbot: Shutting down... :wave:
```

```
[13:37] notELA: ~kill
[13:37] Wumbot: You are not authorized to perform this operation
```

## `on_message` Functionality
Wumbot parses all incoming messages for specific patterns. Commands utilizing the command prefix (`~`) short circuit and are not parsed.

### Subreddit Detection & Embed
When a message is sent containing one or more subreddits (e.g. "`/r/Python` is the best subreddit!"), Wumbot will generate and respond with a `discord.Embed` object that links to the subreddit(s).


### v.Reddit `DashPlaylist.mpd` Detection
Check to see if Reddit's image/video hosting has added `DashPlaylist.mpd` to the end of the URL, which links to a direct download (of nothing) rather than the web content. Wumbot will strip `DashPlaylist.mpd` and respond with the corrected link.

Example:
```
[13:37] ELA: https://v.redd.it/k32sq2cwmdi01/DASHPlaylist.mpd
[13:37] Wumbot: Here ELA, let me fix that v.redd.it link for you: https://v.redd.it/k32sq2cwmdi01/
```