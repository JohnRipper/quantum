from lib.cog import Cog
from lib.command import Command, makeCommand
import random

class Fun(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.settings = self.bot.settings["module"]["fun"]

    @makeCommand(name="roll", description="<sides> <dice>, default is single 6 sided")
    async def roll(self, c: Command):
        parts = c.message.split(" ")
        if len(c.message) == 0:
            await self.send_message(self.rolldice())
        elif parts[0].isdigit() and parts[1].isdigit():
            await self.send_message(self.rolldice(sides=parts[0], dice=parts[1]))
        else:
            await self.send_messages("I need numbers m8")

    def rolldice(self, sides=6, dice=1):
        if sides > 20 or dice > 15:
            msg = "D&D dice only has 20 sides, wtf m8"
            return msg
        else:
            rolled = []
            total = 0
            faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
            for die in range(dice):
                r = random.randint(1,sides)
                total+=r
                if sides == 6 and self.settings["fancydice"] is True:
                    rolled.append(faces[r-1])
                else:
                    rolled.append(str(r))
            msg = "You roll {} for a total of {}".format(
                " ".join(rolled), total)
            return msg

    # TODO
    @makeCommand(name="eightball", description="<query> standard magic 8ball")
    async def eightball(self, c: Command):
        query = c.message
        if len(query) < 3:
            await self.send_message("You must ask a question.")
        elif "?" not in query:
            await self.send_message("....questions should have question marks, no?")
        else:
            # https://en.wikipedia.org/wiki/Magic_8-Ball#Possible_answers
            replies = ["It is certain.", "It is decidedly so.",
                       "Without a doubt.", "Yes - definitely.",
                       "You may rely on it.", "As I see it, yes.",
                       "Most likely.", "Outlook good.", "Yes.",
                       "Signs point to yes.", "Reply hazy, try again.",
                       "Ask again later.", "Better not tell you now.",
                       "Cannot predict now.", "Concentrate and ask again.",
                       "Don't count on it.", "My reply is no.",
                       "My sources say no.", "Outlook not so good.",
                       "Very doubtful"]
            custom = self.settings["8ballcustom"]
            # append custom replies if they exist
            if len(custom) > 0:
                replies.append([c for c in custom])
            msg = "{}".format(random.choice(replies))
            await self.send_message(msg)

    @makeCommand(name="rate", description="<user> rate someones appearance")
    async def rate(self, c: Command):
        # some can find a "rate" command insensitive
        if self.settings["enablerate"] is False or c.message is None:
            pass
        else:
            rates = ["1/10", "2/10", "3/10", "4/10", "5/10",
                     "6/10", "7/10", "8/10", "9/10", "10/10"]
            msg = "I'd rate {} a {}".format(random.choice(rates), c.message)
            await self.send_message(msg)

