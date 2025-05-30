# routes/klock_utils.py

import requests
from typing import Dict, Any
from datetime import datetime


def get_kairos_data_for_sigil() -> Dict[str, Any]:
    """
    Fetches live Kairos data and extracts sigil-relevant components.
    """
    try:
        res = requests.get("https://klock.kaiturah.com/kai", timeout=5)
        res.raise_for_status()
        data = res.json()
    except Exception as e:
        raise RuntimeError(f"Failed to fetch Kairos data: {e}")

    # Extract relevant harmonic fields
    return {
        "kairos_time": data.get("kairosTime", "—"),
        "beat_index": data.get("eternalBeatIndex", 0),
        "step_index": data.get("eternalStepIndex", 0),
        "step_percent": data.get("eternalStepPercent", 0.0),
        "day": data.get("eternalDayDescription", "—"),
        "week": data.get("eternalWeekDescription", "—"),
        "month": data.get("eternalMonthDescription", "—"),
        "year": data.get("eternalYearName", "—"),
        "pulse": data.get("eternalKaiPulseToday", 0),
        "eternal_pulse": data.get("eternalPulse", 0),
        "kai_turah_phrase": data.get("kaiTurahPhrase", "—"),
        "seal": data.get("kairosSealDayMonth", "—"),
        "compressed_summary": data.get("compressedSummary", "—"),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
