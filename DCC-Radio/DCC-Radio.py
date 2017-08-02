import discord
from discord.ext import commands
from .utils import checks


class DCC_RADIO:
    """Its all about Downtown Cab Co - Radio System"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["rf"])
    @checks.mod_or_permissions()
    async def radiofreq(self, ctx, number: int = 9999):
        """Use to announce radio freq number"""

        author = ctx.message.author
        server = ctx.message.server
        await self.bot.delete_message(ctx.message)
        announcements_channel = discord.utils.get(
            server.channels, name='annoucements', type=discord.ChannelType.text)
        await self.bot.send_message(announcements_channel, """@everyone Change your radio frequencies to {} ( /radiofreq {} ) , trainees read #faq-help. \n(By {})""".format(number, number, author.mention))


def setup(bot):
    bot.add_cog(DCC_RADIO(bot))
