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

## Current updates (4/2/2022)
1. Fix **urgent issue**, songs can be play and queue in different server without interfere with each other.
2. Remove unnecessery code in bot.py

## Current bugs
1. From time to time song playing might lags, which already move async probe part to when the song is about to play. Unable to locate the source.
2. Proxy server is unstable, proxy server option is blanked to avoid issue.
3. By stackoverflow and youtube-dl reddit, using account and password in youtube-dl isn't viable anymore, considering remove options in near future.

## Planning
1. Word appear frequency from specific user message (MySQL).
2. Add search video function to `play` command.
3. Considering to implement vpn on a Ubuntu server, might change the host to home hosting.
4. Play the song in queue after disconnecting from voice channel.

## Additional information
1. Proxy resource: http://www.aliveproxy.com/proxy-list/proxies.aspx/Japan-jp
2. Server keep alive function came from Proladon, https://www.youtube.com/c/Proladon