import discord
from discord.ext import commands
from .utils.dataIO import fileIO
from .utils import checks
import os
import asyncio
import time
import logging


class DCC_Inactive:
    """Its all about Downtown Cab Co - Inactive System"""

    def __init__(self, bot):
        self.bot = bot
        self.inactives = fileIO("data/DCC/inactive/inactive.json", "load")
        self.units = {"day": 86400, "week": 604800, "month": 2592000}

    def is_not_channel(id):
        def predicate(ctx):
            return ctx.message.channel.id != id
        return commands.check(predicate)

    @commands.command(pass_context=True, no_pm=True)
    @is_not_channel('310186316442894337')
    async def inactive(self, ctx, quantity: int, time_unit: str, *, reason: str):
        """Generate Inactive Report

        The time unit must be: days, weeks, month
        For example:
        .inactive 3 days Holiday Time"""
        author = ctx.message.author
        server = ctx.message.server
        time_unit = time_unit.lower()
        s = ""
        if time_unit.endswith("s"):
            time_unit = time_unit[:-1]
            s = "s"
        if not time_unit in self.units:
            await self.bot.say("Invalid time unit. Choose days/weeks/month")
            return
        if quantity < 1:
            await self.bot.say("Quantity must not be 0 or negative.")
            return
        if len(reason) > 1960:
            await self.bot.say("The reason is too long.")
            return
        name = author.nick
        seconds = self.units[time_unit] * quantity
        future = int(time.time() + seconds)
        self.inactives.append({"ID": author.id, "NAME": name, "FUTURE": future, "REASON": reason})
        logger.info("{} ({}) set an inactive report.".format(author.name, author.id))
        inactivity_info = discord.utils.get(
            server.channels, name='inactivity-info', type=discord.ChannelType.text)
        embed = discord.Embed(title="Downtown Cab Co. Absence Report", colour=discord.Colour(
            0xffff00), description="I wish to inform you that")
        embed.set_thumbnail(
            url="https://res.cloudinary.com/teepublic/image/private/s--4WWDcpP4--/t_Preview/b_rgb:ffb81c,c_limit,f_jpg,h_630,q_90,w_630/v1468933638/production/designs/84620_4.jpg")
        embed.set_author(name=name, icon_url=author.avatar_url)
        embed.set_footer(text="Posted by " + author.name + "#" + author.discriminator)
        embed.add_field(name="I will be absent for:", value="{} {}".format(
            str(quantity), time_unit + s), inline=False)
        embed.add_field(name="Reason:", value=reason)
        await self.bot.send_message(inactivity_info, embed=embed)
        await self.bot.delete_message(ctx.message)
        fileIO("data/DCC/inactive/inactive.json", "save", self.inactives)

    async def check_inactives(self):
        getDCCserver = self.bot.get_server('301659110104104962')
        management = discord.utils.get(
            getDCCserver.channels, name='management', type=discord.ChannelType.text)
        while self is self.bot.get_cog("DCC_Inactive"):
            to_remove = []
            for inactive in self.inactives:
                if inactive["FUTURE"] <= int(time.time()):
                    try:
                        embed = discord.Embed(colour=discord.Colour(0xff0000))

                        embed.set_thumbnail(url="http://www.freeiconspng.com/download/13396")
                        embed.set_author(name="{}".format(
                            inactive["NAME"]), icon_url="http://www.freeiconspng.com/download/13396")

                        embed.add_field(name="Downtown Cab Co. Annual leave Application",
                                        value="The annual leave application has been expired")

                        await self.bot.send_message(management, embed=embed)
                        reciever = getDCCserver.get_member(inactive["ID"])
                        if reciever is not None:
                            await self.bot.send_message(reciever, embed=embed)
                    except (discord.errors.Forbidden, discord.errors.NotFound):
                        to_remove.append(inactive)
                    except discord.errors.HTTPException:
                        pass
                    else:
                        to_remove.append(inactive)
            for inactive in to_remove:
                self.inactives.remove(inactive)
            if to_remove:
                fileIO("data/DCC/inactive/inactive.json", "save", self.inactives)
            await asyncio.sleep(5)


def check_folders():
    if not os.path.exists("data/DCC/inactive/"):
        print("Creating data/DCC/inactive/ folder...")
        os.makedirs("data/DCC/inactive/")


def check_files():
    f = "data/DCC/inactive/inactive.json"
    if not fileIO(f, "check"):
        print("Creating empty inactive.json...")
        fileIO(f, "save", [])


def setup(bot):
    global logger
    check_folders()
    check_files()
    logger = logging.getLogger("inactive")
    if logger.level == 0:  # Prevents the logger from being loaded again in case of module reload
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(
            filename='data/DCC/inactive/inactive.log', encoding='utf-8', mode='a')
        handler.setFormatter(logging.Formatter(
            '%(asctime)s %(message)s', datefmt="[%d/%m/%Y %H:%M]"))
        logger.addHandler(handler)
    n = DCC_Inactive(bot)
    loop = asyncio.get_event_loop()
    loop.create_task(n.check_inactives())
    bot.add_cog(n)
