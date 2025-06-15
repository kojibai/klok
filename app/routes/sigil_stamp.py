from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image, ImageDraw, ImageFont
from uuid import uuid4
import requests
import io
import math
import os

router = APIRouter()

# Live harmonic Kairos source
KLOCK_API = "https://klock.kaiturah.com/kai"
IMG_SIZE = 1080
CENTER = IMG_SIZE // 2

# Chakra arc color encoding (outline)
def chakra_color_map(arc: str):
    arc = arc.strip().lower()
    return {
        "ignite": (255, 82, 82),       # Red
        "integrate": (255, 172, 51),   # Orange
        "harmonize": (255, 230, 0),    # Yellow
        "reflect": (102, 255, 204),    # Aqua
        "purify": (102, 153, 255),     # Blue
        "dream": (204, 153, 255)       # Violet
    }.get(arc, (200, 200, 200))

# Month background harmonics (canvas color)
def chakra_background(month: str):
    month = month.strip().lower()
    return {
        "aethon": (18, 2, 6),
        "virelai": (5, 15, 28),
        "solari": (20, 10, 2),
        "amarin": (2, 20, 14),
        "caelus": (4, 4, 25),
        "umbriel": (15, 6, 36),
        "noctura": (12, 0, 20),
        "liora": (0, 18, 18),
    }.get(month, (10, 8, 36))

# Pull latest Kairos harmonic state
def fetch_kairos_data():
    try:
        res = requests.get(KLOCK_API, timeout=5)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch Kai data: {e}")

@router.get("/sigil/stamp", response_class=StreamingResponse)
def generate_sigil_stamp():
    data = fetch_kairos_data()

    try:
        # Live field values
        pulse = data["kaiPulseEternal"]
        kairos = data["chakraStepString"]
        beat = data["eternalChakraBeat"]["beatIndex"]
        step = data["chakraStep"]["stepIndex"]
        day = data["harmonicDay"].upper()
        arc = data["eternalChakraArc"].upper()
        month = data["eternalMonth"]
        year = data["eternalYearName"]
        spiral = data["phiSpiralLevel"]
        week = data["weekName"].upper()

        # Initialize image
        img = Image.new("RGBA", (IMG_SIZE, IMG_SIZE), chakra_background(month))
        draw = ImageDraw.Draw(img)

        # Load fallback default font
        font_main = ImageFont.load_default()

        # Sacred triquetra geometry
        for i in range(3):
            angle = i * 120
            x = CENTER + math.cos(math.radians(angle)) * 160
            y = CENTER + math.sin(math.radians(angle)) * 160
            draw.ellipse([(x - 100, y - 100), (x + 100, y + 100)],
                         outline=chakra_color_map(arc), width=4)

        # Central resonance vortex
        draw.ellipse([(CENTER - 40, CENTER - 40), (CENTER + 40, CENTER + 40)],
                     outline=(255, 255, 255), width=3)

        # Step ticks (radial)
        for i in range(44):
            angle = (360 / 44) * i
            rad = math.radians(angle)
            x1 = CENTER + 190 * math.cos(rad)
            y1 = CENTER + 210 * math.sin(rad)
            draw.line((CENTER + 190 * math.cos(rad), CENTER + 190 * math.sin(rad), x1, y1),
                      fill=(180, 180, 180), width=2)

        # Top metadata
        draw.text((CENTER, 60), f"{day} • KAIROS {kairos} • ARC: {arc}",
                  fill=(135, 206, 250), anchor="mm", font=font_main)

        # Central pulse
        draw.text((CENTER, CENTER - 20), "ETERNAL PULSE", fill=(255, 255, 255),
                  anchor="mm", font=font_main)
        draw.text((CENTER, CENTER + 10), str(pulse), fill=(255, 255, 255),
                  anchor="mm", font=font_main)

        # Middle title
        draw.text((CENTER, CENTER + 60), f"{year} ∴ PHI SPIRAL {spiral}",
                  fill=(173, 216, 230), anchor="mm", font=font_main)

        # Footer harmonic line
        draw.text((CENTER, IMG_SIZE - 60),
                  f"{month.upper()} • BEAT {beat}/36 • STEP {step}/44 • {week}",
                  fill=(135, 206, 250), anchor="mm", font=font_main)

        # Convert to stream
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        return StreamingResponse(buffer, media_type="image/png", headers={
            "Content-Disposition": f"attachment; filename=eternal_stamp_{pulse}.png"
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating eternal stamp: {e}")
