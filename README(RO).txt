# 🎧 Discord Music Bot v1.0 by NaDrE27 🚀

Acesta este un bot de muzică pentru Discord (versiunea 1.0), construit în Python, optimizat extrem pentru performanță maximă și zero lag. Folosește un sistem asincron de redare și buffere uriașe în RAM pentru a asigura o audiție perfectă, indiferent de fluctuațiile de rețea.

## ✨ Funcționalități Principale

* **Suport Universal pentru Link-uri:** Redă muzică de pe YouTube, YouTube Music, link-uri scurte (`youtu.be`) și căutări text.
* **Integrare Spotify "API-Free":** Poate reda piese direct din link-uri de Spotify folosind un sistem inteligent de scraping (Discord OEmbed bypass), fără a necesita chei API oficiale de la Spotify.
* **YouTube Playlists (Lazy Loading):** Suportă playlist-uri lungi de pe YouTube. Prima piesă pornește instant, în timp ce restul playlist-ului se încarcă asincron în fundal.
* **Motor Asincron (Non-Blocking):** Botul nu își va pierde niciodată conexiunea ("Heartbeat blocked") în timp ce caută sau descarcă piese.
* **Rachetă Audio (Anti-Lag):** Configurat cu `FFmpeg` folosind multi-threading (2 nuclee) și un buffer RAM uriaș de 200MB pentru a elimina complet sacadarea (stuttering). Descarcă nativ formatul `Opus` pentru a scuti procesorul de conversii inutile.
* **Sistem de Coadă (Queue):** Poți adăuga zeci de piese în așteptare și poți vedea lista folosind comenzile integrate.

## 🛠️ Cerințe Preliminare (Prerequisites)

Pentru a rula acest bot pe calculatorul sau serverul tău, ai nevoie de:
1. **Python 3.10** sau o versiune mai nouă.
2. **Node.js** instalat în locația standard (`C:\Program Files\nodejs`). Este folosit de `yt-dlp` pentru a ocoli restricțiile YouTube.
3. **FFmpeg**: Executabilul `ffmpeg.exe` trebuie să fie descărcat și plasat exact în același folder cu fișierul `main.py`.

## ⚙️ Instalare și Configurare

**1. Clonează acest repository:**
git clone https://github.com/NumeleTau/Discord-Music-Bot.git
cd Discord-Music-Bot

**2. Instalează librăriile necesare:**
Rulează următoarea comandă în terminal pentru a instala dependențele Python:
pip install discord.py yt-dlp PyNaCl requests beautifulsoup4 python-dotenv

**3. Configurează Token-ul (Securitate):**
* Creează un fișier nou în folderul proiectului numit `.env` (exact așa, cu punct în față).
* Deschide fișierul `.env` cu orice editor de text și adaugă token-ul botului tău de Discord în acest format:
DISCORD_TOKEN=pune_aici_token_ul_tau_secret

*(Nu oferi niciodată acest token altor persoane și nu îl urca pe GitHub!)*

## 🚀 Pornirea Botului

După ce ai instalat dependențele, ai pus `ffmpeg.exe` în folder și ai configurat fișierul `.env`, poți porni botul cu o simplă comandă:
python main.py

## 📜 Lista de Comenzi

Prefixul botului este `!`.

* `!play <nume piesă sau link>` - Botul intră pe canalul tău de voce și redă melodia. Dacă deja cântă ceva, o adaugă în coadă.
* `!skip` - Sare peste piesa curentă și trece imediat la următoarea din coadă.
* `!queue` - Îți arată o listă cu următoarele piese care urmează să cânte.
* `!stop` - Șterge toată coada de așteptare și deconectează botul de pe canalul de voce.

## ⚠️ Posibile Erori (Troubleshooting)

* **"This version of %1 is not compatible..."**: Ai descărcat versiunea greșită de FFmpeg sau ai redenumit o arhivă `.zip` în `.exe`. Descarcă arhiva FFmpeg pentru Windows, extrage-o și ia doar fișierul `ffmpeg.exe` din folderul `bin`.
* **Eroare JavaScript / Age Restriction pe YouTube**: Asigură-te că ai instalat Node.js pe PC și ai dat restart. Codul va injecta automat calea către el.