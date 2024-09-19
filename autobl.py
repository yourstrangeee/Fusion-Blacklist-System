import discord
from core.bot import Fusion
from discord.ext import commands
from utils.Tools import add_user_to_blacklist
import json
class AutoBlacklist(commands.Cog):
    def __init__(self, client: Fusion):
      self.blacklisted_guilds = []
      self.load_blacklist()
      self.client = client
      self.spam_cd_mapping = commands.CooldownMapping.from_cooldown(5, 10, commands.BucketType.member)
      self.spam_command_mapping = commands.CooldownMapping.from_cooldown(5, 10, commands.BucketType.member)
    def load_blacklist(self):
        try:
            with open('blguild.json', 'r') as file:
                self.blacklisted_guilds = json.load(file)
                if not isinstance(self.blacklisted_guilds, list):
                    self.blacklisted_guilds = []
        except FileNotFoundError:
            self.blacklisted_guilds = []

    def save_blacklist(self):
        with open('blguild.json', 'w') as file:
            json.dump(self.blacklisted_guilds, file, indent=4)
    @commands.Cog.listener()
    async def on_message(self, message):
      bucket = self.spam_cd_mapping.get_bucket(message)
      fusion = '<@1147798554023305237>'
      retry = bucket.update_rate_limit()
      if retry and message.guild.id == "remove quotes and add guild_id which you don't want to be blacklisted":
         add_user_to_blacklist(message.author.id)
         return None
      if retry:
        if message.content == fusion or message.content == "<@!1147798554023305237>":
          add_user_to_blacklist(message.author.id)
          embed = discord.Embed(description="Successfully **Blacklisted** {} and their Guild for **spamming messages**".format(message.author.mention),color=discord.Color.green())
          await message.channel.send(embed=embed)
          await message.guild.leave()
          self.blacklisted_guilds.append(message.guild.id)
          self.save_blacklist()
    @commands.Cog.listener()
    async def on_command(self, ctx):
      bucket = self.spam_command_mapping.get_bucket(ctx.message)
      retry = bucket.update_rate_limit()
      if retry and ctx.guild.id == "remove quotes and add guild_id which you don't want to be blacklisted":
         add_user_to_blacklist(ctx.author.id)
         return None
      if retry:
        add_user_to_blacklist(ctx.author.id)
        embed = discord.Embed(description="Successfully Blacklisted {} and their Guild For **Spamming messages**".format(ctx.author.mention),color=discord.Color.green())
        await ctx.reply(embed=embed)
        await ctx.guild.leave()
        self.blacklisted_guilds.append(ctx.guild.id)
        self.save_blacklist()
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if guild.id in self.blacklisted_guilds:
            await guild.leave()
