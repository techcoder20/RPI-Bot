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


## Exec Command
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


## Search Command
@client.command(name='search')
async def _search(ctx, NumberOfSearchResults,*, SearchTerm): 
  print(SearchTerm)
  SearchResultsMessage = 'Hey I found a few links which might help you\n```'
  SearchResultNumber = 0
  for SearchResults in search(SearchTerm, tld="co.in", num=int(NumberOfSearchResults), stop=int(NumberOfSearchResults)): 
    SearchResultNumber += 1
    SearchResultsMessage = SearchResultsMessage + f'\n{str(SearchResultNumber)}) {SearchResults}'

  await ctx.send(SearchResultsMessage + '\n```')


## Clear Command
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, number):
  await ctx.message.delete()
  await ctx.channel.purge(limit=int(number))
  InfoMessage = await ctx.message.channel.send(f':white_check_mark: **Finished deleting** `{number} messages` ')
  time.sleep(5)
  await InfoMessage.delete()


## Ping Command
@client.command()
async def ping(ctx):
  await ctx.send('pong :ping_pong:')
  time.sleep(1)
  await ctx.send('Get it :rofl:')
  time.sleep(1)
  await ctx.send(f'Nvm, The latency is: `{round(client.latency * 1000)}` ms')


## Kick Command
@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member : discord.Member,*, reason=None):
  await member.kick(reason=reason)
  await ctx.send(f'{member} has been kicked from the server. Reason for kick is {reason}')


## Ban Command
@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member : discord.Member,*, reason=None):
  await member.ban(reason=reason)
  await ctx.send(f'{member} has been banned from the server. Reason for ban is {reason}')

client.remove_command("help")

@client.group(invoke_without_command=True)
async def help(ctx):
  em = discord.Embed(title = 'Help', description='The help argument will show you the available arguments. Use `rpi <argument name>` to get more information on a command.\n\n **The Available Arguments are:**', color = discord.Color.green())

  em.add_field(name = 'Moderation', value='kick, ban, clear')
  em.add_field(name = 'Helping Others', value = 'exec, search')
  em.add_field(name = 'Other', value = 'ping')
  em.set_thumbnail(url = 'https://publicdomainpictures.net/pictures/150000/velka/help-icon.jpg')
  em.set_footer(icon_url = ctx.author.avatar_url, text = f'Requested by {ctx.author.name}')
  await ctx.send(embed = em)

@help.command(name='kick')
async def _kick(ctx):
  em = discord.Embed(title = 'Kick', description = 'Kick any member in your server. The reason by default is set to none. The user need Administrator permission to use this argument.')
  em.add_field(name='Usage', value='rpi kick [Member Name] [Reason]')
  em.set_footer(icon_url = ctx.author.avatar_url, text = f'Requested by {ctx.author.name}')
  await ctx.send(embed = em)


@help.command(name='ban')
async def _ban(ctx):
  em = discord.Embed(title = 'Ban', description = 'Ban any member in your server. The reason by default is set to none. The user need Administrator permission to use this argument.')
  em.add_field(name='Usage', value='rpi ban [Member Name] [Reason]')
  em.set_footer(icon_url = ctx.author.avatar_url, text = f'Requested by {ctx.author.name}')
  await ctx.send(embed = em)


@help.command(name='clear')
async def _clear(ctx):
  em = discord.Embed(title = 'Clear', description = 'Delete a specific number of messages. It takes one argument which is Number of messages. THis command will only work if the user has manage messages permission.')
  em.add_field(name='Usage', value='rpi clear [Number of messages]')
  em.set_footer(icon_url = ctx.author.avatar_url, text = f'Requested by {ctx.author.name}')
  await ctx.send(embed = em)


@help.command(name='search')
async def __search(ctx):
  em = discord.Embed(title = 'Search', description = 'This argument will help you to search google right from discord. It takes two arguments which are Number of search results and Search query.')
  em.add_field(name='Usage', value='rpi search [Number of Search Results] [Search query]')
  em.set_footer(icon_url = ctx.author.avatar_url, text = f'Requested by {ctx.author.name}')
  await ctx.send(embed = em)


@help.command(name='exec')
async def _exec(ctx):
  em = discord.Embed(title = 'Exec', description = 'This argument will allow you to run commands in a linux terminal and see the output of the command.')
  em.add_field(name='Usage', value='rpi exec [command]')
  em.set_footer(icon_url = ctx.author.avatar_url, text = f'Requested by {ctx.author.name}')
  await ctx.send(embed = em)


@help.command(name='ping')
async def _ping(ctx):
  em = discord.Embed(title = 'Ping', description = 'Sends the latency of the bot.')
  em.add_field(name='Usage', value='rpi ping')
  em.set_footer(icon_url = ctx.author.avatar_url, text = f'Requested by {ctx.author.name}')
  await ctx.send(embed = em)


@client.command()
async def test(ctx):
  pass

#keep_alive()
client.run(os.getenv('TOKEN'))
