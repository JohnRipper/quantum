from lib.cog import Cog
from lib.command import Command, makeCommand
import random

class Fun(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.settings = self.bot.settings["module"]["fun"]

    @makeCommand(name="roll", description="<sides> <dice>, default is single 6 sided")
    def roll(self, sides=6, dice=1):
        if sides.isdigit() and dice.isdigit():
            sides = int(sides); dice = int(dice)
        else:
            self.send_message("Gonna need numbers m8")
        if sides > 20 or dice > 15:
            self.send_message("D&D dice only has 20 sides, wtf m8")
        else:
            rolled = []
            total = 0
            faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
            for die in range(dice):
                r = random.randint(1,sides)
                if sides == 6 and self.settings["fancydice"] is True:
                    rolled.append(faces[r-1])
                else:
                    rolled.append(str(r))
            msg = "You roll {} for a total of {}".format(
                " ".join(rolled), total)
            self.send_message(msg)

    @makeCommand(name="8ball", description="<query> standard magic 8ball")
    def 8ball(query: str = None):
        if len(query) < 3 or "?" not in query:
            self.send_message("You must ask a question.")
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
            self.send_message(msg)

    @makeCommand(name="rate", description="<user> rate someones appearance")
    def rate(query: str = None):
        # some can find a "rate" command insensitive
        if self.settings["enablerate"] is False or query is None:
            pass
        else:
            rates = ["1/10", "2/10", "3/10", "4/10", "5/10",
                     "6/10", "7/10", "8/10", "9/10", "10/10"]
            msg = "I'd rate {} a {}".format(random.choice(rates), user)
            self.send_message(msg)

