import discord
client = discord.Client()


def guild(name):
  for guild in client.guilds:
    if guild.name == name:
      return guild


def channel(guild, name):
  for channel in guild.channels:
    if channel.name == name:
      return channel
            
      
def categorychannel(guild, name):
  for categorychannel in guild.categories:
    if categorychannel.name == name:
      return categorychannel
      
      
def textchannel(guild, name):
  for textchannel in guild.text_channels:
    if textchannel.name == name:
      return textchannel
      
      
def voicechannel(guild, name):
  for voicechannel in guild.voice_channels:
    if voicechannel.name == name:
      return voicechannel
      
      
def user(name):
  for user in client.get_all_members():
    if user.name == name:
      return user
      
      
def member(guild, name):
  for member in guild.members:
    if member.name == name:
      return member
      
    
def role(guild, name):
  for role in guild.roles:
    if role.name == name:
      return role