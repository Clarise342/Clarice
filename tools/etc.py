from discord.ext import commands
from datetime import datetime
import discord
import json


class tool():
  
  
  def __init__(self, bot):
    self.bot = bot
  
  
  async def cb_count(self, guild):
    bot_count = 0
    with open('count.json', 'r', encoding='utf-8') as count: counts = json.load(count)
    if f"{guild.id}" in counts:
      guild_, gu_members = counts[f"{guild.id}"], len(guild.members)
      for member in guild.members:
        if member.bot: bot_count += 1
      guild_["ボイスチャンネル数"], guild_["テキストチャンネル数"], guild_["チャンネル数"], guild_["カテゴリ数"], guild_["役職数"], guild_["BOT数"], guild_["ユーザー数"], guild_["総ユーザー数"] = str(len(guild.voice_channels)), str(len(guild.text_channels)), str(len(guild.channels)), str(len(guild.categories)), str(len(guild.roles)), str(bot_count) ,str(gu_members - bot_count), str(gu_members)
      with open('count.json', 'w', encoding='utf-8') as count: json.dump(counts, count) 
      if guild_["カウンター"] == "True":
        with open("co_ch_id.json", "r", encoding="utf-8") as co_ch_id: co_ch_ids = json.load(co_ch_id)
        values, _guild = [f'総ユーザー数 : {guild_["総ユーザー数"]}',f'ユーザー数 : {guild_["ユーザー数"]}',f'BOT数 : {guild_["BOT数"]}',f'役職数 : {guild_["役職数"]}',f'カテゴリ数 : {guild_["カテゴリ数"]}',f'チャンネル数 : {guild_["チャンネル数"]}',f'テキストチャンネル数 : {guild_["テキストチャンネル数"]}',f'ボイスチャンネル数 : {guild_["ボイスチャンネル数"]}'], co_ch_ids[f"{guild.id}"]
        for l in range(len(_guild)):
          voicechannel = guild.get_channel(_guild[l])
          await voicechannel.edit(name=values[l], reason=None)
      else:
        return


  async def error(self, bot, error, description, date, msg):
    if type(msg.channel) == discord.DMChannel: guild = "不明"
    else: guild = msg.guild.name
    embed = discord.Embed(title="エラー",description=f"発生サーバー : {guild}",color=0xd2fd03)
    embed.add_field(name=error,value=description)
    embed.set_footer(text=date)
    embed.set_author(name="ClariA")
    channel = bot.get_channel(696000855534469181)
    await channel.send(embed=embed)
    embed.clear_fields()


  def command_log(self, message):
    with open("ClariceBOT_Commands_Log.json", "r", encoding="utf-8") as log: logs = json.load(log)
    log_time = datetime.now().strftime("%Y.%m.%d.%H:%M")
    logs.setdefault(f"[{log_time}/{message.author.name}]",f"[{message.content}]")
    with open("ClariceBOT_Commands_Log.json", "w", encoding="utf-8") as log: json.dump(logs, log)