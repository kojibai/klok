from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from uuid import uuid4
from PIL import Image, ImageDraw, ImageFont
import requests
import io
import math
import os

router = APIRouter()

# Constants
KLOCK_API = "https://klock.kaiturah.com/kai"
IMG_SIZE = 1080
CENTER = IMG_SIZE // 2
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(BASE_DIR, "../assets/DejaVuSans-Bold.ttf")  # Adjust if needed

def fetch_kairos_data():
    try:
        resp = requests.get(KLOCK_API, timeout=6)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch Kairos data: {e}")

@router.get("/sigil")
def generate_sigil():
    data = fetch_kairos_data()

    try:
        # 🌐 Real fields from your JSON
        pulse        = data["kaiPulseEternal"]
        eternal_seal = data["eternalSeal"]
        kairos       = data["chakraStepString"]       # e.g. "3:38"
        day_name     = data["harmonicDay"].upper()    # e.g. "SONARI"
        month_name   = data["eternalMonth"].upper()   # e.g. "AETHON"
        arc_name     = data["eternalChakraArc"].upper()  # e.g. "IGNITE"
        week_name    = data["weekName"].upper()       # e.g. "CROWNED LIGHT"
        year_name    = data["eternalYearName"].upper() # e.g. "YEAR OF HARMONIC EMBODIMENT"
        spiral       = data["phiSpiralLevel"]
        beat_idx     = data["eternalChakraBeat"]["beatIndex"]
        step_idx     = data["chakraStep"]["stepIndex"]

        # 🌀 Text blocks
        meta_top    = f"{day_name} • KAIROS {kairos} • ARC: {arc_name}"
        meta_bottom = f"{month_name} • BEAT {beat_idx}/36 • STEP {step_idx}/44 • {week_name}"
        center_text = f"ETERNAL PULSE\n{pulse}"
        inner_title = f"{year_name} ∴ PHI SPIRAL {spiral}"

        # 🎨 Create image
        img = Image.new("RGBA", (IMG_SIZE, IMG_SIZE), (8, 12, 32))
        draw = ImageDraw.Draw(img)

        # 🖋 Font
        try:
            font_large = ImageFont.truetype(FONT_PATH, 60)
            font_small = ImageFont.truetype(FONT_PATH, 34)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # 🌟 Sacred Triquetra
        for angle in [0, 120, 240]:
            x = CENTER + 180 * math.cos(math.radians(angle))
            y = CENTER + 180 * math.sin(math.radians(angle))
            draw.ellipse([(x - 80, y - 80), (x + 80, y + 80)], outline=(255, 255, 0), width=4)

        # ✨ Center Pulse
        draw.multiline_text((CENTER, CENTER - 100), center_text, fill=(255, 255, 255), font=font_large, anchor="mm", spacing=12)

        # 💠 Inner Spiral Year
        draw.text((CENTER, CENTER + 110), inner_title, fill=(173, 216, 230), font=font_small, anchor="mm")

        # 🧭 Top + Bottom Metadata
        draw.text((CENTER, 70), meta_top, fill=(135, 206, 250), font=font_small, anchor="mm")
        draw.text((CENTER, IMG_SIZE - 70), meta_bottom, fill=(135, 206, 250), font=font_small, anchor="mm")

        # 📜 Eternal Seal (small)
        draw.text((CENTER, IMG_SIZE - 30), eternal_seal, fill=(220, 220, 220), font=font_small, anchor="mm")

        # 📤 Send as file download
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        filename = f"eternal_sigil_{pulse}.png"
        return StreamingResponse(buffer, media_type="image/png", headers={
            "Content-Disposition": f"attachment; filename={filename}"
        })

    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Missing Kairos field: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating sigil: {e}")
