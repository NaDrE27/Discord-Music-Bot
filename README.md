# Discord Music Bot v2.0 by NaDrE27 

Un bot de muzică pentru Discord dezvoltat în Python, optimizat pentru a reda piese și playlist-uri de pe YouTube și Spotify, folosind `yt-dlp` și `discord.py`.

## Funcționalități

* **Redare YouTube și Spotify:** Suportă link-uri directe, căutări după nume și link-uri de Spotify. Piesele și playlist-urile de pe Spotify sunt citite și căutate automat pe YouTube.
* **Suport Playlist-uri:** Încarcă instant prima piesă dintr-un playlist pentru o redare rapidă, adăugând restul pieselor (până la 100) în coadă, asincron.
* **Slash Commands:** Suport nativ pentru comenzile integrate Discord (`/`).
* **Sistem de Coadă (Queue):** Gestionează eficient lista de redare.

## Cerințe preliminare

* **Python 3.8** sau mai nou.
* **FFmpeg**: Trebuie să fie instalat pe sistem și adăugat în `PATH` sau fișierul `ffmpeg.exe` trebuie să fie plasat direct în folderul botului.
* **Node.js**: Opțional, dar recomandat pentru anumite extrageri din `yt-dlp`. Botul caută automat calea `C:\Program Files\nodejs`.

## Instalare

1. Clonează acest repository:
```bash
git clone [https://github.com/NaDrE27/Discord-Music-Bot.git](https://github.com/NaDrE27/Discord-Music-Bot.git)
cd Discord-Music-Bot
```

2. Instalează dependențele:
`pip install -r requirements.txt`

## ⚙️ Configurare `.env`

Botul folosește un fișier `.env` pentru a ascunde token-ul în siguranță.

1. Creează un fișier nou numit exact `.env` în folderul principal al proiectului.
2. Deschide fișierul și adaugă următoarea linie, înlocuind `tokenul_tau_aici` cu token-ul botului tău obținut de pe Discord Developer Portal:

```env
DISCORD_TOKEN=tokenul_tau_aici
```

## 🚀 Pornirea botului

Rulează scriptul principal din terminal sau linia de comandă:
```bash
python main.py
```

## 🎵 Comenzi disponibile

* `/play <link/nume>` - Redă o melodie sau un playlist de pe YouTube / Spotify.
* `/pause` - Pune melodia curentă pe pauză.
* `/resume` - Reia melodia pusă pe pauză.
* `/queue` - Afișează coada de redare.
* `/skip` - Trece la următoarea melodie din coadă.
* `/stop` - Oprește muzica, golește coada și deconectează botul.
* `/help` - Afișează meniul de ajutor.