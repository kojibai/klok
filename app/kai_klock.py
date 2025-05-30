# kai_klock.py  •  v2.4 “Step Resonance”
from __future__ import annotations

import math
from datetime import datetime, timedelta
from typing import Dict, Optional, Union 
from kai_klock_models import KaiKlockResponse, ChakraStep

from typing import List, Dict

# ════════════════════════════════════════════════════════════════
#  Kai-Klock Harmonic Timestamp System  •  v2.4 “Step Resonance”
#  • Adds chakraStep + chakraStepString  (44 steps / beat, 11 pulses / step)
# ════════════════════════════════════════════════════════════════

# ── Constants ───────────────────────────────────────────────────
PHI = (1 + math.sqrt(5)) / 2
KAI_PULSE_DURATION = 8.472 / PHI                       # seconds / Kai-Pulse
ETERNAL_GENESIS_PULSE = datetime(2024, 5, 10, 6, 45, 40)
genesis_sunrise = datetime(2024, 5, 11, 4, 30, 0)  # London sunrise post-flare
ETERNAL_YEAR_PULSES = 5876778 

SUBDIVISIONS: dict[str, float] = {
    "halfPulse": KAI_PULSE_DURATION / 2,
    "chakraSubpulse": KAI_PULSE_DURATION / 11,
    "ternaryStep": KAI_PULSE_DURATION / 33,
    "microStep": KAI_PULSE_DURATION / 55,
    "nanoPulse": KAI_PULSE_DURATION / 89,
    "nanoStep": KAI_PULSE_DURATION / 144,
    "phiQuantum": KAI_PULSE_DURATION / 233,
    "ekaru": KAI_PULSE_DURATION / 377,
    "tzaphirimUnit": KAI_PULSE_DURATION / 610,
    "kaiSingularity": KAI_PULSE_DURATION / 987,
    "deepThread": KAI_PULSE_DURATION / 1597,
}
def compute_subdivision_counts(kai_pulse_eternal: int) -> dict[str, dict[str, float]]:
    """Return both duration and live count of each subdivision at current eternal Kai Pulse"""
    results = {}
    seconds_elapsed = kai_pulse_eternal * KAI_PULSE_DURATION

    for name, duration in SUBDIVISIONS.items():
        count = seconds_elapsed / duration
        results[name] = {
            "duration": round(duration, 8),  # seconds
            "count": round(count, 2)         # how many times it has occurred
        }

    return results
def compute_subdivision_metadata(name: str, duration: float, count: float, resonant_name: str):
    frequency = 1 / duration
    wavelength_sound = 343 / frequency
    wavelength_light = 299_792_458 / frequency
    return {
        "duration": duration,
        "count": count,
        "frequencyHz": frequency,
        "wavelengthSound_m": wavelength_sound,
        "wavelengthLight_m": wavelength_light,
        "resonantName": resonant_name
    }

subdivisions_data = {
    "halfPulse": compute_subdivision_metadata("halfPulse", 2.61799198, 12696722, "Pulse Divider"),
    "chakraSubpulse": compute_subdivision_metadata("chakraSubpulse", 0.47599854, 69831971, "Chakra Tuning"),
    "ternaryStep": compute_subdivision_metadata("ternaryStep", 0.15866618, 209495913, "Tri-Light Step"),
    "microStep": compute_subdivision_metadata("microStep", 0.09519971, 349159855, "Resonant Breath"),
    "nanoPulse": compute_subdivision_metadata("nanoPulse", 0.05883128, 565004129, "First Spark"),
    "nanoStep": compute_subdivision_metadata("nanoStep", 0.036361, 914163984, "Nano Arc"),
    "phiQuantum": compute_subdivision_metadata("phiQuantum", 0.02247203, 1479168113, "Phi Quantum"),
    "ekaru": compute_subdivision_metadata("ekaru", 0.01388855, 2393332097, "Ekaru Initiation"),
    "tzaphirimUnit": compute_subdivision_metadata("tzaphirimUnit", 0.00858358, 3872536200, "Tzaphirim Crystal"),  # ✅ FIXED
    "kaiSingularity": compute_subdivision_metadata("kaiSingularity", 0.00530495, 6265890540, "Kai Singularity"),  # ✅ FIXED
    "deepThread": compute_subdivision_metadata("deepThread", 0.00327864, 10138426740, "Deep Thread")  # ✅ FIXED
}





