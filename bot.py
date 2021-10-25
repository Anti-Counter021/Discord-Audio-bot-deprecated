import os

import discord
from discord.ext import commands

from audio import YTDLSource
from config import TOKEN

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if f'{channel}'.lower() == 'general':
                await channel.send(r'I\'m back! My name is AudioBot by \_Counter021_')


@bot.command(name='server', help='Prints details of Server')
async def server(ctx):
    owner = f'{ctx.guild.owner}'
    region = f'{ctx.guild.region}'
    member_count = f'{ctx.guild.member_count}'
    icon = f'{ctx.guild.icon_url}'
    description = f'{ctx.guild.description}'

    embed = discord.Embed(
        title=f'{ctx.guild.name} Server info',
        description=description,
        color=discord.Color.random()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name='Owner', value=owner, inline=True)
    embed.add_field(name='Region', value=region, inline=True)
    embed.add_field(name='Member count', value=member_count, inline=True)

    await ctx.send(embed=embed)


@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send(f'{ctx.message.author.name} is not connected to a voice channel')
        return

    voice_client = ctx.message.guild.voice_client
    if voice_client is not None:
        await ctx.send('The bot already in voice channel')
        return

    channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client is None:
        await ctx.send('The bot is not connected to a voice channel')
    elif voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send('The bot is not connected to a voice channel')


@bot.command(name='play', help='To play song')
async def play(ctx, url):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            await ctx.send('Please waiting...')
            filename, title = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable='ffmpeg', source=filename))
        await ctx.send(f'Now playing: {title}')
    except ValueError:
        await ctx.send('Please check the url! The bot could not find the video')
    except Exception as _ex:
        await ctx.send('The bot is not connected to a voice channel')
    finally:
        if filename:
            os.remove(filename)


@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await ctx.send('Audio has been paused')
    else:
        await ctx.send('The bot is not playing anything at the moment')


@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client and voice_client.is_paused():
        voice_client.resume()
    else:
        await ctx.send('The bot was not playing anything before this. Use play command')


@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()
    else:
        await ctx.send('The bot is not playing anything at the moment')


if __name__ == '__main__':
    bot.run(TOKEN)
