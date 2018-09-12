# Wumbot
Python bot for the Wumbology Discord server!

Built with [Discord.py](https://github.com/Rapptz/discord.py)

## Cogs
### `bot`
Contains the bot's default commands
#### Commands
Commands are prefixed with `~`

##### ver
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

##### uptime
Replies with Wumbot's current uptime.

Example:
```
[13:37] ELA: ~uptime
[13:37] Wumbot: Wumbot has been up for: 1d 2h 13m 37s
```

##### kill
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

### `reddit`
#### `RedditPost`
Helper class to generate an object from Reddit JSON.
##### Input
Dictionary decoding of Reddit's JSON response. A list of submissions in the decoded JSON response dictionary is found under `responsedict['data']['children']`.

##### Attributes
| Name         | Description                      | Type       |
| :--:         | :-                               | :--:       |
| `kind`       | Submission Kind<sup>1</sup>      | `str`      |
| `id`         | Unique Submission ID<sup>2</sup> | `str`      |
| `subreddit`  | Submission Subreddit             | `str`      |
| `title`      | Submission Title                 | `str`      |
| `createdUTC` | Post Creation Date (UTC)         | `datetime` |
| `contentURL` | Submission Permalink             | `str`      |

1. Defined per [Reddit's API documentation](https://www.reddit.com/dev/api/)
2. [Base36](https://en.wikipedia.org/wiki/Base36) encoded


#### `on_message` Functionality
**NOTE:** Commands utilizing the command prefix (`~`) short circuit and are not parsed.

##### Subreddit Detection & Embed
When a message is sent containing one or more subreddits (e.g. "`/r/Python` is the best subreddit!"), Wumbot will generate and respond with a `discord.Embed` object that links to the subreddit(s).


##### v.Reddit `DashPlaylist.mpd` Detection
Check to see if Reddit's image/video hosting has added `DashPlaylist.mpd` to the end of the URL, which links to a direct download (of nothing) rather than the web content. Wumbot will strip `DashPlaylist.mpd` and respond with the corrected link.

Example:
```
[13:37] ELA: https://v.redd.it/k32sq2cwmdi01/DASHPlaylist.mpd
[13:37] Wumbot: Here ELA, let me fix that v.redd.it link for you: https://v.redd.it/k32sq2cwmdi01/
```


### overwatch
#### `OWPatch`
Helper class to generate an object from Blizzard's Patch Notes

##### Input
| Name        | Description              | Example                                 |
| :--:        | :-                       | :--:                                    |
| `patchref`  | Patch Reference ID       | `'patch-50148'`                         |
| `ver`       | Patch Version Number     | `'1.28.0.1'`                            |
| `patchdate` | Patch Date (UTC)         | `dt.strptime('09/11/2018', '%m/%d/%Y')` |
| `patchURL`  | Patch Notes Permalink    | `yarl.URL(patchnoteslink)`              |
| `bannerURL` | Post Creation Date (UTC) | `yarl.URL(imglink)`                     |

**NOTE:** Due to wide variation in formatting between patches, parsing and storage of the patch description is currently not implemented.

##### Attributes
| Name        | Description                       | Type       |
| :--:        | :-                                | :--:       |
| `patchref`  | Patch Reference ID                | `str`      |
| `ver`       | Patch Version Number              | `str`      |
| `patchdate` | Patch Date (UTC)                  | `datetime` |
| `patchURL`  | Patch Notes Permalink<sup>1</sup> | `yarl.URL` |
| `bannerURL` | Post Creation Date (UTC)          | `yarl.URL` |

1. Patch note permalink directs to [BlizzTrack](https://blizztrack.com/patch_notes/overwatch/)

#### PatchNotesParser
Class for parsing Blizzard's [Overwatch Patch Notes](https://playoverwatch.com/en-us/news/patch-notes/pc)

##### Attributes
| Name            | Description                        | Type           |
| :--:            | :-                                 | :--:           |
| `bot`           | Discord Bot Instance               | `WumbotClient` |
| `patchesURL`    | Blizzard Patch Notes URL           | `yarl.URL`     |
| `postchannelID` | Discord Channel ID to send to      | `int`          |
| `logJSONpath`   | Path to JSON Storage File          | `pathlib.Path` |
| `postedpatches` | List of Posted Patches<sup>1</sup> | `list[str]`    |

1. List of patch reference IDs, as `str` (e.g. '50148')

##### Methods
###### `patchcheck()`
This function is a *coroutine*

Excecutes the patch check operations:
  * Parse Blizzard's Patch Notes
  * Build `OWPost` objects
  * Check patch references against those previously posted
  * If new patch(es): Build embed, post to channel, and save reference

##### Static Methods
###### `getblizztrack(patchref:str) -> yarl.URL`
Build a `yarl.URL` object from a patch reference ID

Example:
```python
>>> from cogs import overwatch
>>> patchURL = overwatch.PatchNotesParser.getblizztrack('50148')
>>> print(patchURL)
https://blizztrack.com/patch_notes/overwatch/50148
```

#### PatchGifParser
Class for parsing patch summary GIFs created by Reddit User [/u/itsjieyang](https://reddit.com/u/itsjieyang)

##### Attributes
| Name            | Description                                                 | Type           |
| :--:            | :-                                                          | :--:           |
| `bot`           | Discord Bot Instance                                        | `WumbotClient` |
| `postjsonURL`   | Reddit's JSON URL for /u/itsjieyang submissions<sup>1</sup> | `str`          |
| `postchannelID` | Discord Channel ID to send to                               | `int`          |
| `logJSONpath`   | Path to JSON Storage File                                   | `pathlib.Path` |
| `postedGIFs`    | List of Posted Patches<sup>2</sup>                          | `list[str]`    |

1. Reddit's JSON can be obtained by appending `'.json'` to the end of any valid link (e.g. https://www.reddit.com/user/itsjieyang/submitted.json)
2. List of Gfycat permalinks, as `str` (e.g. 'https://gfycat.com/MajorDiligentIbizanhound')

##### Methods
###### `patchcheck()`
This function is a *coroutine*

Excecutes the patch check operations:
  * Parse /u/itsjieyang's submission JSON for Gfycat submissions to /r/overwatch
  * Build `reddit.RedditPost` objects
  * Check Gfycat URLs against those previously posted
  * If new patch(es): Build embed, post to channel, and save Gfycat URL

##### Static Methods
###### gfygif(inURL: str) -> str
Build a direct GIF link from a Gfycat URL

Example:
```python
>>> from cogs import overwatch
>>> gifURL = overwatch.PatchGifParser.gfygif('https://gfycat.com/MajorDiligentIbizanhound')
>>> print(gif)
https://giant.gfycat.com/MajorDiligentIbizanhound.gif
```

### mhw
### SteamNewsPost
Helper class to generate an object from Steam's News Post API

See: [Steam's Developer API](https://developer.valvesoftware.com/wiki/Steam_Web_API#GetNewsForApp_.28v0002.29) for API details

##### Attributes
| Name              | Description          | Input Type | Type       |
| :--:              | :-                   | :--:       | :--:       |
| `gid`             | Global Post ID       | `str`      | `str`      |
| `title`           | Post Title           | `str`      | `str`      |
| `url`             | Post Permalink       | `str`      | `yarl.URL` |
| `is_external_url` | External URL Boolean | `bool`     | `bool`     |
| `author`          | Post Author          | `str`      | `str`      |
| `contents`        | Post Contents        | `str`      | `str`      |
| `feedlabel`       | News Feed Label      | `str`      | `str`      |
| `date`            | Posted Date (UTC)    | `int`      | `datetime` |
| `feedname`        | Feed Name            | `str`      | `str`      |
| `feed_type`       | Feed Type            | `int`      | `str`      |
| `appid`           | Steam App ID         | `int`      | `str`      |

##### Static Methods
###### getnewsforapp(appID: int=582010, count: int=10, maxlength: int=300, format: str='json') -> typing.List
Generate a list of `SteamNewsPost` objects for the queried Steam App.

See: [Steam's Developer API](https://developer.valvesoftware.com/wiki/Steam_Web_API#GetNewsForApp_.28v0002.29) for API details

Inputs:

| Name              | Description                                | Type  |
| :--:              | :-                                         | :--:  |
| `gid`             | Steam App ID                               | `int` |
| `title`           | Number of News Items to Return             | `int` |
| `url`             | Maximum Length of Returned Contents String | `int` |
| `is_external_url` | API Return Format                          | `str` |

**NOTE**: Additional keyword arguments are discarded

###### asyncgetnewsforapp(appID: int=582010, count: int=10, maxlength: int=300, format: str='json', **kwargs) -> typing.List
This function is a *coroutine*

Async implementation of `SteamNewsPost.getnewsforapp`. See `SteamNewsPost.getnewsforapp` for function description.