# N.Ben
This is a Discord BOT, which inspired by a famous LIHKG user named "N賓"  
**Welcome to the journay of backpack.**  
<img src="https://i.imgur.com/8jXHikK.gif" width="50%">

## Functions provided:
**Prefix of BOT:** `&`
### N.Ben related
| Command | Usage | Objective |
| :---- | :----| :----|
| `smile` | `&smile` | N.Ben smile gif |
| `nteam` | `&nteam` | Many N.Ben picture |
| `backpack` | `&backpack` | N.Ben's backpack picture |
| `dllm` | `&dllm` | Say 「屌你老母」 |
### Music related
| Command | Usage | Objective |
| :---- | :----| :----|
| `join` | `&join` | Join/Change to current voice channel |
| `j` | `&j` | Shorthand of `&join` |
| `discon` | `&discon` | Leave voice channel |
| `ds` | `&ds` | Shorthand of `&discon` |
| `play` | `&play *url*` | Play YouTube video, if it is playing then load into queue <br> *Directly join/change to current voice channel if haven't* |
| `p` | `&p *url*` | Shorthand of `&play *url*` |
| `queue` | `&queue` | List out all the song in queue |
| `q` | `&q` | Shorthand of `&queue` |
| `np` | `&np` | Show info of current song |
| `remove` | `&remove` <br> `&remove *number*` | Remove songs in queue <br> If you don't know the queue number of target video use the upper usage, will show the list and ask you to input the number |
| `rr` | `&rr` <br> `&rr *number*` | Shorthand of `&remove` |
| `skip` | `&skip` | Skip current song |
| `fs` | `&fs` | Shorthand of `&skip` |
| `pause` | `&pause` | Pause current song |
| `resume` | `&resume` | Resume playing song |
| `loop` | `&loop` | Enable/disable looping |
### Twitter related
Following commands only made available for owner of BOT.
| Command | Usage | Objective |
| :---- | :----| :----|
| `starttwitter` | `&starttwitter` | Start post liked post of followed user in specified channel in each day 18:30 (GMT+8) |
| `checkstwitter` | `&checkstwitter *username*` | Checks given Twitter username's ID |
| `addtwitter` | `&addtwitter *username*` | Add given username, current channel into watchlist and save into json |
### Admin related
Following commands only made available for owner of BOT.
| Command | Usage | Objective |
| :---- | :----| :----|
| `kick` | `&kick *@user* *number*` | Add user with kick count into auto kick list |
| `rkick` | `&rkick *@user*` | Remove user from auto kick list |
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

## Current updates (26/5/2022)
1. Added N-word counter, only count the n-words after joining the channels.
2. Change music library from youtube-dl to yt-dlp, which seems fixed issue that song lags when playing.
3. Using RegEx to find the right URL for playing video in music COG, fixed issue that some song is unable to play due to wrong link issue.
4. Using RegEx to detect keywords in events.
5. Added `&loop` fuction for looping same song.
6. Added Misc object for storing looping status and number of songs in queue.
7. Added Admin function set, only serve for multiple kicking at this moment, only avaliable for server owner.

## Current bugs
Not found yet in this update.

## Planning
1. Add search video function to `play` command.
2. Play the song in queue after disconnecting from voice channel.

## Additional information
1. Tweepy, Python library of Twitter API: https://www.tweepy.org/
2. discord.py, Python library of Discord API: https://discordpy.readthedocs.io/en/stable/
3. yt-dlp, Python library for video downloading: https://github.com/yt-dlp/yt-dlp