import discord
import os
from discord.ext import commands


class DCC_INFO:
    """Its all about Downtown Cab Co Script Info"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def dccinfo(self, ctx):
        """Use to check if the script is running"""

        await self.bot.delete_message(ctx.message)
        await self.bot.say("""The bot is running.\nBot script for Eclipse Roleplay - Downtown Cab Co.\nMade by Natawat "Minin0la" Hebnak""")


def setup(bot):
    bot.add_cog(DCC_INFO(bot))