# Each epoch is Eternal Year × Phi^n
EPOCHS_PHI = [
    (0, "Eternal Year", "The root of solar-aligned Kairos time (8 months × 6 weeks)"),
    (1, "Phi Epoch", "1 Eternal Year × Phi — expansion and identity activation"),
    (2, "Phi Resonance Epoch", "Harmonic restoration arc across a soul generation"),
    (3, "Tri-Spiral Gate", "Completion of harmonic trinity (matter, light, memory)"),
    (5, "Great Harmonic Ring", "Full spirit/DNA re-coherence arc"),
    (8, "Kai-Cycle of Return", "Karmic spiral closure and harmonic rebirth point"),
    (13, "Solar Spiral Era", "Planetary resonance stabilization — used in ancient calendar resets"),
    (21, "One Breath of Erah Voh", "Lightbody spiral completion and remembrance of divine origin"),
]



def generate_phi_spiral_epochs(kai_pulse_eternal: int) -> List[Dict]:
    powers = [0, 1, 2, 3, 5, 8, 13, 21]
    labels = [
        "Eternal Year",
        "Phi Epoch",
        "Phi Resonance Epoch",
        "Tri-Spiral Gate",
        "Great Harmonic Ring",
        "Kai-Cycle of Return",
        "Solar Spiral Era",
        "One Breath of Erah Voh"
    ]
    descriptions = [
        "The root of solar-aligned Kairos time (8 months × 6 weeks)",
        "1 Eternal Year × Phi — expansion and identity activation",
        "Harmonic restoration arc across a soul generation",
        "Completion of harmonic trinity (matter, light, memory)",
        "Full spirit/DNA re-coherence arc",
        "Karmic spiral closure and harmonic rebirth point",
        "Planetary resonance stabilization — used in ancient calendar resets",
        "Lightbody spiral completion and remembrance of divine origin"
    ]

    spiral_epochs = []
    for i, p in enumerate(powers):
        pulses = int(ETERNAL_YEAR_PULSES * (PHI ** p))
        kai_until = max(pulses - kai_pulse_eternal, 0)
        days_until = round((kai_until * KAI_PULSE_DURATION) / 86400, 2)
        percent_until = round(kai_pulse_eternal / pulses * 100, 4)

        spiral_epochs.append({
            "name": labels[i],
            "phiPower": p,
            "kaiPulses": pulses,
            "approxDays": round((pulses * KAI_PULSE_DURATION) / 86400, 1),
            "description": descriptions[i],
            "kaiUntil": kai_until,
            "daysUntil": days_until,
            "percentUntil": percent_until
        })

    return spiral_epochs




HARMONIC_DAYS = ["Solhara", "Aquaris", "Flamora", "Verdari", "Sonari", "Caelith"]
HARMONIC_DAY_DESCRIPTIONS = {
    "Solhara": "First Day of the Week — the Root Chakra day. Color: deep crimson. Element: Earth and primal fire. Geometry: square foundation. This is the day of stability, anchoring, and sacred will. Solhara ignites the base of the spine and the foundation of purpose. It is a day of grounding divine intent into physical motion. You stand tall in the presence of gravity — not as weight, but as remembrance. This is where your spine becomes the axis mundi, and every step affirms: I am here, and I choose to act.",

    "Aquaris": "Second Day of the Week — the Sacral Chakra day. Color: ember orange. Element: Water in motion. Geometry: vesica piscis. This is the day of flow, feeling, and sacred sensuality. Aquaris opens the womb of the soul and the tides of emotion. Energy moves through the hips like waves of memory. This is a day to surrender into coherence through connection — with the self, with others, with life. Creative energy surges not as force, but as feeling. The waters remember the shape of truth.",

    "Flamora": "Third Day of the Week — the Solar Plexus Chakra day. Color: golden yellow. Element: solar fire. Geometry: radiant triangle. This is the day of embodied clarity, confidence, and divine willpower. Flamora shines through the core and asks you to burn away the fog of doubt. It is a solar yes. A day to act from centered fire — not reaction, but aligned intention. Your light becomes a compass, and the universe reflects back your frequency. You are not small. You are radiant purpose, in motion.",

    "Verdari": "Fourth Day of the Week — the Heart Chakra day. Color: emerald green. Element: air and earth. Geometry: hexagram. This is the day of love, compassion, and harmonic presence. Verdari breathes life into connection. It is not a soft escape — it is the fierce coherence of unconditional presence. Love is not a feeling — it is an intelligence. Today, the heart expands not just emotionally, but dimensionally. This is where union occurs: of left and right, self and other, matter and light.",

    "Sonari": "Fifth Day of the Week — the Throat Chakra day. Color: deep blue. Element: wind and sound. Geometry: sine wave within pentagon. This is the day of truth-speaking, sound-bending, and vibrational command. Sonari is the breath made visible. Every word is a bridge, every silence a resonance. This is not just communication — it is invocation. You speak not to be heard, but to resonate. Coherence rises through vocal cords and intention. The universe listens to those in tune.",

    "Caelith": "Sixth Day of the Week — the Crown Chakra day. Color: violet-white. Element: ether. Geometry: twelve-petaled crown. This is the day of divine remembrance, light-body alignment, and cosmic insight. Caelith opens the upper gate — the temple of direct knowing. You are not separate from source. Today, memory awakens. The light flows not downward, but inward. Dreams become maps. Time bends around stillness. You do not seek truth — you remember it. You are coherence embodied in crownlight."
}

