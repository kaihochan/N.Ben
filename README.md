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
| `remove` | `&remove` <br> `&remove *num*` | Remove songs in queue <br> If you don't know the queue number of target video use the upper usage, will show the list and ask you to input the number |
| `rr` | `&rr` <br> `&rr *num*` | Shorthand of `&remove` |
| `skip` | `&skip` | Skip current song |
| `fs` | `&fs` | Shorthand of `&skip` |
| `pause` | `&pause` | Pause current song |
| `resume` | `&resume` | Resume playing song |

## Current updates (2/2/2022)
1. Fix the case sensitive problem, now commands can be use in both lower case and upper case
2. Proxy server options added, to avoid geo-blocking in some video which is visible in my location (HK) but not server's (US)
3. Add `&remove` function to remove songs in queue.

## Current bugs
1. From time to time song playing might lags, which already move async probe part to when the song is about to play.
2. Proxy server is unstable, proxy server option is blanked to avoid issue.

## Planning
1. Word appear frequency from specific user message (MySQL).
2. Add search video function to `play` command.
3. Considering to implement vpn if proxy is not stable.

## Additional information
1. Proxy resource: http://www.aliveproxy.com/proxy-list/proxies.aspx/Japan-jp
2. Server keep alive function came from Proladon, https://www.youtube.com/c/Proladon