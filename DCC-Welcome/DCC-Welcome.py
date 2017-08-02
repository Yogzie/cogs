import discord
import os
from discord.ext import commands
from .utils import checks


class DCC_WELCOME:
    """Its all about Downtown Cab Co - Promotion System"""

    def __init__(self, bot):
        self.bot = bot

    async def member_join(self, member):

        server = member.server
        guest_channel = discord.utils.get(server.channels, name='guests',
                                          type=discord.ChannelType.text)
        # role = discord.utils.get(server.roles, name='Guest')
        # await self.bot.add_roles(member, role)
        Join_Message = await self.bot.send_message(guest_channel, """**Welcome to Downtown Cab co. {}.**\nPlease use command .name <FirstName> <LastName> into this channel to get access to Downtown social site.\nFor example: `.name James Cab`""".format(member.mention))
        await self.bot.wait_for_message(author=member)
        await self.bot.delete_message(Join_Message)

    @commands.command(pass_context=True, no_pm=True)
    async def name(self, ctx, first_name: str, last_name: str):

        """Use to change name on first join"""
        server = ctx.message.server
        author = ctx.message.author
        name = first_name + " " + last_name
        general_channel = discord.utils.get(
            server.channels, name='dcc-general', type=discord.ChannelType.text)
        # guest = discord.utils.get(server.roles, name='Guest')
        trainee = discord.utils.get(server.roles, name='Trainee')
        everyone = discord.utils.get(server.roles, name='@everyone')
        # await self.bot.remove_roles(author, guest)
        if author.top_role is everyone:
            await self.bot.add_roles(author, trainee)
            await self.bot.change_nickname(author, name)
            await self.bot.delete_message(ctx.message)
            await self.bot.send_message(general_channel, """Welcome to the team, {}. Read <#307897167832678400> and <#312884892793044992>, if you have any questions feel free to ask, good luck.""".format(author.mention))


def setup(bot):
    n = DCC_WELCOME(bot)
    bot.add_listener(n.member_join, "on_member_join")
    bot.add_cog(n)
