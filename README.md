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
| `discon` | `&discon` | Leave voice channel |
| `play` | `&play *url*` | Play YouTube video, if it is playing then load into queue <br> *Directly join/change to current voice channel if haven't* |
| `queue` | `&queue` | List out all the song in queue |
| `skip` | `&skip` | Skip current song |
| `pause` | `&pause` | Pause current song |
| `resume` | `&resume` | Resume playing song |

## Current updates (23/1/2022)
1. Remaked queue message, added video name, user who queue, and direct hyperlink.
2. Added field and arguments related to YouTube account on youtube-dl.
3. Added `&queue` function to check songs in queue.
4. Added shorthand <s>lazyfuck</s> commands for existing commands

## Current bugs
1. Unable to play age-restricted videos due to HTTP Error 400 (bad request).
2. From time to time song playing might lags.

## Planning
1. Word appear frequency from specific user message (MySQL).
3. Add user cookies to replace YouTube account.
4. Add search video function to `play` command.
