import os
import subprocess
import time

try:
  import discord
  from discord.ext import commands
except:
  os.system('pip3 install discord')

try:
  from googlesearch import search
except:
  os.system('pip3 install google beautifulsoup4')

from keep_alive import keep_alive

client = commands.Bot(command_prefix="rpi ", intents=discord.Intents.all())

@client.event
async def on_ready():
    print('Bot is ready')

@client.command()
async def exec(ctx,*,command):
  NoCommands = ['rm', 'sudo', 'bash']
  commands = command.split(' ')
  ExecuteCommand = True
  for commandcheck in commands:
    for NoCommand in NoCommands:
      if commandcheck.strip() == NoCommand:
        await ctx.send('```\nYou are not allowed to use that command :(\n```')
        ExecuteCommand = False
        break
  
  if ExecuteCommand:
    print(command)
    output = subprocess.getoutput(command)
    await ctx.send(f'```\n{output.strip()}\n```')

@client.command(name='search')
async def _search(ctx, NumberOfSearchResults,*, SearchTerm): 
  print(SearchTerm)
  SearchResultsMessage = 'Hey I found a few links which might help you\n```'
  SearchResultNumber = 0
  for SearchResults in search(SearchTerm, tld="co.in", num=int(NumberOfSearchResults), stop=int(NumberOfSearchResults)): 
    SearchResultNumber += 1
    SearchResultsMessage = SearchResultsMessage + f'\n{str(SearchResultNumber)}) {SearchResults}'

  await ctx.send(SearchResultsMessage + '\n```')

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, number):
  await ctx.message.delete()
  await ctx.channel.purge(limit=int(number))
  InfoMessage = await ctx.message.channel.send(f':white_check_mark: **Finished deleting** `{number} messages` ')
  time.sleep(5)
  await InfoMessage.delete()

@client.command()
async def ping(ctx):
  await ctx.send('pong :ping_pong:')
  time.sleep(1)
  await ctx.send('Get it :rofl:')
  time.sleep(1)
  await ctx.send(f'Nvm, The latency is: `{round(client.latency * 1000)}` ms')

@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member : discord.Member,*, reason=None):
  await member.kick(reason=reason)
  await ctx.send(f'{member} has been kicked from the server. Reason for kick is {reason}')

@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member : discord.Member,*, reason=None):
  await member.ban(reason=reason)
  await ctx.send(f'{member} has been banned from the server. Reason for ban is {reason}')

@client.command()
async def test(ctx):
  channel = ctx.message.channel
  Testmsg = await channel.send('Testing')
  time.sleep(5)
  await Testmsg.delete()



#keep_alive()
client.run(os.getenv('TOKEN'))
