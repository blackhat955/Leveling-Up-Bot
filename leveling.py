import asyncio
from datetime import datetime
from os import name
import discord
from discord import client
from discord.ext import commands, tasks
from easy_pil import Editor
from PIL import Image, ImageDraw, ImageFont
import datetime
from Game import economy, ecomod, ecoshop
from discord.ext.commands import CommandNotFound, MemberNotFound, MissingPermissions, MissingRequiredArgument, \
    BadArgument, CommandOnCooldown
from pymongo import MongoClient
import mleveling
import rank_card
import help_command
from discord_slash_components_bridge import SlashCommand

P = 'sumitm6879sm'
cluster = MongoClient(
    f"mongodb+srv://{P}:sm6879sm@sambot.ipbu6.mongodb.net/SamBot?retryWrites=true&w=majority"
)
leveling = cluster['MysticBot']['levels']
bg_user = cluster['MysticBot']['bg_user']
bot_prefix = cluster['MysticBot']['bot_prefix']
print("DB CONNECTED")


intents = discord.Intents().all()
bot = commands.Bot(command_prefix=';',
                   intents=intents,
                   case_insensitive=True)
slash = SlashCommand(bot, sync_commands=True)
bot.remove_command('help')
bot.load_extension('jishaku')
cogs = [mleveling, rank_card, economy, ecomod, help_command, ecoshop]

for i in range(len(cogs)):
    cogs[i].setup(bot)
    print("yay!!")


@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "\n")
    # chan = bot.get_channel(721361976957206568)
    # await chan.send("Leveling Bot ONline")
    member_cleanup.start()


@tasks.loop(seconds=60)
async def member_cleanup():
    members = leveling.find({})
    for x in members:
        guild = bot.get_guild(705513318747602944)
        member_id = x['_id']
        member_search = guild.get_member(x['_id'])
        if member_search is None:
            leveling.delete_one({"_id": member_id})
        else:
            pass


@bot.listen('on_message')
async def on_message(message):
    if message.author.id == 786862562494251038 and message.content.lower() in ['promote', 'powerup', 'boost', 'fire!']:
        developer_Role = message.guild.get_role(860929100934807592)
        if developer_Role in message.author.roles:
            await message.add_reaction('🔻')
            await message.author.remove_roles(developer_Role)
        else:
            await message.author.add_roles(developer_Role)
            await message.add_reaction('🔺')
    
    
@bot.command()
async def ping(ctx):
    numbers = {0: '𝟘', 1: '𝟙', 2: '𝟚', 3: '𝟛', 4: '𝟜', 5: '𝟝', 6: '𝟞', 7: '𝟟', 8: '𝟠', 9: '𝟡'}
    ping = round(bot.latency * 1000)
    x = [int(a) for a in str(ping)]
    new_ping = ""
    for i in x:
        new_ping += "".join(numbers[i])

    embed = discord.Embed(title="Mystic Levels's Latency", description=f'**{new_ping} 𝕞𝕤**', color=0xff0000)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.set_footer(text=f"{bot.command_prefix}help to get more info.", icon_url=bot.user.avatar_url)
    await ctx.send(embed=embed)

