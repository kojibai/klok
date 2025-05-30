# app/routes/sigil_data_api.py

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

KAI_KLOCK_API = "https://klock.kaiturah.com/kai"

class SigilDataResponse(BaseModel):
    kai_pulse: int
    eternal_pulse: int
    kairos_time: str
    beat_index: int
    beat_total: int
    step_index: int
    step_total: int
    harmonic_percent: float
    day_name: str
    day_index: int
    chakra_day: str
    week_index: int
    chakra_week: str
    month_name: str
    month_index: int
    chakra_month: str
    kai_turah: str

@router.get("/sigil/data", response_model=SigilDataResponse)
async def get_sigil_data():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(KAI_KLOCK_API)
            response.raise_for_status()
            klock = response.json()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Failed to fetch Kai-Klock data: {e}")

    try:
        return SigilDataResponse(
            kai_pulse=klock["kaiPulseToday"],
            eternal_pulse=klock["kaiPulseEternal"],
            kairos_time=klock["kairos_seal"].strip(),
            beat_index=klock["eternalChakraBeat"]["beatIndex"],
            beat_total=klock["eternalChakraBeat"]["totalBeats"],
            step_index=klock["chakraStep"]["stepIndex"],
            step_total=klock["chakraStep"]["stepsPerBeat"],
            harmonic_percent=round(klock["eternalChakraBeat"]["percentToNext"], 4),
            day_name=klock["harmonicDay"],
            day_index=klock["harmonicWeekProgress"]["weekDayIndex"],
            chakra_day=klock["harmonicDayDescription"].split("—")[0].strip(),
            week_index=klock["weekIndex"],
            chakra_week=klock["weekName"],
            month_name=klock["eternalMonth"],
            month_index=klock["eternalMonthIndex"],
            chakra_month=klock["eternalMonthDescription"].split("—")[0].strip(),
            kai_turah=klock["kaiTurahPhrase"]
        )
    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Malformed Kai-Klock response: missing '{e.args[0]}'")
