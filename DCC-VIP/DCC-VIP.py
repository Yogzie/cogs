import discord
import os
from discord.ext import commands
from .utils import checks
from __main__ import user_allowed, send_cmd_help

viplistfile_path = "data/DCC/vip/list.txt"


class DCC_VIP:
    """Its all about Downtown Cab Co - VIP System"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def vip(self, ctx):

        """Use to check and manage VIP List"""
        if ctx.invoked_subcommand is None:
            file = open(viplistfile_path, "r")
            namelist = file.read()
            await self.bot.say(namelist)

    @vip.command(pass_context=True, no_pm=True)
    async def help(self, ctx):
        await self.bot.say("""```Downtown Cab Co. VIPs List System Help Page\n----------------------------\n\n(?)vip - Show VIPs List\n(?)vip add "Name" - Add Name into VIPs List\n(?)vip delete "Name" - Delete Name from VIPs List\n(?)vip clear - Clear VIPs List\n(?)vip search "Name" - Search Name in VIPs List\n(?) = Command Prefix```""")

    @vip.command(pass_context=True)
    @checks.mod_or_permissions()
    async def add(self, ctx, vipname: str):

        """Use to add VIP name\nUsage: (?)vip add "Name"\nMake sure you put " " or else the name will be cut off"""

        file = open(viplistfile_path, "a")
        file.write("- {}\n".format(vipname))
        file.close()
        await self.bot.say("{} has been added to VIPs list".format(vipname))

    @vip.command(pass_context=True, aliases=["del", "remove"])
    @checks.mod_or_permissions()
    async def delete(self, ctx, vipname: str):

        """Use to delete VIP name\nUsage: (?)vip delete/del/remove "Name"\nMake sure you put" " or else the name will be cut off"""

        vipremoved = 0
        nameremoved = ""
        file = open(viplistfile_path, "r")
        lines = file.readlines()
        file.close()
        file = open(viplistfile_path, "w")
        for line in lines:
            if line.lower() != "- " + vipname.lower() + "\n":
                file.write(line)
            if line == "- " + vipname + "\n":
                vipremoved = 1
                nameremoved = line
        file.close()
        if vipremoved == 1:
            await self.bot.say(nameremoved.rstrip() + " has been removed from VIPs list")
        else:
            await self.bot.say("{} could not be found in VIPs list".format(vipname))

    @vip.command(pass_context=True)
    @checks.admin_or_permissions()
    async def clear(self):

        """Use to delete all VIPs name"""

        file = open(viplistfile_path, "w")
        file.write("Downtown Cab Co. VIPs\n----------------------------\n\n")
        file.close()
        await self.bot.say("VIPs list has been cleared")

    @vip.command(pass_context=True)
    async def search(self, ctx, vipname: str):

        """Use to search VIP name\nUsage: (?)vip search "Name"\nMake sure you put " " or else the name will be cut off"""
        file = open(viplistfile_path, "r")
        VIP_Found = 0
        Done = 0
        while (Done == 0):
            await self.bot.say("I found the following:\n\n")
            for line in file:
                if line.lower().find(vipname.lower()) != -1:
                    await self.bot.say("`" + line + "`")
                    VIP_Found = 1
            file.close()
            Done = 1
        if VIP_Found == 0:
            await self.bot.say("`{} is not inside the VIPs list`".format(vipname))


def check_folders(bot):
    if not os.path.exists("data/DCC/vip"):
        print("Creating data/DCC/vip folder...")
        os.makedirs("data/DCC/vip")


def check_files(bot):
    f = "data/DCC/vip/list.txt"
    try:
        file = open(f, 'r')
    except IOError:
        file = open(f, 'w')
        file.write("Downtown Cab Co. VIPs\n----------------------------\n\n")
        file.close()
        print("Creating VIP List files...")


def setup(bot):
    check_folders(bot)
    check_files(bot)
    bot.add_cog(DCC_VIP(bot))
