import discord
import os
from discord.ext import commands
from .utils import checks
from datetime import datetime


class DCC_PROMOTION:
    """Its all about Downtown Cab Co - Promotion System"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def promotion(self, ctx):
        author = ctx.message.author
        await self.bot.say("""{},\nPromotions happen each weekend (saturday or sunday) also depends when you were hired . Yet you do have to fill "Promotion application" - http://bit.ly/2stHBPn on friday to apply for one.""".format(author.mention))

    @commands.command(pass_context=True)
    @checks.mod_or_permissions(manage_roles=True)
    async def promote(self, ctx, user: discord.Member, *, role_name: discord.Role):

        """Use to promote players"""
        server = ctx.message.server
        author = ctx.message.author
        channel = discord.utils.get(server.channels, name='dcc-general',
                                    type=discord.ChannelType.text)
        bot_coders_channel = discord.utils.get(
            server.channels, name='bot-coders', type=discord.ChannelType.text)
        old_role = user.top_role
        await self.bot.delete_message(ctx.message)
        await self.bot.add_roles(user, role_name)
        embed = discord.Embed(title="Downtown Cab Co. Management", colour=discord.Colour(
            0x7CFC00), description="Congratulations {},\n\nWe would like to inform you that you have been promoted from **{}** to **{}**\n\nKeep up the good work!".format(user.display_name, old_role.name, role_name.name))
        embed.set_thumbnail(
            url="https://res.cloudinary.com/teepublic/image/private/s--4WWDcpP4--/t_Preview/b_rgb:ffb81c,c_limit,f_jpg,h_630,q_90,w_630/v1468933638/production/designs/84620_4.jpg")
        await self.bot.send_message(channel, "{}".format(user.mention), embed=embed)
        await self.bot.send_message(user, "{}".format(user.mention), embed=embed)
        await self.bot.send_message(bot_coders_channel, "{} uses command .promote to promote {} to rank {}".format(author.mention, user.mention, role_name.mention))

    @commands.command(pass_context=True)
    @checks.mod_or_permissions(manage_roles=True)
    async def demote(self, ctx, user: discord.Member, *, role_name: discord.Role):

        """Use to demote players"""

        server = ctx.message.server
        author = ctx.message.author
        channel = discord.utils.get(server.channels, name='dcc-general',
                                    type=discord.ChannelType.text)
        bot_coders_channel = discord.utils.get(
            server.channels, name='bot-coders', type=discord.ChannelType.text)
        old_role = user.top_role
        await self.bot.delete_message(ctx.message)
        await self.bot.remove_roles(user, user.top_role)
        await self.bot.add_roles(user, role_name)
        while (user.top_role != role_name):
            try:
                await self.bot.remove_roles(user, user.top_role)
            except discord.Forbidden:
                await self.bot.say("I don't have permissions to demote {}!".format(user.mention))
        date = datetime.now().strftime('%Y-%m-%d')
        embed = discord.Embed(title="Downtown Cab Co. Management", colour=discord.Colour(
            0xFF0000), description="Dear {},\n\nThe Management has reviewed your case and based on the information and testimonials available, henceforth effective from {}, you are demoted from **{}** to **{}**.\n\nIf you have any question,  contact the management.".format(user.display_name, date, old_role.name, role_name.name))
        embed.set_thumbnail(
            url="https://res.cloudinary.com/teepublic/image/private/s--4WWDcpP4--/t_Preview/b_rgb:ffb81c,c_limit,f_jpg,h_630,q_90,w_630/v1468933638/production/designs/84620_4.jpg")
        await self.bot.send_message(channel, "{}".format(user.mention), embed=embed)
        await self.bot.send_message(user, "{}".format(user.mention), embed=embed)
        await self.bot.send_message(bot_coders_channel, "{} uses command .demote to demote {} to rank {}".format(author.mention, user.mention, role_name.mention))


def setup(bot):
    bot.add_cog(DCC_PROMOTION(bot))
