## Modules
Modules are a large part of Quantum, allowing users to only use modules they want and creates an environment that allows others to extend the bot, with relative ease.<br>
`template.py` gives an overview of how to write a module and events you can interact with. For a more a detailed explanation (including if you're just starting and want to add something neat or port over some existing neatness) read on.
#### The Anatomy of a Module
-------------
<sub>You can take a look at [template.py](https://github.com/JohnRipper/quantum/blob/master/modules/template.py) if you'd like to follow along</sub><br>
Modules are enabled by uncommenting in the [configuration](https://github.com/JohnRipper/quantum/blob/master/default.toml). A module that is untested; meaning it may break horribly, is noted with `#UNTESTED`, use at your discretion or test it out and report back via an [issue](https://github.com/JohnRipper/quantum/issues)<br>
We'll be creating a module named `Math` as an example, using `template.py` as a reference.<br>

All modules will start with the following:
```py
from lib.cog import Cog
from lib.command import Command, makeCommand
```
Your module will inherit the class `Cog`, allowing interactions with the bot such as sending messages to the chat (`send_message`) and room events like recieving messages, users joining, users camming, etc.<br>
From here the `Math` class begins:
```py
class Math(Cog):
    def __init__(self, bot):
        super().__init__(bot)
```
This initializes our `Math` class and inherits the attributes of `QuantumBot` in `bot.py`. This allows us to use things like [`self.version`](https://github.com/JohnRipper/quantum/blob/master/bot.py#L35) by calling `self.bot.version`. To get settings from our configuration we would call `self.bot.settings["module"]["yourmodule"]["somesetting"]`<br>
Next lets add a simple function for some math. `template.py` already has a function for addition so we can use some of that.
```py
    def addnumbers(self, num1: int, num2: int):
        self.logger.info(f"Adding {num1} + {num2}")
        return num1 + num2
```
Here we name the function `addnumbers`, `self` allows interaction with the class (see `self.logger.info()`), and requires two arguments, `num1` and `num2`, both have the expected type of `int` (for integer). We then ensure we're keeping track of the command by logging it with the log level of `info`. And return the sum of our arguments with `num1 + num2`<br>
Now that we have a simple function that returns the sum of two numbers we need to write an additional function to act as our command.<br>
This command will call `self.addnumbers()`:
```py
@makeCommand(name="add", description="<int int> return the sum of two numbers")
async def add(self, c: Command):
    message = c.message.split(" ")
    if len(message) == 2:
        for each in message:
            if each.isnumeric():
                self.logger.info(f"{each} is a number!")
            else:
                self.logger.info(f"{each} is not a number!")
                await self.bot.send_message(f"{each} is not a number!")
                break
        else:
            num1 = int(message[0])
            num2 = int(message[1])
            sum_ = self.addnumbers(num1=num1, num2=num2)
            await self.bot.send_message(f"{num1} + {num2} = {sum_}!")
    else:
        self.logger.info(f"Expected 2 parts, got {len(message)}")
        await self.bot.send_message(f"That's {len(message)} number(s)")
```
For the sake of brevity we won't be going into a ton of detail about how this works but instead focus on how it interacts with Quantum.<br>
If you're coming from an existing bot it's important to note the use of async of await. A few rules of thumb is:
- Command functions need to be async
- Functions that are part of QuantumBot need to be "awaited", such as `await self.bot.send_message()`
- If you're making a remote request, say to an API, it should also be async

```py
@makeCommand(name="add", description="<int int> return the sum of two numbers")
```
This is how we add new commands to Quantum, `name=` is the name of the command to use. In this case the user would call something like `!add 5 5`. `description=` supplies a brief description of the command.
```py3
async def add(self, c: Command):
    message = c.message.split(" ")
```
`c` is our Command object, this allows interaction with the command. With this you can get info about the user and message sent. Say you wanted the nickname of the user, `c.account.nick` would have it. Eventually this will be documented a bit better. For now have a look [command.py](https://github.com/JohnRipper/quantum/blob/master/lib/account.py#L5) for the command objects and [account.py](https://github.com/JohnRipper/quantum/blob/master/lib/account.py#L5) for info available from `c.account`
```py
self.logger.info(f"{each} is a number!")
```
Again we make sure to log all the things.
```py3
self.bot.send_message()
```
Finally we send a message to the chat.<br>
In some cases you might want modules to be automated, say for a greet message when a user joins the room. Here we would inherit a function from `Cog`.
```py3
async def join(self, data):
    nickname = data["nick"]
    self.bot.send_message(f"Welcome to the room {nickname}")
```
These functions differ from commands because we get a dictionary of the actual data from Tinychat and it's up to you how you want to handle it. If would like the data from Tinychat in your command you can use `Command.raw_data` to get a dictionary.<br>
You can also restrict commands to a set level. First by importing `Role` and `restrictTo`. So your module would start out like the following:
```py3
from lib.account import Role
from lib.cog import Cog
from lib.command import Command, makeCommand, restrictTo
```
Then in the same way you use `makeCommand` add `restrictTo`
```py3
@makeCommand(name="add", description="<int int> return the sum of two numbers")
@restrictTo(role=Role.OWNER)
async def add(self, c: Command):
    # sprinkle your magic here
```
This restricts the `add` command to only the room owner. This is another bit that will be documented later. For now you can use [constants.py](https://github.com/JohnRipper/quantum/blob/master/lib/constants.py#L32)

-------------
This README will most likely change radically or be out of date very soon. So keep that in mind.

