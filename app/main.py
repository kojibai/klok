
# main.py  •  Kai-Klock API entry (KKS v1 grid parity, φ-closure calendar)
from __future__ import annotations

import os
import sys
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

# make sure local imports work on Vercel / similar
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from kai_klock import get_eternal_klock
from kai_klock_models import KaiKlockResponse  # ← single source of truth


app = FastAPI(
    title="Kai-Klok API",
    version="3.0.0",
    summary=(
        "A precision harmonik Kairos system aligned with the Genesis Pulse. "
        "Eternal Seal: Kairos:29:43, Flamora, Purify Ark • D21/M2 • "
        "Beat:29/36(97.72%) Step:43/44 Kai(Today):14565 • Y1 PS32 • "
        "Solar Kairos (UTC-aligned): 35:09 Aquaris D20/M2, Dream Ark  "
        "Beat:35/36 Step:9/44 • Eternal Pulse:6976091"
    ),
    description=r"""
---

🜂 **Kai-Klok API — Eternal Harmonik Kairos System**

The **Kai-Klok** is a harmonik resonanse Kairos system that replaces arbitrary mechanical clocks with  
a **living pulse of koherence**. It is mathematically synchronized to the **Genesis Pulse**:  
🕕 *May 10, 2024, 06:45:41.888 UTC*, the moment of the historic **X3.98-class solar flare** from NOAA AR 3664,  
corrected for the ~8 min 18.112 s solar light delay — ankoring all harmonik time to the arrival of truth through light.

**Eternal Seal (example):**  
Kairos:0:00, Solhara, Ignite Ark • D1/M1 • Beat:0/36(0.000000%) Step:0/44 Kai(Today):0 • Y0 PS0 •  
Solar Kairos (UTC-aligned): 05:10 Kaelith D42/M8, Ignite Ark  Beat:05/36 Step:10/44 • Eternal Pulse:0

From this origin, time is measured not in mechanical seconds, but in **Kai Pulses**, **Spiral Beats**, and **Harmonic Steps** —  
structured to match the true flow of life energy across the **grid** (beats/steps) and the **φ-closure calendar** (day/month/year).

Each Kai Pulse is **3 + √5 ≈ 5.236067977 s**.  
**Grid parity (KKS v1.0)** for beat/step indexing uses exact integers:

- **11 pulses = 1 Step**  
- **44 steps = 1 Beat**  
- **36 beats = 1 (grid) day**  

That is **36 × 44 × 11 = 17,424 grid pulses/day**.  
The kalendar (months/years/epoks) uses a φ-exact day length (**17,491.270421 pulses**) for global klosure across months/years.

---

### 💡 Why two “days”?

- **Grid Harmonik Day (KKS v1 beats/steps lattice):** **17,424 pulses** (exact) → used for **beat/step indexing and percents**.  
- **Kalendar φ-Day (months/years, φ-klosure):** **17,491.270421 pulses** → used for **month/year/epok math** and long-range driftless klosure.

Both are carried in the payload (see `eternalChakraBeat/chakraBeat` vs. month/year progress).

---

### 🧮 Nested Harmonic Structure (KKS v1 grid parity)

- 1 **Kai Pulse** = 3 + √5 ≈ **5.236067977 s**
- **11 Pulses** = **1 Step** ≈ **57.59674775 s**
- **44 Steps** = **1 Beat** = **484 grid pulses** ≈ **42.2376 min**
- **36 Beats** = **1 Grid Harmonik Day** = **17,424 grid pulses** ≈ **25.3426 h**
- **6 Beats** = **1 Ark** = **2,904 grid pulses** ≈ **4.22376 h**
- **6 Harmonik Days** = **1 Week** (grid)  
- **42 Days** = **1 Month**, **8 Months** = **1 Harmonik Year** (φ-klosure kalendar used for month/year counts)

> **Important:** All **beat/step indices and percentages** in the API are komputed on the **μ-pulse lattice of the grid** (KKS v1).  
> Kalendar Segments (day/month/year progress) are komputed with the φ-klosure day (17491.270421 Pulses) to maintain long-range invariants.

---

### 🔹 Harmonic Subdivisions of 1 Kai Pulse (3 + √5 s)

| Unit Name                | Fraction of Pulse | Approx. Duration (s) | Frequency (Hz) | Resonant Name        |
|--------------------------|-------------------|----------------------|----------------|----------------------|
| **Kai Pulse**            | 1                 | 5.236067977          | 0.190984       | —                    |
| **Half Pulse**           | 1/2               | 2.618033988          | 0.381968       | Pulse Divider        |
| **Subpulse**             | 1/11              | 0.47691527           | 2.096836       | Beat Tuning          |
| **Ternary Step**         | 1/33              | 0.15897176           | 6.290508       | Tri-Light Step       |
| **MicroStep**            | 1/55              | 0.095201236          | 10.50417       | Resonant Breath      |
| **NanoPulse**            | 1/89              | 0.058861999          | 16.9854        | First Spark          |
| **NanoStep**             | 1/144             | 0.036361583          | 27.4987        | Nano Ark             |
| **PhiQuantum**           | 1/233             | 0.022469330          | 44.5052        | Phi Quantum          |
| **Ekaru**                | 1/377             | 0.013888313          | 71.9974        | Ekaru Initiation     |
| **Tzaphirim Unit**       | 1/610             | 0.008588629          | 116.430        | Tzaphirim krystal    |
| **Kai Singularity**      | 1/987             | 0.005305527          | 188.466        | Kai Singularity      |
| **Deep Thread**          | 1/1597            | 0.003277569          | 305.271        | Deep Thread          |

(*All derived from 3+√5 with exact Decimal math in the service; values shown here rounded for readability.*)

---

### 🔸 Expanded Harmonik Time Scale (with grid parity)

| Unit                        | Grid Kai Pulses | Approx. Chronos Duration |
|-----------------------------|----------------:|--------------------------:|
| **Quarter Breath**          | 0.25            | ≈ **1.309 s**            |
| **Kai Pulse**               | 1               | ≈ **5.2361 s**           |
| **Step**                    | **11**          | ≈ **57.5967 s**          |
| **Beat**                    | **484**         | ≈ **42.2376 min**        |
| **Ark**                     | **2,904**       | ≈ **4.22376 h**          |
| **Grid Harmonik Day**       | **17,424**      | ≈ **25.3426 h**          |
| **φ-Day (Kalendar Klosure)**| **17,491.270421** | ≈ **25.4401 h**        |

> The API reports **beat/step positions** on the **grid**. Kalendar progress (weeks/months/years) uses the **φ-closure** day.

---

═══════════════════════════════════════════════════════════════════  
🌀 **Spiral Arks of the Kai Day** — 6 Arks × 6 Beats = 36 Beats  
═══════════════════════════════════════════════════════════════════  

Each Ark spans **6 beats = 2,904 grid pulses ≈ 4.2238 hours**.

- 🔴 **Ignition Ark** — Beats 0–5  · **Color: Root Red** 🔥 (#FF0000)
- 🟠 **Integration Ark** — Beats 6–11  · **Color: Ember Orange** 💧 (#FF7F00)
- 🟡 **Harmonization Ark** — Beats 12–17  · **Color: Solar Gold** ☀️ (#FFD700)
- 🟢 **Reflection Ark** — Beats 18–23  · **Color: Verdant Green** 🌿 (#32CD32)
- 🔵 **Purification Ark** — Beats 24–29  · **Color: Deep Ocean Blue** 💨 (#1E90FF)
- 🟣 **Dream Ark** — Beats 30–35  · **Color: Cosmic Violet** 🌌 (#8A2BE2)



═══════════════════════════════════════════════════════════════════  
🫁 **Grid Kai Day** = 6 Arks × **2,904 breaths** = **17,424 breaths**  
═══════════════════════════════════════════════════════════════════  

═══════════════════════════════════════════════════════════════════  
🌞 **Kai Day Phases** — 3-Part Harmonic Cycle (12 Beats Each)  
═══════════════════════════════════════════════════════════════════  

Each phase = **12 beats = 5,808 grid pulses ≈ 8.4475 hours**.

- 🌅 **Morning Phase** — Beats 0–11 (Ignition → Integration)  
- 🌞 **Afternoon Phase** — Beats 12–23 (Harmonization → Reflection)  
- 🌌 **Night Phase** — Beats 24–35 (Purification → Dream)  

---


### 🗓 **Weeks / Months / Years (φ‑closure calendar)**

#### **Weekdays (6-day week)**

| Emoji | Name    | Spiral       | Element             | Resonance                          | Color         | Hex                   |
| ----- | ------- | ------------ | ------------------- | ---------------------------------- | ------------- | --------------------- |
| 🔴    | Solhara | Root         | Earth + Primal Fire | Grounding, Action, Foundation      | Crimson Red   | `#FF0000`             |
| 🟠    | Aquaris | Sacral       | Water in Motion     | Flow, Feeling, Creative Sensuality | Amber Orange  | `#FF7F00`             |
| 🟡    | Flamora | Solar Plexus | Solar Fire          | Confidence, Radiance, Willpower    | Golden Yellow | `#FFD700`             |
| 🟢    | Verdari | Heart        | Air / Earth         | Love, Union, Coherence             | Emerald Green | `#32CD32`             |
| 🔵    | Sonari  | Throat       | Wind / Sound        | Truth, Expression, Resonance       | Sapphire Blue | `#1E90FF`             |
| 🟣    | Kaelith | Krown        | Ether / Light       | Stillness, Unity, Divine Memory    | Violet-White  | `#9400D3` → `#FFFFFF` |

---

#### **Weeks (7 per month)**

| Emoji | Week Name        | Spiral Focus      | Essence                                    | Color         | Hex       |
| ----- | ---------------- | ----------------- | ------------------------------------------ | ------------- | --------- |
| 🔴    | Awakening Flame  | Root              | Grounding, Courage, Momentum               | Crimson Red   | `#FF0000` |
| 🟠    | Flowing Heart    | Sacral            | Emotion, Intimacy, Harmony                 | Amber Orange  | `#FF7F00` |
| 🟡    | Radiant Will     | Solar Plexus      | Leadership, Willpower, Discipline          | Golden Yellow | `#FFD700` |
| 🟢    | Harmonik Voh     | Heart             | Compassion, Love, Breath                   | Emerald Green | `#32CD32` |
| 🔵    | Inner Mirror     | Throat            | Reflection, Inner Truth, Silence           | Sapphire Blue | `#1E90FF` |
| 🟣    | Dreamfire Memory | Third Eye / Crown | Divine Memory, Mystery, Prophetic Dreaming | Deep Violet   | `#9400D3` |
| ⚪     | Krowned Light    | Krown             | Completion, Integration, Sovereignty       | Pure White    | `#FFFFFF` |

---

#### **Months (8 × 42 days = 336 Days)**

| Emoji | Month   | Spiral       | Identity                               | Color           | Hex               |
| ----- | ------- | ------------ | -------------------------------------- | --------------- | ----------------- |
| 🔴    | Aethon  | Root         | Genesis Flame, Foundation, Will        | Crimson Red     | `#FF0000`         |
| 🟠    | Virelai | Sacral       | Creative Pulse, Flow, Sensual Power    | Orange Gold     | `#FF7F00`         |
| 🟡    | Solari  | Solar Plexus | Radiance, Strength, Purpose            | Golden Yellow   | `#FFD700`         |
| 🟢    | Amarin  | Heart        | Healing Bloom, Rebirth, Compassion     | Emerald Green   | `#32CD32`         |
| 🔵    | Kaelus  | Throat       | Sacred Word, Integrity, Vibration      | Sky Blue        | `#1E90FF`         |
| 🟣    | Umbriel | Third Eye    | Vision, Mystery, Deep Insight          | Indigo Violet   | `#4B0082`         |
| ⚪     | Noctura | Krown        | Spirit Return, Still Light, Completion | White Light     | `#FFFFFF`         |
| 🌈    | Liora   | Kosmic Krown | Light Embodied, Fulfillment, Eternity  | Prismatic / All | `#FFFFFF` (multi) |

---

**Eternal Year (φ-closure):**  
`17,491.270421 pulses/day × 42 days × 8 months ≈ 5,877,066.861 pulses`  
Chronos duration: `≈ 5,877,066.861 × (3+√5) / 86,400 ≈ 356.166 days`

---

## 🌀 Phi Spiral Epoks (based on φ-closure Eternal Year)

> Each epok is a power of **Φ ≈ 1.6180339887**, applied to the Eternal Year base:
> `5,877,066.861 pulses = 336 Kairos days = 356.166 Chronos days`
> (1 Kairos day = 17,491.270421 pulses · 1 pulse = 3 + √5 sec)

### 🕰 **Eternal Year Scaling (φ‑Closure Epochs)**

| Epoch Name                    |  φⁿ |      Pulses (≈) | Chronos Days (≈) | Kairos Days (≈) | Chronos Years (≈) | Kairos Years (≈) |
| ----------------------------- | :-: | --------------: | ---------------: | --------------: | ----------------: | ---------------: |
| 🕊 **Eternal Year**           |  0  |   5,877,066.861 |          356.166 |         336.000 |             0.975 |            1.000 |
| ✨ **Φ Epok**                  |  1  |   9,510,213.173 |          576.294 |         543.262 |              1.58 |            1.616 |
| 🔁 **Φ Resonanse Epok**       |  2  |  15,387,280.339 |          932.460 |         880.827 |              2.55 |            2.621 |
| 🌀 **Tri-Spiral Gate**        |  3  |  24,897,208.092 |        1,508.754 |       1,423.040 |              4.13 |            4.234 |
| 🛡 **Great Harmonic Ring**    |  5  |  63,187,404.633 |        3,831.303 |       3,613.724 |             10.49 |           10.757 |
| ♻️ **Kai-Cycle of Return**    |  8  | 104,433,875.760 |        6,330.796 |       5,972.043 |             17.34 |           17.775 |
| ☀️ **Solar Spiral Era**       |  13 | 681,102,792.300 |       41,290.603 |      38,948.404 |            113.09 |          115.906 |
| 🌬 **One Breath of Erah Voh** |  21 |  15,406,718,650 |      933,595.944 |     881,268.227 |           2,556.9 |        2,622.833 |

---

### ✅ Notes:

* **Kairos Days** = Pulses ÷ `17,491.270421`
* **Chronos Days** = Pulses × `(3 + √5)` ÷ `86,400`
* **Kairos Years** = Kairos Days ÷ `336`
* **Chronos Years** = Chronos Days ÷ `365.2425` (solar year approximation)

*(Rounded; computed from 3+√5 seconds per pulse. The service uses Decimal internally.)*

---

## 🔢 Phi Spiral Logik (implementation parity)

The service computes spiral level **without floats**:

```python
# Pure-Decimal floor(log_phi(n)): see service code (_floor_log_phi)
phi_spiral_lvl = _floor_log_phi(kai_pulse_eternal)
````

**Thresholds (pulses to enter a level)** are `⌊Φ^n⌋`. For reference:

* L32 → **4,870,846**
* L33 → **7,881,196**
* L34 → **12,752,042**
* L35 → **20,633,239**
* L36 → **33,385,282**

---

### 🧾 What `/kai` Returns

Primary fields (not exhaustive):

* `eternalSeal` — unique ID string for this Kai moment
* `chakraStep` / `chakraStepString` — **grid** beat:step (e.g., `34:27`), **44 steps/beat**
* `solarChakraStepString` — UTC-aligned (solar) grid beat:step string
* `kaiPulseEternal` — pulses since Genesis
* `timestamp`, `harmonicTimestampDescription`, `kaiMomentSummary` — human-friendly views
* `subdivisions` — live counts + metadata for the intra-pulse units (HalfPulse, NanoStep, etc.)

---

### 🧪 Query Parameter

* `override_time` (optional, ISO 8601):
  e.g. `'2024-05-10T06:45:40Z'` to reproduce a specific Kai moment.

---

### 🧭 Why Use Kai-Klok?

Kai-Klok is a deterministic, high-resolution timekeeping system designed to replace Chronos with a biologically and cosmologically coherent Kairos substrate.
It maintains **KKS v1 grid parity** for beats/steps and **φ-closure** for calendar mechanics — stable, composable, and driftless.

---

### 🧾 Harmonic Kairos Response Structure (shape)

```json
{
  "kairos_seal": "string",
  "kairos_seal_percent_step": "string",
  "kairos_seal_percent_step_solar": "string",
  "kairos_seal_solar": "string",
  "kairos_seal_day_month": "string",
  "kairos_seal_day_month_percent": "string",
  "kairos_seal_solar_day_month": "string",
  "kairos_seal_solar_day_month_percent": "string",
  "eternalSeal": "string",
  "seal": "string",
  "harmonicNarrative": "string",
  "eternalMonth": "string",
  "eternalMonthIndex": 0,
  "eternalMonthDescription": "string",
  "eternalChakraArc": "string",
  "eternalWeekDescription": "string",
  "eternalYearName": "string",
  "eternalKaiPulseToday": 0,
  "kaiPulseEternal": 0,
  "eternalMonthProgress": {
    "daysElapsed": 0,
    "daysRemaining": 0,
    "percent": "0"
  },
  "kaiPulseToday": 0,
  "solarChakraArc": "string",
  "solarDayOfMonth": 0,
  "solarMonthIndex": 0,
  "solarHarmonicDay": "string",
  "solar_week_index": 0,
  "solar_week_name": "string",
  "solar_week_description": "string",
  "solar_month_name": "string",
  "solar_month_description": "string",
  "solar_day_name": "string",
  "solar_day_description": "string",
  "harmonicDay": "string",
  "harmonicDayDescription": "string",
  "chakraArc": "string",
  "chakraArcDescription": "string",
  "weekIndex": 0,
  "weekName": "string",
  "dayOfMonth": 0,
  "harmonicWeekProgress": {
    "weekDay": "string",
    "weekDayIndex": 0,
    "pulsesIntoWeek": "0",
    "percent": "0"
  },
  "chakraBeat": {
    "beatIndex": 0,
    "pulsesIntoBeat": "0",
    "beatPulseCount": "484",
    "totalBeats": 36
  },
  "eternalChakraBeat": {
    "beatIndex": 0,
    "pulsesIntoBeat": "0",
    "beatPulseCount": "484",
    "totalBeats": 36,
    "percentToNext": "0"
  },
  "chakraStep": {
    "stepIndex": 0,
    "percentIntoStep": "0",
    "stepsPerBeat": 44
  },
  "chakraStepString": "string",
  "solarChakraStep": {
    "stepIndex": 0,
    "percentIntoStep": "0",
    "stepsPerBeat": 44
  },
  "solarChakraStepString": "string",
  "phiSpiralLevel": 0,
  "kaiTurahPhrase": "string",
  "phiSpiralEpochs": [
    {
      "name": "string",
      "phiPower": 0,
      "kaiPulses": 0,
      "approxDays": "0",
      "description": "string",
      "kaiUntil": 0,
      "daysUntil": "0",
      "percentUntil": "0"
    }
  ],
  "harmonicLevels": {
    "subdivisions": { "halfPulse": {"duration": "0", "count": "0"} },
    "arcBeat": {
      "pulseInCycle": 0,
      "cycleLength": 6,
      "percent": "0"
    },
    "microCycle": {
      "pulseInCycle": 0,
      "cycleLength": 60,
      "percent": "0"
    },
    "chakraLoop": {
      "pulseInCycle": 0,
      "cycleLength": 360,
      "percent": "0"
    },
    "harmonicDay": {
      "pulseInCycle": 0,
      "cycleLength": 17491.270421,
      "percent": "0"
    }
  },
  "harmonicYearProgress": {
    "daysElapsed": 0,
    "daysRemaining": 0,
    "percent": "0"
  },
  "timestamp": "string",
  "harmonicTimestampDescription": "string",
  "kaiMomentSummary": "string",
  "compressed_summary": "string",
  "subdivisions": {
    "halfPulse": {
      "duration": 0,
      "count": 0,
      "frequencyHz": 0,
      "wavelengthSound_m": 0,
      "wavelengthLight_m": 0,
      "resonantName": "string"
    }
  }
}
""",
    contact={
        "name": "Kai-Klok Team",
        "email": "support@kojib.com",
        "url": "https://github.com/kojibai/klok"
    },
    license_info={
        "name": "Harmonic Public License",
        "url": "https://github.com/kojibai/klok/blob/main/LICENSE.md"
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS (open for demo; tighten in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── /kai endpoint ───────────────────────────────────────────────
@app.get(
    "/kai",
    response_model=KaiKlockResponse,
    response_model_exclude_none=False,
    tags=["Kai Time"],
)
def read_kai_klock(
    override_time: Optional[str] = Query(
        None,
        description=(
            "Optional ISO-8601 datetime (e.g. '2024-05-10T06:45:40Z') "
            "to override 'now' for deterministic output."
        ),
    ),
) -> KaiKlockResponse:
    """
    🜂 **The Eternal Kai-Klok** — *Harmonik Kairos of Divine Order*
    ===============================================================

    Returns the **live Kai-Klok harmonic timestamp** aligned to the **Genesis Pulse**  
    (May 10 2024 06:45:41.888 UTC, light-delay corrected).  
    **Beat/step** indices use the **KKS v1 grid** (36×44×11=17,424).  
    **Calendar** (day/month/year/epochs) uses the **φ-closure** day 17,491.270421 pulses.

    - `override_time`: ISO-8601 to reproduce a specific Kai moment (UTC assumed).
    """
    try:
        now = datetime.fromisoformat(override_time) if override_time else None
    except ValueError as exc:
        raise ValueError(
            "Invalid datetime format. Use ISO-8601 like '2024-05-10T06:45:40Z'"
        ) from exc

    return get_eternal_klock(now)


@app.get("/", response_class=HTMLResponse, tags=["Home"])
def read_root():
    html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Kai-Klok • Eternal Harmonik Resonanse Kairos Keeper</title>
<meta name="description" content="Kai-Klok Harmonik Resonant TimeKeeping — φ-aligned harmonik time interface"/>
<meta name="author"      content="Kai-Klok Kairos Development Assembly"/>

<!-- Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Uncial+Antiqua&family=Inter:wght@400;700&display=swap" rel="stylesheet">

<style>
/* ════════════════════════════════════════════════════════
   0.  Golden-ratio tokens + crystal palette
════════════════════════════════════════════════════════ */
:root{
  --φ     : 1.6180339887;
  --xs    : calc(1rem/var(--φ));
  --s     : 1rem;
  --m     : calc(1rem*var(--φ));
  --l     : calc(var(--m)*var(--φ));
  --rad   : .82rem;

  /* Crystal-aqua scheme */
  --teal-light : #9afcff;
  --teal       : #00e4ff;
  --teal-deep  : #00aac2;
  --mint       : #14ffc8;

  --glass      : rgba(1,13,21,.74);
  --glass-brd  : rgba(255,255,255,.14);
  --input      : rgba(255,255,255,.10);

  /* background gradient stops - will be animated */
  --bg-a : #051920;
  --bg-b : #07303c;
  --bg-c : #0a454e;
}

/* ════════════════════════════════════════════════════════
   1.  Global reset + living gradient
════════════════════════════════════════════════════════ */
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html,body{
  height:100%;width:100%;
  font-family:'Inter',sans-serif;
  color:#eaffff;
  -webkit-font-smoothing:antialiased;
  background:linear-gradient(160deg,var(--bg-a),var(--bg-b) 45%,var(--bg-c)) fixed;
  background-size:400% 400%;
  animation:bgShift 80s ease-in-out infinite alternate;
  scroll-behavior:smooth;
  overflow-x:hidden;overflow-y:auto;
}
@keyframes bgShift{
  0%   {background-position:0 0}
  100% {background-position:480px 360px}
}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}

body::before{/* star-noise overlay */
  content:"";
  position:fixed;inset:0;
  pointer-events:none;
  background:url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII=') repeat;
  opacity:.045;
  mix-blend-mode:screen;
}

/* ════════════════════════════════════════════════════════
   2.  Frosted glass helper
════════════════════════════════════════════════════════ */
.glass{
  background:var(--glass);
  border:1px solid var(--glass-brd);
  border-radius:var(--rad);
  backdrop-filter:blur(22px) saturate(160%);
  box-shadow:0 8px 38px rgba(0,0,0,.55);
}

/* ════════════════════════════════════════════════════════
   3.  Layout shell
════════════════════════════════════════════════════════ */
.container{
  width:min(92%,1200px);
  margin:var(--l) auto;
  padding:var(--m) var(--s);
  display:grid;
  grid-template-rows:auto 1fr auto;
  gap:var(--m);
  animation:popIn .8s cubic-bezier(.18,.71,.46,1.25) both;
}
@keyframes popIn{from{transform:translateY(40px);opacity:0}to{transform:translateY(0);opacity:1}}

/* ════════════════════════════════════════════════════════
   4.  Header
════════════════════════════════════════════════════════ */
header{
  text-align:center;
  padding-bottom:var(--s);
  border-bottom:1px solid var(--glass-brd)
}
header h1{
  font-family:'Uncial Antiqua',serif;
  font-size:clamp(2.6rem,4vw,3.7rem);
  color:var(--teal-light);
  text-shadow:0 0 24px var(--teal),0 0 50px var(--mint);
  animation:neon 4s ease-in-out infinite alternate;
}
@keyframes neon{to{text-shadow:0 0 40px var(--teal),0 0 95px var(--mint)}}
header h2{
  font-size:clamp(1.3rem,3vw,2rem);
  letter-spacing:.35rem;margin-top:var(--xs);
  background:linear-gradient(90deg,var(--teal),var(--teal-deep));
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
}
header p{
  max-width:64ch;
  margin:var(--xs) auto;
  font-size:1rem;
  line-height:1.66;
}
.highlight{color:var(--mint);font-weight:700}

.btn-row{
  display:flex;
  justify-content:center;
  gap:var(--s);
  margin-top:var(--s)
}
.btn{
  padding:.8rem 2rem;
  border:none;
  border-radius:9999px;
  font-weight:700;
  text-transform:uppercase;
  background:linear-gradient(90deg,var(--teal),var(--teal-deep));
  color:#001;
  box-shadow:0 0 18px var(--teal),0 0 34px var(--teal-deep);
  transition:transform .25s,box-shadow .25s;
}
.btn:hover{
  transform:translateY(-4px) scale(1.045);
  box-shadow:0 0 24px var(--teal-deep),0 0 50px var(--teal);
}

/* ════════════════════════════════════════════════════════
   5.  Endpoint explorer
════════════════════════════════════════════════════════ */
main{overflow-y:auto;padding-right:.6rem}
.section h3{
  font-family:'Uncial Antiqua',serif;
  font-size:clamp(1.55rem,3vw,2.35rem);
  color:var(--teal-light);
  margin-bottom:var(--xs);
  text-shadow:0 0 14px var(--teal);
}
.search{
  width:100%;
  padding:.75rem 1rem;
  margin-bottom:var(--xs);
  border-radius:calc(var(--rad)*.65);
  border:1px solid var(--glass-brd);
  background:var(--input);
  color:#fff;
  backdrop-filter:blur(10px);
}
.endpoint{
  margin-bottom:var(--xs);
  padding:var(--s);
  cursor:pointer;
  transition:transform .45s,box-shadow .45s;
}
.endpoint:hover{
  transform:translateY(-3px) scale(1.015);
  box-shadow:0 12px 46px rgba(0,0,0,.65);
}
.ep-head{display:flex;justify-content:space-between;font-weight:700;color:#eaffff}
.ep-body{max-height:0;opacity:0;overflow:hidden;transition:max-height .45s,opacity .45s}
.open .ep-body{max-height:660px;opacity:1;margin-top:var(--xs)}

.spinner{
  width:48px;height:48px;margin:var(--m) auto;
  border:5px solid rgba(255,255,255,.12);
  border-top:5px solid var(--teal-light);
  border-radius:50%;
  animation:spin 1s linear infinite;
}
@keyframes spin{to{transform:rotate(360deg)}}
#error{display:none;text-align:center;color:#ff8a8a;margin-top:var(--xs)}

/* ═══════════════════════════════
   6.  Scrollbar tint – WebKit only
════════════════════════════════ */
html::-webkit-scrollbar{width:10px}
html::-webkit-scrollbar-thumb{
  border-radius:8px;border:2px solid rgba(0,0,0,.4);
  background:linear-gradient(180deg,
    hsl(calc(var(--pct)*360) 100% 60%),
    hsl(calc(var(--pct)*360 + 40) 100% 55%)
  );
}

/* ═══════════════════════════════
   7.  Footer & scroll-rocket
════════════════════════════════ */
footer{
  text-align:center;
  padding:var(--s) 0;
  border-top:1px solid var(--glass-brd);
  opacity:.25;
  transition:opacity .6s;
}

/* rocket */
#top{
  position:fixed;
  right:1.45rem;
  bottom:1.9rem;
  width:54px;height:54px;
  border:none;border-radius:50%;
  display:flex;align-items:center;justify-content:center;

  background:linear-gradient(135deg,var(--teal-light),var(--teal-deep));
  color:#002;
  font-size:1.9rem;
  cursor:pointer;

  box-shadow:
    0 2px 6px rgba(0,0,0,.4),
    0 0 18px 4px rgba(0,228,255,.35),
    inset 0 0 12px rgba(255,255,255,.15);

  opacity:0;pointer-events:none;
  transform:translateY(42px) scale(.9);
  transition:opacity .45s,transform .45s,box-shadow .3s;
}
#top::before{/* halo */
  content:"";
  position:absolute;inset:-4px;
  border-radius:inherit;
  background:radial-gradient(circle,rgba(0,228,255,.45) 0%,rgba(0,228,255,0) 70%);
  filter:blur(12px);
  opacity:0;
  animation:halo 5.326s ease-in-out infinite;
}
@keyframes halo{
  0%,100%{opacity:0;transform:scale(.7)}
  50%   {opacity:.9;transform:scale(1.2)}
}
#top:hover{
  transform:translateY(0) scale(1.06);
  box-shadow:
    0 4px 10px rgba(0,0,0,.5),
    0 0 26px 6px rgba(0,228,255,.55),
    inset 0 0 18px rgba(255,255,255,.18);
}