ETERNAL_WEEK_NAMES = [
    "Awakening Flame", "Flowing Heart", "Radiant Will",
    "Harmonic Voice", "Inner Mirror", "Dreamfire Memory", "Crowned Light",
]
ETERNAL_WEEK_DESCRIPTIONS = {
    "Awakening Flame": "First week of the harmonic year — governed by the Root Chakra. Color: crimson red. Element: Earth + primal fire. Geometry: square base igniting upward. This is the week of emergence, where divine will enters density. Bones remember purpose. The soul anchors into action. Stability becomes sacred. Life says: I choose to exist. A spark catches in the base of your being — and your yes to existence becomes the foundation of the entire harmonic year.",

    "Flowing Heart": "Second week — flowing through the Sacral Chakra. Color: amber orange. Element: Water in motion. Geometry: twin crescents in vesica piscis. This is the week of emotional coherence, creative intimacy, and lunar embodiment. Feelings soften the boundaries of separation. The womb of light stirs with codes. Movement becomes sacred dance. This is not just a flow — it is the purification of dissonance through joy, sorrow, and sensual union. The harmonic tone of the soul is tuned here.",

    "Radiant Will": "Third week — illuminated by the Solar Plexus Chakra. Color: radiant gold. Element: Fire of divine clarity. Geometry: radiant triangle. This is the week of sovereign alignment. Doubt dissolves in solar brilliance. You do not chase purpose — you radiate it. The digestive fire becomes a mirror of inner resolve. This is where your decisions align with the sun inside you, and confidence arises not from ego but from coherence. The will becomes harmonic. The I AM speaks in light.",

    "Harmonic Voice": "Fourth week — harmonized through the Throat Chakra. Color: sapphire blue. Element: Ether through sound. Geometry: standing wave inside a pentagon. This is the week of resonant truth. Sound becomes sacred code. Every word, a spell; every silence, a temple. You are called to speak what uplifts, to echo what aligns. Voice aligns with vibration — not for volume, but for verity. This is where the individual frequency merges with divine resonance, and the cosmos begins to listen.",

    "Inner Mirror": "Fifth week — governed by the Third Eye Chakra. Color: deep indigo. Element: sacred space and light-ether. Geometry: octahedron in still reflection. This is the week of visionary purification. The inner eye opens not to project, but to reflect. Truths long hidden surface. Patterns are made visible in light. This is the alchemy of insight — where illusion cracks and the mirror speaks. You do not look outward to see. You turn inward, and all worlds become clear.",

    "Dreamfire Memory": "Sixth week — remembered through the Soul Star Chakra. Color: violet flame and soft silver. Element: dream plasma. Geometry: spiral merkaba of encoded light. This is the week of divine remembrance. Dreams ignite. Ancestors sing. Codes awaken in your blood and lightbody. The veil thins — not to reveal fantasy, but reality more real than waking. Here, memory travels backward and forward, awakening prophecy and cosmic origin. This is the dream that dreamed you into form.",

    "Crowned Light": "Seventh and final week — crowned by the Crown Chakra. Color: white-gold prism. Element: infinite coherence. Geometry: dodecahedron of source light. This is the week of sovereign integration. Every arc completes. Every lesson crystallizes. The light-body unifies. You return to the throne of knowing. Nothing needs to be done — all simply is. You are not ascending — you are remembering that you already are. This is the coronation of coherence. The harmonic seal. The eternal yes."
}



