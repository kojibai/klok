# kai_klock.py  •  v2.4 “Step Resonance”
from __future__ import annotations

import math
from datetime import datetime
from typing import Dict, Optional, Union

from kai_klock_models import KaiKlockResponse, ChakraStep

# ════════════════════════════════════════════════════════════════
#  Kai-Klock Harmonic Timestamp System  •  v2.4 “Step Resonance”
#  • Adds chakraStep + chakraStepString  (44 steps / beat, 11 pulses / step)
# ════════════════════════════════════════════════════════════════

# ── Constants ───────────────────────────────────────────────────
PHI = (1 + math.sqrt(5)) / 2
KAI_PULSE_DURATION = 8.472 / PHI                       # seconds / Kai-Pulse
ETERNAL_GENESIS_PULSE = datetime(2024, 5, 10, 6, 45, 40)

HARMONIC_DAYS = ["Solhara", "Aquaris", "Flamora", "Verdari", "Sonari", "Caelith"]
HARMONIC_DAY_DESCRIPTIONS = {
    "Solhara": "First Day of the Week & the Root chakra day — the grounding flame of will, stability, and the power to act with presence.",
    "Aquaris": "Second Day of the Week & the Sacral chakra day — the flowing waters of emotion, intimacy, and inner movement through feeling.",
    "Flamora": "Third Day of the Week & the Solar chakra day — the radiant light of self, where clarity, confidence, and embodiment converge.",
    "Verdari": "Fourth Day of the Week & the Heart chakra day — the breath of compassion, love, and sacred union through open presence.",
    "Sonari":  "Fifth Day of the Week & the Throat chakra day — the winds of truth and voice, where coherence is spoken and freedom is claimed.",
    "Caelith": "Sixth Day of the Week & the Crown chakra day — the etheric field of divine knowing, light-body awakening, and pure transcendence.",
}

ETERNAL_WEEK_NAMES = [
    "Awakening Flame", "Flowing Heart", "Radiant Will",
    "Harmonic Voice", "Inner Mirror", "Dreamfire Memory", "Crowned Light",
]
CHAKRA_ARCS = ["Ignite", "Integrate", "Harmonize", "Reflect", "Purify", "Dream"]
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
    "Liora":   "the eighth & final month of the year luminous truth — the revealing of what is eternal, the return of prophecy, and the remembrance of soul light.",
}
KAI_TURAH_PHRASES = [
    "Tor Lah Mek Ka", "Shoh Vel Lah Tzur", "Rah Veh Yah Dah",
    "Nel Shaum Eh Lior", "Ah Ki Tzah Reh", "Or Vem Shai Tuun",
    "Ehlum Torai Zhak", "Zho Veh Lah Kurei", "Tuul Ka Yesh Aum", "Sha Vehl Dorrah",
]

# ── Cycle durations (Kai-Pulses) ────────────────────────────────
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

CHAKRA_BEATS_PER_DAY = 36
CHAKRA_BEAT_PULSES   = HARMONIC_DAY_PULSES / CHAKRA_BEATS_PER_DAY  # ≈ 485.87