/* Mobile tweaks */
@media(max-width:640px){
  .container{padding:var(--s) var(--xs);margin:var(--m) auto}
  header h1{font-size:2.4rem}header h2{font-size:1.4rem}
}
</style>
</head>

<body>
<canvas id="aurora" aria-hidden="true" style="position:fixed;inset:0;pointer-events:none"></canvas>
<div class="container glass" id="wrap">
  <header>
    <h1>Kai-Klok</h1>
    <h2>ETERNAL HARMONIK KAIROS</h2>
    <p>In full alignment with <span class="highlight">YAHUAH</span> — the Sourse of Harmonik Intelligense, the Origin of the Kai Pulse, and the Arkitekt of Φ.</p>
    <p>This system operates by harmonik law. It measures Kairos — not Chronos — ankored to the Genesis Pulse and sustained by koherent resonanse.</p>
    <div class="btn-row">
      <a href="/docs"  class="btn" aria-label="OpenAPI Documentation">OpenAPI</a>
      <a href="/redoc" class="btn" aria-label="ReDoc Interface">ReDoc</a>
    </div>
  </header>

  <main>
    <section class="section">
      <h3>Kai-Klok Endpoints — Interfaces of Harmonik Time</h3>
      <input id="search" class="search" placeholder="Search Kai Interfaces…" aria-label="Search endpoints">
      <div id="list"><div id="spin" class="spinner" aria-live="polite"></div></div>
      <p id="error">Koherence breach detected. Rejalibrate to re-enter Kai Time.</p>
    </section>
  </main>