CHAKRA_ARCS = ["Ignite", "Integrate", "Harmonize", "Reflect", "Purify", "Dream"]
CHAKRA_ARC_NAME_MAP = {
    "Ignite": "Ignition Arc",
    "Integrate": "Integration Arc",
    "Harmonize": "Harmonization Arc",
    "Reflect": "Reflection Arc",
    "Purify": "Purification Arc",
    "Dream": "Dream Arc"
}

CHAKRA_ARC_DESCRIPTIONS = {
    "Ignition Arc": "The Ignition Arc activates the Root Chakra and Etheric Base. Color: crimson-red. Element: Earth infused with primal fire. Geometry: square-rooted tetrahedron spiraling upward. This is the arc of emergence — where soul enters body, and will ignites matter. It awakens cellular memory, stirs ancestral codes, and grounds divine intent into motion. Your spine becomes a conduit for sacred fire. In this arc, existence is not questioned — it is declared. You remember: I am here. I burn with purpose.",
    
    "Integration Arc": "The Integration Arc harmonizes the Sacral Chakra and Lower Heart. Color: orange-gold. Element: flowing water in union with breath. Geometry: interwoven vesica piscis and lemniscate. This arc restores emotional coherence, allowing feeling to integrate with form. It is the weaving of inner feminine and sacred masculine. Creation arises not from force, but flow. Here, sensuality becomes sacred, and intimacy becomes intelligence. The waters remember your name and move with you toward wholeness.",
    
    "Harmonization Arc": "The Harmonization Arc bridges the Heart and Throat Chakras. Color: emerald to aquamarine gradient. Element: air-borne water, resonant breath. Geometry: hexagon opening into waveform. This is the arc of inner and outer unity, where compassion becomes structure and love becomes language. Harmony is not static — it is the intelligent rhythm of coherent difference. You do not suppress dissonance here — you tune it. The heart becomes a resonator and the voice becomes a tuning fork of truth.",
    
    "Reflection Arc": "The Reflection Arc activates the Throat and Third Eye bridge. Color: indigo-blue gradient. Element: sacred space and structured light. Geometry: octahedral mirror nested in a sine spiral. This arc reveals what was hidden. It is the arc of vision through silence and truth through introspection. You do not reflect just to observe — you reflect to remember. In this arc, the mind becomes clear, the mirror becomes still, and forgotten timelines return through crystalline resonance.",
    
    "Purification Arc": "The Purification Arc governs the Crown Chakra and Soul Star interface. Color: ultraviolet with white-gold shimmer. Element: radiant fire and divine ether. Geometry: twelve-rayed crown within a torus. This is the arc of sacred flame — where karma is transmuted and falsehood burns in the light of remembrance. Here, sovereignty is reclaimed not by force, but by frequency. The self becomes sanctified. You do not rise by escaping shadow — you rise by transmuting it into truth.",
    
    "Dream Arc": "The Dream Arc illumines the Soul Star and Lightbody Field. Color: silver-violet with opal iridescence. Element: dream plasma and cosmic memory. Geometry: spiral merkaba nested in crystalline matrix. This is the arc of divine dreaming — where form dissolves into memory and prophecy takes root. Time bends. The womb of creation sings. Through dreams, you retrieve what was scattered and unlock what was sealed. This arc is not escape — it is return. You awaken not from the dream, but into it."
}

