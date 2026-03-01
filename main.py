import os
import sys
from dotenv import load_dotenv

#INJECTARE NODE.JS
NODE_PATH = r"C:\Program Files\nodejs"
if os.path.exists(NODE_PATH):
    os.environ["PATH"] = NODE_PATH + os.pathsep + os.environ["PATH"]

import discord
from discord.ext import commands
import yt_dlp
import asyncio
import requests
from bs4 import BeautifulSoup

#CONFIGURARE
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)
queues = {}

#SETARI YT-DLP (MEDIA)
ydl_opts_meta = {
    'extract_flat': True,
    'quiet': True,
    'ignoreerrors': True,
    'nocheckcertificate': True,
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

#SETĂRI YT-DLP (AUDIO)
ydl_opts_audio = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'source_address': '0.0.0.0',
    'http_chunk_size': 10485760, 
}

#SETĂRI FFMPEG
ffmpeg_options = {
    'before_options': (
        '-reconnect 1 '
        '-reconnect_streamed 1 '
        '-reconnect_delay_max 5 '
        '-reconnect_on_network_error 1 '
        '-nostdin '
    ),
    'options': (
        '-vn '
        '-threads 2 '
        '-bufsize 200M '
        '-probesize 50M ' 
        '-analyzeduration 0 '
    )
}

#FUNCTIE CITIRE SPOTIFY
def get_spotify_full_name(spotify_url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)'}
        response = requests.get(spotify_url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('meta', property='og:title')
            description = soup.find('meta', property='og:description')
            
            piesa = "Necunoscut"
            artist = ""
            if title: piesa = title['content']
            if description:
                desc_content = description['content']
                if " · " in desc_content:
                    artist = desc_content.split(" · ")[0].replace("Listen to ", "").replace(" on Spotify", "")
            
            if artist: return f"{artist} - {piesa}"
            return piesa
    except Exception as e:
        print(f"Eroare scraping: {e}")
    return None

#REDARE ASINCRON
async def play_next(ctx):
    guild_id = ctx.guild.id
    if guild_id in queues and len(queues[guild_id]) > 0:
        song = queues[guild_id].pop(0)
        print(f"🎵 Procesez: {song['title']}")

        loop = asyncio.get_event_loop()
        try:
            data = await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts_audio).extract_info(song['url'], download=False))
            
            if not data or 'url' not in data:
                print("Link invalid, skip.")
                await play_next(ctx)
                return

            audio_url = data['url']
            exe_path = "./ffmpeg.exe" if os.path.exists("./ffmpeg.exe") else "ffmpeg"
            
            ctx.voice_client.play(
                discord.FFmpegPCMAudio(audio_url, executable=exe_path, **ffmpeg_options),
                after=lambda e: bot.loop.create_task(play_next(ctx))
            )
            await ctx.send(f'▶️ Acum cântă: **{song["title"]}**')
            
        except Exception as e:
            print(f"Eroare redare: {e}")
            await play_next(ctx)
    else:
        print("Coada gata.")

async def load_rest_of_playlist(ctx, playlist_url):
    try:
        opts = ydl_opts_meta.copy()
        opts['playlist_items'] = '2-' 
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(opts).extract_info(playlist_url, download=False))
        
        if 'entries' in data:
            new_songs = []
            for entry in data['entries']:
                if entry:
                    url = entry.get('url')
                    if len(url) == 11: url = f"https://www.youtube.com/watch?v={url}"
                    new_songs.append({'title': entry.get('title'), 'url': url})
            
            guild_id = ctx.guild.id
            if guild_id not in queues: queues[guild_id] = []
            queues[guild_id].extend(new_songs)
            await ctx.send(f"✅ Fundal: +{len(new_songs)} piese.")
    except:
        pass

@bot.event
async def on_ready():
    print(f'✅ Botul {bot.user} este ONLINE! (Link Master V4)')

@bot.command(name='play')
async def play(ctx, *, search: str):
    if not ctx.author.voice:
        return await ctx.send("❌ Intră în voce!")

    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)

    #YouTube Music
    if "music.youtube.com" in search:
        search = search.replace("music.youtube.com", "www.youtube.com")

    #Short Links (youtu.be)
    if "youtu.be/" in search:
        # Transformăm https://youtu.be/ID în https://www.youtube.com/watch?v=ID
        # Păstrăm tot ce e după ID (de ex ?si=...) că nu strică
        video_id = search.split("youtu.be/")[1]
        search = f"https://www.youtube.com/watch?v={video_id}"

    #Detectie Spotify
    if "spotify.com/track" in search:
        await ctx.send("🟢 Link Spotify detectat...")
        full_name = await asyncio.to_thread(get_spotify_full_name, search)
        
        if full_name:
            await ctx.send(f"🔎 Caut pe YouTube: **{full_name}**")
            search = full_name
        else:
            return await ctx.send("⚠️ Nu pot citi detaliile piesei.")

    #LOGICA YOUTUBE
    is_playlist = search.startswith("http") and ("list=" in search or "album" in search)

    if is_playlist:
        await ctx.send(f'⚡ Playlist detectat...')
        first_item_opts = ydl_opts_meta.copy()
        first_item_opts['playlist_items'] = '1'
        loop = asyncio.get_event_loop()
        try:
            data = await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(first_item_opts).extract_info(search, download=False))
            if 'entries' in data:
                entry = data['entries'][0]
                url = entry.get('url')
                if len(url) == 11: url = f"https://www.youtube.com/watch?v={url}"
                
                song = {'title': entry.get('title'), 'url': url}
                guild_id = ctx.guild.id
                if guild_id not in queues: queues[guild_id] = []
                queues[guild_id].append(song)
                
                if not ctx.voice_client.is_playing():
                    await play_next(ctx)
                else:
                    await ctx.send(f'📝 La coadă: **{song["title"]}**')
                
                bot.loop.create_task(load_rest_of_playlist(ctx, search))
        except Exception as e:
            await ctx.send("❌ Eroare playlist.")
            
    else:
        loop = asyncio.get_event_loop()
        try:
            if search.startswith("http"):
                 data = await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts_meta).extract_info(search, download=False))
            else:
                 data = await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts_meta).extract_info(f"ytsearch:{search}", download=False))

            song = None
            if 'entries' in data:
                entry = data['entries'][0]
                url = entry.get('url')
                if url and len(url) == 11: url = f"https://www.youtube.com/watch?v={url}"
                song = {'title': entry.get('title'), 'url': url}
            
            #V erificam și webpage_url sau id (pentru linkuri scurte)
            elif 'url' in data or 'webpage_url' in data or 'id' in data:
                url = data.get('url') or data.get('webpage_url')
                if not url and data.get('id'):
                    url = f"https://www.youtube.com/watch?v={data.get('id')}"
                
                song = {'title': data.get('title'), 'url': url}

            if song:
                guild_id = ctx.guild.id
                if guild_id not in queues: queues[guild_id] = []
                queues[guild_id].append(song)
                
                if not ctx.voice_client.is_playing():
                    await play_next(ctx)
                else:
                    await ctx.send(f'📝 La coadă: **{song["title"]}**')
            else:
                await ctx.send("⚠️ Nu am găsit rezultate.")
        except Exception as e:
            print(e)
            await ctx.send("❌ Eroare.")

@bot.command(name='skip')
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏭️ Skip.")

@bot.command(name='stop')
async def stop(ctx):
    if ctx.voice_client:
        queues[ctx.guild.id] = []
        await ctx.voice_client.disconnect()
        await ctx.send("👋")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot.run(TOKEN)