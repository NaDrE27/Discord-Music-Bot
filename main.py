import os
import sys
import asyncio
import requests
import discord
import yt_dlp
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from discord.ext import commands

NODE_PATH = r"C:\Program Files\nodejs"
if os.path.exists(NODE_PATH):
    os.environ["PATH"] = NODE_PATH + os.pathsep + os.environ["PATH"]

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command('help')
queues = {}

ydl_opts_meta = {
    'extract_flat': 'in_playlist', 'quiet': True, 'ignoreerrors': True, 'nocheckcertificate': True, 'playlistend': 100,
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

ydl_opts_audio = {
    'format': 'bestaudio/best', 'noplaylist': True, 'quiet': True, 'nocheckcertificate': True,
    'ignoreerrors': True, 'source_address': '0.0.0.0', 'http_chunk_size': 10485760
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -reconnect_on_network_error 1 -nostdin',
    'options': '-vn -threads 2 -bufsize 200M -probesize 50M -analyzeduration 0'
}

def get_spotify_full_name(spotify_url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(spotify_url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('meta', property='og:title')
            description = soup.find('meta', property='og:description')
            piesa = title['content'] if title else "Necunoscut"
            artist = ""
            if description and " · " in description['content']:
                artist = description['content'].split(" · ")[0].replace("Listen to ", "").replace(" on Spotify", "")
            return f"{artist} - {piesa}" if artist else piesa
    except Exception:
        pass
    return None

async def play_next(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    if guild_id in queues and queues[guild_id]:
        song = queues[guild_id].pop(0)
        try:
            data = await asyncio.get_event_loop().run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts_audio).extract_info(song['url'], download=False))
            if not data or 'url' not in data: 
                return await play_next(interaction)
            vc = interaction.guild.voice_client
            if vc:
                exe_path = "./ffmpeg.exe" if os.path.exists("./ffmpeg.exe") else "ffmpeg"
                vc.play(discord.FFmpegPCMAudio(data['url'], executable=exe_path, **ffmpeg_options), after=lambda e: bot.loop.create_task(play_next(interaction)))
                await interaction.channel.send(f'▶️ Acum cântă: **{song["title"]}**')
        except Exception: 
            await play_next(interaction)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'✅ Botul {bot.user} este ONLINE!')

@bot.tree.command(name='help', description="Afișează meniul de ajutor")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="🎵 Meniu de Ajutor - Comenzi Muzică", color=discord.Color.blurple())
    embed.add_field(name="▶️ /play <link/nume>", value="Redă o melodie de pe YouTube sau Spotify.", inline=False)
    embed.add_field(name="⏸️ /pause", value="Pune melodia curentă pe pauză.", inline=False)
    embed.add_field(name="▶️ /resume", value="Reia melodia pusă pe pauză.", inline=False)
    embed.add_field(name="📜 /queue", value="Afișează coada de redare.", inline=False)
    embed.add_field(name="⏭️ /skip", value="Trece la următoarea melodie din coadă.", inline=False)
    embed.add_field(name="⏹️ /stop", value="Oprește muzica și golește coada.", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='play', description="Redă o melodie de pe YouTube sau Spotify")
