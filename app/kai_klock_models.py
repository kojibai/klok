# kai_klock_models.py  •  v2.5 “Eternal Spheres”

from pydantic import BaseModel
from typing import List, Dict, Union, Optional


# ════════════════════════════════════════════════════════════════
# Kai-Klock Harmonic Time Models – v2.5 "Eternal Spheres"
# Fully aligned with six-domain payload grouping from get_eternal_klock
# NOTHING OMITTED • ALL DATA FIELDS INCLUDED • STRUCTURALLY COHERENT
# ════════════════════════════════════════════════════════════════


# ────────────────────────────────────────────────────────────────
# ── Primitive Cycle Types ───────────────────────────────────────
# ────────────────────────────────────────────────────────────────

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


class ChakraStep(BaseModel):
    stepIndex: int
    percentIntoStep: float
    stepsPerBeat: int
    
class SubdivisionCount(BaseModel):
    duration: float
    count: float


# ────────────────────────────────────────────────────────────────
# ── Harmonic Aggregates ─────────────────────────────────────────
# ────────────────────────────────────────────────────────────────

class HarmonicLevels(BaseModel):
    arcBeat: HarmonicCycle
    microCycle: HarmonicCycle
    chakraLoop: HarmonicCycle
    harmonicDay: HarmonicCycle


# ────────────────────────────────────────────────────────────────
# ── Top-Level Kai-Klock Response ────────────────────────────────
# ────────────────────────────────────────────────────────────────

class KaiKlockResponse(BaseModel):

    # ── 1. Divine Narrative & Seals ─────────────────────────────
    kairos_seal: Optional[str] = None
    kairos_seal_percent_step: Optional[str] = None
    kairos_seal_percent_step_solar: Optional[str] = None
    kairos_seal_solar: Optional[str] = None
    kairos_seal_day_month: Optional[str] = None
    kairos_seal_day_month_percent: Optional[str] = None
    kairos_seal_solar_day_month: Optional[str] = None
    kairos_seal_solar_day_month_percent: Optional[str] = None
    eternalSeal: str
    seal: str
    harmonicNarrative: str
    
    # ── 2. Eternal Calendar (Kai-based) ─────────────────────────
    eternalMonth: str
    eternalMonthIndex: int
    eternalMonthDescription: str
    eternalChakraArc: str
    eternalWeekDescription: str
    eternalYearName: str
    eternalKaiPulseToday: int
    kaiPulseEternal: int
    eternalMonthProgress: EternalMonthProgress



    # ── 3. Solar Calendar (Sunrise-aligned) ─────────────────────
    kaiPulseToday: int
    solarChakraArc: str
    solarDayOfMonth: int
    solarMonthIndex: int
    solarHarmonicDay: str
    solar_week_index: int
    solar_week_name: str
    solar_week_description: str
    solar_month_name: str
    solar_month_description: str
    solar_day_name: str
    solar_day_description: str

    # ── 4. Harmonic Day & Week Structure ────────────────────────
    harmonicDay: str
    harmonicDayDescription: str
    chakraArc: str
    chakraArcDescription: str
    weekIndex: int
    weekName: str
    dayOfMonth: int
    harmonicWeekProgress: HarmonicWeekProgress

    # ── 5. Resonance Structure (Beat/Step) ──────────────────────
    chakraBeat: ChakraBeat
    eternalChakraBeat: EternalChakraBeat
    chakraStep: ChakraStep
    chakraStepString: str
    solarChakraStep: ChakraStep
    solarChakraStepString: str

    # ── 6. Phi Identity / Spiral Signature ──────────────────────
    phiSpiralLevel: int
    kaiTurahPhrase: str
    phiSpiralEpochs: List[Dict[str, Union[str, int, float]]]

    # ── 7. Harmonic Cycle Progress ──────────────────────────────
    harmonicLevels: HarmonicLevels
    harmonicYearProgress: HarmonicYearProgress


    # ── 8. Unified Composite Outputs ────────────────────────────
    timestamp: str
    harmonicTimestampDescription: str
    kaiMomentSummary: str
    compressed_summary: str
    subdivisions: Dict[str, SubdivisionCount]

    