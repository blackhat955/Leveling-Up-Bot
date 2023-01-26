import discord 
from discord.ext import commands
import asyncio
import datetime
from discord_components import Button, ButtonStyle, Select, SelectOption, Interaction, component

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_button_click")
    async def on_button_click(self, interaction):
        if interaction.component.custom_id == str(interaction.author.id):
            member = interaction.author
            mesg = interaction.message
            em = discord.Embed(description="Process Ended!\n**`;help` to get help menu again!**", color = 0xff0000)
            em.set_author(name=member.name, icon_url=member.avatar_url)
            await mesg.edit(embed=em, components=[])
            await interaction.defer(ignore=True)

    @commands.command(aliases=['h'])
    async def help(self, ctx):
        embed1 = get_embed1(self, ctx)
        embed2 = get_embed2(self, ctx)
        
        em = discord.Embed(description="Choose from the below to get help on the listed topic", color = 0xff0000)
        em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

        compo = [ 
        Select(
        placeholder="Choose from the options",
        options=[
            SelectOption(
                label="Leveling Commands",
                emoji = "🏅",value = "LC",
                description="Commands used by members for level info."),
            SelectOption(
                label="Economy Commands",
                emoji="💰",value="EC",
                description="Commands used to progress in Economy!")]),
        Button(
            label="Quit",
            style=ButtonStyle.red,
            custom_id=str(ctx.author.id))]

        msg = await ctx.send(embed=em, components=compo)
        while True:
            try:
                event = await self.bot.wait_for("select_option", timeout=60)
                if event.author.id == ctx.author.id and event.message.id == msg.id:
                    if event.values[0] == "LC":
                        await msg.edit(embed=embed1)
                        await event.defer(ignore=True)
                    elif event.values[0] == "EC":
                        await msg.edit(embed=embed2)
                        await event.defer(ignore=True)
            except asyncio.TimeoutError:
                em.description = f"Timeout\n**`;help` to get menu again!**" 
                await msg.edit(embed=em,components=[Button(label='Timeout', style = ButtonStyle.grey, emoji='⏱', disabled=True)])
                break

def get_embed1(self, ctx):
    embed = discord.Embed(
        title='Mystic Leveling System',
        description='Everyone Gets **1xp** per message\nServer boosters Get **2xp** per message',
        color=0xff0000,
        timestamp=datetime.datetime.utcnow())
    embed.add_field(name='Commands', value='🔻🔻🔻🔻', inline=False)
    embed.add_field(name=f"level", value="Shows your level\n**Aliases**\n> `lvl`, `rank`", inline=False)
    embed.add_field(name=f"leaderboard", value="Shows server Leaderboard\n**Aliases**\n> "
                                                                    "`lb`, `top`", inline=False)
    embed.add_field(name=f'background', value='Shows available background\n**Aliases**\n> '
                                                                    '`bg`, `background`', inline=False) 
    embed.set_thumbnail(url=self.bot.user.avatar_url)
    embed.set_author(name=f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
    return embed

def get_embed2(self, ctx):
    embed = discord.Embed(
        title = "Economy",
        description = "This is a server **Economy** to keep people entertained and progress in server by fun!\n**The prefix is `;`**\n**`;start`** to get started",
        color = 0xff0000)
    embed.add_field(name="🎁 Rewards", value="`Daily`, `Hourly`", inline=False)
    embed.add_field(name="🪙 Economy", value='`Beg`, `Roam`', inline=False)
    embed.add_field(name="🎲 Gambling", value="`Coinflip [h/t] [$]`, `slots [$]`")
    embed.set_thumbnail(url=self.bot.user.avatar_url)
    embed.set_author(name=f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
    return embed


def setup(bot):
    bot.add_cog(Help(bot))