import discord
import asyncio
from discord.ext import commands
import typing
import datetime
import random
from discord.member import Member
from pymongo import MongoClient, message

cluster = MongoClient("mongodb+srv://sumitm6879sm:sm6879sm@sambot.ipbu6.mongodb.net/SamBot?retryWrites=true&w=majority")
leveling = cluster['MysticBot']['levels']
# level Roles
level_role = ['Verified', 'Guest', 'Member', 'Super User', 'Addict', 'Veteran', 'Extreme user', 'Godly', 'Above all',
              'Legend']

levelnum = [2, 5, 10, 20, 40, 80, 120, 150, 180, 200]

no_xp_channels = [794815002095386654]
blacklist_words = [';lvl', ';rank', ';help']

prefix = [';', 'mh', 'mb', 'MH', 'MB', 'Mh', 'Mb', 'mH', 'mB', '.']


class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(1, 5, commands.BucketType.member)

    def get_ratelimit(self, message: discord.Message) -> typing.Optional[int]:
        """Returns the ratelimit left"""
        bucket = self._cd.get_bucket(message)
        return bucket.update_rate_limit()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Leveling system ONline")
        member = self.bot.fetch_user

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content not in blacklist_words and len(
                message.content) > 3 and not message.content.startswith(tuple(prefix)) and message.guild.id == 705513318747602944:
            if message.author.bot or message.channel.id in no_xp_channels:
                return
            ratelimit = self.get_ratelimit(message)
            stats = leveling.find_one({"_id": message.author.id})
            if stats is None:
                server_booster = message.guild.get_role(777611697312628776)
                if server_booster in message.author.roles:
                    new_user = {"_id": message.author.id, "xp": 2}
                else:
                    new_user = {"_id": message.author.id, "xp": 1}
                leveling.insert_one(new_user)
            else:
                if ratelimit is None:
                    member = message.author
                    stats = leveling.find_one({"_id": message.author.id})
                    server_booster = message.guild.get_role(777611697312628776)
                    if server_booster in member.roles:
                        xp = stats['xp'] + 2
                    else:
                        xp = stats['xp'] + 1
                    leveling.update_one({"_id": member.id}, {"$set": {"xp": xp}})
                    lvl = 0
                    while True:
                        if xp < ((20 * (lvl ** 2)) + (20 * lvl)):
                            break
                        lvl += 1
                    xp -= ((20 * ((lvl - 1) ** 2)) + (20 * (lvl - 1)))
                    if xp == 0:
                        xp = stats['xp'] + 2
                        leveling.update_one({"_id": message.author.id}, {"$set": {"xp": xp}})
                        await asyncio.create_task(level_up(message, lvl))
                    elif xp == 1:
                        xp -= 1
                        xp = stats['xp'] + 1
                        leveling.update_one({"_id": message.author.id}, {"$set": {"xp": xp}})
                        await asyncio.create_task(level_up(message, lvl))
                else:
                    return

    @commands.command(aliases=['lb', 'top'])
    async def leaderboard(self, ctx, page: int = None):
        if page is None or page == 1:
            ranking = leveling.find().sort('xp', -1)
            i = 1
            embed = discord.Embed(title=f"{ctx.guild.name}'s Leaderboard", description="# ┃ 🔹 Name 🔹 ┃ 🔸 Level 🔸\n", color=0xff0000,
                                  timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=ctx.guild.icon_url)
            for x in ranking:
                tempmember = ctx.guild.get_member(x['_id'])
                xp = x['xp']
                lvl = 0
                while True:
                    if xp < ((20 * (lvl ** 2)) + (20 * lvl)):
                        break
                    lvl += 1
                if i == 1:
                    a = '<:one:875010959817719849>'
                    embed.description += f"\n{a} {tempmember.mention} ~-~ Level: **{lvl}**\n"
                elif i == 2:
                    a = '<:two:875009735886241853>'
                    embed.description += f"\n{a} {tempmember.mention} ~-~ Level: **{lvl}**\n"
                elif i == 3:
                    a = '<:three:875012270063751178>'
                    embed.description += f"\n{a} {tempmember.mention} ~-~ Level: **{lvl}**\n"
                else:
                    embed.description += f"\n**{i})** {tempmember.mention} ~-~ Level: **{lvl}**\n"

                i += 1
                if i == 11:
                    break
            embed.add_field(
                name='More Members',
                value='> Example:-`;top 2` (up to 5 pages)'
            )
            await ctx.send(embed=embed)
        if page == 2:
            ranking = leveling.find().sort('xp', -1).skip(10)
            i = 11
            embed = discord.Embed(title=f"{ctx.guild.name}'s Leaderboard [{page}]", description="# ┃ 🔹 Name 🔹 ┃ 🔸 Level 🔸\n", color=0xff0000,
                                  timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=ctx.guild.icon_url)
            for x in ranking:
                tempmember = ctx.guild.get_member(x['_id'])
                xp = x['xp']
                lvl = 0
                while True:
                    if xp < ((20 * (lvl ** 2)) + (20 * lvl)):
                        break
                    lvl += 1
                embed.description += f"\n**{i})** {tempmember.mention} ~-~ Level: **{lvl}**\n"

                i += 1
                if i == 21:
                    break
            if embed.description == "":
                embed.description += "No Data to show"
            await ctx.send(embed=embed)

        if page == 3:
            ranking = leveling.find().sort('xp', -1).skip(20)
            i = 21
            embed = discord.Embed(title=f"{ctx.guild.name}'s Leaderboard [{page}]", description="# ┃ 🔹 Name 🔹 ┃ 🔸 Level 🔸\n", color=0xff0000,
                                  timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=ctx.guild.icon_url)
            for x in ranking:
                tempmember = ctx.guild.get_member(x['_id'])
                xp = x['xp']
                lvl = 0
                while True:
                    if xp < ((20 * (lvl ** 2)) + (20 * lvl)):
                        break
                    lvl += 1
                embed.description += f"\n**{i})** {tempmember.mention} ~-~ Level: **{lvl}**\n"

                i += 1
                if i == 31:
                    break
            if embed.description == "":
                embed.description += "No Data to show"
            await ctx.send(embed=embed)

        if page == 4:
            ranking = leveling.find().sort('xp', -1).skip(30)
            i = 31
            embed = discord.Embed(title=f"{ctx.guild.name}'s Leaderboard [{page}]", description="# ┃ 🔹 Name 🔹 ┃ 🔸 Level 🔸\n", color=0xff0000,
                                  timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=ctx.guild.icon_url)
            for x in ranking:
                tempmember = ctx.guild.get_member(x['_id'])
                xp = x['xp']
                lvl = 0
                while True:
                    if xp < ((20 * (lvl ** 2)) + (20 * lvl)):
                        break
                    lvl += 1
                embed.description += f"\n**{i})** {tempmember.mention} ~-~ Level: **{lvl}**\n"

                i += 1
                if i == 41:
                    break
            if embed.description == "":
                embed.description += "No Data to show"
            await ctx.send(embed=embed)

        if page == 5:
            ranking = leveling.find().sort('xp', -1).skip(40)
            i = 41
            embed = discord.Embed(title=f"{ctx.guild.name}'s Leaderboard [{page}]", description="# ┃ 🔹 Name 🔹 ┃ 🔸 Level 🔸\n", color=0xff0000,
                                  timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=ctx.guild.icon_url)
            for x in ranking:
                tempmember = ctx.guild.get_member(x['_id'])
                xp = x['xp']
                lvl = 0
                while True:
                    if xp < ((20 * (lvl ** 2)) + (20 * lvl)):
                        break
                    lvl += 1
                embed.description += f"\n**{i})** {tempmember.mention} ~-~ Level: **{lvl}**\n"

                i += 1
                if i == 51:
                    break
            if embed.description == "":
                embed.description += "No Data to show"
            await ctx.send(embed=embed)

    @commands.command(aliases=['add-xp'])
    @commands.has_permissions(kick_members=True)
    async def add_xp(self, ctx, member: discord.Member = None, amount: int = None):
        if amount is None:
            return await ctx.send(
                f"Exp Amount Not Found Please use the format:-\n**{self.bot.command_prefix}add_xp [member] [amount]**")
        stats = leveling.find_one({"_id": member.id})
        if amount <= 0:
            return await ctx.send("This Amount is Not Accepted enter a amount greater than 0")
        if stats is None:
            await ctx.send("Mmber has never sent a message\nAdding Him in Database")
            server_booster = ctx.guild.get_role(777611697312628776)
            if server_booster in member.roles:
                await ctx.send(f"{member.mention} is a **Server Booster**")
            xp = amount
            new_user = {"_id": member.id, "xp": xp}
            leveling.insert_one(new_user)
            await asyncio.create_task(verify_level_up(ctx, xp, stats))
            await ctx.send(f"Added {amount}xp to {member.mention}")
        else:
            server_booster = ctx.guild.get_role(777611697312628776)
            if server_booster in member.roles:
                await ctx.send(f"{member.mention} is a Server Booster")
            xp = stats['xp'] + amount
            leveling.update_one({"_id": member.id}, {"$set": {'xp': xp}})
            await asyncio.create_task(verify_level_up(ctx, xp, stats))
            await ctx.send(f"Added **{amount}**xp to {member.mention}")

    @commands.command(aliases=['rev-xp'])
    @commands.has_permissions(kick_members=True)
    async def rev_xp(self, ctx, member: discord.Member = None, amount: int = None):
        if member is None:
            return await ctx.send(f"Wrong syntax use:-\n**{self.bot.command_prefix}add_xp [member] [amount]**")
        if amount is None:
            return await ctx.send(
                f"Exp Amount Not Found Please use the format:-\n**{self.bot.command_prefix}add_xp [member] [amount]**")
        stats = leveling.find_one({"_id": member.id})
        if amount <= 0:
            return await ctx.send("This Amount is Not Accepted! Enter a amount greater than 0")
        if stats is None:
            return await ctx.send("Member has No Ranks in the server")
        else:
            server_booster = ctx.guild.get_role(777611697312628776)
            if server_booster in member.roles:
                await ctx.send(f"{member.mention} is a Server Booster")
            xp = stats['xp']
            if xp < amount:
                return await ctx.send(
                    f"You cannot deduct `{amount}xp` form **{member.name}** as they only have `{xp}xp` ")
            else:
                xp = stats['xp'] - amount
                leveling.update_one({"_id": member.id}, {"$set": {'xp': xp}})
                await ctx.send(f"Removed **{amount}**xp from {member.mention}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def set(self, ctx, g: str, member: discord.Member = None, level: int = None):
        if Member is None and ctx.message.reference:
            msg = await ctx.channel.fetch_message(id=ctx.message.reference.message_id)
            member = msg.author
        if member is None:
            return await ctx.send(
                f"**Member** is a required argument missing!\n**{self.bot.command_prefix}set level [member] [level]**")
        if level is None:
            return await ctx.send(
                f"**Level** is a required argument missing!\n**{self.bot.command_prefix}set level [member] [level]**")
        if g.lower() in ['lvl', 'level']:
            xp = ((20 * ((level - 1) ** 2)) + (20 * (level - 1)))
            stats = leveling.find_one({"_id": member.id})
            if stats is None:
                new_member = {"_id": member.id, 'xp': xp}
                leveling.insert_one(new_member)
                await ctx.channel.send(f"Congratulations {member.mention} You Leveled up to level **{level}**")
                chan = ctx.author.guild.get_channel(874705596597813288)
                embed = get_embed_for_set_level(ctx, member, level)
                await chan.send(embed=embed)
                for i in range(len(level_role)):
                    if level == levelnum[i]:
                        await member.add_roles(discord.utils.get(member.guild.roles, name=level_role[i]))
                        await member.remove_roles(discord.utils.get(member.guild.roles, name=level_role[i - 1]))
                        await ctx.channel.send(
                            f"Congratulations {member.mention} You have unlocked the new role **{level_role[i]}**")
                await ctx.send(f"Set the level of {member.mention} to Level: **{level}**")
            else:
                xp = xp
                leveling.update_one({"_id": member.id}, {"$set": {'xp': xp}})
                chan = ctx.author.guild.get_channel(874705596597813288)
                embed = get_embed_for_set_level(ctx, member, level)
                await chan.send(embed=embed)
                for i in range(len(level_role)):
                    if level == levelnum[i]:
                        await member.add_roles(discord.utils.get(member.guild.roles, name=level_role[i]))
                        await member.remove_roles(discord.utils.get(member.guild.roles, name=level_role[i - 1]))
                        await ctx.channel.send(
                            f"Congratulations {member.mention} You have unlocked the new role **{level_role[i]}**")
                await ctx.send(f"Set the level of {member.mention} to Level: **{level}**")

    @commands.command()
    async def rewards(self, ctx):
        embed = discord.Embed(
            title=f"{ctx.guild.name} Level Rewards",
            description="",
            color=0xff0000,
            timestamp=datetime.datetime.utcnow()
        )
        for i in range(len(level_role)):
            temprole = discord.utils.get(ctx.author.guild.roles, name=level_role[i])
            templevel = levelnum[i]
            embed.description += f"\nLevel **{templevel}** ~-~> {temprole.mention}"
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Leveling(bot))


# Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_embed_for_set_level(ctx, member, level):
    embed = discord.Embed(
        title=f"{ctx.author.name} used set level",
        description=f"{ctx.author.mention} used `set level` command and set the level of {member.mention} to Level: **{level}**\nChannel: {ctx.channel.mention}",
        color=discord.Color.random(),
        timestamp=datetime.datetime.utcnow()
    )
    return embed


def get_embed_level_up(message, lvl):
    embed = discord.Embed(
        title=f"{message.author.name} Leveled up!",
        description=f"Name: **{message.author.name}{message.author.discriminator}**\nLevel: **{lvl}**",
        color=discord.Color.random(),
        timestamp=datetime.datetime.utcnow()
    )
    return embed


async def level_up(message, lvl):
    chan = message.author.guild.get_channel(874705596597813288)
    embed = get_embed_level_up(message, lvl)
    await message.channel.send(f"Congratulations {message.author.mention} You Leveled up to level **{lvl}**")
    for i in range(len(level_role)):
        if lvl == levelnum[i]:
            await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=level_role[i]))
            await message.author.remove_roles(discord.utils.get(message.author.guild.roles, name=level_role[i - 1]))
            await message.channel.send(embed=discord.Embed(
                title="New Role Unlocked!",
                description=f"Congratulations {message.author.mention} You have unlocked the new role **{level_role[i]}**",
                color=0x00ff00,
                timestamp=datetime.datetime.utcnow())
            )
            embed.description += f"\nNew Role: **{level_role[i]}**"
    await chan.send(embed=embed)