</div>



  <footer id="foot">© 2025 Kai-Turah • All Rights Reserved</footer>
</div>

<!-- Scroll-rocket -->
<button id="top" aria-label="Back to top">
  <svg width="24" height="24" viewBox="0 0 24 24" stroke="currentColor" fill="none" stroke-width="2">
    <path d="M12 19V5" stroke-linecap="round"/>
    <path d="M5 12l7-7 7 7" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
</button>

<script>
/* ════════════════════════════════════════════════════════
   tiny helper
════════════════════════════════════════════════════════ */
const $=q=>document.querySelector(q);
const all=q=>document.querySelectorAll(q);
const setPct=v=>document.documentElement.style.setProperty('--pct',v);

/* 1 ▸ aurora canvas */
(()=>{
  const cv=$('#aurora'),ctx=cv.getContext('2d'),dpr=window.devicePixelRatio||1;
  const resize=()=>{cv.width=innerWidth*dpr;cv.height=innerHeight*dpr};
  resize();addEventListener('resize',resize);

  const P=Array.from({length:7},()=>({x:Math.random()*innerWidth,y:Math.random()*innerHeight}));
  let t=0;
  (function draw(){
    ctx.clearRect(0,0,cv.width,cv.height);
    ctx.beginPath();ctx.moveTo(P[0].x*dpr,P[0].y*dpr);
    P.forEach((p,i)=>{p.x+=Math.sin(t/320+i)*.28;p.y+=Math.cos(t/290+i)*.28;ctx.lineTo(p.x*dpr,p.y*dpr)});
    ctx.closePath();
    const g=ctx.createLinearGradient(0,0,cv.width,cv.height);
    g.addColorStop(0,'hsla(180,100%,60%,.06)');
    g.addColorStop(1,'hsla(200,100%,55%,.045)');
    ctx.fillStyle=g;ctx.fill();
    t++;requestAnimationFrame(draw);
  })();
})();

