from pydantic import BaseModel
from typing import Optional


# ── Small primitives ───────────────────────────────────────────
class HarmonicCycle(BaseModel):
    pulseInCycle: float
    cycleLength: float
    percent: float


class HarmonicWeekProgress(BaseModel):
    weekDay: str
    weekDayIndex: int
    pulsesIntoWeek: float
    percent: float


class EternalMonthProgress(BaseModel):
    daysElapsed: int
    daysRemaining: int
    percent: float


class HarmonicYearProgress(BaseModel):
    daysElapsed: int
    daysRemaining: int
    percent: float


# ── Nested level groups ────────────────────────────────────────
class HarmonicLevels(BaseModel):
    arcBeat: HarmonicCycle
    microCycle: HarmonicCycle
    chakraLoop: HarmonicCycle
    harmonicDay: HarmonicCycle


class ChakraBeat(BaseModel):
    beatIndex: int
    pulsesIntoBeat: float
    beatPulseCount: float
    totalBeats: int


class EternalChakraBeat(ChakraBeat):
    """Adds the % progress metric that’s unique to the eternal-aligned beat."""
    percentToNext: float


# ── Top-level Kai-Klock payload ────────────────────────────────
class KaiKlockResponse(BaseModel):
    # — Narrative & seal —
    eternalSeal: str
    harmonicNarrative: str

    # — Epochal identifiers —
    eternalMonth: str
    eternalMonthIndex: int
    eternalMonthDescription: str

    harmonicDay: str
    harmonicDayDescription: str

    chakraArc: str

    # — Pulse counts —
    kaiPulseToday: int                # solar-aligned pulses since UTC midnight
    eternalKaiPulseToday: int         # pulses into the current eternal Kai-Day
    kaiPulseEternal: int              # total pulses since Genesis

    # — Beat breakdowns —
    chakraBeat: ChakraBeat            # solar-aligned
    eternalChakraBeat: EternalChakraBeat  # eternal-aligned

    # — Annual & cyclic indices —
    phiSpiralLevel: int
    kaiTurahPhrase: str
    eternalYearName: str

    # — Calendar position within month/year —
    weekIndex: int
    weekName: str
    dayOfMonth: int

    # — Composite strings —
    timestamp: str
    harmonicTimestampDescription: str

    # — Progress & cycle structures —
    harmonicLevels: HarmonicLevels
    harmonicWeekProgress: HarmonicWeekProgress
    eternalMonthProgress: EternalMonthProgress
    harmonicYearProgress: HarmonicYearProgress
