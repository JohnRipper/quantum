# Quantum
A modularized bot for Tinychat. **WIP AF**
Note while the bot works as of 10/31/2019, this project is no longer being actively maintained. Feel free to fork and learn from it.


## Running
Quantum relies on Python 3.7+ and only 3.7+ any version less and it *probably* won't work. It's advised to copy [`default.toml`](ttps://github.com/JohnRipper/quantum/blob/master/default.toml) and rename it. Current options are `bot.py -h,-c,-l`; --help, --config, --logging respectively.

Run the bot with the following:
```
python3 bot.py -c your_config.toml
```
`-c` and `-l` are both optional, without `-c` the bot will load `default.toml`

Available log levels are:
- `i` - Info
- `c` - Chat
- `ws` - WebSocket
- `w` - Warning
- `e` - Error
The default log level is `i` - Info

<sub>Note: if your configuration is missing anything it needs then the bot will break</sub>
<sub><sub><sub><sub>maybe</sub></sub></sub></sub>

### Requirements
Via `make $opt`:
- `base` - websockets requests tomlkit (default for make)
- `extras` (modules) - bs4 anticaptcha isodate wikipedia
- `baseextras` - both base and extras dependencies will be installed
- `webcam` (win32 may not work) - aioice aiortc
- `all` - all of the above
<sub>Note: `webcam` requires some extra headers to build, will sort out which and list then later</sub>

### Modules
Information on implementing new modules can be found in: [Modules](https://github.com/JohnRipper/quantum/tree/master/modules)

A table of commands for each module can be found in: [Commands](https://github.com/JohnRipper/quantum/blob/master/COMMANDS.md)

## Configuration
This document is divided into sections the same as [`default.toml`](https://github.com/JohnRipper/quantum/blob/master/default.toml)
### Account
- `username` - TC account username
- `password` - TC account password

### Room
- `nickname` - Nickname for the bot
- `rooname` - Room to join
- `password` - Room password, if any

### Bot
- `prefixes` - Prefixes for the commands, e.g. `!command` or `.command`, multiple prefixes are allowed
- `chat_level` - TODO
- `message_limit` - maximum number of messages to send in response. Say the bot's reply is an essay, it will break that essay up into message sizes TC allows, but only send this many messages
- `modules` - Modules to be loaded, each module and it's source can be found in the [modules directory](https://github.com/JohnRipper/quantum/tree/master/modules). Comment with `#` to disable the module, remove `#` to enable it. All modules are optional.

### Discord
Discord has it's own section because it contains a lot of options, most likely even more to come.
- `channel` - The channel ID to send messages to. **Not compatible with `use_webhook`**
- `use_webhook` - Enable/Disable the use of discord webhooks. **Not compatible with `channel`**
- `webhook_url` - URL the Discord channel's webhook (See: [Intro To Webhooks](https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks))
- `include_avatar` - Optionally add the user's avatar to the webhook message
- `bot.username` - Username the bot will use when posting to the webhook
- `bot.icon_url` - Icon the bot will use when posting to the webhook (default is the Tinychat logo)
- `bot.message` - Message that will be posted to the webhook, It will be formated with `{option}`. List of available options to format will come, eventually

#### Module.Admin
- `vip_enabled` - TODO
- `kick_as_ban` - Don't ever ban, only kick

#### Module.Autourl
**WARNING:** Autourl can and will reveal the bot's IP address by posting it in the room. This is not an issue for those who run the bot on a remote server, but certainly something to be aware of when running from home. To be honest this is unavoidable, if you think you've sorted out a way to prevent it from happening then feel free to make a pull request. Use with discretion.
- `pattern` - regular expression pattern to use when matching URLs from messages. Be sure to escape characters
- `exclusion_char` - Leave blank to look up every URL, otherwise if the exclusion_char is found at the beginning of the URL the module will not look up the title for said URL
- `ignores` - A list of domains/things to ignore. URLs posted by the bot and with the `play` command are ignored already. Supports regular expressions.

#### Module.Captcha
- `key` - the API key for AntiCaptcha (see: [AntiCaptcha](https://anti-captcha.com/mainpage))

#### Module.Food2fork
- `key` - the API key for Food2fork (see: [Food2fork API](https://www.food2fork.com/about/api))

#### Module.Fun
- `fancydice` - use unicode dice (⚀ ⚁ ⚂ ⚃ ⚄ ⚅) only applies to 6 sided die
- `8ballcustom` - list of custom 8ball replies to add to "[official](https://en.wikipedia.org/wiki/Magic_8-Ball#Possible_answers)" replies
- `enablerate` - enable/disable the `rate` command

#### Module.Movie
- `key` - the API key for The Movie Db (see: [The Movie Database API](https://developers.themoviedb.org/3/getting-started))
- `include_url` - include the iMDb URL in the reply 

#### Module.Tokes
- `hourly_420` - enable/disable hourly 4:20 notifications

#### Module.Wikipedia
- `sentences` - number of sentences to pull from wikipedia summary
- `language` - language to use, requires the ISO code. (see: [Wikipedia Supported Languages](https://gist.github.com/Autotonic/96632746355607caa2a611b48552396c))
- `url` - enable/disable appending the URL for the wikipedia page

#### Module.Youtube
- `key` - Youtube Data API key, *optional* if you choose to use [your own API](https://developers.google.com/youtube/v3/)
- `playlist_max` - Maximum amount of videos to add from a playlist (current is 50 until the API is paginated)

## Thanks to those who have helped make quantum a thing

[`@autotonic`](https://github.com/Autotonic) for big brain

[`@tech`](https://github.com/Technetium1) design and code review

[`xbc4000`](https://github.com/xbc4000) for the name 

