from __future__ import annotations

from datetime import datetime
import math
from typing import Dict, Union, Optional
from pydantic import BaseModel

# ════════════════════════════════════════════════════════════════
#  Kai-Klock Harmonic Timestamp System  •  v2.3 “Dual-Day Resonance”
#  • Adds %-to-next-beat in Timestamp *and* Eternal Seal
#  • Adds compact “Seal” string for breath-by-breath daily use
#  • Drops “[Kai-Day Coordinate Signature]” label — now simply
#    “Eternal Seal: …”
# ════════════════════════════════════════════════════════════════


# ── Constants ───────────────────────────────────────────────────
PHI = (1 + math.sqrt(5)) / 2
KAI_PULSE_DURATION = 8.472 / PHI                     # seconds per Kai-Pulse
ETERNAL_GENESIS_PULSE = datetime(2024, 5, 10, 6, 45, 40)

HARMONIC_DAYS = [
    "Solhara", "Aquaris", "Flamora",
    "Verdari", "Sonari", "Caelith",
]

HARMONIC_DAY_DESCRIPTIONS = {
    "Solhara": "First Day of the Week & the Root chakra day — the grounding flame of will, stability, and the power to act with presence.",
    "Aquaris": "Second Day of the Week & the Sacral chakra day — the flowing waters of emotion, intimacy, and inner movement through feeling.",
    "Flamora": "Third Day of the Week & the Solar chakra day — the radiant light of self, where clarity, confidence, and embodiment converge.",
    "Verdari": "Fourth Day of the Week & the Heart chakra day — the breath of compassion, love, and sacred union through open presence.",
    "Sonari":  "Fifth Day of the Week & the Throat chakra day — the winds of truth and voice, where coherence is spoken and freedom is claimed.",
    "Caelith": "Sixth Day of the Week & the Crown chakra day — the etheric field of divine knowing, light-body awakening, and pure transcendence.",
}


ETERNAL_WEEK_NAMES = [
    "Awakening Flame",
    "Flowing Heart",
    "Radiant Will",
    "Harmonic Voice",
    "Inner Mirror",
    "Dreamfire Memory",
    "Crowned Light",
]

CHAKRA_ARCS = [
    "Ignite", "Integrate", "Harmonize",
    "Reflect", "Purify", "Dream",
]

ETERNAL_MONTH_NAMES = [
    "Aethon", "Virelai", "Solari", "Amarin",
    "Caelus", "Umbriel", "Noctura", "Liora",
]

ETERNAL_MONTH_DESCRIPTIONS = {
    "Aethon":  "the first month, resurrection fire — the reignition of primal purpose and the awakening of the root flame within.",
    "Virelai": "the second month of the year harmonic song — where the heart tunes itself to coherence, and truth flows through sound.",
    "Solari":  "the third month of the year radiant clarity — a solar unveiling of insight, confidence, and conscious alignment.",
    "Amarin":  "the fourth month of the year sacred waters — a time of feminine flow, deep receptivity, and emotional grace in motion.",
    "Caelus":  "the fifth month of the year celestial mind — where vision expands into sky thought, weaving logic with ethereal knowing.",
    "Umbriel": "the sixth month of the year shadow healing — an inward turning, where the unseen is transmuted and the subconscious finds its voice.",
    "Noctura": "the seventh month of the year lucid dreaming — portals open within, memory awakens, and divine imagination guides the way.",
    "Liora":   "the eigth & Final month of the year luminous truth — the revealing of what is eternal, the return of prophecy, and the remembrance of soul light.",
}


KAI_TURAH_PHRASES = [
    "Tor Lah Mek Ka", "Shoh Vel Lah Tzur", "Rah Veh Yah Dah",
    "Nel Shaum Eh Lior", "Ah Ki Tzah Reh", "Or Vem Shai Tuun",
    "Ehlum Torai Zhak", "Zho Veh Lah Kurei", "Tuul Ka Yesh Aum",
    "Sha Vehl Dorrah",
]

