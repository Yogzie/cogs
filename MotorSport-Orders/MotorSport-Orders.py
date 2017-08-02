import discord
import random
import pygsheets
from discord.ext import commands
from .utils import checks

# gc = pygsheets.authorize(service_file='client_secret.json')


class MOTORSPORT_ORDERS:
    """Its all about MotorSport - Ordering System"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def order(self, ctx):
        gs_convert = []
        server = self.bot.get_server('341928926098096138')
        author = ctx.message.author
        order_channel = discord.utils.get(
            server.channels, name='orders', type=discord.ChannelType.text)
        await self.bot.send_message(author, """Hi, How may I help you today?\n\n `Reply '1' : Buy a vehicle`\n\n""")
        msg = await self.bot.wait_for_message(author=author, timeout=10)
        if msg is None:
            await self.bot.send_message(author, "You did not choose the correct option. Please type .order to start again")
        elif msg.content != '1':
            await self.bot.send_message(author, "You did not choose the correct option. Please type .order to start again")
        elif msg.content == '1':
            while True:
                await self.bot.send_message(author, "What is the vehicle name?")
                car_name = await self.bot.wait_for_message(author=author, timeout=120)
                if car_name is None:
                    await self.bot.send_message(author, "Timeout! Please type .order to place order again")
                    break
                await self.bot.send_message(author, """What is your First and Last name? (Character Name)""")
                customer_name = await self.bot.wait_for_message(author=author, timeout=120)
                if customer_name is None:
                    await self.bot.send_message(author, "Timeout! Please type .order to place order again")
                    break
                await self.bot.send_message(author, """Do you preferred to be contacted by Phone (In-game) or Email (Discord)?""")
                contact_method = await self.bot.wait_for_message(author=author, timeout=120)
                if contact_method is None:
                    await self.bot.send_message(author, "Timeout! Please type .order to place order again")
                    break
                await self.bot.send_message(author, """Any questions and comments?""")
                customer_remarks = await self.bot.wait_for_message(author=author, timeout=120)
                if customer_remarks is None:
                    await self.bot.send_message(author, """Nothing? Alright.""")
                    customer_remarks = "None"
                else:
                    customer_remarks = customer_remarks.content
                await self.bot.send_message(author, """__**Please check the following:**__\n\nVehicle Name: **{}**\nName: **{}**\nPreferred to be contacted by: **{}**\nRemarks: **{}**""".format(car_name.content, customer_name.content, contact_method.content, customer_remarks))
                await self.bot.send_message(author, """Is that correct? (**Yes**/**No**)""")
                answer = await self.bot.wait_for_message(author=author, timeout=120)
                if answer is None:
                    await self.bot.send_message(author, "Timeout! Please type .order to place order again")
                    break
                elif answer.content.lower() == 'yes':
                    embed = discord.Embed(colour=discord.Colour(0x7CFC00))
                    embed.set_thumbnail(
                        url="http://www.buygosleep.com/wp-content/uploads/2016/01/Car-Icon.png")
                    embed.set_author(name=customer_name.content, icon_url=author.avatar_url)
                    embed.set_footer(text="Posted by " + author.name + "#" + author.discriminator)
                    embed.add_field(name="Vehicle Name", value=car_name.content, inline=True)
                    embed.add_field(name="Preferred to be contacted by",
                                    value=contact_method.content, inline=True)
                    embed.add_field(name="Remarks", value=customer_remarks)
                    await self.bot.send_message(order_channel, content="@everyone, we have new order from {}.".format(author.mention), embed=embed)
                    # sh = gc.open("DCC Google Sheet")
                    # wks = sh.worksheet_by_title("HeavyFlow")
                    # gs_convert.append([car_name.content, customer_name.content,
                    #                   author.name + '#' + str(author.discriminator), contact_method.content, customer_remarks])
                    # wks.append_table(start='D2', end=None, values=gs_convert,
                    #                 dimension='ROWS', overwrite=False)
                    await self.bot.send_message(author, """Thank you for shopping with HeavyFlow, **{}**. Our sales team will contact you as soon as possible.""".format(customer_name.content))
                    break
                elif answer.content.lower() == 'no':
                    pass


def setup(bot):
    bot.add_cog(MOTORSPORT_ORDERS(bot))