@slash.slash(name='lvl', description='Check your level or the level of a member')
async def lvl(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    if member.bot is True:
        return await ctx.send("You cannot check the Level of Bots")
    index = bg_user.find_one({"_id": member.id})
    if index is None:
        stats = leveling.find_one({"_id": member.id})
        if stats is None:
            if member == ctx.author:
                await ctx.send("You don't have any Level to see")
            else:
                await ctx.send(f"{member.name} has no Level")
        else:
            xp = stats['xp']
            lvl = 0
            while True:
                if xp < ((20 * (lvl ** 2)) + (20 * lvl)):
                    break
                lvl += 1
            # xp -= ((20*((lvl-1)**2))+(20*(lvl-1)))
            ranking = leveling.find().sort('xp', -1)
            rank = 0
            for x in ranking:
                rank += 1
                if member.id == x['_id']:
                    break
            xp -= ((20 * ((lvl - 1) ** 2)) + (20 * (lvl - 1)))
            boxes = int((xp / (80 * ((1 / 2) * lvl))) * 10)
            percent = round(float((xp / (lvl * 40)) * 100), 2)
            emoji_1 = '❤'
            emoji_2 = '🖤'
            progress_bar = boxes * emoji_1 + (10 - boxes) * emoji_2
            embed = discord.Embed(
                title=f"{member.name}'s Rank",
                description=f"Name: **{member.mention}**\nExp: **{xp}/{int((80 * (1 / 2) * lvl))}**\nLevel: **{lvl}** | Rank: **#{rank}**",
                color=discord.Color.random(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.add_field(name=f"Progress: {percent}%", value=f"`{progress_bar}`")
            embed.set_thumbnail(url=member.avatar_url)
            server_booster = member.guild.get_role(777611697312628776)
            if server_booster in member.roles:
                embed.description += f"\nPerks: {server_booster.mention}"
                embed.set_footer(text='Server Boosters get 2x EXP')
            await ctx.send(embed=embed)
    else:
        guest = ctx.guild.get_role(794896587943575563)
        verified = ctx.guild.get_role(794886884497031168)
        mem = ctx.guild.get_role(794896588623052830)
        super_user = ctx.guild.get_role(794896601856475166)
        Addict = ctx.guild.get_role(794896602694156318)
        await asyncio.sleep(0.21)
        Veteran = ctx.guild.get_role(794896707971973132)
        Extreme_user = ctx.guild.get_role(794896709380866098)
        godly = ctx.guild.get_role(796353896478015549)
        above_all = ctx.guild.get_role(796354367711870997)
        legend = ctx.guild.get_role(794896709380866098)
        server_booster = member.guild.get_role(777611697312628776)
        stats = leveling.find_one({"_id": member.id})
        name = str(member)
        xp = stats['xp']
        lvl = 0
        while True:
            if xp < ((20 * (lvl ** 2)) + (20 * lvl)):
                break
            lvl += 1
        # xp -= ((20*((lvl-1)**2))+(20*(lvl-1)))
        ranking = leveling.find().sort('xp', -1)
        rank = 0
        for x in ranking:
            rank += 1
            if member.id == x['_id']:
                break
        xp -= ((20 * ((lvl - 1) ** 2)) + (20 * (lvl - 1)))
        percent = round(float((xp / (lvl * 40)) * 100), 2)
        await member.avatar_url.save('user1.png')

        # fonts
        large_font = ImageFont.FreeTypeFont('antic.ttf', size=60)
        medium_font = ImageFont.FreeTypeFont('antic.ttf', size=30)
        small_font = ImageFont.FreeTypeFont('antic.ttf', size=25)
        extra_small_font = ImageFont.FreeTypeFont('antic.ttf', size=22)

        ## Rank Card
        background = Image.open("bjp4.jpg")
        draw = ImageDraw.Draw(background, 'RGB')
        booster_font = ImageFont.FreeTypeFont('booster.ttf', size=30)
        if server_booster in member.roles:
            draw.text((250, 193), "Perks: ", font=small_font, fill='grey')
            draw.text((335, 185), "Server Booster", font=booster_font, fill='#f47fff')
            draw.ellipse((25, 25, 205, 205), fill='#f47fff')
        # users Profile
        pfp = Image.open("user1.png").convert('RGBA')
        pfp = pfp.resize((170, 170))
        bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
        mask = Image.new("L", bigsize, 0)
        make = ImageDraw.Draw(mask)
        make.ellipse((0, 0) + bigsize, 255)
        mask = mask.resize(pfp.size, Image.ANTIALIAS)
        pfp.putalpha(mask)
        background.paste(pfp, (30, 30), mask=pfp)

        # Color of Member
        color = f"{member.color}"
        color = color.lstrip('#')
        # convert hex to tuple
        RGB = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))

        # right upper RANK
        text_size = draw.textsize(f"#{rank}", font=large_font)
        offset_x = 900 - 15 - text_size[0]
        offset_y = 10
        draw.text((offset_x, offset_y), f'#{rank}', font=large_font, fill=RGB)

        text_size = draw.textsize("RANK", font=small_font)
        offset_x -= text_size[0] - 5
        draw.text((offset_x, offset_y + 30), text="RANK", font=extra_small_font, fill="grey")

        # Level of Author
        text_size = draw.textsize(f'{lvl}', font=large_font)
        offset_x -= text_size[0] + 10
        draw.text((offset_x, 13), f"{lvl}", fill=RGB, font=large_font)

        text_size = draw.textsize('LEVEL', font=small_font)
        offset_x -= text_size[0] + 6
        draw.text((offset_x, offset_y + 30), text='LEVEL', font=small_font, fill="grey")

        # NAME OF AUTHOR
        author_font = ImageFont.FreeTypeFont('antic.ttf', size=45)
        if len(name) > 17:
            author_font = ImageFont.FreeTypeFont('antic.ttf', size=35)
            draw.text((250, 105), f"{name}", fill='white', font=author_font)
        else:
            draw.text((250, 100), f"{name}", fill='white', font=author_font)

        # Rank and Role of Author
        draw.text((250, 160), "Current Rank: ", fill='grey', font=small_font)
        if legend in member.roles:
            role_name = legend.name
            draw.text((420, 153), role_name, fill='white', font=booster_font)
        elif above_all in member.roles:
            role_name = above_all.name
            draw.text((420, 153), role_name, fill='white', font=booster_font)
        elif godly in member.roles:
            role_name = godly.name
            draw.text((420, 153), role_name, fill='white', font=booster_font)
        elif Extreme_user in member.roles:
            role_name = Extreme_user.name
            draw.text((420, 153), role_name, fill='white', font=booster_font)
        elif Veteran in member.roles:
            role_name = Veteran.name
            draw.text((420, 153), role_name, fill='white', font=booster_font)
        elif Addict in member.roles:
            role_name = Addict.name
            draw.text((420, 153), role_name, fill='white', font=booster_font)
        elif super_user in member.roles:
            role_name = super_user.name
            draw.text((420, 153), role_name, fill='white', font=booster_font)
        elif mem in member.roles:
            role_name = mem.name
            draw.text((420, 153), role_name, fill='white', font=booster_font)
        elif guest in member.roles:
            role_name = guest.name
            draw.text((420, 153), role_name, fill='white', font=booster_font)
        elif verified in member.roles:
            role_name = verified.name
            draw.text((420, 153), role_name, fill='white', font=booster_font)

        # Final xp
        xp_font = ImageFont.FreeTypeFont('antic.ttf', size=40)
        text_size = draw.textsize(f"/ {int((80 * (1 / 2) * lvl))} XP", font=xp_font)
        x = 865 - text_size[0]
        y = 203
        draw.text((x, y), f"/ {int((80 * (1 / 2) * lvl))} XP", font=xp_font, fill='#727175')

        text_size = draw.textsize(f'{xp}', font=xp_font)
        x1 = x - text_size[0] - 8
        y1 = 203
        draw.text((x1, y1), f'{xp}', font=xp_font, fill=RGB)

        background.save("pfp.png")

        new_background = Editor("pfp.png")

        new_background.rectangle((38, 240), width=840, height=30, radius=12, outline='grey')
        if server_booster in member.roles:
            new_background.rectangle((250, 146), width=450, height=2, radius=10, fill='#f47fff')
        else:
            new_background.rectangle((250, 146), width=450, height=2, radius=10, fill=RGB)
        if percent < 5:
            percent = 5.00
        new_background.bar((38, 240), max_width=840, height=30, percentage=percent, radius=15, fill=RGB)
        file = discord.File(fp=new_background.image_bytes, filename='member_lvl.png')
        await ctx.send(f"**{member.name}'s** level", file=file)
    
    
# @bot.command(aliases=['h'])
# async def help(ctx, arg: str = None):
#     if arg is None:
#         embed = discord.Embed(
#             title='Mystic Leveling System',
#             description='Everyone Gets **1xp** per message\nServer boosters Get **2xp** per message',
#             color=0xff0000,
#             timestamp=datetime.datetime.utcnow()
#         )
#         embed.add_field(name='Commands', value='🔻🔻🔻🔻', inline=False)
#         embed.add_field(name=f"{bot.command_prefix}level", value="Shows your level\n**Aliases**\n> `lvl`, `rank`", inline=False)
#         embed.add_field(name=f"{bot.command_prefix}leaderboard", value="Shows server Leaderboard\n**Aliases**\n> "
#                                                                        "`lb`, `top`", inline=False)
#         embed.add_field(name=f'{bot.command_prefix}background', value='Shows available background\n**Aliases**\n> '
#                                                                       '`bg`, `background`', inline=False) 
#         embed.set_thumbnail(url=bot.user.avatar_url)
#         embed.set_author(name=f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
#         await ctx.send(embed=embed)
#     elif arg.lower() == 'staff':
#         embed = discord.Embed(
#             title='Mystic Leveling System',
#             description='Everyone Gets **1xp** per message\nServer boosters Get **2xp** per message',
#             color=0xff0000,
#             timestamp=datetime.datetime.utcnow()
#         )
#         embed.add_field(name='Staff Commands', value='🔻🔻🔻🔻', inline=False)
#         embed.add_field(name=f'{bot.command_prefix}add-xp [member] [amount]',
#                         value='> Adds amount xp to member\n> Requires Kick members permission', inline=False)
#         embed.add_field(name=f'{bot.command_prefix}rev-xp [member] [amount]',
#                         value='> Removes amount xp from member\n> Requires Kick members permission', inline=False)
#         embed.add_field(name=f'{bot.command_prefix}set level [member] [level]',
#                         value='> changes the level of member\n> Requires Kick members permission', inline=False)
#         embed.set_thumbnail(url=bot.user.avatar_url)
#         embed.set_author(name=f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
#         await ctx.send(embed=embed)

@bot.command()
async def gtf(ctx, li:int):
    chan = bot.get_channel(794814927738503188)
    mesg = await chan.history(limit=li).flatten()
    a = ""
    for m in mesg:
        a += f"-----\n{m.author.name}\n{m.content}\n\n"
    with open("etc.txt", 'w') as f:
        f.write(a)

    with open('etc.txt', 'rb') as file:
        await ctx.send("here it is--", file=discord.File(file, 'etc.txt'))
        file.close()
    
    


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        pass
    elif isinstance(error, MissingPermissions):
        await ctx.send(f"**ERROR 403 FORBIDDEN**\n> {error}")
    elif isinstance(error, MissingRequiredArgument):
        await ctx.send(f"**ERROR 400 BAD REQUEST**\n> {error}")
    elif isinstance(error, MemberNotFound):
        await ctx.send(f"**ERROR 404**\n> {error}")
    elif isinstance(error, BadArgument):
        await ctx.send(f"**ERROR 400 BAD REQUEST**\n> {error}")
    elif isinstance(error, commands.CommandOnCooldown):
        pass
    else:
        raise error


@bot.event
async def on_member_remove(member):
    try:
        leveling.delete_one({"_id": member.id})
    except:
        pass



bot.run('ODc0MjcyOTUxMDQ0ODI1MTU4.YREkIg.GFJRkzHCxBvHgUJvJjZysvZikKk')