async def play(interaction: discord.Interaction, search: str):
    await interaction.response.defer()
    vc = interaction.guild.voice_client

    if vc and vc.is_paused(): 
        return await interaction.followup.send("❌ Muzica este pe pauză. Folosește /resume.")
    if not interaction.user.voice: 
        return await interaction.followup.send("❌ Intră într-un canal de voce!")

    if not vc:
        vc = await interaction.user.voice.channel.connect()
    else:
        await vc.move_to(interaction.user.voice.channel)

    search = search.replace("music.youtube.com", "www.youtube.com")
    
    if "http://googleusercontent.com/spotify.com/" in search or "spotify.com" in search:
        full_name = await asyncio.to_thread(get_spotify_full_name, search)
        if not full_name: 
            return await interaction.followup.send("⚠️ Nu pot citi detaliile piesei.")
        search = full_name

    try:
        query = search if search.startswith("http") else f"ytsearch:{search}"
        data = await asyncio.get_event_loop().run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts_meta).extract_info(query, download=False))
        if not data: 
            return await interaction.followup.send("⚠️ Eroare accesare piesă.")

        entries = data.get('entries')
        if entries is not None:
            entries = list(entries)
            if not entries: 
                return await interaction.followup.send("⚠️ Playlist gol sau privat.")
            
            if query.startswith("ytsearch:"): 
                entries = [entries[0]]
            
            new_songs = [{'title': e.get('title', 'Necunoscut'), 'url': f"https://www.youtube.com/watch?v={e.get('id')}" if e.get('id') else e.get('url')} for e in entries if e and (e.get('id') or e.get('url'))]
            
            if not new_songs: 
                return await interaction.followup.send("⚠️ Nu am putut extrage piesele.")
            
            guild_id = interaction.guild.id
            if guild_id not in queues: 
                queues[guild_id] = []
            
            queues[guild_id].append(new_songs[0])
            
            if not vc.is_playing(): 
                await interaction.followup.send("⏳ Piesa se încarcă...")
                await play_next(interaction)
            else: 
                await interaction.followup.send(f'📝 La coadă: **{new_songs[0]["title"]}**')
            
            if len(new_songs) > 1:
                queues[guild_id].extend(new_songs[1:])
                await interaction.channel.send(f"✅ Fundal: +{len(new_songs) - 1} piese adăugate din playlist.")
                
        else:
            url = data.get('id') or data.get('url') or data.get('webpage_url')
            if not url: 
                return await interaction.followup.send("⚠️ Nu am găsit rezultate.")
            song = {'title': data.get('title', 'Necunoscut'), 'url': f"https://www.youtube.com/watch?v={url}" if len(str(url)) == 11 else url}
            
            guild_id = interaction.guild.id
            if guild_id not in queues: 
                queues[guild_id] = []
                
            queues[guild_id].append(song)
            
            if not vc.is_playing(): 
                await interaction.followup.send("⏳ Piesa se încarcă...")
                await play_next(interaction)
            else: 
                await interaction.followup.send(f'📝 La coadă: **{song["title"]}**')
                
    except Exception: 
        await interaction.followup.send("❌ Eroare la adăugarea piesei.")

@bot.tree.command(name='queue', description="Afișează coada de redare")
async def show_queue(interaction: discord.Interaction):
    q = queues.get(interaction.guild.id, [])
    if q: 
        await interaction.response.send_message(f"📜 **Coada de redare:**\n" + "\n".join([f"{i+1}. {s['title']}" for i, s in enumerate(q[:15])]) + (f"\n... și încă {len(q)-15} piese." if len(q) > 15 else ""))
    else: 
        await interaction.response.send_message("📭 Coada este goală.")

@bot.tree.command(name='pause', description="Pune melodia curentă pe pauză")
async def pause(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and vc.is_playing(): 
        vc.pause()
        await interaction.response.send_message("⏸️ Pauză.")
    else: 
        await interaction.response.send_message("❌ Nu se redă nicio melodie.")

@bot.tree.command(name='resume', description="Reia melodia")
async def resume(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and vc.is_paused(): 
        vc.resume()
        await interaction.response.send_message("▶️ Reluat.")
    else: 
        await interaction.response.send_message("❌ Muzica nu este pe pauză.")

@bot.tree.command(name='skip', description="Trece la următoarea melodie din coadă")
async def skip(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and vc.is_playing(): 
        vc.stop()
        await interaction.response.send_message("⏭️ Skip.")
    else: 
        await interaction.response.send_message("❌ Nu se redă nicio melodie.")

@bot.tree.command(name='stop', description="Oprește muzica și golește coada")
async def stop(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        queues[interaction.guild.id] = []
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("👋 Deconectat.")
    else: 
        await interaction.response.send_message("❌ Nu sunt conectat pe un canal vocal.")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN:
    bot.run(TOKEN)