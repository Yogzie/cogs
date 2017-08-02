import discord
import random
import pygsheets
from discord.ext import commands
from .utils import checks

# gc = pygsheets.authorize(service_file='client_secret.json')


class DCC_REPORT:
    """Its all about Downtown Cab Co. - Report System"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def report(self, ctx):
        gs_convert = []
        server = self.bot.get_server('301659110104104962')
        author = ctx.message.author
        management = discord.utils.get(
            server.channels, name='management', type=discord.ChannelType.text)
        await self.bot.send_message(author, """Hi, How may I help you today?\n\n `Reply '1' : Report an employee`\n\n""")
        msg = await self.bot.wait_for_message(author=author, timeout=10)
        if msg.content != '1' or msg is None:
            await self.bot.send_message(author, "You did not choose the correct option. Please type .report to start again")
        elif msg.content == '1':
            while True:
                await self.bot.send_message(author, "What is the employee's First and Last name? (Character Name)")
                report_name = await self.bot.wait_for_message(author=author, timeout=120)
                if report_name is None:
                    await self.bot.send_message(author, "Timeout! Please type .report to start again")
                    break
                await self.bot.send_message(author, """What is your First and Last name? (Character Name)""")
                employee_name = await self.bot.wait_for_message(author=author, timeout=120)
                if employee_name is None:
                    await self.bot.send_message(author, "Timeout! Please type .report to start again")
                    break
                await self.bot.send_message(author, """Explanation of events/why you are reporting. Please include the time and date. (You have 5 minutes to write)""")
                report_reason = await self.bot.wait_for_message(author=author, timeout=300)
                if report_reason is None:
                    await self.bot.send_message(author, "Timeout! Please type .report to start again")
                    break
                await self.bot.send_message(author, """Any evidence?""")
                evidence = await self.bot.wait_for_message(author=author, timeout=120)
                if evidence is None:
                    await self.bot.send_message(author, """Nothing? Alright.""")
                    evidence = "None"
                else:
                    evidence = evidence.content
                await self.bot.send_message(author, """__**Please check the following:**__\n\nYou are reporting **{}**\nYour name is **{}**\nExplanation of events/why you are reporting. Please include the time and date:\n**{}**\nEvidence:\n**{}**""".format(report_name.content, employee_name.content, report_reason.content, evidence))
                await self.bot.send_message(author, """Is that correct? (**Yes**/**No**)""")
                answer = await self.bot.wait_for_message(author=author, timeout=120)
                if answer is None:
                    await self.bot.send_message(author, "Timeout! Please type .report to start again")
                    break
                elif answer.content.lower() == 'yes':
                    embed = discord.Embed(colour=discord.Colour(0xFF0000))
                    embed.set_thumbnail(
                        url="https://cdn2.iconfinder.com/data/icons/freecns-cumulus/32/519791-101_Warning-512.png")
                    embed.set_author(name=employee_name.content, icon_url=author.avatar_url)
                    embed.set_footer(text="Posted by " + author.name + "#" + author.discriminator)
                    embed.add_field(name="Reporting employee name:", value=report_name.content, inline=False)
                    embed.add_field(name="Report made by:", value=employee_name.content, inline=False)
                    embed.add_field(name="Reason:", value=report_reason.content, inline=False)
                    embed.add_field(name="Evidence:", value=evidence, inline=False)
                    await self.bot.send_message(management, content="""We have a new report from {} ({}).""".format(author.mention, employee_name.content), embed=embed)
                    # sh = gc.open("DCC Google Sheet")
                    # wks = sh.worksheet_by_title("HeavyFlow")
                    # gs_convert.append([report_name.content, employee_name.content,
                    #                   author.name + '#' + str(author.discriminator), report_reason.content, evidence])
                    # wks.append_table(start='D2', end=None, values=gs_convert,
                    #                 dimension='ROWS', overwrite=False)
                    await self.bot.send_message(author, """Thank you for reporting **{}**. The management team will review your report as soon as possible.""".format(employee_name.content))
                    break
                elif answer.content.lower() == 'no':
                    pass


def setup(bot):
    bot.add_cog(DCC_REPORT(bot))
