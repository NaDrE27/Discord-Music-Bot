# 🎧 Discord Music Bot v1.0 by NaDrE27 🚀

This is a Discord music bot (version 1.0) built in Python, heavily optimized for **maximum performance** and **zero lag**. It uses an asynchronous playback system and massive RAM buffers to ensure perfect audio quality, regardless of network fluctuations.

## ✨ Main Features

* **Universal Link Support:** Plays music from YouTube, YouTube Music, short links (`youtu.be`), and plain text searches.
* **"API-Free" Spotify Integration:** Can play tracks directly from Spotify links using a smart scraping system (Discord OEmbed bypass), without requiring official Spotify API keys.
* **YouTube Playlists (Lazy Loading):** Supports long YouTube playlists. The first track starts instantly, while the rest of the playlist loads asynchronously in the background.
* **Asynchronous Engine (Non-Blocking):** The bot will never lose its connection ("Heartbeat blocked") while searching or downloading tracks.
* **Audio Rocket (Anti-Lag):** Configured with `FFmpeg` using multi-threading (2 cores) and a massive 200MB RAM buffer to completely eliminate stuttering. It natively downloads the `Opus` format to save the CPU from unnecessary conversions.
* **Queue System:** You can add dozens of tracks to the queue and view the list using built-in commands.

## 🛠️ Prerequisites

To run this bot on your local machine or server, you need:
1. **Python 3.10** or a newer version.
2. **Node.js** installed in the standard location (`C:\Program Files\nodejs`). This is used by `yt-dlp` to bypass YouTube's age restrictions and bot protections.
3. **FFmpeg**: The `ffmpeg.exe` executable must be downloaded and placed exactly in the same folder as the `main.py` file.

## ⚙️ Installation and Setup

**1. Clone this repository:**
git clone https://github.com/YourName/Discord-Music-Bot.git
cd Discord-Music-Bot

**2. Install required libraries:**
Run the following command in your terminal to install the Python dependencies:
pip install discord.py yt-dlp PyNaCl requests beautifulsoup4 python-dotenv

**3. Configure the Token (Security):**
* Create a new file in the project folder named `.env` (exactly like this, with a dot at the beginning).
* Open the `.env` file with any text editor and add your Discord bot token in this format:
DISCORD_TOKEN=your_secret_bot_token_here

*(Never share this token with anyone and do not upload it to GitHub!)*

## 🚀 Running the Bot

After installing the dependencies, placing `ffmpeg.exe` in the folder, and configuring the `.env` file, you can start the bot with a simple command:
python main.py

## 📜 Command List

The bot's prefix is `!`.

* `!play <track name or link>` - The bot joins your voice channel and plays the song. If a song is already playing, it gets added to the queue.
* `!skip` - Skips the current track and immediately plays the next one in the queue.
* `!queue` - Shows a list of the upcoming tracks.
* `!stop` - Clears the entire queue and disconnects the bot from the voice channel.

## ⚠️ Troubleshooting

* **"This version of %1 is not compatible..."**: You downloaded the wrong version of FFmpeg or renamed a `.zip` archive to `.exe`. Download the Windows FFmpeg archive, extract it, and grab *only* the `ffmpeg.exe` file from the `bin` folder.
* **JavaScript Error / YouTube Age Restriction**: Make sure you have Node.js installed on your PC and that you have restarted your system. The code will automatically inject the path to it.