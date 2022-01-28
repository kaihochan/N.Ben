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
| `skip` | `&skip` | Skip current song |
| `fs` | `&fs` | Shorthand of `&skip` |
| `pause` | `&pause` | Pause current song |
| `resume` | `&resume` | Resume playing song |

## Current updates (29/1/2022)
1. Added `&np` function to check current song.
2. Add user cookies to play age-restricted videos, while YouTube account details is kept. 

## Current bugs
1. From time to time song playing might lags.
2. Geo-blocking from videos which able to seen in my current location (HK)

## Planning
1. Word appear frequency from specific user message (MySQL).
2. Add search video function to `play` command.
3. Add remove videos on queue function.
4. Add proxy server or vpn to address geo-blocking on server side.
5. Show time playing in `np` command.
