# 🎵 Guía: Configurar Música Diaria Automática con GitHub Actions

Esta guía te explica paso a paso cómo hacer que tu perfil de GitHub actualice automáticamente todos los días una canción recomendada (con enlace a Spotify, YouTube, etc.) junto con tu GIF, usando **GitHub Actions (100% gratuito)**.

---

## 🎧 1. Plataformas que puedes usar

Puedes enlazar cualquier plataforma que proporcione URLs públicas a canciones:

| Plataforma | Ventajas | Tipo de Enlace |
| :--- | :--- | :--- |
| **Spotify** *(Recomendada)* | Muy popular, abre la app directamente en móviles y web player en desktop. | `https://open.spotify.com/track/{ID}` |
| **YouTube / YT Music** | Accesible para todos sin necesidad de cuenta activa. | `https://youtu.be/{ID}` o `https://music.youtube.com/watch?v={ID}` |
| **SoundCloud** | Ideal para remixes, lo-fi, podcasts y música indie. | `https://soundcloud.com/{artista}/{track}` |
| **Apple Music** | Enlaces limpios con reproductor web integrado. | `https://music.apple.com/us/album/{id}?i={track_id}` |

---

## 🚀 2. Enfoque recomendado: Lista Curada (`songs.json`) + Action diaria

Este método es el más confiable y no requiere registrar tarjetas ni configurar APIs complicadas. Tú defines una lista de tus canciones favoritas y GitHub Actions selecciona una diferente cada día.

### Estructura de archivos:
```text
Tyreans/
├── .github/
│   └── workflows/
│       └── daily-music.yml      <-- Workflow de GitHub Actions
├── scripts/
│   ├── songs.json               <-- Tu lista de canciones
│   └── update_music.py          <-- Script que actualiza el README
├── assets/
│   └── 1013(1).gif              <-- Tu GIF
└── README.md
```

---

## 🛠️ 3. Paso a Paso

### Paso 1: Crear la lista de canciones (`scripts/songs.json`)
Crea una carpeta `scripts/` y dentro el archivo `songs.json` con tus temas favoritos:

```json
[
  {
    "title": "Resonance",
    "artist": "HOME",
    "genre": "Synthwave / Chill",
    "url": "https://open.spotify.com/track/1Tu2r6gEuhLwQz209s1eT2",
    "platform": "Spotify"
  },
  {
    "title": "After Dark",
    "artist": "Mr.Kitty",
    "genre": "Darkwave",
    "url": "https://open.spotify.com/track/2LKOHdZ0jF9KiOP49V7PR8",
    "platform": "Spotify"
  },
  {
    "title": "Space Song",
    "artist": "Beach House",
    "genre": "Dream Pop",
    "url": "https://open.spotify.com/track/7H0ya83CMmgFcOhw0UB6ow",
    "platform": "Spotify"
  },
  {
    "title": "Sunflower",
    "artist": "Post Malone & Swae Lee",
    "genre": "Hip-Hop / Pop",
    "url": "https://open.spotify.com/track/3KkXRQHbMCARz0aVfEt68P",
    "platform": "Spotify"
  }
]
```

---

### Paso 2: Crear el script actualizador (`scripts/update_music.py`)
Crea el script en Python que leerá la fecha del día, elegirá una canción y reemplazará el bloque en `README.md`:

```python
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
```

---

### Paso 3: Crear el Workflow de GitHub Actions (`.github/workflows/daily-music.yml`)
Crea `.github/workflows/daily-music.yml`:

```yaml
name: Update Daily Soundtrack

on:
  schedule:
    # Se ejecuta todos los días a las 06:00 UTC (00:00 hora central México)
    - cron: '0 6 * * *'
  workflow_dispatch: # Permite ejecutarlo manualmente desde la pestaña "Actions"

permissions:
  contents: write # Permiso para hacer commit y push al repositorio

jobs:
  update-soundtrack:
    runs-on: ubuntu-latest

    steps:
      - name: 📥 Clonar repositorio
        uses: actions/checkout@v4

      - name: 🐍 Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: 🎵 Ejecutar script de actualización
        run: python scripts/update_music.py

      - name: 💾 Guardar cambios si hubo novedades
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add README.md
          if git diff --staged --quiet; then
            echo "No hay cambios para commitear."
          else
            git commit -m "chore(music): update daily soundtrack"
            git push
          fi
```

---

### Paso 4: Dar permisos de escritura en GitHub (Importante)
Para que el bot de GitHub Actions pueda actualizar tu `README.md`:
1. Ve a tu repositorio en GitHub: `https://github.com/Tyreans/Tyreans`
2. Ve a **Settings** > **Actions** > **General**.
3. Baja hasta **Workflow permissions**.
4. Selecciona **Read and write permissions**.
5. Marca la casilla **Allow GitHub Actions to create and approve pull requests** (opcional pero recomendada).
6. Haz clic en **Save**.

---

## 🎯 4. Probar que funciona
1. Haz commit y push de estos nuevos archivos a `main`.
2. Ve a la pestaña **Actions** en tu repositorio en GitHub.
3. En la barra lateral izquierda, selecciona **Update Daily Soundtrack**.
4. Haz clic en **Run workflow** > botón verde **Run workflow**.
5. Espera unos segundos y recarga tu perfil: verás el badge y enlace actualizado con la canción correspondiente al día.
