import discord
import os
from discord.ext import commands
from .utils import checks


class DCC_GENERAL:
    """Its all about Downtown Cab Co - General"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["bc"])
    async def businesscard(self, ctx, Your_Name: str, Your_Photo: str, Your_Position: str, Your_Phone_Number: str, Your_Email: str):

        """Use to generate businesscard\n\nUsage: (?)businesscard/(?)bc "Your Name" "URL of your photo" "Your Position" "Your Phone Number" "Your Email"\n\nExample: (?)bc "Mr Name Surname" "http://i.imgur.com/picture.png" "Trainee" "(323) 222-2222" "someone@downtowncab.co" """
        author = ctx.message.author

        await self.bot.say("Here is your businesscard, {}".format(author.mention))
        embed = discord.Embed(title="Downtown Cab Co",
                              url='http://downtowncab.co', color=10122825)
        embed.set_author(name="{}".format(
            Your_Name), icon_url='https://res.cloudinary.com/teepublic/image/private/s--4WWDcpP4--/t_Preview/b_rgb:ffb81c,c_limit,f_jpg,h_630,q_90,w_630/v1468933638/production/designs/84620_4.jpg')
        embed.set_thumbnail(url='{}'.format(Your_Photo))
        embed.add_field(name="Position:", value="{}".format(Your_Position), inline=False)
        embed.add_field(name="Phone Number: ", value="{}".format(
            Your_Phone_Number), inline=True)
        embed.add_field(name="Email: ", value="{} (({}))".format(
            Your_Email, author.mention), inline=True)
        embed.set_image(
            url='https://ih1.redbubble.net/image.108030494.9939/flat,1000x1000,075,f.u5.jpg')
        await self.bot.say(embed=embed)


def setup(bot):
    n = DCC_GENERAL(bot)
    bot.add_cog(DCC_GENERAL(bot))
