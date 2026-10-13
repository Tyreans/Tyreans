import json
import re
from datetime import date
from pathlib import Path

# Rutas
root_dir = Path(__file__).resolve().parent.parent
readme_path = root_dir / "README.md"
songs_path = root_dir / "scripts" / "songs.json"

# Cargar canciones
with open(songs_path, "r", encoding="utf-8") as f:
    songs = json.load(f)

# Seleccionar canción determinista por día del año (cambia exactamente a medianoche)
day_of_year = date.today().timetuple().tm_yday
selected_song = songs[day_of_year % len(songs)]

title = selected_song["title"]
artist = selected_song["artist"]
url = selected_song["url"]
platform = selected_song.get("platform", "Music")

# Generar badge según la plataforma
badge_logo = "spotify" if "spotify" in platform.lower() else "youtube"
badge_color = "1DB954" if "spotify" in platform.lower() else "FF0000"

# Nuevo contenido entre etiquetas
new_block = f"""<!-- MUSIC:START -->
<p align="center">
  <a href="{url}" target="_blank">
    <img src="https://img.shields.io/badge/Listening_Today-{title.replace(' ', '_')}--_{artist.replace(' ', '_')}-{badge_color}?style=for-the-badge&logo={badge_logo}&logoColor=white" alt="{title} - {artist}" />
  </a>
  <br /><br />
  <a href="{url}" target="_blank">
    <img src="assets/1013(1).gif" alt="Daily Soundtrack" width="380" />
  </a>
  <br />
  <sub>🎧 <em>Click en el banner o título para escuchar en {platform}</em></sub>
</p>
<!-- MUSIC:END -->"""

# Leer README
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

# Reemplazar bloque
pattern = r"<!-- MUSIC:START -->.*?<!-- MUSIC:END -->"
updated_content = re.sub(pattern, new_block, content, flags=re.DOTALL)

# Guardar README
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(updated_content)

print(f"✅ README actualizado con: {title} - {artist}")