from discord.ext import commands
from tools import sort, etc
from datetime import datetime
import discord
import asyncio
import random
import json

results = ["あなたがぐーで\n私もぐーなので\nあいこです！","あなたがぐーで\n私がちょきなので\nあなたの勝ちです！","あなたがぐーで\n私がぱーなので\n私の勝ちです！","あなたがちょきで\n私がぐーなので\n私の勝ちです！","あなたがちょきで\n私もちょきなので\nあいこです！","あなたがちょきで\n私がぱーなので\nあなたの勝ちです！","あなたがぱーで\n私がぐーなので\nあなたの勝ちです！","あなたがぱーで\n私がちょきなので\n私の勝ちです！","あなたがぱーで\n私もぱーなので\nあいこです！"]
developer_id = [536506865883021323, 537031688610512896]

class FD(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    self.etc = etc.tool(bot)
    bot.remove_command("help")
  
  
  @commands.command()
  async def say(self, ctx, *, msg):
    await ctx.message.delete()
    await ctx.send(msg)
    self.etc.command_log(ctx.message)
    
  @commands.command(aliases=["es"])
  async def embed_say(self, ctx, *, msg):
    self.etc.command_log(ctx.message)
    await ctx.message.delete()
    e = discord.Embed(title=msg)
    await ctx.send(embed=e)
   
  @commands.command(name="おみくじ")
  async def omikuji(self, ctx):
    omikuji, omi_results, member = random.randint(0,20), ["大吉です！","中吉です！","中吉です！","小吉です!","小吉です!","末吉です","末吉です","末吉です","凶です","凶です","凶です","小凶です","小凶です","小凶です","半凶です…","半凶です…","半凶です…","半凶です…","大凶です…","大凶です…","大凶です…"], ctx.guild.get_member(ctx.author.id)
    embed = discord.Embed(title=f'{member.name}さんのおみくじ結果は…' + omi_results[omikuji],color=member.color)    
    await ctx.send(embed=embed)
    self.etc.command_log(ctx.message)
    
  @commands.command(aliases=["じゃんけん"])
  async def janken(self, ctx):
    await ctx.send("最初はぐー、じゃんけん...？\n(ぐー or ちょき or ぱー)")
    def check(m): return m.author == ctx.author and m.channel == ctx.message.channel
    try:
      hand = await self.bot.wait_for('message', timeout=10.0, check=check)
      if hand.content == "ぐー": reply = results[random.randint(0,2)]
      elif hand.content == "ちょき": reply = results[random.randint(3,5)]
      elif hand.content == "ぱー": reply = results[random.randint(6,8)]
      else: reply = ":thinking:"
      await ctx.send(reply)
    except asyncio.TimeoutError: await ctx.send("遅いですよ…")
    self.etc.command_log(ctx.message)
  
  @commands.command()
  async def dice(self,ctx):  
    dice, dice2 = random.randint(1,6), random.randint(1,6)
    await ctx.send(f">>> 1回目 : {dice}\n2回目 : {dice2}\n合計 : {dice + dice2}です")
    if dice == dice2: await ctx.send("ゾロ目です！")
    self.etc.command_log(ctx.message)

  @commands.command()
  async def alarm(self, ctx, hour, minute):
    await ctx.message.delete()
    with open("time.json", "r", encoding="utf-8") as c_time: times = json.load(c_time)
    times.setdefault(f"{hour}:{minute}", f"{ctx.author.id}")
    with open("time.json", "w", encoding="utf-8") as w_time: json.dump(times, w_time)
    await ctx.send(f"{hour}:{minute}にDMを送信します", delete_after=5.0)
    self.etc.command_log(ctx.message)
  
  @commands.command()
  async def report(self, ctx, *, value):
    await ctx.message.delete()
    channel, embed = self.bot.get_channel(704660687443460126), discord.Embed(title=f"`{value}`",color=0xabc9ec)
    embed.set_author(name=ctx.guild.name,icon_url=ctx.guild.icon_url)
    await channel.send(embed=embed)
    await ctx.send("送信しました", delete_after=5.0)
    self.etc.command_log(ctx.message)
    
  @commands.command()
  async def vote(self, ctx, title, *args):
    await ctx.message.delete()
    args_, embed, emoji = '\n'.join(list(args)), discord.Embed(title="📊投票📊",description=title,color=ctx.author.color), ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
    embed.add_field(name="以下から選択してください",value=args_)
    embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
    message = await ctx.send(embed=embed)
    for t in range(len(args)): await message.add_reaction(emoji[t])
    self.etc.command_log(ctx.message)
    
  @commands.command(aliases=["da"])
  async def dict_add(self, ctx, key, *, value):
    await ctx.message.delete()
    with open("dict.json", "r", encoding="utf-8") as cladict: dic = json.load(cladict)
    if key in dic: await ctx.send(f"そのkeyは既に登録されています\n(value= {dic[key]})", delete_after=5.0)
    else:
      dic.setdefault(key, value)
      with open("dict.json", "w", encoding="utf-8") as cladict: json.dump(dic, cladict)
      await ctx.send(f"辞書に登録しました\n(key= {key}, value= {value})")
    self.etc.command_log(ctx.message)
  
  @commands.command(aliases=["ds"])
  async def dict_say(self, ctx, key):
    await ctx.message.delete()
    with open("dict.json", "r", encoding="utf-8") as clasay: clasays = json.load(clasay)
    if key in clasays: await ctx.send(clasays[key])
    else:        
      message = await ctx.send("それに対応するvalueは見つかりませんでした", delete_after=5.0)
    self.etc.command_log(ctx.message)
  
  @commands.command(aliases=["dd"])
  async def dict_delete(self, ctx, key):
    await ctx.message.delete()
    with open("dict.json", "r", encoding="utf-8") as cladel: dic = json.load(cladel)
    if key in dic:
      value = dic[key]
      del dic[key]
      with open("dict.json", "w", encoding="utf-8") as cladict: json.dump(dic, cladict)
      await ctx.send(f"辞書から削除しました\n(key= {key}, value= {value})")
    else:
      message = await ctx.send("そのkeyは辞書に登録されていません", delete_after=5.0)
    self.etc.command_log(ctx.message)
  
  @commands.command(aliases=["de"])
  async def dict_edit(self, ctx, key, value):
    await ctx.message.delete()
    with open("dict.json", "r", encoding="utf-8") as claedi: dic = json.load(claedi)
    if key in dic:
      dic[key] = value
      with open("dict.json", "w", encoding="utf-8") as claedi: json.dump(dic, claedi)
      await ctx.send(f"登録されたvalueを編集しました\n(key= {key}, value= {value})")
    else:
      message = await ctx.send("そのkeyは辞書に登録されていません", delete_after=5.0)
    self.etc.command_log(ctx.message)
    
  @commands.command(aliases=["h"])
  async def help(self, ctx):
    await ctx.message.delete()
    self.etc.command_log(ctx.message)
    embed_o, embed_a, embed_n = discord.Embed(title="Other",color=0xabc9ec), discord.Embed(title="Manager Command",description="以下が管理者専用のコマンドです",color=0xabc9ec), discord.Embed(title="Normal Command",description="以下が一般のコマンドです",color=0xabc9ec)
    embed_n.add_field(name="| ユーザー情報 |",value="`user_info`, `avatar`, `level`")
    embed_n.add_field(name="| サーバー情報 |",value="`guild_info`, `guild_managed`, `role_info`, `channel_info`, `bans`, `ban_info`, `search_user`, `search_role`, `search_channel`")
    embed_n.add_field(name="| BOT情報 |",value="`bot_status`, `latency`")
    embed_n.add_field(name="| 外部情報 |",value="`search`, `translate`, `weather`, `translate_help`, `weather_help`")
    embed_n.add_field(name="| 辞書機能 |",value="`dict_add`, `dict_delete`, `dict_edit`, `dict_say`")
    embed_n.add_field(name="| その他 |",value="`say`, `embed_say`, `おみくじ`, `じゃんけん`, `dice`, `alarm`, `report`, `vote`")
    embed_n.set_footer(text="詳細はc!help_info(c!.hi) [コマンド]\n➡️で次のページへ")
    embed_n.set_author(name=f"{self.bot.user.name} Help",icon_url=self.bot.user.avatar_url)
    embed_a.add_field(name="| ⚠ 権限 : `サーバー管理`以上 ⚠ |",value="`global`, `globalexcept`, `role`, `count`, `kick`, `ban`, `unban`")
    embed_a.add_field(name="| 🚫 権限 : `管理者`以上 🚫 |",value="`set_join_message`, `set_levelup_message`, `set_levelup_add_role`")
    embed_a.set_footer(text="詳細はc!help_info(c!.hi) [コマンド]\n⬅️で前のページへ、➡️で次のページへ")
    embed_a.set_author(name=f"{self.bot.user.name} Help",icon_url=self.bot.user.avatar_url)
    embed_o.add_field(name="`cblog`チャンネル",value="ClariceBOTが関係するログを表示します")
    embed_o.add_field(name="`claricebot`チャンネル",value="dsayを短縮して辞書のvalueを表示出来ます")
    embed_o.add_field(name="カウントチャンネル",value="随時、カウンターの値が反映されます")
    embed_o.add_field(name="BOT起動時間",value="日によって変わります\n平日 `7時〜24時`\n休日 `10時〜26時`")
    embed_o.add_field(name="BOT導入(招待)",value="[ここをタップ(クリック)して導入！](https://discordapp.com/api/oauth2/authorize?client_id=642320951987535893&permissions=336194679&scope=bot)")
    embed_o.add_field(name="総合サーバー",value="[ここをタップ(クリック)して参加！](https://discord.gg/jrUPRbc)")
    embed_o.set_footer(text="⬅️で前のページへ")
    embed_o.set_author(name=f"{self.bot.user.name} Help",icon_url=self.bot.user.avatar_url)
    emojis_2, emojis, message, embeds, l = ["➡️","No","⬅️"], ["⬅️","➡️"], await ctx.send(embed=embed_n), [embed_n,embed_a,embed_o], 0
    def check(reaction, user): return user == ctx.author and str(reaction.emoji) in ["⬅️","➡️"]
    while not self.bot.is_closed():
      if l == 1: 
        for r in emojis: await message.add_reaction(r)
      else: await message.add_reaction(emojis_2[l])
      try:
        reaction = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
        await message.clear_reactions()
        if str(reaction[0]) == "⬅️": l -= 1
        elif str(reaction[0]) == "➡️": l += 1
        await message.edit(embed=embeds[l])
      except asyncio.TimeoutError: 
        await message.delete()
        return
 
  @commands.command(aliases=["hi"])
  async def help_info(self, ctx, command):
    with open("commands.json", "r", encoding="utf-8") as command_: commands_ = json.load(command_)
    if command in commands_:
      embed = discord.Embed(title="Command Info",description=f"以下がコマンドの詳細です",color=0xabc9ec)
      embed.add_field(name="コマンド名 (短縮系)",value=f"{command} ({commands_[f'{command}']['alias']})")
      embed.add_field(name="オプション",value=f"```{commands_[f'{command}']['command']}```")
      embed.add_field(name="説明",value=commands_[f"{command}"]["description"])
      embed.set_author(name=f"{self.bot.user.name} Help",icon_url=self.bot.user.avatar_url)
      embed.set_footer(text="[オプション]を含むコマンドはオプションを省略することで更に詳しいコマンドを確認できます")
      await ctx.send(embed=embed)
    else: message = await ctx.send("そのコマンドは存在しません", delete_after=5.0)
    self.etc.command_log(ctx.message)
  
  @commands.command(name="global")
  async def global_add(self, ctx):
    await ctx.message.delete()
    if ctx.author.guild_permissions.manage_guild:
      with open("globalguild.json", "r", encoding="utf-8") as glo_guild: glo_guilds = json.load(glo_guild)
      if str(ctx.guild.id) not in glo_guilds:
        glo_guilds.setdefault(str(ctx.guild.id), ctx.channel.name)
        with open("globalguild.json", "w", encoding="utf-8") as glo_guild: json.dump(glo_guilds,glo_guild)
        embed = discord.Embed(title="ClariceBOT",description="Global Chat",color=0xabc9ec)
        embed.add_field(name="globalchat規約",value="**このサービスは以下の内容に従う事が可能なユーザーに提供されます**\n・誹謗中傷や暴言は禁止\n・論争等は禁止\n・スパム禁止\n・メンション禁止\n・ClariceBOTの操作は禁止\n万が一違反した場合、globalchatを利用出来なくなる場合があります")
        await ctx.send(embed=embed)
        embed.clear_fields()
      else: message = await ctx.send("既に登録されています", delete_after=5.0)
    else: message = await ctx.send("サーバー管理権限が必要です", delete_after=5.0)
    self.etc.command_log(ctx.message)
     
  @commands.command()
  @commands.has_permissions(kick_members=True)
  async def kick(self, ctx, member: discord.Member, reason=None):
    await ctx.message.delete()
    self.etc.command_log(ctx.message)
    if ctx.author.id != member.id:
      try: await ctx.guild.kick(member, reason=reason) 
      except Exception: await ctx.send("失敗しました\n指定したメンバーや権限を確認して下さい",delete_after=5.0)
      else:
        channel, embed = sort.channel(ctx.guild, "cblog"), discord.Embed(title=f"{member.name} (`{member.id}`)",description=f"理由: {reason}",color=member.color)
        embed.set_footer(text=f"時刻 {datetime.now().strftime('%Y年%m月%d日 %H時%M分')}")
        embed.set_author(name="❖ メンバーがKickされました ❖",icon_url=member.avatar_url)  
        if not channel == None: await channel.send(embed=embed)
    else: await ctx.send("貴方自身をKickしないで下さい", delete_after=5.0)
            
  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def ban(self, ctx, member: discord.Member, reason=None):
    await ctx.message.delete()
    self.etc.command_log(ctx.message)
    if ctx.author.id != member.id:
      try: await ctx.guild.ban(member, delete_message_days=0, reason=reason)
      except Exception: await ctx.send("失敗しました\n指定したメンバーや権限を確認して下さい", delete_after=5.0)
      else:
        channel, embed = sort.channel(ctx.guild, "cblog"), discord.Embed(title=f"{member.name} (`{member.id}`)",description=f"理由: {reason}",color=member.color)
        embed.set_footer(text=f"時刻 {datetime.now().strftime('%Y年%m月%日 %H時%M分')}")
        embed.set_author(name="❖ メンバーがBanされました ❖",icon_url=member.avatar_url)
        await channel.send(embed=embed)
    else: await ctx.send("貴方自身をBANしないで下さい", delete_after=5.0)
  
  @commands.command()
  @commands.has_permissions(manage_guild=True)
  async def unban(self, ctx, user_id: int, reason=None):
    await ctx.message.delete()
    self.etc.command_log(ctx.message)
    user = await self.bot.fetch_user(user_id)
    try: await ctx.guild.unban(user, reason=reason)
    except Exception: await ctx.send("失敗しました\n指定したメンバーや権限を確認して下さい", delete_after=5.0)
    else:
      channel, embed = sort.channel(ctx.guild, "cblog"), discord.Embed(title=f"{user.name} (`{user.id}`)",description=f"理由: {reason}",color=0xabc9ec)
      embed.set_footer(text=f"時刻 {datetime.now().strftime('%Y年%m月%日 %H時%M分')}")  
      embed.set_author(name="❖ メンバーのBanが解除されました ❖",icon_url=user.avatar_url)
      await channel.send(embed=embed)
  
  @commands.command(aliases=["slm"])
  @commands.has_permissions(administrator=True)
  async def set_levelup_message(self, ctx, *, message):
    await ctx.message.delete()
    c, e = discord.Embed(title="レベルアップ時のメッセージを設定しました",description="`(送信するチャンネルを確定しました)`",color=ctx.guild.me.color), discord.Embed(title="レベルアップ時のメッセージを編集しました",color=ctx.guild.me.color)
    if ctx.author.guild_permissions.administrator:
      with open("rank.json", "r", encoding="utf-8") as level: levels = json.load(level)
      if f"{ctx.guild.id}" not in levels["guild"]:
        value = {"channel_id":ctx.channel.id, "message":message, "roles":{}}
        levels["guild"].setdefault(f"{ctx.guild.id}", value)
        await ctx.send(embed=c, delete_after=5.0)
      else:
        levels["guild"][f"{ctx.guild.id}"]["message"] = message
        await ctx.send(embed=e, delete_after=5.0)
      with open("rank.json", "w", encoding="utf-8") as level: json.dump(levels, level, indent=4)
    self.etc.command_log(ctx.message)
    
  @commands.command(aliases=["dlm"])
  @commands.has_permissions(administrator=True)
  async def delete_levelup_message(self, ctx):
    s, f = discord.Embed("レベルアップ時のメッセージを削除しました",description="`(送信するチャンネルをリセットしました)`",color=ctx.guild.me.color), discord.Embed(title="このサーバーには設定されていません",color=ctx.guild.me.color)
    self.etc.command_log(ctx.message)
    await ctx.message.delete()
    with open("rank.json", "r", encoding="utf-8") as level: levels = json.load(level)
    if f"{ctx.guild.id}" in levels["guild"]:
      del levels["guild"][f"{ctx.guild.id}"]
      await ctx.send(embed=s, delete_after=5.0)
    else: await ctx.send(embed=f, delete_after=5.0)
    with open("rank.json", "r", encoding="utf-8") as level: json.dump(levels, level, indent=4)
    
  @commands.command(aliases=["sjm"])
  @commands.has_permissions(administrator=True)
  async def set_join_message(self, ctx, *, jm):
    self.etc.command_log(ctx.message)
    await ctx.message.delete()
    e, c = discord.Embed(title="参加メッセージを編集しました",color=ctx.guild.me.color), discord.Embed(title="参加メッセージを設定しました",color=ctx.guild.me.color)
    with open("jm.json", "r", encoding="utf-8") as jm_g: jms = json.load(jm_g)
    if f"{ctx.guild.id}" in jms:
      jms[f"{ctx.guild.id}"] = jm
      await ctx.send(embed=e, delete_after=5.0)
    else:
      jms.setdefault(f"{ctx.guild.id}", jm)
      await ctx.send(embed=c, delete_after=5.0)
    with open("jm.json", "w", encoding="utf-8") as jm_g: json.dump(jms, jm_g)
    
  @commands.command(aliases=["djm"])
  @commands.has_permissions(administrator=True)
  async def delete_join_message(self, ctx):
    self.etc.command_log(ctx.message)
    await ctx.message.delete()
    s, f = discord.Embed(title="参加メッセージを削除しました",color=ctx.guild.me.color), discord.Embed(title="このサーバーは設定されていません", color=ctx.guild.me.color)
    with open("jm.json", "r", encoding="utf-8") as jm: jms = json.load(jm)
    if f"{ctx.guild.id}" in jms:
      del jms[f"{ctx.guild.id}"]
      await ctx.send(embed=s, delete_after=5.0)
    else: await ctx.send(embed=f, delete_after=5.0)
    with open("jm.json", "w", encoding="utf-8") as jm: json.dump(jms, jm, indent=4)


def setup(bot):
  bot.add_cog(FD(bot)) 