# ── Cycle Durations (Kai-Pulses) ────────────────────────────────
ARC_BEAT_PULSES       = 6
MICRO_CYCLE_PULSES    = 60
CHAKRA_LOOP_PULSES    = 360
SOLAR_DAY_PULSES      = 17_491.270_421
HARMONIC_DAY_PULSES   = SOLAR_DAY_PULSES
HARMONIC_MONTH_DAYS   = 42
HARMONIC_YEAR_DAYS    = 336
HARMONIC_MONTH_PULSES = HARMONIC_DAY_PULSES * HARMONIC_MONTH_DAYS
HARMONIC_YEAR_PULSES  = HARMONIC_MONTH_PULSES * 8
HARMONIC_WEEK_PULSES  = HARMONIC_DAY_PULSES * 6

CHAKRA_BEATS_PER_DAY  = 36
CHAKRA_BEAT_PULSES    = HARMONIC_DAY_PULSES / CHAKRA_BEATS_PER_DAY  # ≈ 485.87


# ── Helpers ─────────────────────────────────────────────────────
def ordinal_suffix(n: int) -> str:
    if 11 <= (n % 100) <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


# ── Pydantic Response Model ─────────────────────────────────────
class KaiKlockResponse(BaseModel):
    eternalSeal: str          # full, verbose seal
    seal: str                 # compact breath-by-breath seal

    timestamp: str
    harmonicNarrative: str

    eternalMonth: str
    eternalMonthIndex: int
    harmonicDay: str
    chakraArc: str
    weekName: str
    weekIndex: int
    dayOfMonth: int
    phiSpiralLevel: int
    kaiTurahPhrase: str
    eternalYearName: str

    kaiPulseToday: int
    eternalKaiPulseToday: int
    kaiPulseEternal: int

    chakraBeat: Dict[str, Union[int, float]]
    eternalChakraBeat: Dict[str, Union[int, float]]

    harmonicLevels: Dict[str, Dict[str, Union[int, float]]]
    harmonicWeekProgress: Dict[str, Union[int, float, str]]
    eternalMonthProgress: Dict[str, Union[int, float]]
    harmonicYearProgress: Dict[str, Union[int, float]]

    harmonicDayDescription: Optional[str]
    eternalMonthDescription: Optional[str]
    harmonicTimestampDescription: Optional[str]
    kaiMomentSummary: str


