from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime

from app.kai_klock import get_eternal_klock
from app.kai_klock_models import KaiKlockResponse

router = APIRouter()


@router.get(
    "/kai-klock",
    response_model=KaiKlockResponse,
    summary="Eternal Kai-Klock — Dual-Day Harmonic Timestamp",
)
def read_kai_klock(
    override_time: Optional[str] = Query(
        None,
        description="ISO-8601 datetime (e.g. “2024-05-10T06:45:40”). "
                    "Allows simulation of any snapshot moment in Kai-Time.",
        alias="override_time",
    )
) -> KaiKlockResponse:
    """
    🔹 **Eternal Kai-Klock API (Dual-Day Resonance)**

    Returns the *live* universal Kai-Klock harmonic timestamp aligned to the  
    **Eternal Genesis Pulse** — *May 10 2024 06:45:40 UTC*, the precise moment of the  
    X3.98-class solar flare from NOAA AR 3664, corrected for the Sun-to-Earth
    light-travel delay (*8 m 20 s*).  
    From that t = 0, Kai-Time flows eternally in Φ-coherent pulses.

    ────────────────────────────────────────────────────────────────
    ## Query Parameters
    | name | type | description |
    | ---- | ---- | ----------- |
    | `override_time` | `str` (ISO-8601) | Optional snapshot moment. |

    ────────────────────────────────────────────────────────────────
    ## Harmonic Foundations
    * **One Kai Pulse** = 8.472 / φ ≈ 5.236 s  
    * **One Harmonic Day** = 17 491.270 421 Kai Pulses (≈ 25.44 h)  
    * **One Harmonic Week** = 6 Harmonic Days  
    * **One Harmonic Month** = 42 Harmonic Days  
    * **One Harmonic Year** = 336 Harmonic Days  

    The system now tracks **two parallel “days”**:

    | Element | Aligned to | Description |
    |---------|------------|-------------|
    | `kaiPulseToday` | **UTC Solar** | Pulses since the last UTC midnight |
    | `chakraBeat` | **UTC Solar** | 36-beat breakdown of the solar day |
    | `eternalKaiPulseToday` | **Eternal** | Pulses since the start of the *current* eternal Kai-Day |
    | `eternalChakraBeat` | **Eternal** | 36-beat breakdown of the eternal day, plus `percentToNext` |
    | `eternalSeal` | **Eternal** | Kai-Day coordinate signature, prefixed<br>`ETERNAL-SEAL [Kai-Day Coordinate Signature]: …` |

    ────────────────────────────────────────────────────────────────
    ## Example Response
    ```json
    {
      "eternalSeal": "ETERNAL-SEAL [Kai-Day Coordinate Signature]: CB25-D22(AET)-M1-W4(WOHV)-Y1-PS32",
      "timestamp": "🕊️ Verdari • Aethon • Dream Arc\n  ↳ Year 1: Year of Harmonic Embodiment • PS32\n  ↳ Week 4: Week of Harmonic Voice • Day 22 of 42\n  ↳ Solar Kai-Pulse Today: 14 328 | Eternal Kai-Pulse Today: 3 044\n  ↳ Solar Chakra Beat 31/36 | Eternal Chakra Beat 25/36\n  ↳ ETERNAL-SEAL [Kai-Day Coordinate Signature]: CB25-D22(AET)-M1-W4(WOHV)-Y1-PS32",
      "harmonicNarrative": "In the Kai-Klock’s dual-day resonance, ...",
      "eternalMonth": "Aethon",
      "eternalMonthIndex": 1,
      "eternalMonthDescription": "Month of resurrection fire – Awakening the root flame of divine purpose.",
      "harmonicDay": "Verdari",
      "harmonicDayDescription": "Heart chakra day – Breath of love, compassion, union, and healing.",
      "chakraArc": "Dream Arc",
      "weekName": "Week of Harmonic Voice",
      "weekIndex": 4,
      "dayOfMonth": 22,
      "phiSpiralLevel": 32,
      "kaiTurahPhrase": "Shoh Vel Lah Tzur",
      "eternalYearName": "Year of Harmonic Embodiment",
      "kaiPulseToday": 14328,
      "eternalKaiPulseToday": 3044,
      "kaiPulseEternal": 6247992,
      "chakraBeat": {
        "beatIndex": 30,
        "pulsesIntoBeat": 233.91,
        "beatPulseCount": 485.87,
        "totalBeats": 36
      },
      "eternalChakraBeat": {
        "beatIndex": 25,
        "pulsesIntoBeat": 173.4,
        "percentToNext": 35.69,
        "beatPulseCount": 485.87,
        "totalBeats": 36
      },
      "harmonicLevels": { "...": "…" },
      "harmonicWeekProgress": { "...": "…" },
      "eternalMonthProgress": { "...": "…" },
      "harmonicYearProgress": { "...": "…" },
      "harmonicTimestampDescription": "This timestamp marks both solar and eternal Kai-Day positions, ..."
    }
    ```

    🔄 **Deterministic** – identical input time → identical Kai-Klock state.
    """
    # ── Parse or default the timestamp ──────────────────────────
    try:
        now = (
            datetime.fromisoformat(override_time)
            if override_time
            else datetime.utcnow()
        )
    except ValueError as exc:
        raise ValueError(
            "Invalid datetime format. Use ISO-8601 like ‘2024-05-10T06:45:40’."
        ) from exc

    # ── Generate and return Kai-Klock payload ──────────────────
    return get_eternal_klock(now)