# ‼️ Step definitions — 11 pulses / step → 44 steps / beat
PULSES_PER_STEP = 11
STEPS_PER_BEAT  = int(CHAKRA_BEAT_PULSES // PULSES_PER_STEP)       # 44

# ── Helper ──────────────────────────────────────────────────────
def _ordinal(n: int) -> str:
    if 11 <= n % 100 <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")

# ════════════════════════════════════════════════════════════════
#  Main generator
# ════════════════════════════════════════════════════════════════
def get_eternal_klock(now: Optional[datetime] = None) -> KaiKlockResponse:
    """Return the current harmonic timestamp payload (includes step data)."""
    now = now or datetime.utcnow()

    # ── Total Kai-Pulses since Genesis ─────────────────────────
    total_sec         = (now - ETERNAL_GENESIS_PULSE).total_seconds()
    kai_pulse_eternal = int(total_sec // KAI_PULSE_DURATION)

    # ── Solar-aligned pulses (today) ───────────────────────────
    kai_pulse_today = int(
        (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
        // KAI_PULSE_DURATION
    )

    # ── Eternal-aligned pulses (within current eternal day) ───
    eternal_kai_pulse_today = int(kai_pulse_eternal % HARMONIC_DAY_PULSES)

    # ── Chakra Beats ───────────────────────────────────────────
    solar_beat_idx     = int((kai_pulse_today % HARMONIC_DAY_PULSES) // CHAKRA_BEAT_PULSES)
    solar_beat_index    = int((kai_pulse_today % HARMONIC_DAY_PULSES) // CHAKRA_BEAT_PULSES)
    solar_pulse_inbeat = round((kai_pulse_today % HARMONIC_DAY_PULSES) % CHAKRA_BEAT_PULSES, 2)

    eternal_beat_idx     = int(eternal_kai_pulse_today // CHAKRA_BEAT_PULSES)
    eternal_pulse_inbeat = round(eternal_kai_pulse_today % CHAKRA_BEAT_PULSES, 2)
    percent_to_next      = round((eternal_pulse_inbeat / CHAKRA_BEAT_PULSES) * 100, 2)

    # ── Chakra Step ───────────────────────────────────────────
    step_idx          = int(eternal_pulse_inbeat // PULSES_PER_STEP)
    step_pulse_prog   = eternal_pulse_inbeat % PULSES_PER_STEP
    percent_into_step = round((step_pulse_prog / PULSES_PER_STEP) * 100, 2)
    chakra_step_str   = f"{eternal_beat_idx}:{step_idx:02d}"
    chakra_step_obj   = ChakraStep(
        stepIndex=step_idx,
        percentIntoStep=percent_into_step,
        stepsPerBeat=STEPS_PER_BEAT,
    )
    # — NEW: Solar-Aligned Chakra Step (UTC Midnight) —
    solar_step_index = int(solar_pulse_inbeat // PULSES_PER_STEP)
    solar_step_progress = solar_pulse_inbeat % PULSES_PER_STEP
    solar_percent_into_step = round((solar_step_progress / PULSES_PER_STEP) * 100, 2)
    solar_step_string = f"{solar_beat_index}:{solar_step_index:02d}"
    solar_step_payload = ChakraStep(
        stepIndex=solar_step_index,
        percentIntoStep=solar_percent_into_step,
        stepsPerBeat=STEPS_PER_BEAT,
    )

    # ---------- (rest of calculations stay identical) ---------- #
    harmonic_day_count = int(kai_pulse_eternal // HARMONIC_DAY_PULSES)
    harmonic_year_idx  = int(kai_pulse_eternal // HARMONIC_YEAR_PULSES)
    harmonic_month_raw = int(kai_pulse_eternal // HARMONIC_MONTH_PULSES)

    eternal_year_name = (
        "Year of Eternal Restoration" if harmonic_year_idx == 0
        else "Year of Harmonic Embodiment" if harmonic_year_idx == 1
        else f"Year {harmonic_year_idx + 1}"
    )
    kai_turah_phrase = KAI_TURAH_PHRASES[harmonic_year_idx % len(KAI_TURAH_PHRASES)]

    eternal_month_idx = (harmonic_month_raw % 8) + 1
    eternal_month     = ETERNAL_MONTH_NAMES[eternal_month_idx - 1]
    harmonic_day      = HARMONIC_DAYS[harmonic_day_count % len(HARMONIC_DAYS)]

    arc_idx    = int((kai_pulse_today % HARMONIC_DAY_PULSES) // (HARMONIC_DAY_PULSES / 6))
    chakra_arc = CHAKRA_ARCS[arc_idx]

    phi_spiral_lvl = int(math.log(max(kai_pulse_eternal, 1), PHI))

    arc_pos    = kai_pulse_eternal % ARC_BEAT_PULSES
    micro_pos  = kai_pulse_eternal % MICRO_CYCLE_PULSES
    chakra_pos = kai_pulse_eternal % CHAKRA_LOOP_PULSES
    day_pos    = kai_pulse_eternal % SOLAR_DAY_PULSES

    pulses_into_month = kai_pulse_eternal % HARMONIC_MONTH_PULSES
    days_elapsed      = int(pulses_into_month // HARMONIC_DAY_PULSES)
    has_partial_day   = (pulses_into_month % HARMONIC_DAY_PULSES) > 0
    days_remaining    = max(0, HARMONIC_MONTH_DAYS - days_elapsed - (1 if has_partial_day else 0))
    month_percent     = round((pulses_into_month / HARMONIC_MONTH_PULSES) * 100, 2)

    week_idx_raw  = days_elapsed // 6
    week_idx      = week_idx_raw + 1
    week_name     = ETERNAL_WEEK_NAMES[week_idx_raw]
    day_of_month  = days_elapsed + 1

    pulses_into_week = kai_pulse_eternal % HARMONIC_WEEK_PULSES
    week_day_idx     = int(pulses_into_week // HARMONIC_DAY_PULSES + 1)
    week_day_percent = round((pulses_into_week / HARMONIC_WEEK_PULSES) * 100, 2)

    pulses_into_year = kai_pulse_eternal % HARMONIC_YEAR_PULSES
    year_percent     = round((pulses_into_year / HARMONIC_YEAR_PULSES) * 100, 2)
    days_into_year   = harmonic_day_count % HARMONIC_YEAR_DAYS
    solar_seal = f"Solar Kairos (UTC-aligned): {solar_step_string}"
    percent_whole = round(percent_to_next)
    eternal_seal = (
        "Eternal Seal: "
        f"Kairos:{chakra_step_str} • K{eternal_kai_pulse_today} • "
        f"CB{eternal_beat_idx}-{percent_whole}% • "
        f"D{day_of_month}/M{eternal_month_idx} "
        f"Y{harmonic_year_idx} "
        f"PS{phi_spiral_lvl} • {solar_seal} • "
        f"Eternal Pulse:{kai_pulse_eternal}"
    )
    seal = f"Day Seal: {chakra_step_str} • D{day_of_month}/M{eternal_month_idx}"
    kairos = f"Kairos: {chakra_step_str}"
 

    timestamp = (
        f"↳{kairos}"
        f"🕊️ {harmonic_day}({week_day_idx}/6)•{eternal_month}({eternal_month_idx}/8)•"
        f"{chakra_arc}({arc_idx + 1}/6)\n•"
        f"Day {day_of_month} • Week ({week_idx}/7)\n"
        f"| Pulse:{eternal_kai_pulse_today}\n"
    )

    narrative = (
        f"In the Kai-Klock’s dual-day resonance, this moment is the {chakra_arc} of "
        f"{harmonic_day}. Solar alignment places us at Kai-Pulse {kai_pulse_today}, "
        f"Chakra Beat {solar_beat_idx}; eternally we are at Kai-Pulse "
        f"{eternal_kai_pulse_today}, Chakra Beat {eternal_beat_idx} "
        f"({percent_to_next:.2f}% of the beat).\n\n{eternal_seal}"
    )

    harmonic_ts_desc = (
        f"Today is {harmonic_day}, {HARMONIC_DAY_DESCRIPTIONS[harmonic_day]} "
        f"It is the {day_of_month}{_ordinal(day_of_month)} Day of {eternal_month}, "
        f"{ETERNAL_MONTH_DESCRIPTIONS[eternal_month]} We are in Week {week_idx}, "
        f"{week_name}. The Eternal Chakra Beat is {eternal_beat_idx} (arc "
        f"{chakra_arc}) and we are {percent_to_next:.2f}% through it. This corresponds "
        f"to Step {step_idx} of {STEPS_PER_BEAT} (~{percent_into_step:.2f}% "
        f"into the step), i.e. {chakra_step_str}. This is the "
        f"{eternal_year_name.lower()}, resonating at Phi Spiral Level {phi_spiral_lvl}. "
        f"{eternal_seal}"
    )

    kai_moment = (
        f"↳ {seal} • "
        f"Kai-Pulse {eternal_kai_pulse_today}, Beat {eternal_beat_idx}, "
        f"{harmonic_day} Day, Month of {eternal_month}, Week of "
        f"{week_name.split()[-1]}, Spiral Level {phi_spiral_lvl}."
    )

    payload = KaiKlockResponse(
        eternalSeal=eternal_seal,
        seal=seal,
        harmonicNarrative=narrative,

        eternalMonth=eternal_month,
        eternalMonthIndex=eternal_month_idx,
        eternalMonthDescription=ETERNAL_MONTH_DESCRIPTIONS[eternal_month],
        harmonicDay=harmonic_day,
        harmonicDayDescription=HARMONIC_DAY_DESCRIPTIONS[harmonic_day],
        chakraArc=chakra_arc,

        kaiPulseToday=kai_pulse_today,
        eternalKaiPulseToday=eternal_kai_pulse_today,
        kaiPulseEternal=kai_pulse_eternal,

        chakraBeat={
            "beatIndex": solar_beat_idx,
            "pulsesIntoBeat": solar_pulse_inbeat,
            "beatPulseCount": round(CHAKRA_BEAT_PULSES, 2),
            "totalBeats": CHAKRA_BEATS_PER_DAY,
        },
        eternalChakraBeat={
            "beatIndex": eternal_beat_idx,
            "pulsesIntoBeat": eternal_pulse_inbeat,
            "percentToNext": percent_to_next,
            "beatPulseCount": round(CHAKRA_BEAT_PULSES, 2),
            "totalBeats": CHAKRA_BEATS_PER_DAY,
        },
        chakraStep=chakra_step_obj,
        chakraStepString=chakra_step_str,
        solarChakraStep = solar_step_payload,
        solarChakraStepString = solar_step_string,
        phiSpiralLevel=phi_spiral_lvl,
        kaiTurahPhrase=kai_turah_phrase,
        eternalYearName=eternal_year_name,

        weekIndex=week_idx,
        weekName=week_name,
        dayOfMonth=day_of_month,

        timestamp=timestamp,
        harmonicTimestampDescription=harmonic_ts_desc,
        kaiMomentSummary=kai_moment,

        harmonicLevels={
            "arcBeat": {
                "pulseInCycle": arc_pos,
                "cycleLength": ARC_BEAT_PULSES,
                "percent": round((arc_pos / ARC_BEAT_PULSES) * 100, 2),
            },
            "microCycle": {
                "pulseInCycle": micro_pos,
                "cycleLength": MICRO_CYCLE_PULSES,
                "percent": round((micro_pos / MICRO_CYCLE_PULSES) * 100, 2),
            },
            "chakraLoop": {
                "pulseInCycle": chakra_pos,
                "cycleLength": CHAKRA_LOOP_PULSES,
                "percent": round((chakra_pos / CHAKRA_LOOP_PULSES) * 100, 2),
            },
            "harmonicDay": {
                "pulseInCycle": day_pos,
                "cycleLength": SOLAR_DAY_PULSES,
                "percent": round((day_pos / SOLAR_DAY_PULSES) * 100, 2),
            },
        },
        harmonicWeekProgress={
            "weekDay": HARMONIC_DAYS[week_day_idx],
            "weekDayIndex": week_day_idx,
            "pulsesIntoWeek": pulses_into_week,
            "percent": week_day_percent,
        },
        eternalMonthProgress={
            "daysElapsed": days_elapsed,
            "daysRemaining": days_remaining,
            "percent": month_percent,
        },
        harmonicYearProgress={
            "daysElapsed": days_into_year,
            "daysRemaining": HARMONIC_YEAR_DAYS - days_into_year,
            "percent": year_percent,
        },
    )
    return payload