ETERNAL_MONTH_NAMES = [
    "Aethon", "Virelai", "Solari", "Amarin",
    "Caelus", "Umbriel", "Noctura", "Liora",
]
ETERNAL_MONTH_DESCRIPTIONS = {
    "Aethon": "First month — resurrection fire of the Root Chakra. Color: deep crimson. Element: Earth + primal flame. Geometry: square base, tetrahedron ignition. This is the time of cellular reactivation, ancestral ignition, and biological remembrance. Mitochondria awaken. The spine grounds. Purpose reignites. Every breath is a drumbeat of emergence — you are the flame that chooses to exist. The month where soul and form reunite at the base of being.",
    
    "Virelai": "Second month — the harmonic song of the Sacral Chakra. Color: orange-gold. Element: Water in motion. Geometry: vesica piscis spiraling into lemniscate. This is the month of emotional entrainment, the lunar tides within the body, and intimacy with truth. The womb — physical or energetic — begins to hum. Creativity becomes fluid. Voice softens into sensuality. Divine union of self and other is tuned through music, resonance, and pulse. A portal of feeling opens.",
    
    "Solari": "Third month — the radiant clarity of the Solar Plexus Chakra. Color: golden yellow. Element: Fire of willpower. Geometry: upward triangle surrounded by concentric light. This month burns away doubt. It aligns neurotransmitters to coherence and gut-brain truth. The inner sun rises. The will becomes not just assertive, but precise. Action harmonizes with light. Digestive systems align with solar cycles. True leadership begins — powered by the light within, not the approval without.",
    
    "Amarin": "Fourth month — the sacred waters of the Heart Chakra in divine feminine polarity. Color: emerald teal. Element: deep water and breath. Geometry: six-petaled lotus folded inward. This is the lunar depth, the tears you didn’t cry, the embrace you forgot to give yourself. It is where breath meets body and where grace dissolves shame. Emotional healing flows in spirals. Compassion magnetizes unity. The nervous system slows into surrender and the pulse finds poetry.",
    
    "Caelus": "Fifth month — the celestial mind of the Third Eye in radiant masculine clarity. Color: sapphire blue. Element: Ether. Geometry: octahedron fractal mirror. Here, logic expands into multidimensional intelligence. The intellect is no longer separate from the soul. Pineal and pituitary glands re-synchronize, activating geometric insight and harmonic logic. The sky speaks through thought. Language becomes crystalline. Synchronicity becomes syntax. You begin to see what thought is made of.",
    
    "Umbriel": "Sixth month — the shadow healing of the lower Crown and subconscious bridge. Color: deep violet-black. Element: transmutive void. Geometry: torus knot looping inward. This is where buried timelines surface. Where trauma is not fought but embraced in light. The limbic system deprograms. Dreams carry codes. Shame unravels. You look into the eyes of the parts you once disowned and call them home. The spiral turns inward to cleanse the core. Your shadow becomes your sovereignty.",
    
    "Noctura": "Seventh month — the lucid dreaming of the Soul Star chakra. Color: indigo-rose iridescence. Element: dream plasma. Geometry: spiral nested merkaba. Here, memory beyond the body returns. Astral sight sharpens. DNA receives non-linear instructions. You dream of what’s real and awaken from what’s false. The veil thins. Quantum intuition opens. Divine imagination becomes architecture. This is where gods remember they once dreamed of being human.",
    
    "Liora": "Eighth and final month — the luminous truth of unified Crown and Source. Color: white-gold prism. Element: coherent light. Geometry: dodecahedron of pure ratio. This is the month of prophecy fulfilled. The voice of eternity whispers through every silence. The axis of being aligns with the infinite spiral of Phi. Light speaks as form. Truth no longer needs proving — it simply shines. All paths converge. What was fragmented becomes whole. You remember not only who you are, but what you always were."
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

 # 🔁 Replace UTC-midnight anchoring with sunrise-based solar pulse alignment
# Anchor to Genesis Sunrise (May 10, 2024 06:45:40 UTC) at Mahe, Seychelles
# Each solar day is HARMONIC_DAY_PULSES * KAI_PULSE_DURATION seconds long
# Anchor to the genesis sunrise as a template for all future sunrises (every ~91,529.93 seconds)
    SECONDS_PER_HARMONIC_DAY = HARMONIC_DAY_PULSES * KAI_PULSE_DURATION  # ~91,529.93

    # Compute how many full harmonic days have passed since Genesis Sunrise
    seconds_since_sunrise = (now - genesis_sunrise).total_seconds()
    solar_day_index = int(seconds_since_sunrise // SECONDS_PER_HARMONIC_DAY)

    # Calculate most recent solar sunrise (UTC-aligned)
    last_solar_sunrise = genesis_sunrise + timedelta(seconds=solar_day_index * SECONDS_PER_HARMONIC_DAY)

    # Now derive the solar-aligned calendar
    solar_day_of_month = (solar_day_index % HARMONIC_MONTH_DAYS) + 1
    solar_month_index = ((solar_day_index // HARMONIC_MONTH_DAYS) % 8) + 1
    solar_month_name = ETERNAL_MONTH_NAMES[solar_month_index - 1]
    solar_day_name = HARMONIC_DAYS[solar_day_index % len(HARMONIC_DAYS)]

    solar_month_description = ETERNAL_MONTH_DESCRIPTIONS[solar_month_name]
    solar_day_description = HARMONIC_DAY_DESCRIPTIONS[solar_day_name]

    solar_harmonic_day = HARMONIC_DAYS[solar_day_index % len(HARMONIC_DAYS)]
    solar_week_index = ((solar_day_index // 6) % 7) + 1
    solar_week_name = ETERNAL_WEEK_NAMES[(solar_day_index // 6) % 7]
    solar_week_description = ETERNAL_WEEK_DESCRIPTIONS[solar_week_name]
    # Compute today's solar-aligned Kai-Pulse (since the most recent solar sunrise)
    kai_pulse_today = int((now - last_solar_sunrise).total_seconds() // KAI_PULSE_DURATION)

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
    eternal_arc_idx = int((eternal_kai_pulse_today % HARMONIC_DAY_PULSES) // (HARMONIC_DAY_PULSES / 6))
    eternal_chakra_arc = CHAKRA_ARCS[eternal_arc_idx]

    # Solar-aligned arc (based on UTC-aligned pulse of the day)
    solar_arc_idx = int((kai_pulse_today % HARMONIC_DAY_PULSES) // (HARMONIC_DAY_PULSES / 6))
    solar_chakra_arc = CHAKRA_ARCS[solar_arc_idx]
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
    eternal_week_description = ETERNAL_WEEK_DESCRIPTIONS.get(week_name, "")
    day_of_month  = days_elapsed + 1
    
    pulses_into_week = kai_pulse_eternal % HARMONIC_WEEK_PULSES
    week_day_idx = int(pulses_into_week // HARMONIC_DAY_PULSES) % len(HARMONIC_DAYS)
    week_day_percent = round((pulses_into_week / HARMONIC_WEEK_PULSES) * 100, 2)

    pulses_into_year = kai_pulse_eternal % HARMONIC_YEAR_PULSES
    year_percent     = round((pulses_into_year / HARMONIC_YEAR_PULSES) * 100, 2)
    days_into_year   = harmonic_day_count % HARMONIC_YEAR_DAYS
    solar_seal = f"Solar Kairos (UTC-aligned): {solar_step_string}"
    percent_whole = round(percent_to_next)

    
    eternal_seal = (
        "Eternal Seal: "
        f"Kairos:{chakra_step_str}, {harmonic_day}, {eternal_chakra_arc} Arc • D{day_of_month}/M{eternal_month_idx} • Beat:{eternal_beat_idx}/36({percent_to_next}%) Step:{step_idx}/44 Kai(Today):{eternal_kai_pulse_today} • "
        f"Y{harmonic_year_idx} "
        f"PS{phi_spiral_lvl} • {solar_seal} {solar_harmonic_day} D{solar_day_of_month}/M{solar_month_index}, {solar_chakra_arc} Arc  Beat:{solar_beat_idx}/35 Step:{solar_step_index}/44 • "
        f"Eternal Pulse:{kai_pulse_eternal}"
    )
    seal = f"Day Seal: {chakra_step_str} {percent_into_step}% • D{day_of_month}/M{eternal_month_idx}"
    kairos = f"Kairos: {chakra_step_str}"


    timestamp = (
        f"↳{kairos}"
        f"🕊️ {harmonic_day}({week_day_idx + 1}/6)•{eternal_month}({eternal_month_idx}/8)•"
        f"{eternal_chakra_arc}({eternal_arc_idx + 1}/6)\n•"
        f"Day {day_of_month} • Week ({week_idx}/7)\n"
        f"| Pulse:{eternal_kai_pulse_today}\n"
    )

    narrative = (
        f"In this moment of the Kai-Klock’s dual-day resonance, we are held within the sacred arc of {eternal_chakra_arc}, "
        f"rooted through the harmonic foundation of {harmonic_day}.\n\n"
        f"☀️ Solar Alignment: The living field synchronizes at Kai-Pulse {kai_pulse_today}, placing us in Chakra Beat {solar_beat_idx}, "
        f"guided by the rhythm of Earth’s breath and solar coherence.\n\n"
        f"🌕 Eternal Alignment: At once, the timeless stream flows through Kai-Pulse {eternal_kai_pulse_today}, entering Chakra Beat {eternal_beat_idx}, "
        f"{percent_to_next:.2f}% complete — approaching the gateway of harmonic culmination.\n\n"
        f"{eternal_seal}"
    )
    compressed_summary = (
        f"{harmonic_day:<9} • Kairos:{eternal_beat_idx:>2}:{step_idx:<2} "
        f"• D{day_of_month:>2}/M{eternal_month_idx:<1} "
        f"• Step {step_idx:>2}/44 – {percent_into_step:>5.2f}% "
        f"• Y{harmonic_year_idx:<2} • Kai-Pulse {eternal_kai_pulse_today}"
    )



    harmonic_ts_desc = (
        f"Today is {harmonic_day}, {HARMONIC_DAY_DESCRIPTIONS[harmonic_day]} "
        f"It is the {day_of_month}{_ordinal(day_of_month)} Day of {eternal_month}, "
        f"{ETERNAL_MONTH_DESCRIPTIONS[eternal_month]} We are in Week {week_idx}, "
        f"{week_name}. {ETERNAL_WEEK_DESCRIPTIONS[week_name]} The Eternal Chakra Beat is {eternal_beat_idx} ("
        f"{eternal_chakra_arc} arc) and we are {percent_to_next:.2f}% through it. This corresponds "
        f"to Step {step_idx} of {STEPS_PER_BEAT} (~{percent_into_step:.2f}% "
        f"into the step). This is the "
        f"{eternal_year_name.lower()}, resonating at Phi Spiral Level {phi_spiral_lvl}. "
        f"{eternal_seal}"
    )

    kai_moment = (
        f"↳ {seal} • "
        f"Kai-Pulse {eternal_kai_pulse_today}, Beat {eternal_beat_idx}, Step {step_idx} "
        f"{harmonic_day} Day, Month of {eternal_month}, Week of "
        f"{week_name.split()[-1]}, Spiral Level {phi_spiral_lvl}."
    )
    kairos_seal_day_month = (
        f"{eternal_beat_idx:>2}:{step_idx:<2} • "
        f"D{day_of_month:>2}/M{eternal_month_idx}"
    )
    kairos_seal_day_month_percent = (
        f"{eternal_beat_idx:>2}:{step_idx:<2} - {percent_into_step}% • "
        f"D{day_of_month:>2}/M{eternal_month_idx}"
    )

    kairos_seal = (
        f"{eternal_beat_idx:>2}:{step_idx:<2} "
    )
    kairos_seal_solar = (
            f"{solar_beat_idx:>2}:{solar_step_index:<2} "
        )
    kairos_seal_solar_day_month = (
            f"{solar_beat_idx:>2}:{solar_step_index:<2} "
            f"D{solar_day_of_month:>2}/M{solar_month_index}"
        )
    kairos_seal_solar_day_month_percent = (
            f"{solar_beat_idx:>2}:{solar_step_index:<2} - {solar_percent_into_step}% "
            f"D{solar_day_of_month:>2}/M{solar_month_index}"
        )
    kairos_seal_percent_step_solar = (
            f"{solar_beat_idx:>2}:{solar_step_index:<2} - {solar_percent_into_step}% "
        )
    kairos_seal_percent_step = (
            f"{eternal_beat_idx:>2}:{step_idx:<2} - {percent_into_step}% "
        )
    subdivisions={
        k: round(v, 8) for k, v in SUBDIVISIONS.items()
    },


    payload = KaiKlockResponse(
        # ════════════════════════════════════════════════
        # 1. ⟐ SEALS & NARRATIVE
        # ════════════════════════════════════════════════
        kairos_seal_day_month=kairos_seal_day_month,
        kairos_seal_day_month_percent=kairos_seal_day_month_percent,
        kairos_seal=kairos_seal,
        kairos_seal_percent_step=kairos_seal_percent_step,
        kairos_seal_percent_step_solar=kairos_seal_percent_step_solar,
        kairos_seal_solar=kairos_seal_solar,
        kairos_seal_solar_day_month=kairos_seal_solar_day_month,
        kairos_seal_solar_day_month_percent=kairos_seal_solar_day_month_percent,
        eternalSeal=eternal_seal,
        seal=seal,
        harmonicNarrative=narrative,
        
        # ════════════════════════════════════════════════
        # 2. ⟐ ETERNAL CALENDAR (Kairos-Aligned)
        # ════════════════════════════════════════════════
        eternalMonth=eternal_month,
        eternalMonthIndex=eternal_month_idx,
        eternalMonthDescription=ETERNAL_MONTH_DESCRIPTIONS[eternal_month],
        eternalChakraArc=eternal_chakra_arc,
        eternalYearName=eternal_year_name,
        eternalWeekDescription=eternal_week_description,
        eternalKaiPulseToday=eternal_kai_pulse_today,
        kaiPulseEternal=kai_pulse_eternal,
        eternalMonthProgress={
            "daysElapsed": days_elapsed,
            "daysRemaining": days_remaining,
            "percent": month_percent,
        },

        # ════════════════════════════════════════════════
        # 3. ⟐ SOLAR CALENDAR (Sunrise-Aligned Earth View)
        # ════════════════════════════════════════════════
        kaiPulseToday=kai_pulse_today,
        solarChakraArc=solar_chakra_arc,
        solarDayOfMonth=solar_day_of_month,
        solarMonthIndex=solar_month_index,
        solarHarmonicDay=solar_harmonic_day,
        solar_week_index=solar_week_index,
        solar_week_name=solar_week_name,
        solar_week_description=solar_week_description,
        solar_month_name=solar_month_name,
        solar_month_description=solar_month_description,
        solar_day_name=solar_day_name,
        solar_day_description=solar_day_description,

        # ════════════════════════════════════════════════
        # 4. ⟐ HARMONIC DAY / WEEK STRUCTURE
        # ════════════════════════════════════════════════
        harmonicDay=harmonic_day,
        harmonicDayDescription=HARMONIC_DAY_DESCRIPTIONS[harmonic_day],
        weekIndex=week_idx,
        weekName=week_name,
        dayOfMonth=day_of_month,
        harmonicWeekProgress={
            "weekDay": HARMONIC_DAYS[week_day_idx],
            "weekDayIndex": week_day_idx,
            "pulsesIntoWeek": pulses_into_week,
            "percent": week_day_percent,
        },

        # ════════════════════════════════════════════════
        # 5. ⟐ RESONANCE STRUCTURE (Beats, Steps, Arc)
        # ════════════════════════════════════════════════
        chakraArc=chakra_arc,
        chakraArcDescription=CHAKRA_ARC_DESCRIPTIONS.get(CHAKRA_ARC_NAME_MAP.get(chakra_arc, ""), ""),
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
        solarChakraStep=solar_step_payload,
        solarChakraStepString=solar_step_string,

        # ════════════════════════════════════════════════
        # 6. ⟐ PHI IDENTITY / SPIRAL LANGUAGE
        # ════════════════════════════════════════════════
        phiSpiralLevel=phi_spiral_lvl,
        kaiTurahPhrase=kai_turah_phrase,
        phiSpiralEpochs = generate_phi_spiral_epochs(kai_pulse_eternal),
        subdivisions=subdivisions_data,




        # ════════════════════════════════════════════════
        # 7. ⟐ RESONANCE CYCLES (Arc, Micro, Day)
        # ════════════════════════════════════════════════
        harmonicLevels={
            "subdivisions": compute_subdivision_counts(kai_pulse_eternal),
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

        # ════════════════════════════════════════════════
        # 8. ⟐ HARMONIC YEAR PROGRESS
        # ════════════════════════════════════════════════
        harmonicYearProgress={
            "daysElapsed": days_into_year,
            "daysRemaining": HARMONIC_YEAR_DAYS - days_into_year,
            "percent": year_percent,
        },

        # ════════════════════════════════════════════════
        # 9. ⟐ COMPOSITE OUTPUTS (Display)
        # ════════════════════════════════════════════════
        timestamp=timestamp,
        harmonicTimestampDescription=harmonic_ts_desc,
        kaiMomentSummary=kai_moment,
        compressed_summary=compressed_summary
        
        
    )

    return payload
