from discord.ext import commands
from tools import sort, etc
import discord
import asyncio
import json

class MC(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    self.etc = etc.tool(bot)
    
    
  @commands.group()
  @commands.has_permissions(manage_guild=True)
  async def role(self, ctx):
    if ctx.invoked_subcommand is None:
      embed = discord.Embed(title="role",description="ヘルプ",color=0xabc9ec)
      embed.add_field(name="/c [`名前`] [`権限`] [`表示`] [`メンション`]",value="役職を作成します\n`権限`:\n0: 権限無し\n1: 一般\n2: チャンネル権限\n3: 高権限\n`表示`:\n0: オンライン時に特別表示します\n1: オンライン時に特別表示しません\n`メンション`:\n0: 可能にします\n1: 不可能にします")
      embed.add_field(name="/d [`役職名`]",value="指定した役職を削除します")
      embed.add_field(name="/a [`ユーザーid`] [`役職id`]",value="指定した役職を指定したユーザーに付与します")
      embed.add_field(name="/r [`ユーザーid`] [`役職id`]",value="指定した役職を指定したユーザーから削除します")
      embed.set_author(name=self.bot.user.name,icon_url=self.bot.user.avatar_url)
      await ctx.send(embed=embed)
      embed.clear_fields()
      self.etc.command_log(ctx.message)
      
  @role.command(name="/c")
  async def role_create(self, ctx, name, permission: int, hoist: int, mentionable: int):
    await ctx.message.delete()
    permissions = [discord.Permissions.none(),discord.Permissions.general(),discord.Permissions.all_channel(),discord.Permissions.all()]
    r_a_p = permissions[permission]
    h_m = [True,False] 
    r_a_h = h_m[hoist]
    r_a_m = h_m[mentionable]
    await ctx.guild.create_role(name=name, permissions=r_a_p, hoist=r_a_h, mentionable=r_a_m)
    await ctx.send(f"役職`{name}`を作成しました")
    self.etc.command_log(ctx.message)
  
  @role.command(name="/d")
  async def role_delete(self, ctx, role: discord.Role):
    await ctx.message.delete()
    await role.delete()
    await ctx.send(f"役職`{name}`を削除しました")
    self.etc.command_log(ctx.message)
  
  @role.command(name="/a")
  async def role_add(self, ctx, member: discord.Member, role: discord.Role):
    await ctx.message.delete()
    await member.add_roles(role)
    await ctx.send(f"役職`{role.name}`を{member.name}に追加しました")
    self.etc.command_log(ctx.message)
    
  @role.command(name="/r")
  async def role_remove(self, ctx, member: discord.Member, role: discord.Role):
    await ctx.message.delete()
    await member.remove_roles(role)
    await ctx.send(f"役職`{role.name}`を{member.name}から削除しました")
    self.etc.command_log(ctx.message)
  
  @commands.group(aliases=[".ge"])
  @commands.has_permissions(manage_guild=True)
  async def globalexcept(self, ctx):
    if ctx.invoked_subcommand is None:
      embed = discord.Embed(title="globalexcept",description="ヘルプ",color=0xabc9ec)
      embed.add_field(name="/a [`id`]",value="指定した`id`のユーザーを除外します")
      embed.add_field(name="/r [`id`]",value="指定した`id`のユーザーを除外対象から削除します")
      embed.set_author(name=self.bot.user.name,icon_url=self.bot.user.avatar_url)
      await ctx.send(embed=embed)
      embed.clear_fields()
      self.etc.command_log(ctx.message)
    
  @globalexcept.command(name="/a")
  async def globalexcept_add(self, ctx, user: discord.User):
    await ctx.message.delete()
    with open("exceptglobal.json", "r", encoding="utf-8") as glo_except:
      glo_excepts = json.load(glo_except)
    if str(user.id) not in glo_excepts:
      glo_excepts.setdefault(user.id, user.name)
      with open("exceptglobal.json", "w", encoding="utf-8") as glo_except:
        json.dump(glo_excepts, glo_except)
      await ctx.send(f"{user.name}をglobalchatから除外しました")
    else:
      message = await ctx.send(f"{user.name}は既に除外されています")
      await asyncio.sleep(5)
      await message.delete()
    self.etc.command_log(ctx.message)
                  
  @globalexcept.command(name="/r")
  async def globalexcept_remove(self, ctx, user: discord.User):
    await ctx.message.delete()
    with open("exceptglobal.json", "r", encoding="utf-8") as glo_except:
      glo_excepts = json.load(glo_except)
    if str(user.id) in glo_excepts:
      del glo_excepts[str(user.id)]
      with open("exceptglobal.json", "w", encoding="utf-8") as glo_except:
        json.dump(glo_excepts, glo_except)
      await ctx.send(f"{user.name}を除外対象から削除しました")
    else:
      message = await ctx.send(f"{user.name}は除外されていません")
      await asyncio.sleep(5)
      await message.delete()
    self.etc.command_log(ctx.message)

  @commands.group()
  @commands.has_permissions(manage_guild=True)
  async def count(self, ctx):
    if ctx.invoked_subcommand is None:
      embed = discord.Embed(title="count",description="ヘルプ",color=0xabc9ec)
      embed.add_field(name="/a",value="カウンターを登録します")
      embed.add_field(name="/t",value="カウントチャンネルを作成します\n(カウンターの値を反映します)")
      embed.add_field(name="/f",value="カウントチャンネルを削除します")
      embed.set_author(name=self.bot.user.name,icon_url=self.bot.user.avatar_url)
      await ctx.send(embed=embed)
      embed.clear_fields()
      self.etc.command_log(ctx.message)
  
  @count.command(name="/a")
  async def count_add(self, ctx):
    await ctx.message.delete()
    bot_count = 0
    with open('count.json', 'r', encoding='utf-8') as count:
      counts = json.load(count)
    if str(ctx.guild.id) not in counts:
      for member in ctx.guild.members:
        if member.bot:
          bot_count += 1
      all_count = {
        "カウンター":"False",
        "総ユーザー数":str(len(ctx.guild.members)),
        "ユーザー数":str(len(ctx.guild.members) - bot_count),
        "BOT数":str(bot_count),
        "役職数":str(len(ctx.guild.roles)),
        "カテゴリ数":str(len(ctx.guild.categories)),
        "チャンネル数":str(len(ctx.guild.channels)),
        "テキストチャンネル数":str(len(ctx.guild.text_channels)),
        "ボイスチャンネル数":"8"
      }
      counts.setdefault(str(ctx.guild.id), all_count)
      with open('count.json', 'w', encoding='utf-8') as count:
        json.dump(counts, count)
      await ctx.send("このグループを登録しました\n`c!count /t`で有効化が出来ます")   
    else:
      message = await ctx.send("このグループは既に登録されています")
      await asyncio.sleep(5)
      await message.delete()
    self.etc.command_log(ctx.message)
    
  @count.command(name="/t")
  async def count_true(self, ctx):
    await ctx.message.delete()
    with open('count.json', 'r', encoding='utf-8') as count:
      counts = json.load(count)
    if str(ctx.guild.id) in counts:
      if counts[str(ctx.guild.id)]["カウンター"] == "False":
        counts[str(ctx.guild.id)]["カウンター"] = "True"
        with open('count.json', 'w', encoding='utf-8') as count:
           json.dump(counts, count)
        category_ = await ctx.guild.create_category("CB-count", overwrites=None, reason=None)
        with open('co_ch_id.json', 'r', encoding='utf-8') as co_ch_id:
          co_ch_ids = json.load(co_ch_id)
        channel_ids = [] 
        voicechannel = await ctx.guild.create_voice_channel("総ユーザー数 : " + str(counts[str(ctx.guild.id)]["総ユーザー数"]), overwrites=None, category=category_, reason=None, bitrate=8000, user_limit=0)
        channel_ids.append(voicechannel.id)
        voicechannel = await ctx.guild.create_voice_channel("ユーザー数 : " + str(counts[str(ctx.guild.id)]["ユーザー数"]), overwrites=None, category=category_, reason=None, bitrate=8000, user_limit=0)
        channel_ids.append(voicechannel.id)
        voicechannel = await ctx.guild.create_voice_channel("BOT数 : " + str(counts[str(ctx.guild.id)]["BOT数"]), overwrites=None, category=category_, reason=None, bitrate=8000, user_limit=0)
        channel_ids.append(voicechannel.id)
        voicechannel = await ctx.guild.create_voice_channel("役職数 : " + str(counts[str(ctx.guild.id)]["役職数"]), overwrites=None, category=category_, reason=None, bitrate=8000, user_limit=0)
        channel_ids.append(voicechannel.id)
        voicechannel = await ctx.guild.create_voice_channel("カテゴリ数 : " + str(counts[str(ctx.guild.id)]["カテゴリ数"]), overwrites=None, category=category_, reason=None, bitrate=8000, user_limit=0)
        channel_ids.append(voicechannel.id)
        voicechannel = await ctx.guild.create_voice_channel("チャンネル数 : " + str(counts[str(ctx.guild.id)]["チャンネル数"]), overwrites=None, category=category_, reason=None, bitrate=8000, user_limit=0)
        channel_ids.append(voicechannel.id)
        voicechannel = await ctx.guild.create_voice_channel("テキストチャンネル数 : " + str(counts[str(ctx.guild.id)]["テキストチャンネル数"]), overwrites=None, category=category_, reason=None, bitrate=8000, user_limit=0)
        channel_ids.append(voicechannel.id)
        voicechannel = await ctx.guild.create_voice_channel("ボイスチャンネル数 : " + str(int(counts[str(ctx.guild.id)]["ボイスチャンネル数"])), overwrites=None, category=category_, reason=None, bitrate=8000, user_limit=0)     
        channel_ids.append(voicechannel.id)
        co_ch_ids[str(ctx.guild.id)] = channel_ids
        with open('co_ch_id.json', 'w', encoding='utf-8') as co_ch_id:
          json.dump(co_ch_ids, co_ch_id)
        await ctx.send("カウントチャンネルを作成しました\n`c!count /f`で無効化出来ます")
      else:
        message = await ctx.send("このグループのカウントは既に有効化されています")
        await asyncio.sleep(5)
        await message.delete()
    else:
      message = await ctx.send("このグループは登録されていません\n`c!count /a`で登録して下さい")
      await asyncio.sleep(5)
      await message.delete()
    self.etc.command_log(ctx.message)
        
  @count.command(name="/f")
  async def count_false(self, ctx):
    await ctx.message.delete()
    with open('count.json', 'r', encoding='utf-8') as count:
      counts = json.load(count)
    if str(ctx.guild.id) in counts:
      if counts[str(ctx.guild.id)]["カウンター"] == "True":
        counts[str(ctx.guild.id)]["カウンター"] = "False"
        with open('count.json', 'w', encoding='utf-8') as count:
          json.dump(counts, count)
        with open('co_ch_id.json', 'r', encoding='utf-8') as co_ch_id:
          co_ch_ids = json.load(co_ch_id)
        voicechannel = ctx.guild.get_channel(co_ch_ids[str(ctx.guild.id)][0])
        await voicechannel.delete(reason=None)
        voicechannel = ctx.guild.get_channel(co_ch_ids[str(ctx.guild.id)][1])
        await voicechannel.delete(reason=None)
        voicechannel = ctx.guild.get_channel(co_ch_ids[str(ctx.guild.id)][2])
        await voicechannel.delete(reason=None)
        voicechannel = ctx.guild.get_channel(co_ch_ids[str(ctx.guild.id)][3])
        await voicechannel.delete(reason=None)
        voicechannel = ctx.guild.get_channel(co_ch_ids[str(ctx.guild.id)][4])
        await voicechannel.delete(reason=None)
        voicechannel = ctx.guild.get_channel(co_ch_ids[str(ctx.guild.id)][5])
        await voicechannel.delete(reason=None)
        voicechannel = ctx.guild.get_channel(co_ch_ids[str(ctx.guild.id)][6])
        await voicechannel.delete(reason=None)
        voicechannel = ctx.guild.get_channel(co_ch_ids[str(ctx.guild.id)][7])
        await voicechannel.delete(reason=None)
        categorychannel = sort.categorychannel(ctx.guild, "CB-count")
        await categorychannel.delete(reason=None)
        await ctx.send("カウントチャンネルを削除しました\n`c!count /t`で有効化出来ます")
      else:
        message = await ctx.send("このグループのカウントは有効化されていません")
        await asyncio.sleep(5)
        await message.delete()
    else:
      message = await ctx.send("このグループは登録されていません\n`c!count /a`で登録して下さい")
      await asyncio.sleep(5)
      await message.delete()
    self.etc.command_log(ctx.message)
  
  @commands.group(aliases=[".slr"])
  @commands.has_permissions(administrator=True)
  async def set_levelup_add_role(self, ctx): 
    if ctx.invoked_subcommand is None:
      embed = discord.Embed(title="setluar",description="ヘルプ",color=0xabc9ec)
      embed.add_field(name="/a [`レベル`] [`役職id`]",value="ユーザーが指定した`レベル`に到達した際に指定した`id`の役職を付与する様にします")
      embed.add_field(name="/r [`レベル`]",value="指定した`レベル`では役職が付与されなくなります")
      embed.add_field(name="/e [`レベル`] [`役職id`]",value="指定した`レベル`で付与される役職を変更します")
      embed.add_field(name="/l",value="設定された役職のリストを表示します")
      embed.set_author(name=self.bot.user.name,icon_url=self.bot.user.avatar_url)
      await ctx.send(embed=embed)
      embed.clear_fields()
      self.etc.command_log(ctx.message)
  
  @set_levelup_add_role.command(name="/a")
  async def luar_add(self, ctx, level: str, role: int):
    await ctx.message.delete()
    with open("rank.json", "r", encoding="utf-8") as level_l:
      levels = json.load(level_l)
    if level not in levels:
      levels["guild"][f"{ctx.guild.id}"]["roles"].setdefault(level, role)
      with open("rank.json", "w", encoding="utf-8") as level_l:
        json.dump(levels, level_l)
      await ctx.send(f"レベル{level}到達時に役職を付与します")
    else:
      message = await ctx.send(f"レベル{level}には既に設定されています")
      await asyncio.sleep(5)
      await message.delete()
    self.etc.command_log(ctx.message)
    
  @set_levelup_add_role.command(name="/r")
  async def luar_remove(self, ctx, level: str):
    await ctx.message.delete()
    with open("rank.json", "r", encoding="utf-8") as level_l:
      levels = json.load(level_l)
    if level in levels["guild"][f"{ctx.guild.id}"]["roles"]:
      del levels["guild"][f"{ctx.guild.id}"]["roles"][level]
      with open("rank.json", "w", encoding="utf-8") as level_l:
        json.dump(levels, level_l)
      await ctx.send(f"レベル{level}到達時の役職付与を解除しました")
    else:
      message = await ctx.send(f"レベル{level}には役職が設定されていません")
      await asyncio.sleep(5)
      await message.delete()
    self.etc.command_log(ctx.message)
  
  @set_levelup_add_role.command(name="/e")
  async def luar_edit(self, ctx, level: str, role: int):
    await ctx.message.delete()
    with open("rank.json", "r", encoding="utf-8") as level_l:
      levels = json.load(level_l)
    if level in levels:
      levels["guild"][f"{ctx.guild.id}"]["roles"][level] = role
      with open("rank.json", "w", encoding="utf-8") as level_l:
        json.dump(levels, level_l)
      await ctx.send(f"レベル{level}到達時の役職を変更しました")
    else:
      message = await ctx.send(f"レベル{level}には役職が設定されていません")
      await asyncio.sleep(5)
      await message.delete()
    self.etc.command_log(ctx.message)
  
  @set_levelup_add_role.command(name="/l")
  async def luar_list(self, ctx):
    await ctx.message.delete()
    with open("rank.json", "r", encoding="utf-8") as level_l:
      levels = json.load(level_l)
    if len(levels["guild"][f"{ctx.guild.id}"]["roles"]) >= 1:
      embed = discord.Embed(title="setluar",description="役職リスト",color=0xabc9ec)
      for key in levels["guild"][f"{ctx.guild.id}"]["roles"].keys():
        embed.add_field(name=key,value=levels["guild"][f"{ctx.guild.id}"]["roles"][f"{key}"])
      embed.set_author(name=self.bot.user.name,icon_url=self.bot.user.avatar_url)
      await ctx.send(embed=embed)
      embed.clear_fields()
    else:
      message = await ctx.send("設定されていません")
      await asyncio.sleep(5)
      await message.delete()
    self.etc.command_log(ctx.message)
  
    
def setup(bot):
  bot.add_cog(MC(bot))