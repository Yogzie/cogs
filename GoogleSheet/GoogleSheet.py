import discord
import gspread
from discord.ext import commands
from .utils import checks
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('data/DCC/Drive.json', scope)
gc = gspread.authorize(credentials)


class GOOGLESHEET:
    """Google Sheet"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def gs(self, ctx):
        msg = await self.bot.say("Please wait while I feteching the data....")
        wks = gc.open("DCC Google Sheet").sheet1
        val = wks.acell('A1').value
        values_list = wks.col_values(1)
        output = '%s' % '\n'.join(filter(None, map(str, values_list)))
        await self.bot.edit_message(msg, output)


def setup(bot):
    bot.add_cog(GOOGLESHEET(bot))
