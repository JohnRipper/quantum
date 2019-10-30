 # Commands
 ## Builtins
| Command | Argument | Description                                         |
|---------|----------|-----------------------------------------------------|
| `uptime`    | N/A      | Show the bot's running time                         |
| `version`  | N/A      | Show the bot's current version and upstream version |
## Debug
| Command  | Argument | Description                    |
| ------   | -------- | ----------                     |
| `people` | N/A      | Return a list of current users |
|    `load` | module   | Load a module (BORKED)          |
|     `reload` | module   |  Reload a module               |
|   `unload` |  module  |     Unload an active module (borked?) |
| `modules` |  N/A     |  Return a list of modules      |
|  `cogs`   |    N/A   |  Return a list of active modules? |
## Food2Fork
| Command | Argument | Description |
| ------  | -------- | ----------  |
| `food`    |  str     | Look up recipes related to the argument and return a random one |
## Fun
| Command     | Argument            | Description                                                        |
| ------      | --------            | ----------                                                         |
| `roll`      | sides:total or none | roll some dice with sides * total die or just a single 6 sided die |
| `rate`      | string              | rate a thing 0 out of 10                                           |
| `eightball` | question?           |  Ask the 8ball a thing                                             |
## Tokes
| Command   | Argument | Description                             |
| ------    | -------- | ----------                              |
| `420hour` | N/A      | Enable/Disable hourly 420 notifications |
| `timer`   | int      | Start a timer for tokes                 |
| `tokes`   | int      | Call tokes in `int` seconds             |
## Urban
| Command | Argument | Description |
| ------  | -------- | ----------  |
| `urb`     |  str     |  Return the first match for `str` from Urban Dictionary |
## Wikipedia
| Command | Argument    | Description                                    |
| ------  | --------    | ----------                                     |
| `wiki`  | str or none | Search `str` in wikipedia or none for a random |
## Wundertime
| Command | Argument | Description                                              |
| ------  | -------- | ----------                                               |
| `time`  | str      | Lookup `str` as a location and return the locations time |
## Youtube
| Command  | Argument               | Description                                                                                                              |
| ------   | --------               | ----------                                                                                                               |
| `yt`     | str or url             | Play or add a video to the playlist                                                                                      |
| `addpl`  | str or url             | Add a youtube playlist to the bot's playlist                                                                             |
| `cpl`    | N/A                    | Clear the current playlist                                                                                               |
| `pause`  | N/A                    | Pause the current video                                                                                                  |
| `resume` | N/A                    | Resume the current video                                                                                                 |
| `skip`   | N/A                    | Skip the current video                                                                                                   |
| `rm`     | title or index or none | Remove `title` (regex supported) from the playlist or remove the video at `index`, if `none` remove the last added video |
| `now`    | N/A                    | Show information about the current video                                                                                 |
|   `next`  |  N/A                   | Display the next video in the playlist                                                                                   |
|     `pl`   | N/A                    |  Display all the videos in the playlist and their current index (TODO: currently spammy)                                    |
