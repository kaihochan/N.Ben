# N.Ben
## This is the update log of the discord BOT, N.Ben
### Current updates (3/5/2022)
1. Added Twitter function set, only avaliable for BOT owner.
2. Added Events set, will execute auto-reply and auto-disconnect.
3. Changed to home hosting, geo-block issue resolved, with keep_alive.py removed.
4. Changed json file location.
5. Switch back to youtube-dl as link retreve format of yt-dlp is differ from youtube-dl, causing error
6. Added BOT execulsive role, name N.Ben, with permission of administrator.
### Updates (11/4/2022)
1. Change all array in various list into class objects, Queue object and TimeList object.
2. Use yt-dlp instead of youtube-dl.
3. Remove options related to account and proxy in json file.
4. Remove redundant coding in `rr` and `np` function.
5. yt-dlp option add no playlist to avoid runtime error in `play` and `p`.
### Updates (4/2/2022)
1. Fix **urgent issue**, songs can be play and queue in different server without interfere with each other.
2. Remove unnecessery code in bot.py
### Updates (2/2/2022)
1. Fix the case sensitive problem, now commands can be use in both lower case and upper case
2. Proxy server options added, to avoid geo-blocking in some video which is visible in my location (HK) but not server's (US)
3. Add `&remove` function to remove songs in queue.
### Updates (31/1/2022)
1. Show time playing in `np` command.
2. Fix auto-stop all song when using `skip` command. 
### Updates (29/1/2022)
1. Added `&np` function to check current song.
2. Add user cookies to play age-restricted videos, while YouTube account details is kept. 
### Updates (23/1/2022)
1. Remaked queue message, added video name, user who queue, and direct hyperlink.
2. Added field and arguments related to YouTube account on youtube-dl.
3. Added `&queue` function to check songs in queue.
4. Added shorthand <s>lazyfuck</s> commands for existing commands