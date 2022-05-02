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
### Twitter related
Following commands only made available for owner of BOT.
| Command | Usage | Objective |
| :---- | :----| :----|
| `starttwitter` | `&starttwitter` | Start post liked post of followed user in specified channel in each day 18:30 (GMT+8) |
| `checkstwitter` | `&checkstwitter *username*` | Checks given Twitter username's ID |
| `addtwitter` | `&addtwitter *username*` | Add given username, current channel into watchlist and save into json |
### Events related
| Event | Action |
| :----| :----|
| Text channel contain only DW with no case sensitive | Reply Gay |
| Text channel contain only gay with no case sensitive | Reply DW |
| Text channel contain DW and gay with no case sensitive | Reply Yes |
| Text channel contain DW, not and gay with no case sensitive | Reply No |
| If only BOT in voice channel | Leave channel in 60s if no one join that channel or disconnect BOT |

## Current updates (3/5/2022)
1. Added Twitter function set, only avaliable for BOT owner.
2. Added Events set, will execute auto-reply and auto-disconnect.
3. Changed to home hosting, geo-block issue resolved, with keep_alive.py removed.
4. Changed json file location.
5. Switch back to youtube-dl as link retreve format of yt-dlp is differ from youtube-dl, causing error
6. Added BOT execulsive role, name N.Ben, with permission of administrator.

## Current bugs
1. From time to time song playing might lags, which already move async probe part to when the song is about to play. Unable to locate the source.
2. Sometimes unable to play some song, which ffmpeg will give error as <span style="color:red"> Output file #0 does not contain any stream </span>.

## Planning
1. Word appear frequency from specific user message (MySQL).
2. Add search video function to `play` command.
3. Play the song in queue after disconnecting from voice channel.

## Additional information
Tweepy, Python library of Twitter API: https://www.tweepy.org/
discord.py, Python library of Discord API: https://discordpy.readthedocs.io/en/stable/