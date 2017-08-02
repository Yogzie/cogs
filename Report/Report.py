import discord
import random
from discord.ext import commands
from .utils import checks
from .utils.chat_formatting import pagify, box


class MININ0LA_REPORT:
    """Its all about HeavyFlow - Ordering System"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def reportbot(self, ctx, *, report: str):
        gs_convert = []
        server = self.bot.get_server('324778372674617346')
        author = ctx.message.author
        report_channel = discord.utils.get(
            server.channels, name='bot-reports', type=discord.ChannelType.text)
        minin0la = server.get_member('151618321203200000')
        await self.bot.delete_message(ctx.message)
        msg = await self.bot.say("""Thank you for reporting. The message has been sent to {}!""".format(minin0la.mention))
        await self.bot.wait_for_message(author=author, timeout=10)
        await self.bot.delete_message(msg)
        await self.bot.send_message(report_channel, """__**New Report**__\n**Report made by** {}\n**Message:** {}""".format(author.mention, report))


def setup(bot):
    bot.add_cog(MININ0LA_REPORT(bot))