# ════════════════════════════════════════════════════════════════
#  Main Kai-Klock Routine
# ════════════════════════════════════════════════════════════════
def get_eternal_klock(now: datetime | None = None) -> Dict[str, Union[str, int, float, Dict]]:
    now = now or datetime.utcnow()

    # — Total Kai-Pulses since Genesis —
    total_seconds     = (now - ETERNAL_GENESIS_PULSE).total_seconds()
    kai_pulse_eternal = int(total_seconds // KAI_PULSE_DURATION)

    # — Solar-aligned pulses (UTC midnight) —
    kai_pulse_today = int(
        (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
        // KAI_PULSE_DURATION
    )

    # — Eternal-aligned pulses (within current eternal day) —
    eternalKaiPulseToday = int(kai_pulse_eternal % HARMONIC_DAY_PULSES)

    # — Chakra Beats —
    solar_beat_index    = int((kai_pulse_today % HARMONIC_DAY_PULSES) // CHAKRA_BEAT_PULSES)
    solar_pulses_inbeat = round((kai_pulse_today % HARMONIC_DAY_PULSES) % CHAKRA_BEAT_PULSES, 2)

    eternal_beat_index    = int(eternalKaiPulseToday // CHAKRA_BEAT_PULSES)
    eternal_pulses_inbeat = round(eternalKaiPulseToday % CHAKRA_BEAT_PULSES, 2)
    percent_to_next       = round((eternal_pulses_inbeat / CHAKRA_BEAT_PULSES) * 100, 2)

    # — Harmonic indices —
    harmonic_day_comp = int(kai_pulse_eternal // HARMONIC_DAY_PULSES)
    harmonic_year_idx = int(kai_pulse_eternal // HARMONIC_YEAR_PULSES)
    harmonic_month_raw = int(kai_pulse_eternal // HARMONIC_MONTH_PULSES)

    eternal_year_name = (
        "Year of Eternal Restoration" if harmonic_year_idx == 0
        else "Year of Harmonic Embodiment" if harmonic_year_idx == 1
        else f"Year {harmonic_year_idx + 1}"
    )
    kai_turah_phrase = KAI_TURAH_PHRASES[harmonic_year_idx % len(KAI_TURAH_PHRASES)]

    eternal_month_idx = (harmonic_month_raw % 8) + 1
    eternal_month     = ETERNAL_MONTH_NAMES[eternal_month_idx - 1]
    harmonic_day      = HARMONIC_DAYS[harmonic_day_comp % len(HARMONIC_DAYS)]

    # — Chakra Arc (solar-aligned split) —
    arc_index  = int((kai_pulse_today % HARMONIC_DAY_PULSES) // (HARMONIC_DAY_PULSES / 6))
    chakra_arc = CHAKRA_ARCS[arc_index]

    # — Phi Spiral Level —
    phi_spiral_level = int(math.log(max(kai_pulse_eternal, 1), PHI))

    # — Cycle positions for meta-report —
    arc_pos    = kai_pulse_eternal % ARC_BEAT_PULSES
    micro_pos  = kai_pulse_eternal % MICRO_CYCLE_PULSES
    chakra_pos = kai_pulse_eternal % CHAKRA_LOOP_PULSES
    day_pos    = kai_pulse_eternal % SOLAR_DAY_PULSES

    # — Month / Week / Day (eternal) —
    pulses_into_month = kai_pulse_eternal % HARMONIC_MONTH_PULSES
    days_elapsed      = int(pulses_into_month // HARMONIC_DAY_PULSES)
    partial_day       = (pulses_into_month % HARMONIC_DAY_PULSES) > 0
    days_remaining    = max(0, HARMONIC_MONTH_DAYS - days_elapsed - (1 if partial_day else 0))
    month_percent     = round((pulses_into_month / HARMONIC_MONTH_PULSES) * 100, 2)

    week_idx_raw   = days_elapsed // 6
    week_idx       = week_idx_raw + 1
    week_name      = ETERNAL_WEEK_NAMES[week_idx_raw]
    day_of_month   = days_elapsed + 1

    pulses_into_week  = kai_pulse_eternal % HARMONIC_WEEK_PULSES
    week_day_index    = int(pulses_into_week // HARMONIC_DAY_PULSES)
    week_day_progress = round((pulses_into_week / HARMONIC_WEEK_PULSES) * 100, 2)

    # — Year Progress —
    pulses_into_year = kai_pulse_eternal % HARMONIC_YEAR_PULSES
    year_percent     = round((pulses_into_year / HARMONIC_YEAR_PULSES) * 100, 2)
    days_into_year   = harmonic_day_comp % HARMONIC_YEAR_DAYS

  # Round to the nearest whole number percent
    percent_whole = round(percent_to_next)

# — Eternal Seal (verbose) —
    eternal_seal_value = (
        "Eternal Seal: "
        f"K{eternalKaiPulseToday} • "
        f"CB{eternal_beat_index + 1}-{percent_whole}% • "
        f"D{day_of_month}/M{eternal_month_idx} "
        f"Y{harmonic_year_idx} "
        f"PS{phi_spiral_level} • "
        f"{kai_pulse_eternal}"
    )


    seal_value = (
    f"Seal: "
    f"CB{eternal_beat_index + 1}-{percent_whole}% • "
    f"D{day_of_month}/M{eternal_month_idx} "
)




    # — Timestamp —
    timestamp_str = (
    f"🕊️ {harmonic_day}({week_day_index + 1})•{eternal_month}({eternal_month_idx})•{chakra_arc}({arc_index + 1})\n"
    f"  Day {day_of_month} • Week {week_idx}\n"
    f"| Kai-Pulse: {eternalKaiPulseToday}\n"
    f"↳ {seal_value}"
)


    # — Narrative (unchanged aside from Seal wording) —
    day_suffix = ordinal_suffix(day_of_month)
    narrative = (
        f"In the Kai-Klock’s dual-day resonance, this moment is the {chakra_arc} of "
        f"{harmonic_day}. Solar alignment places us at Kai-Pulse {kai_pulse_today}, "
        f"Chakra Beat {solar_beat_index + 1}; eternally we are at Kai-Pulse "
        f"{eternalKaiPulseToday}, Chakra Beat {eternal_beat_index + 1} "
        f"({percent_to_next:.2f}% of the beat).\n\n"
        f"{eternal_seal_value}"
    )

    harmonic_timestamp_description = (
        f"Today is {harmonic_day}, the {HARMONIC_DAY_DESCRIPTIONS[harmonic_day]} "
        f"It is the {day_of_month}{ordinal_suffix(day_of_month)} Day  "
        f"in the month of {eternal_month}, known as {ETERNAL_MONTH_DESCRIPTIONS[eternal_month]} "
        f"We are in Week {week_idx},{week_name},  "
        f"The Eternal Chakra Beat is {eternal_beat_index + 1}, it belongs to the arc {chakra_arc}, "
        f"and we are {percent_to_next:.2f}% of the way through it. "
        f"This is the {eternal_year_name.lower()},"
        f"and we are currently resonating at Phi Spiral Level {phi_spiral_level}. "
        f" {eternal_seal_value}"
        
    )
    
    kai_moment_summary = (
        f"Kai-Pulse {eternalKaiPulseToday}, "
        f"Beat {eternal_beat_index + 1}, "
        f"{harmonic_day} Day, "
        f"Month of {eternal_month}, "
        f"Week of {week_name.split()[-1]}, "
        f"Spiral Level {phi_spiral_level}."
    )


    # — Build Payload —
    payload: KaiKlockResponse = KaiKlockResponse(  # type: ignore[arg-type]
        eternalSeal = eternal_seal_value,
        seal        = seal_value,

        timestamp   = timestamp_str,
        harmonicNarrative = narrative,

        eternalMonth  = eternal_month,
        eternalMonthIndex = eternal_month_idx,
        harmonicDay   = harmonic_day,
        chakraArc     = chakra_arc,
        weekName      = week_name,
        weekIndex     = week_idx,
        dayOfMonth    = day_of_month,
        phiSpiralLevel = phi_spiral_level,
        kaiTurahPhrase = kai_turah_phrase,
        eternalYearName = eternal_year_name,

        kaiPulseToday       = kai_pulse_today,
        eternalKaiPulseToday = eternalKaiPulseToday,
        kaiPulseEternal     = kai_pulse_eternal,

        chakraBeat = {
            "beatIndex":      solar_beat_index,
            "pulsesIntoBeat": solar_pulses_inbeat,
            "beatPulseCount": round(CHAKRA_BEAT_PULSES, 2),
            "totalBeats":     CHAKRA_BEATS_PER_DAY,
        },
        eternalChakraBeat = {
            "beatIndex":      eternal_beat_index,
            "pulsesIntoBeat": eternal_pulses_inbeat,
            "percentToNext":  percent_to_next,
            "beatPulseCount": round(CHAKRA_BEAT_PULSES, 2),
            "totalBeats":     CHAKRA_BEATS_PER_DAY,
        },

        harmonicLevels = {
            "arcBeat": {
                "pulseInCycle": arc_pos,
                "cycleLength":  ARC_BEAT_PULSES,
                "percent":      round((arc_pos / ARC_BEAT_PULSES) * 100, 2),
            },
            "microCycle": {
                "pulseInCycle": micro_pos,
                "cycleLength":  MICRO_CYCLE_PULSES,
                "percent":      round((micro_pos / MICRO_CYCLE_PULSES) * 100, 2),
            },
            "chakraLoop": {
                "pulseInCycle": chakra_pos,
                "cycleLength":  CHAKRA_LOOP_PULSES,
                "percent":      round((chakra_pos / CHAKRA_LOOP_PULSES) * 100, 2),
            },
            "harmonicDay": {
                "pulseInCycle": day_pos,
                "cycleLength":  SOLAR_DAY_PULSES,
                "percent":      round((day_pos / SOLAR_DAY_PULSES) * 100, 2),
            },
        },
        harmonicWeekProgress = {
            "weekDay":        HARMONIC_DAYS[week_day_index],
            "weekDayIndex":   week_day_index,
            "pulsesIntoWeek": pulses_into_week,
            "percent":        week_day_progress,
        },
        eternalMonthProgress = {
            "daysElapsed":    days_elapsed,
            "daysRemaining":  days_remaining,
            "percent":        month_percent,
        },
        harmonicYearProgress = {
            "daysElapsed":    days_into_year,
            "daysRemaining":  HARMONIC_YEAR_DAYS - days_into_year,
            "percent":        year_percent,
        },

        harmonicDayDescription   = HARMONIC_DAY_DESCRIPTIONS[harmonic_day],
        eternalMonthDescription  = ETERNAL_MONTH_DESCRIPTIONS[eternal_month],
        harmonicTimestampDescription = harmonic_timestamp_description,  # ← updated
        kaiMomentSummary = kai_moment_summary,

        
    )

    return payload.dict()
