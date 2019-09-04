# Quantum
A modularized bot for Tinychat. **WIP AF**
## Running
Quantum relies on Python 3.7+ and only 3.7+ any version less and it *probably* won't work. It's advised to copy [`default.toml`](ttps://github.com/JohnRipper/quantum/blob/master/default.toml) and rename it. Current options are `bot.py -h,-c,-l`; --help, --config, --logging respectively. Run the bot with the following:
```
python3 bot.py -c your_config.toml
```
`-c` and `-l` are both optional, without `-c` the bot will load `default.toml` (*TODO:* notate log levels)
```
python3 bot.py
```
<sub>Note: if your configuration is missing anything it needs then the bot will break</sub>
<sub><sub><sub><sub>maybe</sub></sub></sub></sub>

### Requirements
- `base` - websockets requests tomlkit
- `extras` (modules) - bs4 anticaptcha isodate
- `webcam` (win32 may not work) - aioice aiortc
- `all` - all of the above

The above are available via `./install.sh $opt`

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

#### Module.Autourl
**WARNING:** Autourl can and will reveal the bot's IP address by posting it in the room. This is not an issue for those who run the bot on a remote server, but certainly something to be aware of when running from home. To be honest this is unavoidable, if you think you've sorted out a way to prevent it from happening then feel free to make a pull request. Use with discretion.
- `pattern` - regular expression pattern to use when matching URLs from messages. Be sure to escape characters
- `exclusion_char` - Leave blank to look up every URL, otherwise if the exclusion_char is found at the beginning of the URL the module will not look up the title for said URL

#### Module.Captcha
- `key` - the API key for AntiCaptcha

#### Module.Youtube
- `key` - Youtube Data API key, *optional* if you choose to use [your own API](https://developers.google.com/youtube/v3/) key. Has prevented breakage in the past 
