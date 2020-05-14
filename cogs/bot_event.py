from discord.ext import commands
from tools import sort, etc
from datetime import datetime
from googlesearch import search
from googletrans import Translator
import discord, sys, asyncio, random, json, urllib

developer_id = [536506865883021323, 537031688610512896]

class Be(commands.Cog):
  
  
  def __init__(self, bot):
    self.bot = bot
    self.etc = etc.tool(bot)
    self.translator = Translator()
    bot.remove_command("help")
    
    
  @commands.command(aliases=["e"])
  async def exit(self, ctx):
    self.etc.command_log(ctx.message)
    await ctx.message.delete()
    if ctx.author.id in developer_id:
      print("ClariAは停止しました")
      await self.bot.logout()
      await sys.exit()
    else: await ctx.send("このコマンドは開発者以外使用できません",delete_after=5.0)
    
  @commands.command(name="eval")
  @commands.has_permissions(administrator=True)
  async def evaluate(self, ctx, *, code):
    try: eval(code)
    except Exception: return
      
  @commands.command(aliases=["ui"])
  async def user_info(self, ctx, member: discord.Member=None):
    self.etc.command_log(ctx.message)
    if member == None: member = ctx.author
    bot_tf, roles = {True:"botです",False:"botではありません"}, list(reversed(list(map(lambda x: x.mention, member.roles))))
    if member.activity == None: role, activity = '\n'.join(roles[0:5]), "なし" 
    else: role, activity = '\n'.join(roles[0:5]), str(member.activity)
    embed = discord.Embed(title=f"`(このユーザーは{bot_tf[member.bot]})`\n◇ ユーザーID ◇",description=f"`{member.id}`",color=member.color)
    embed.timestamp = datetime.utcnow()
    embed.add_field(name="◇ アカウント作成日時 ◇",value=f"`{member.created_at.strftime('%Y年%m月%d日(%a) %H時%M分')}`",inline=False)
    embed.add_field(name="◇ サーバー参加日時 ◇",value=f"`{member.joined_at.strftime('%Y年%m月%d日(%a) %H時%M日')}`",inline=False)
    embed.add_field(name=f"◇ 役職({len(member.roles)}) 上位5役職 ◇",value=role,inline=False)
    embed.add_field(name="◇ アクティビティ ◇",value=f"`{activity}`",inline=False)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_author(name=f"❖ {str(member)}の情報 ❖")
    embed.set_footer(text=f"送信者 {ctx.author.name}",icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
    
  @commands.command()
  async def avatar(self, ctx, member: discord.Member=None):
    self.etc.command_log(ctx.message)
    if member == None: member = ctx.author
    embed = discord.Embed(color=member.color)
    embed.timestamp = datetime.utcnow()
    embed.set_author(name=f"❖ {str(member)}さんのアイコン画像 ❖",url=member.avatar_url)
    embed.set_image(url=member.avatar_url)
    embed.set_footer(text=f"送信者 {ctx.author.name}",icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
     
  @commands.command()
  async def level(self, ctx, member: discord.Member=None):
    self.etc.command_log(ctx.message)
    if member == None: member = ctx.author
    with open("rank.json", "r", encoding="utf-8") as rank: ranks = json.load(rank)
    embed = discord.Embed(title=f"◇ レベル {ranks['user'][f'{member.id}']['level']}\n◇ Exp. {ranks['user'][f'{member.id}']['exp']}",color=member.color) if f"{member.id}" in ranks["user"] else discord.Embed(title="◇ レベル なし\n◇ Exp. なし",color=member.color)
    embed.timestamp = datetime.utcnow()
    embed.set_author(name=f"❖ {str(member)}さんのレベル情報 ❖")
    embed.set_footer(text=f"送信者 {ctx.author.name}",icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
    
  @commands.command(aliases=["gi"])
  async def guild_info(self, ctx):
    self.etc.command_log(ctx.message)
    roles, guild = list(reversed(list(map(lambda x: x.mention, ctx.guild.roles)))), ctx.guild
    role = '\n'.join(roles[0:5])
    bots = [member for member in guild.members if member.bot]
    embed = discord.Embed(title="◇ オーナー ◇",description=f"名前: `{str(guild.owner)}`\nID: `{guild.owner.id}`",color=guild.me.color)
    embed.timestamp = datetime.utcnow()
    embed.add_field(name="◇ ステータス ◇",value=f"**◆メンバー(** *{guild.member_count}*  **)◆**:\n❖ユーザー: `{guild.member_count - len(bots)}`  ❖BOT: `{len(bots)}`\n\n**◆役職(** *{len(guild.roles)}*  **)◆** 上位5役職\n{role}\n\n**◆チャンネル(** *{len(guild.channels)}*  **)◆**\n❖カテゴリ: `{len(guild.categories)}`\n❖テキストチャンネル: `{len(guild.text_channels)}`\n❖ボイスチャンネル: `{len(guild.voice_channels)}`",inline=False)
    embed.add_field(name="◇ 作成日 ◇",value=f'`{guild.created_at.strftime("%Y年%m月%d日(%a) %H時%M分")}`',inline=False)
    embed.add_field(name="◇ サーバー地域 ◇",value=f"`{guild.region}`",inline=False)
    embed.set_author(name=f"❖ {guild.name}の情報 ❖")
    embed.set_thumbnail(url=guild.icon_url)
    embed.set_footer(text=f"送信者 {ctx.author.name}",icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
    
  @commands.command(aliases=["gm"])
  @commands.has_permissions(manage_guild=True)
  async def guild_managed(self, ctx):
    self.etc.command_log(ctx.message)
    await ctx.message.delete()
    available, notification, filter, verification, mfa, embed = {True:"せん",False:"す"}, {"NotificationLevel.all_messages":"全てのメッセージ","NotificationLevel.only_mentions":"メンションのみ"}, {"disabled":"無効","no_role":"有効 - 役職の無いメンバーのみ","all_members":"有効 - 全てのメンバー"}, {"none":"無制限","low":"メール認証","medium":"メール認証(+ アカウント登録後5分経過)","high":"メール認証(+ サーバー参加後10分経過)","extreme":"電話認証"}, {0:"なし",1:"あり"}, discord.Embed(title="| ID |",description=f"`{ctx.guild.id}`",color=ctx.guild.me.color)
    embed.timestamp = datetime.utcnow()
    embed.add_field(name="◇ シャード ◇",value=f"`{ctx.guild.shard_id}`",inline=False)
    embed.add_field(name="◇ 認証 ◇",value=f"❖2段階認証: `{mfa[ctx.guild.mfa_level]}`\n❖認証レベル: `{ctx.guild.verification_level}`\n```{verification[str(ctx.guild.verification_level)]}```",inline=False)
    embed.add_field(name="◇ フィルター ◇",value=f"`{filter[str(ctx.guild.explicit_content_filter)]}`",inline=False)
    embed.add_field(name="◇ 通知 ◇",value=f"`{notification[str(ctx.guild.default_notifications)]}`",inline=False)
    embed.add_field(name="◇ AFK ◇",value=f"❖チャンネル: `{ctx.guild.afk_channel}`\n❖タイムアウト時間: `{round(ctx.guild.afk_timeout / 60)}分`",inline=False)
    embed.add_field(name="◇ システムチャンネル ◇",value=f"`{ctx.guild.system_channel}`",inline=False)
    embed.add_field(name="◇ ファイルサイズ最大 ◇",value=f"`{round(ctx.guild.filesize_limit / 1000000)}MB`")
    embed.set_author(name=f"❖ {ctx.guild.name}の情報 ❖\n(このサーバーは利用できま{available[ctx.guild.unavailable]})")
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"送信者 {ctx.author.name}",icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
    
  @commands.command(aliases=["ri"])
  @commands.has_permissions(manage_roles=True)
  async def role_info(self, ctx, role: discord.Role=None):
    self.etc.command_log(ctx.message)
    await ctx.message.delete()
    r = discord.Embed(title="役職は見つかりませんでした",color=ctx.guild.me.color)
    if role != None:
      tf, e = {True:"可能",False:"不可能"}, discord.Embed(title="◇ 役職名 ◇",description=f"{role.mention}",color=role.color)
      e.timestamp = datetime.utcnow()
      e.add_field(name="◇ ID ◇",value=f"`{role.id}`",inline=False)
      e.add_field(name="◇ 色 ◇",value=f"`{role.color}`",inline=False)
      e.add_field(name="◇ 権限値 ◇",value=f"`{role.permissions.value}`",inline=False)
      e.add_field(name="◇ オンライン表示 ◇",value=f"`{tf[role.hoist]}`",inline=False)
      e.add_field(name="◇ メンション ◇",value=f"`{tf[role.mentionable]}`",inline=False)
      e.add_field(name="◇ サーバー内位置 ◇",value=f"`{role.position}`")
      e.set_author(name=f"❖ {ctx.guild.name}の役職情報 ❖",icon_url=ctx.guild.icon_url)
      e.set_footer(text=f"送信者 {ctx.author.name}",icon_url=ctx.author.avatar_url)
      await ctx.send(embed=e)
    else: await ctx.send(embed=r, delete_after=5.0)
    
  @commands.command(aliases=["tci"])
  @commands.has_permissions(manage_channels=True)
  async def text_channel_info(self, ctx, channel: discord.TextChannel=None):
    self.etc.command_log(ctx.message)
    await ctx.message.delete()
    r = discord.Embed(title="チャンネルは見つかりませんでした",color=ctx.guild.me.color)
    if channel != None:
      n, e = {True:"有効",False:"無効"}, discord.Embed(title="◇ チャンネル名 ◇",description=f"{channel.mention}",color=ctx.guild.me.color)
      e.timestamp = datetime.utcnow()
      e.add_field(name="◇ ID ◇",value=f"`{channel.id}`",inline=False)
      e.add_field(name="◇ トピック ◇",value=f"`{channel.topic}`",inline=False)
      e.add_field(name="◇ 閲覧注意 ◇",value=f"`{n[channel.is_nsfw()]}`",inline=False)
      e.add_field(name="◇ スローモード ◇",value=f"`{channel.slowmode_delay}秒`",inline=False)
      e.add_field(name="◇ サーバー内位置 ◇",value=f"`{channel.position}`",inline=False)
      e.add_field(name="◇ 作成日 ◇",value=f"`{channel.created_at.strftime('%Y年%m月%d日(%a) %H時%M分')}`",inline=False)
      e.set_footer(text=f"送信者 {ctx.author.name}",icon_url=ctx.author.avatar_url)
      e.set_author(name=f"❖ {ctx.guild.name}のチャンネル情報 ❖",icon_url=ctx.guild.me.avatar_url)
      await ctx.send(embed=e)
    else: await ctx.send(embed=r, delete_after=5.0)
    
  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def bans(self, ctx):
    self.etc.command_log(ctx.message)
    await ctx.message.delete()
    b = await ctx.guild.bans()
    embed = discord.Embed(title=f"◇ これまでにBANされたメンバーは{len(b)}です",color=ctx.guild.me.color)
    embed.set_author(name=f"❖ {ctx.guild.name}のBANリスト ❖",icon_url=ctx.guild.icon_url)
    for member in await ctx.guild.bans(): 
      embed.add_field(name=f"◇ {member.user.name} (ID: {member.user.id})",value=f"◆ 理由: `{member.reason}`",inline=False)
      if len(embed.fields) == 20:
        await ctx.author.send(embed=embed)
        embed.clear_fields()
    if len(embed.fields) != 0:
      await ctx.author.send(embed=embed)
        
  @commands.command(aliases=["bi"])
  @commands.has_permissions(ban_members=True)
  async def ban_info(self, ctx, id: int=None):
    self.etc.command_log(ctx.message)
    await ctx.message.delete()
    e, nbe = discord.Embed(title="そのユーザーは見つかりませんでした",color=ctx.guild.me.color), discord.Embed(title="そのユーザーはBANされていません",color=ctx.guild.me.color)
    if id == None: await ctx.send(embed=e,delete_after=5.0)
    user = await self.bot.fetch_user(id)
    if user == None: await ctx.send(embed=e,delete_after=5.0)
    r = await ctx.guild.fetch_ban(user)
    if r != None:
      embed = discord.Embed(title="◇ アカウント作成日 ◇",description=f"`{user.created_at.strftime('%Y年%m月%d日(%a) %H時%M分')}`",color=ctx.guild.me.color)
      embed.timestamp = datetime.utcnow()
      embed.add_field(name="◇ BAN理由 ◇",value=f"`{r.reason}`",inline=False)
      embed.set_author(name=f"❖ {user.name}さんの情報 ❖")
      embed.set_thumbnail(url=user.avatar_url)
      embed.set_footer(text=f"送信者 {ctx.author.name}",icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)
    else: ctx.send(embed=nbe,delete_after=5.0)
    
  @commands.command(aliases=["su"])
  async def search_user(self, ctx, name=None):
    self.etc.command_log(ctx.message)
    member = ctx.guild.get_member(ctx.author.id)
    e = discord.Embed(title=f"{member.mention} 名前を指定してください",color=ctx.guild.me.color)
    if name != None:
      l = [l for l in ctx.guild.members if name in l.name]
      sl = '\n'.join(l)
      r = discord.Embed(title="◇ 検索結果は 0 です",color=ctx.guild.me.color) if len(l) == 0 else discord.Embed(title=f"◇ 検索結果は {len(l)} です",description=sl,color=ctx.guild.me.color)
      r.timestamp = datetime.utcnow()
      r.set_author(name=f"❖ {ctx.guild.name}内のユーザーを検索 ❖",icon_url=ctx.guild.icon_url)
      r.set_footer(text=f"送信者 {ctx.author.name}",icon_url=ctx.author.avatar_url)
      await ctx.send(embed=r)
    else: await ctx.send(embed=e,delete_after=5.0)
    
  @commands.command(aliases=["sr"])
  async def search_role(self, ctx, name=None):
    self.etc.command_log(ctx.message)
    member = ctx.guild.get_member(ctx.author.id)
    l, e = [], discord.Embed(title=f"{member.mention} 名前を指定してください",color=ctx.guild.me.color)
    if name != None:
      for role in ctx.guild.roles:
        if name in role.name: l.append(role.mention)
      sl = '\n'.join(l)
      if len(l) == 0: r = discord.Embed(title="◇ 検索結果は 0 です",color=ctx.guild.me.color)
      else: r = discord.Embed(title=f"◇ 検索結果は {len(l)} です",description=sl,color=ctx.guild.me.color)
      r.timestamp = datetime.utcnow()
      r.set_author(name=f"❖ {ctx.guild.name}内の役職を検索 ❖",icon_url=ctx.guild.icon_url)
      r.set_footer(text=f"送信者 {ctx.author.name}",icon_url=ctx.author.avatar_url)
      await ctx.send(embed=r)
    else: await ctx.send(embed=e,delete_after=5.0)
     
  @commands.command(aliases=["sc"])
  async def search_channel(self, ctx, name=None):
    self.etc.command_log(ctx.message)
    member = ctx.guild.get_member(ctx.author.id)
    l, e = [], discord.Embed(title=f"{ctx.author.mention} 名前を指定してください",color=ctx.guild.me.color)
    if name != None:
      for channel in ctx.guild.channels:
        if name in channel.name: l.append(channel.mention)
      sl = '\n'.join(l)
      if len(l) == 0: r = discord.Embed(title="◇ 検索結果は 0 です",color=ctx.guild.me.color)
      else: r = discord.Embed(title=f"◇ 検索結果は {len(l)} です",description=sl,color=ctx.guild.me.color)
      r.timestamp = datetime.utcnow()
      r.set_author(name=f"❖ {ctx.guild.name}内のチャンネルを検索 ❖",icon_url=ctx.guild.icon_url)
      r.set_footer(text=f"送信者 {ctx.author.name}",icon_url=ctx.author.avatar_url)
      await ctx.send(embed=r)
    else: await ctx.send(embed=e,delete_after=5.0)

  @commands.command(name="bot_status",aliases=["bs"])
  async def status(self, ctx):
    self.etc.command_log(ctx.message)
    uss, chs, ems, ros = [], 0, 0, (len(self.bot.guilds)-1)*-1
    for guild in self.bot.guilds:
      for member in guild.members:
        if not member in uss: uss.append(member)
      chs += len(guild.channels)
      ems += len(guild.emojis)
      ros += len(guild.roles)
    embed = discord.Embed(title="◇ 導入サーバー数 ◇",description=f"`{len(self.bot.guilds)}`",color=ctx.guild.me.color)
    embed.timestamp = datetime.utcnow()
    embed.add_field(name="◇ 認識ユーザー数 ◇",value=f"`{len(uss)}`",inline=False)
    embed.add_field(name="◇ 認識チャンネル数 ◇",value=f"`{chs}`",inline=False)
    embed.add_field(name="◇ 認識絵文字数 ◇",value=f"`{ems}`",inline=False)
    embed.add_field(name="◇ 認識役職数 ◇",value=f"`{ros}`",inline=False)
    embed.set_author(name=f"❖ {ctx.guild.me.name}の情報 ❖")
    embed.set_thumbnail(url=self.bot.user.avatar_url)
    embed.set_footer(text=f"送信者 {ctx.author.name}",icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
    
  @commands.command(name="bot_latency",aliases=["bl"])
  async def latency(self, ctx):
    self.etc.command_log(ctx.message)
    embed = discord.Embed(title=f"{round(self.bot.latency * 1000)}ms",color=ctx.guild.me.color)
    embed.set_author(name="❖ BOTのレイテンシ ❖",icon_url=self.bot.user.avatar_url)
    embed.set_footer(text=f"送信者 {ctx.author.name}",icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
    
  @commands.command()
  async def weather(self, ctx, locate=None):
    self.etc.command_log(ctx.message)
    with open("citycodes.json", "r", encoding="utf-8") as f: cities, e = json.load(f), discord.Embed(title="都市名を正しく指定してください")
    if locate in cities:
      citycode = cities[locate]
      resp = urllib.request.urlopen(f'http://weather.livedoor.com/forecast/webservice/json/v1?city={citycode}').read() 
      wc, resp = {"晴れ":0xff9c18,"曇り":0xd0d0d0,"雨":0x059ae2,"雪":0x92a3fc,"晴時々曇":0xdfac6e,"晴時々雨":0x18ff74,"晴時々雪":0x70e2bd,"曇時々晴":0xdfac6e,"曇時々雨":0x6ab2d4,"曇時々雪":0xb8c0ec,"雨時々晴":0x18ff74,"雨時々曇":0x6ab2d4,"雨時々雪":0x2078e2,"雪時々晴":0x70e2bd,"雪時々曇":0xb8c0ec,"雪時々雨":0x2078e2,"晴のち曇":0xdfac6e,"晴のち雨":0x18ff74,"晴のち雪":0x70e2bd,"曇のち晴":0xdfac6e,"曇のち雨":0x6ab2d4,"曇のち雪":0xb8c0ec,"雨のち晴":0x18ff74,"雨のち曇":0x6ab2d4,"雨のち雪":0x2078e2,"雪のち晴":0x70e2bd,"雪のち曇":0xb8c0ec,"雪のち雨":0x2078e2}, json.loads(resp.decode('utf-8'))
      d4, d3, d2, d1 = discord.Embed(title="地方の天気情報",description=resp['description']['text'],color=0xfa4c4c), discord.Embed(title=f"◇ 明後日の天気`({resp['forecasts'][2]['date']})`: {resp['forecasts'][2]['telop']}",color=wc[resp['forecasts'][2]['telop']]), discord.Embed(title=f"◇ 明日の天気`({resp['forecasts'][1]['date']})`: {resp['forecasts'][1]['telop']}",description=f"◆ 最低気温: `{resp['forecasts'][1]['temperature']['min']['celsius']}℃` ◆ 最高気温: `{resp['forecasts'][1]['temperature']['max']['celsius']}℃`",color=wc[resp['forecasts'][1]['telop']]), discord.Embed(title=f"◇ 今日の天気`({resp['forecasts'][0]['date']})`: {resp['forecasts'][0]['telop']}",color=wc[resp['forecasts'][0]['telop']])
      embeds, emojis, page = [d1,d2,d3,d4], [["🗑","➡️"],["⬅️","🗑","➡️"],["⬅️","🗑","➡️"],["⬅️","🗑"]], 0
      for l in range(3): embeds[l].set_thumbnail(url=resp['forecasts'][l]['image']['url'])
      for embed in embeds: 
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f"by {resp['copyright']['provider'][0]['name']}")
        embed.set_author(name=f"❖ {resp['title']} ❖",url=resp['copyright']['link'],icon_url=resp['copyright']['image']['url'])
      def check(reaction, user): return user == ctx.author and str(reaction.emoji) in ["⬅️","🗑","➡️"]
      msg = await ctx.send(embed=embeds[page])
      while not self.bot.is_closed():
        try:
          for emoji in emojis[page]: await msg.add_reaction(emoji)
          emoji = await self.bot.wait_for('reaction_add', timeout=45.0, check=check)
          await msg.clear_reactions()
          if str(emoji[0]) == "⬅️": page -= 1
          elif str(emoji[0]) == "➡️": page += 1
          else: return await msg.delete()
          await msg.edit(embed=embeds[page])
        except asyncio.TimeoutError: return await msg.delete()
    else: await ctx.send(embed=e, delete_after=5.0)
       
  @commands.Cog.listener()
  async def on_ready(self):
    print("ClariAは起動しました")
    await self.bot.change_presence(activity=discord.Game(name=f"ClariA - {len(self.bot.guilds)}サーバー - c!helpでヘルプを表示します"))
    
  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if "found" in str(error).split(" ") and "Command" in str(error).split(" "): return
    await self.etc.error(self.bot, str(type(error)).strip("<class''>"), error, datetime.now().strftime('%m/%d %H:%M'), ctx.message)
    
  @commands.Cog.listener()
  async def on_message(self, message):
    with open("rank.json", "r", encoding="utf-8") as rj: r = json.load(rj)
    return
    
    
def setup(bot): bot.add_cog(Be(bot))                                   