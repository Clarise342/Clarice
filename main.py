#python 3.8.1
#pip 20.0.2
#discord.py 1.3.2
#coding: utf-8

from discord.ext import commands, tasks
from datetime import datetime
import sys
import discord
import asyncio
import json
import os

developer_id = [536506865883021323, 537031688610512896]
token = os.environ['TOKEN']
extension = [
  'cogs.bot_event',
  'cogs.fun_dict',
  'cogs.many_command'
]

class Claria(commands.Bot):
  
  def __init__(self, command_prefix):
    super().__init__(command_prefix)
    
    for cog in extension:
      try: self.load_extension(cog)
      except Exception: print("エラーが発生しました")
      else: print(f"コグ: {cog}を読み込みました")
      
if __name__ == '__main__':
  bot = Claria(command_prefix="c!")

  @bot.command(name="reload",aliases=["r"])
  async def system_reload(ctx):
    await ctx.message.delete()
    s, f, e = discord.Embed(title="再読み込み中です",color=ctx.guild.me.color), discord.Embed(title="読み込みが完了しました",color=ctx.guild.me.color), discord.Embed(title="このコマンドは開発者以外使用できません",color=ctx.guild.me.color)
    if ctx.author.id in developer_id:
      msg = await ctx.send(embed=s)
      await asyncio.sleep(1)
      for cog in extension:
        try: bot.unload_extension(cog)
        except Exception: pass
        finally: 
          try: bot.load_extension(cog)
          except Exception as e: print(e)   
      await msg.edit(embed=f,delete_after=3.0)
    else: await ctx.send(embed=e)

  @tasks.loop(seconds=60)
  async def loop():
    with open("time.json", "r", encoding="utf-8") as c_time: now, times = datetime.now().strftime("%H:%M"), json.load(c_time)
    if now in times:
      user = bot.get_user(int(times[now]))
      await user.send(f"【アラーム】\n{now} になりました！🔔")
      del times[now]
      with open("time.json", "w", encoding="utf-8") as w_time: json.dump(times, w_time)
    else: pass 
      
  @tasks.loop(seconds=60)
  async def loop_():  
    hour_12, hour_24, now = int(datetime.now().strftime('%I')), int(datetime.now().strftime('%H')), datetime.now().strftime('%H:%M')
    if now in ['00:00','03:00','06:00','09:00','12:00','15:00','18:00','21:00']:
      if hour_24 < 13 and hour_24 > 0: lmsg = f"| 午前 {hour_12} 時 | latency check |"  
      else: lmsg = f"| 午後 {hour_12} 時 | latency check |" 
      embed = discord.Embed(title=lmsg,description=f"{round(bot.latency * 1000)}ms",color=0xabc9ec)
      embed.set_author(name=bot.user.name,icon_url=bot.user.avatar_url)
      channel = bot.get_channel(670200667717238824)
      await channel.send(embed=embed)
      
  with open("token.json", "r", encoding="utf-8") as token: TOKEN = json.load(token)
  loop.start()
  loop_.start()
  bot.run(token)
