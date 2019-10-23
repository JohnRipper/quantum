# Quantum
A modularized bot for Tinychat. **WIP AF**
## Running
Quantum relies on Python 3.7+ and only 3.7+ any version less and it *probably* won't work. It's advised to copy [`default.toml`](ttps://github.com/JohnRipper/quantum/blob/master/default.toml) and rename it. Current options are `bot.py -h,-c,-l`; --help, --config, --logging respectively. Run the bot with the following:
```
python3 bot.py -c your_config.toml
```
`-c` and `-l` are both optional, without `-c` the bot will load `default.toml`<break>
Available log levels are:
- `i` - Info
- `c` - Chat
- `ws` - WebSocket
- `w` - Warning
- `e` - Error
The default log level is `i` - Info
```
python3 bot.py
```
<sub>Note: if your configuration is missing anything it needs then the bot will break</sub>
<sub><sub><sub><sub>maybe</sub></sub></sub></sub>

### Requirements
Via `make $opt`:
- `base` - websockets requests tomlkit (default for make)
- `extras` (modules) - bs4 anticaptcha isodate
- `baseextras` - both base and extras dependencies will be installed
- `webcam` (win32 may not work) - aioice aiortc
- `all` - all of the above
<sub>Note: `webcam` requires some extra headers to build, will sort out which and list then later</sub>

### Configuration
For general configuration and enabling/disabling available modules; see: [CONFIGURATION.md](https://github.com/JohnRipper/quantum/blob/master/CONFIGURATION.md)

### Modules
Information on implementing new modules can be found in: [Modules](https://github.com/JohnRipper/quantum/tree/master/modules)
