import discord
import random
from discord.ext import commands
from .utils import checks

giveawaylistfile_path = "data/HeavyFlow/giveaway/list.txt"


class HEAVYFLOW_GIVEAWAY:
    """Its all about HeavyFlow - Giveaway System"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @checks.admin_or_permissions()
    async def giveaway(self, ctx):

        file = open(giveawaylistfile_path, "w")
        file.write("")
        file.close()
        Complete = 0
        Giveaway_Found = 0
        server = ctx.message.server
        author = ctx.message.author
        await self.bot.delete_message(ctx.message)
        members_name = list(server.members)
        while (Complete != 1):
            answer = ""
            Done = 0
            winner = random.choice(members_name)
            while (Done != 1):
                file = open(giveawaylistfile_path, "r")
                for line in file:
                    if line.lower().find(winner.lower()) != -1:
                        Giveaway_Found = 1
                file.close()
                if winner.status == discord.Status.online and Giveaway_Found != 1:
                    await self.bot.say("""Congratulations {}, you have been selected! Please reply `I Agree` within `30 minutes` to claim your prize, if not we will re-roll!""".format(winner.mention))
                    Done = 1
                else:
                    winner = random.choice(members_name)
            answer = await self.bot.wait_for_message(timeout=10, author=winner)
            if answer is None:
                await self.bot.say("""Sorry {}, you did not accept your prize in time!""".format(winner.mention))
            elif answer.content.lower() == "i agree":
                await self.bot.say("""Congratulations {}, you have accept your prize! Our Staff will contact you shortly.""".format(winner.mention))
                Complete = 1


def check_folders(bot):
    if not os.path.exists("data/HeavyFlow/giveaway"):
        print("Creating data/HeavyFlow/giveaway folder...")
        os.makedirs("data/HeavyFlow/giveaway")


def check_files(bot):
    f = "data/HeavyFlow/giveaway/list.txt"
    try:
        file = open(f, 'r')
    except IOError:
        file = open(f, 'w')
        file.write("")
        file.close()
        print("Creating Giveaway List files...")


def setup(bot):
    check_folders(bot)
    check_files(bot)
    bot.add_cog(HEAVYFLOW_GIVEAWAY(bot))