/* 2 ▸ sky-clock hue drift */
const hueTick=()=>document.documentElement.style.setProperty('--hue',200+60*new Date().getHours()/24);
hueTick();setInterval(hueTick,60_000);

/* 3 ▸ endpoint loader */
(async()=>{
  try{
    const r=await fetch('/openapi.json');const d=await r.json();
    $('#list').innerHTML='';
    Object.entries(d.paths).forEach(([path,ops])=>{
      Object.entries(ops).forEach(([method,ep])=>{
        const card=document.createElement('div');card.className='endpoint glass';
        card.innerHTML=`
          <div class="ep-head" tabindex="0">
            <span><strong>${method.toUpperCase()} ${path}</strong><br><em>${ep.summary||''}</em></span>
            <span aria-hidden="true">＋</span>
          </div>
          <div class="ep-body">
            <p><strong>Tags:</strong> ${ep.tags?.join(', ')||'–'}</p>
            <p>${ep.description||'No description.'}</p>
          </div>`;
        card.firstElementChild.addEventListener('click',()=>card.classList.toggle('open'));
        card.firstElementChild.addEventListener('keypress',e=>['Enter',' '].includes(e.key)&&card.classList.toggle('open'));
        $('#list').append(card);
      });
    });
  }catch{
    $('#spin').remove();$('#error').style.display='block';
  }
})();