async def verify_level_up(ctx, xp, stats):
    lvl = 0
    while True:
        if xp < ((20 * (lvl ** 2)) + (20 * lvl)):
            break
        lvl += 1
    xp -= ((20 * ((lvl - 1) ** 2)) + (20 * (lvl - 1)))
    if xp == 0:
        xp = stats['xp'] + 1
        leveling.update_one({"_id": message.author.id}, {"$set": {"xp": xp}})
        chan = ctx.author.guild.get_channel(874705596597813288)
        embed = discord.Embed(
            title=f"{ctx.author.mention} Leveled up!",
            description=f"Name: **{ctx.author.name}{ctx.author.discriminator}**\nLevel: **{lvl}**",
            color=discord.Color.random(),
            timestamp=datetime.datetime.utcnow()
        )
        await ctx.send(f"Congratulations {message.author.mention} You Leveled up to level **{lvl}**")
        for i in range(len(level_role)):
            if lvl == levelnum[i]:
                await ctx.author.add_roles(discord.utils.get(ctx.author.guild.roles, name=level_role[i]))
                await ctx.author.remove_roles(discord.utils.get(ctx.author.guild.roles, name=level_role[i - 1]))
                await ctx.channel.send(embed=discord.Embed(
                    title="New Role Unlocked!",
                    description=f"Congratulations {ctx.author.mention} You have unlocked the new role **{level_role[i]}**",
                    color=0x00ff00,
                    timestamp=datetime.datetime.utcnow())
                )
                embed.description += f"\nNew Role: **{level_role[i]}**"
        await chan.send(embed=embed)
    elif xp == 1:
        xp -= 1
        xp = stats['xp'] + 1
        leveling.update_one({"_id": message.author.id}, {"$set": {"xp": xp}})
        chan = ctx.author.guild.get_channel(874705596597813288)
        embed = discord.Embed(
            title=f"{ctx.author.mention} Leveled up!",
            description=f"Name: **{ctx.author.name}{ctx.author.discriminator}**\nLevel: **{lvl}**",
            color=discord.Color.random(),
            timestamp=datetime.datetime.utcnow()
        )
        await ctx.send(f"Congratulations {message.author.mention} You Leveled up to level **{lvl}**")
        for i in range(len(level_role)):
            if lvl == levelnum[i]:
                await ctx.author.add_roles(discord.utils.get(ctx.author.guild.roles, name=level_role[i]))
                await ctx.author.remove_roles(discord.utils.get(ctx.author.guild.roles, name=level_role[i - 1]))
                await ctx.channel.send(embed=discord.Embed(
                    title="New Role Unlocked!",
                    description=f"Congratulations {ctx.author.mention} You have unlocked the new role **{level_role[i]}**",
                    color=0x00ff00,
                    timestamp=datetime.datetime.utcnow())
                )
                embed.description += f"\nNew Role: **{level_role[i]}**"
        await chan.send(embed=embed)
