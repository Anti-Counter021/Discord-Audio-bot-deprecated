import discord
from discord.ext import commands

from audio import YTDLSource
from config import TOKEN

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)


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
        await ctx.send('The bot is not connected to a voice channel.')
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
            filename, title = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable='ffmpeg', source=filename))
        await ctx.send(f'Now playing: {title}')
    except Exception as _ex:
        print(_ex)
        await ctx.send('The bot is not connected to a voice channel.')


if __name__ == '__main__':
    bot.run(TOKEN)