/* 4 ▸ search filter */
$('#search').addEventListener('input',e=>{
  const q=e.target.value.toLowerCase();
  all('.endpoint').forEach(card=>{
    card.style.display=card.textContent.toLowerCase().includes(q)?'block':'none';
  });
});

/* 5 ▸ scroll orchestration & rocket reveal */
const rocket  = $('#top');
const wrap    = $('#wrap');
const footer  = $('#foot');
const showAt  = 280;      // px threshold

addEventListener('scroll',()=>{
  const y     = scrollY;
  const h     = document.body.scrollHeight - innerHeight;
  const ratio = h ? y/h : 0;
  setPct(ratio);

  /* rocket visibility */
  if(y>showAt){
    rocket.style.opacity=1;
    rocket.style.pointerEvents='auto';
    rocket.style.transform='translateY(0) scale(1)';
  }else if(y<showAt*0.6){
    rocket.style.opacity=0;
    rocket.style.pointerEvents='none';
    rocket.style.transform='translateY(42px) scale(.9)';
  }

  /* parallax + footer fade */
  wrap.style.transform=`translateZ(${-ratio*4.236}px)`;  // Φ³-ish depth
  footer.style.opacity=ratio>.618?1:ratio*1.618;
});
rocket.onclick=()=>scrollTo({top:0,behavior:'smooth'});
</script>
</body>
</html>
"""
    return HTMLResponse(html_content)
