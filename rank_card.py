import discord
from discord.ext import commands
from pymongo import MongoClient, message
import datetime
from easy_pil import Editor
from PIL import Image, ImageDraw, ImageFont
import asyncio

cluster = MongoClient("mongodb+srv://sumitm6879sm:sm6879sm@sambot.ipbu6.mongodb.net/SamBot?retryWrites=true&w=majority")
leveling = cluster['MysticBot']['levels']
bg_user = cluster['MysticBot']['bg_user']


class rank_card(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("rank cards Ready!")

    @commands.command(aliases=['lvl', 'level'])
    async def rank(self, ctx, member: discord.Member = None):
        if member is None and ctx.message.reference:
            msg = await ctx.channel.fetch_message(id=ctx.message.reference.message_id)
            member = msg.author
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
                emoji_1 = '❤️'
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
            offset_x -= text_size[0] + 5
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
            new_background.bar((37, 240), max_width=840, height=30, percentage=percent, radius=12, fill=RGB)
            file = discord.File(fp=new_background.image_bytes, filename='member_lvl.png')
            await ctx.send(file=file)

    @commands.command(aliases=['bg'])
    async def background(self, ctx, bg: str = None):
        user = bg_user.find_one({"_id": ctx.author.id})
        if bg is None:
            embed = discord.Embed(title='Backgrounds', description="There are only 2 backgrounds:",
                                  color=0xf47fff)
            if user is None:
                embed.description += "\n1 ~-~> **Default** \✔\n2 ~-~> **Black**"
            else:
                embed.description += "\n1 ~-~> **Default**\n2 ~-~> **Black** \✔"
            embed.set_footer(text=f'{self.bot.command_prefix}bg [name]', icon_url=self.bot.user.avatar_url)
            return await ctx.send(embed=embed)
        if bg.lower() in ['black', 'dark', 'blk']:
            if user is None:
                new_user = {"_id": ctx.author.id}
                bg_user.insert_one(new_user)
                await ctx.send(f"{ctx.author.mention} changed you background to black")
            else:
                await ctx.send(f"You already have a black background")
        elif bg.lower() in ['default', 'original', 'dfut']:
            if user is None:
                await ctx.send(f"{ctx.author.mention} You already have and Default background")
            else:
                bg_user.delete_one({"_id": ctx.author.id})
                await ctx.send(f"{ctx.author.mention} set your background to default")
        else:
            await ctx.send(f"{ctx.author.mention} No background found with the name {bg}")


def setup(bot):
    bot.add_cog(rank_card(bot))

