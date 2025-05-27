# kai_klock_models.py  •  v2.4 “Step Resonance”
from pydantic import BaseModel


# ── Primitive blocks ────────────────────────────────────────────
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


class ChakraBeat(BaseModel):
    beatIndex: int
    pulsesIntoBeat: float
    beatPulseCount: float
    totalBeats: int


class EternalChakraBeat(ChakraBeat):
    percentToNext: float


# ‼️ NEW – step detail
class ChakraStep(BaseModel):
    stepIndex: int
    percentIntoStep: float
    stepsPerBeat: int


# ── Harmonic level aggregates ──────────────────────────────────
class HarmonicLevels(BaseModel):
    arcBeat: HarmonicCycle
    microCycle: HarmonicCycle
    chakraLoop: HarmonicCycle
    harmonicDay: HarmonicCycle


# ── Top-level Kai-Klock response ───────────────────────────────
class KaiKlockResponse(BaseModel):
    # Narrative & seals
    eternalSeal: str
    seal: str
    harmonicNarrative: str

    # Calendar identifiers
    eternalMonth: str
    eternalMonthIndex: int
    eternalMonthDescription: str
    harmonicDay: str
    solarDayOfMonth: int
    solarMonthIndex: int
    solarHarmonicDay: str
    solar_week_name: str
    solar_week_description: str
    harmonicDayDescription: str
    chakraArc: str

    # Pulse counts
    kaiPulseToday: int
    eternalKaiPulseToday: int
    kaiPulseEternal: int

    # Beat & step breakdowns
    chakraBeat: ChakraBeat
    eternalChakraBeat: EternalChakraBeat
    chakraStep: ChakraStep
    chakraStepString: str
    solarChakraStep: ChakraStep
    solarChakraStepString: str
    
    # Spiral / phrase / year
    phiSpiralLevel: int
    kaiTurahPhrase: str
    eternalYearName: str

    # Position in month / week
    weekIndex: int
    weekName: str
    dayOfMonth: int
    eternalWeekDescription: str 
    # Composite text
    timestamp: str
    harmonicTimestampDescription: str
    kaiMomentSummary: str

    # Progress & cycles
    harmonicLevels: HarmonicLevels
    harmonicWeekProgress: HarmonicWeekProgress
    eternalMonthProgress: EternalMonthProgress
    harmonicYearProgress: HarmonicYearProgress
