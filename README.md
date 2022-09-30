# N.Ben
This is a Discord BOT, which inspired by a famous LIHKG user named "N賓"  
**Welcome to the journay of backpack.**  
<img src="https://i.imgur.com/8jXHikK.gif" width="50%">

## Functions provided:
**Prefix of BOT:** `&`
### Music related
| Command | Aliases | Parameter | Objective |
| :---- | :----| :----| :----|
| `clear` | `pg` | None | Clear songs in queue |
| `disconnect` | `ds` | None | Leave voice channel |
| `join` | `j` | None | Join/Change to current voice channel |
| `loop` | None | None | Enable/disable looping |
| `np` | None | None | Show info of current song |
| `play` | `p` | url | Play YouTube video, if it is playing then load into queue <br> *Directly join/change to current voice channel if haven't* |
| `queue` | `q` | None | List out all the song in queue |
| `remove` | `r` | *number* | Remove songs in queue <br> leaving number blank will show the list and ask to input the number |
| `skip` | `fs` | None | Skip current song |
### Twitter related
Following commands only made available for owner of BOT.
| Command | Parameter | Objective |
| :---- | :----| :----|
| `pause_update` | None | Pause/resume regular update on Twitter channel |
| `username_to_id` | username | Checks given Twitter username's ID |

Following commands only made available for server admins.
| Command | Parameter | Objective |
| :---- | :----| :----|
| `subscribe` | username | Add given username, current channel into watchlist and save into json |

Following tasks are run periodicly
| Task | Period | Information |
| :---- | :----| :----|
| `post_liked_tweets` | 6 hours | Post subscribed users' liked tweets in 00:30, 06:30, 12:30, 18:30 (UTC+8) everyday |
### Admin related
Following commands only made available for owner of BOT.
| Command | Parameter | Objective |
| :---- | :----| :----|
| `load` | None | Load function set in Cogs folers |
| `reload` | None | Reload function set in Cogs folers |
| `shutdown` | None | Shutdown the BOT service |
| `unload` | None | Unload function set in Cogs folers |

Following commands only made available for server admins.
| Command | Parameter | Objective |
| :---- | :----| :----|
| `kick` | *@user*, *number* | Add user with kick count into auto kick list |
| `rkick` | *@user* | Remove user from auto kick list |
### Events related
| Event | Action |
| :----| :----|
| Text channel contain only DW with no case sensitive | Reply Gay |
| Text channel contain only gay with no case sensitive | Reply DW |
| Text channel contain DW and gay with no case sensitive | Reply Yes |
| Text channel contain DW, not and gay with no case sensitive | Reply No |
| Text channel contain n-word | Add count to n-word counter |
| If only BOT in voice channel | Leave channel in 60s if no one join that channel or disconnect BOT |
| If user is in the kick list and join the voice channel | Kick that user out of voice channel |

## Current updates (1/10/2022)
1. Migrated to discord.py v2.0.
2. Remove `setting.json` and `twitter.json`, changed into `.env`.
3. Remove entire NBen function set.
4. Remove `pause` and `resume` function in Music.
5. Categorise `load`, `unload`, `reload`, `shutdown` into Admin
6. Open `subscribe` function in Twitter to server admins
7. Remove redundant code in all cogs
8. Change all code to meet PEP8 standard

## Current bugs
Not found yet in this update.

## Planning
1. Add search video function to `play` command.
2. Play the song in queue after disconnecting from voice channel.

## Additional information
1. discord.py, Python library of Discord API: https://discordpy.readthedocs.io/en/stable/
    - Guide of migrating to v2.0: https://discordpy.readthedocs.io/en/stable/migrating.html
2. Tweepy, Python library of Twitter API: https://www.tweepy.org/
3. yt-dlp, Python library for video downloading: https://github.com/yt-dlp/yt-dlp
4. regex, Python library with Unicode categories supported and standard re library backward compatible: https://pypi.org/project/regex/