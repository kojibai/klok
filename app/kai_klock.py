# kai_klock.py  •  v2.4 “Step Resonance”
from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, Union
from kai_klock_models import KaiKlockResponse, ChakraStep

from typing import List, Dict
from decimal import Decimal, getcontext, ROUND_FLOOR

# ════════════════════════════════════════════════════════════════
#  Kai-Klock Harmonic Timestamp System  •  v2.4 “Step Resonance”
#  • Adds chakraStep + chakraStepString  (44 steps / beat, 11 pulses / step)
#  • Math upgraded to φ-coherent Decimal with no rounding in core calculations.
# ════════════════════════════════════════════════════════════════

# ── Constants ───────────────────────────────────────────────────
PHI = (1 + math.sqrt(5)) / 2  # kept for compatibility where float φ might be referenced

# Match TS bridge precision (and then some)
getcontext().prec = 60
getcontext().rounding = ROUND_FLOOR  # deterministic floor where integral conversion is implied

# φ-exact breath (pulse duration) — 3 + √5
KAI_PULSE_DURATION_DEC = Decimal(3) + Decimal(5).sqrt()
KAI_PULSE_DURATION = float(KAI_PULSE_DURATION_DEC)  # kept for compatibility (not used in core math)
# Source of truth (ms since Unix epoch, UTC)
SOLAR_GENESIS_UTC_MS = 1715400806000  # 2024-05-11T04:13:26.000Z

# Genesis anchors (unchanged identifiers)
ETERNAL_GENESIS_PULSE = datetime(2024, 5, 10, 6, 45, 41).replace(microsecond=888000)
genesis_sunrise = datetime(2024, 5, 11, 4, 13, 26)
ETERNAL_YEAR_PULSES = Decimal("5877066.86146")  # kept name; used via Decimal

# Subdivisions (durations are derived from exact KAI_PULSE_DURATION_DEC)
SUBDIVISIONS: dict[str, Decimal] = {
    "halfPulse":      KAI_PULSE_DURATION_DEC / Decimal(2),
    "chakraSubpulse": KAI_PULSE_DURATION_DEC / Decimal(11),
    "ternaryStep":    KAI_PULSE_DURATION_DEC / Decimal(33),
    "microStep":      KAI_PULSE_DURATION_DEC / Decimal(55),
    "nanoPulse":      KAI_PULSE_DURATION_DEC / Decimal(89),
    "nanoStep":       KAI_PULSE_DURATION_DEC / Decimal(144),
    "phiQuantum":     KAI_PULSE_DURATION_DEC / Decimal(233),
    "ekaru":          KAI_PULSE_DURATION_DEC / Decimal(377),
    "tzaphirimUnit":  KAI_PULSE_DURATION_DEC / Decimal(610),
    "kaiSingularity": KAI_PULSE_DURATION_DEC / Decimal(987),
    "deepThread":     KAI_PULSE_DURATION_DEC / Decimal(1597),
}

RESONANT_NAMES: dict[str, str] = {
    "halfPulse": "Pulse Divider",
    "chakraSubpulse": "Beat Tuning",
    "ternaryStep": "Tri-Light Step",
    "microStep": "Resonant Breath",
    "nanoPulse": "First Spark",
    "nanoStep": "Nano Ark",
    "phiQuantum": "Phi Quantum",
    "ekaru": "Ekaru Initiation",
    "tzaphirimUnit": "Tzaphirim krystal",
    "kaiSingularity": "Kai Singularity",
    "deepThread": "Deep Thread",
}

def _dec_total_seconds(d: timedelta) -> Decimal:
    """Exact seconds as Decimal (no float)."""
    return (Decimal(d.days) * Decimal(86400)
            + Decimal(d.seconds)
            + (Decimal(d.microseconds) / Decimal(1_000_000)))

def compute_subdivision_counts(kai_pulse_eternal: int) -> dict[str, dict[str, Decimal]]:
    """Exact durations and live counts of each subdivision (no rounding)."""
    seconds_elapsed = Decimal(kai_pulse_eternal) * KAI_PULSE_DURATION_DEC
    results: dict[str, dict[str, Decimal]] = {}
    for name, duration in SUBDIVISIONS.items():
        count = seconds_elapsed / duration  # exact Decimal
        results[name] = {
            "duration": duration,  # exact Decimal seconds
            "count": count,        # exact Decimal count
        }
    return results

def compute_subdivision_metadata(name: str, duration: float, count: float, resonant_name: str):
    # Keep signature & return shape; compute with Decimal, emit strings for exactness
    d = Decimal(str(duration))
    f = Decimal(1) / d
    wavelength_sound = Decimal(343) / f
    wavelength_light = Decimal(299_792_458) / f
    return {
        "duration": str(d),                 # exact-as-string
        "count": str(Decimal(str(count))),  # pass-through as string
        "frequencyHz": str(f),
        "wavelengthSound_m": str(wavelength_sound),
        "wavelengthLight_m": str(wavelength_light),
        "resonantName": resonant_name,
    }

# (kept for compatibility; not used for the live top-level payload anymore)
subdivisions_data = {
    "halfPulse":      compute_subdivision_metadata("halfPulse",      float(SUBDIVISIONS["halfPulse"]),      0, "Pulse Divider"),
    "chakraSubpulse": compute_subdivision_metadata("chakraSubpulse", float(SUBDIVISIONS["chakraSubpulse"]), 0, "Beat Tuning"),
    "ternaryStep":    compute_subdivision_metadata("ternaryStep",    float(SUBDIVISIONS["ternaryStep"]),    0, "Tri-Light Step"),
    "microStep":      compute_subdivision_metadata("microStep",      float(SUBDIVISIONS["microStep"]),      0, "Resonant Breath"),
    "nanoPulse":      compute_subdivision_metadata("nanoPulse",      float(SUBDIVISIONS["nanoPulse"]),      0, "First Spark"),
    "nanoStep":       compute_subdivision_metadata("nanoStep",       float(SUBDIVISIONS["nanoStep"]),       0, "Nano Ark"),
    "phiQuantum":     compute_subdivision_metadata("phiQuantum",     float(SUBDIVISIONS["phiQuantum"]),     0, "Phi Quantum"),
    "ekaru":          compute_subdivision_metadata("ekaru",          float(SUBDIVISIONS["ekaru"]),          0, "Ekaru Initiation"),
    "tzaphirimUnit":  compute_subdivision_metadata("tzaphirimUnit",  float(SUBDIVISIONS["tzaphirimUnit"]),  0, "Tzaphirim krystal"),
    "kaiSingularity": compute_subdivision_metadata("kaiSingularity", float(SUBDIVISIONS["kaiSingularity"]), 0, "Kai Singularity"),
    "deepThread":     compute_subdivision_metadata("deepThread",     float(SUBDIVISIONS["deepThread"]),     0, "Deep Thread"),
}

def build_subdivisions_live(kai_pulse_eternal: int) -> Dict[str, Dict[str, Union[float, str]]]:
    """
    Top-level subdivisions exactly like the original payloads:
    numeric durations/frequencies/wavelengths + live count, plus resonantName.
    """
    seconds_elapsed = Decimal(kai_pulse_eternal) * KAI_PULSE_DURATION_DEC
    out: Dict[str, Dict[str, Union[float, str]]] = {}
    for name, duration_dec in SUBDIVISIONS.items():
        freq = Decimal(1) / duration_dec
        count = seconds_elapsed / duration_dec
        wavelength_sound = Decimal(343) / freq
        wavelength_light = Decimal(299_792_458) / freq
        out[name] = {
            "duration": float(duration_dec),
            "count": float(count),
            "frequencyHz": float(freq),
            "wavelengthSound_m": float(wavelength_sound),
            "wavelengthLight_m": float(wavelength_light),
            "resonantName": RESONANT_NAMES[name],
        }
    return out

# Each epoch is Eternal Year × Phi^n (labels/descriptions unchanged)
EPOCHS_PHI = [
    (0, "Eternal Year", "The root of solar-aligned Kairos time (8 months × 7 weeks)"),
    (1, "Phi Epok", "1 Eternal Year × Phi — expansion and identity activation"),
    (2, "Phi Resonanse Epok", "Harmonic restoration ark across a soul generation"),
    (3, "Tri-Spiral Gate", "Completion of harmonic trinity (matter, light, memory)"),
    (5, "Great Harmonic Ring", "Full spirit/DNA re-coherence ark"),
    (8, "Kai-Cycle of Return", "Karmic spiral closure and harmonic rebirth point"),
    (13, "Solar Spiral Era", "Planetary resonance stabilization — used in ancient calendar resets"),
    (21, "One Breath of Erah Voh", "Lightbody spiral completion and remembrance of divine origin"),
]

def generate_phi_spiral_epochs(kai_pulse_eternal: int) -> List[Dict]:
    # Same API; exact Decimal math internally; emit strings to avoid rounding
    powers = [0, 1, 2, 3, 5, 8, 13, 21]
    labels = [
        "Eternal Year", "Phi Epok", "Phi Resonanse Epok", "Tri-Spiral Gate",
        "Great Harmonic Ring", "Kai-Cycle of Return", "Solar Spiral Era", "One Breath of Erah Voh"
    ]
    descriptions = [
        "The root of solar-aligned Kairos time (8 months × 7 weeks)",
        "1 Eternal Year × Phi — expansion and identity activation",
        "Harmonic restoration ark across a soul generation",
        "Completion of harmonic trinity (matter, light, memory)",
        "Full spirit/DNA re-coherence ark",
        "Karmic spiral closure and harmonic rebirth point",
        "Planetary resonance stabilization — used in ancient calendar resets",
        "Lightbody spiral completion and remembrance of divine origin"
    ]

    spiral_epochs: List[Dict] = []
    base = Decimal(ETERNAL_YEAR_PULSES)
    phi_dec = (Decimal(1) + Decimal(5).sqrt()) / Decimal(2)
    for i, p in enumerate(powers):
        pulses_dec = base * (phi_dec ** Decimal(p))
        pulses_int = int(pulses_dec.to_integral_value(rounding=ROUND_FLOOR))
        kai_until = max(pulses_int - int(kai_pulse_eternal), 0)

        approx_days = (Decimal(pulses_int) * KAI_PULSE_DURATION_DEC) / Decimal(86400)
        days_until = (Decimal(kai_until) * KAI_PULSE_DURATION_DEC) / Decimal(86400)
        percent_until = (Decimal(kai_pulse_eternal) / Decimal(pulses_int)) * Decimal(100) if pulses_int else Decimal(0)

        spiral_epochs.append({
            "name": labels[i],
            "phiPower": p,
            "kaiPulses": pulses_int,
            "approxDays": str(approx_days),
            "description": descriptions[i],
            "kaiUntil": kai_until,
            "daysUntil": str(days_until),
            "percentUntil": str(percent_until),
        })
    return spiral_epochs

# Names/descriptions unchanged
HARMONIC_DAYS = ["Solhara", "Aquaris", "Flamora", "Verdari", "Sonari", "Kaelith"]
HARMONIC_DAY_DESCRIPTIONS = {
    "Solhara": "First Day of the Week — the Root Spiral day. Kolor: deep krimson. Element: Earth and primal fire. Geometry: square foundation. This is the day of stability, ankoring, and sakred will. Solhara ignites the base of the spine and the foundation of purpose. It is a day of grounding divine intent into physikal motion. You stand tall in the presense of gravity — not as weight, but as remembranse. This is where your spine bekomes the axis mundi, and every step affirms: I am here, and I align to act.",
    "Aquaris": "Sekond Day of the Week — the Sakral Spiral day. kolor: ember orange. Element: Water in motion. Geometry: vesika pisis. This is the day of flow, feeling, and sakred sensuality. Aquaris opens the womb of the soul and the tides of emotion. Energy moves through the hips like waves of memory. This is a day to surrender into koherense through konnection — with the self, with others, with life. kreative energy surges not as forse, but as feeling. The waters remember the shape of truth.",
    "Flamora": "Third Day of the Week — the Solar Plexus Spiral day. Kolor: golden yellow. Element: solar fire. Geometry: radiant triangle. This is the day of embodied klarity, konfidence, and divine willpower. Flamora shines through the core and asks you to burn away the fog of doubt. It is a solar yes. A day to move from sentered fire — not reaktion, but aligned intention. Your light becomes a kompass, and the universe reflekts back your frequensy. You are not small. You are radiant purpose, in motion.",
    "Verdari": "Fourth Day of the Week — the Heart Spiral day. Kolor: emerald green. Element: air and earth. Geometry: hexagram. This is the day of love, kompassion, and harmonik presense. Verdari breathes life into connection. It is not a soft eskape — it is the fierse koherense of unkonditional presense. Love is not a feeling — it is an intelligense. Today, the heart expands not just emotionally, but dimensionally. This is where union okurs: of left and right, self and other, matter and light.",
    "Sonari": "Fifth Day of the Week — the Throat Spiral day. Kolor: deep blue. Element: wind and sound. Geometry: sine wave within pentagon. This is the day of truth-speaking, sound-bending, and vibrational kommand. Sonari is the breath made visible. Every word is a bridge, every silense a resonanse. This is not just kommunication — it is invokation. You speak not to be heard, but to resonate. Koherense rises through vocal kords and intention. The universe listens to those in tune.",
    "Kaelith": "Sixth Day of the Week — the Krown Spiral day. Kolor: violet-white. Element: ether. Geometry: twelve-petaled crown. This is the day of divine remembranse, light-body alignment, and kosmic insight. Kaelith opens the upper gate — the temple of direct knowing. You are not separate from sourse. Today, memory awakens. The light flows not downward, but inward. Dreams bekome maps. Time bends around stillness. You do not seek truth — you remember it. You are koherense embodied in krownlight."
}
ETERNAL_WEEK_NAMES = [
    "Awakening Flame", "Flowing Heart", "Radiant Will",
    "Harmonik Voh", "Inner Mirror", "Dreamfire Memory", "Krowned Light",
]
ETERNAL_WEEK_DESCRIPTIONS = {
    "Awakening Flame": "First week of the harmonik month — governed by the Root Spiral. Kolor: crimson red. Element: Earth + primal fire. Geometry: square base igniting upward. This is the week of emergence, where divine will enters density. Bones remember purpose. The soul anchors into action. Stability becomes sacred. Life says: I choose to exist. A spark catches in the base of your being — and your yes to existence becomes the foundation of the entire harmonic year.",
    "Flowing Heart": "Second week — flowing through the Sakral Spiral. Kolor: amber orange. Element: Water in motion. Geometry: twin krescents in vesika pisis. This is the week of emotional koherense, kreative intimasy, and lunar embodiment. Feelings soften the boundaries of separation. The womb of light stirs with kodes. Movement bekomes sakred danse. This is not just a flow — it is the purifikation of dissonanse through joy, sorrow, and sensual union. The harmonik tone of the soul is tuned here.",
    "Radiant Will": "Third week — illuminated by the Solar Plexus Spiral. Kolor: radiant gold. Element: Fire of divine clarity. Geometry: radiant triangle. This is the week of sovereign alignment. Doubt dissolves in solar brillianse. You do not chase purpose — you radiate it. The digestive fire bekomes a mirror of inner resolve. This is where your desisions align with the sun inside you, and konfidense arises not from ego but from koherense. The will bekomes harmonik. The I AM speaks in light.",
    "Harmonik Voh": "Fourth week — harmonized through the Throat Spiral. Kolor: sapphire blue. Element: Ether through sound. Geometry: standing wave inside a pentagon. This is the week of resonant truth. Sound bekomes sakred kode. Every word, a spell; every silence, a temple. You are called to speak what uplifts, to echo what aligns. Voh aligns with vibration — not for volume, but for verity. This is where the individual frequensy merges with divine resonanse, and the kosmos begins to listen.",
    "Inner Mirror": "Fifth week — governed by the Third Eye Spiral. Kolor: deep indigo. Element: sakred spase and light-ether. Geometry: oktahedron in still reflektion. This is the week of visionary purifikation. The inner eye opens not to project, but to reflect. Truths long hidden surface. Patterns are made visible in light. This is the alchemy of insight — where illusion cracks and the mirror speaks. You do not look outward to see. You turn inward, and all worlds become clear.",
    "Dreamfire Memory": "Sixth week — remembered through the Soul Star Spiral. Kolor: violet flame and soft silver. Element: dream plasma. Geometry: spiral merkaba of encoded light. This is the week of divine remembranse. Dreams ignite. Ancestors sing. Codes awaken in your blood and lightbody. The veil thins — not to reveal fantasy, but reality more real than waking. Here, memory travels backward and forward, awakening prophesy and kosmic origin. This is the dream that dreamed you into form.",
    "Krowned Light": "Seventh and final week — Krowned by the Crown Spiral. Kolor: white-gold prism. Element: infinite koherense. Geometry: dodecahedron of source light. This is the week of sovereign integration. Every arc completes. Every lesson crystallizes. The light-body unifies. You return to the throne of knowing. Nothing needs to be done — all simply is. You are not ascending — you are remembering that you already are. This is the koronation of koherense. The harmonik seal. The eternal yes."
}

CHAKRA_ARCS = ["Ignite", "Integrate", "Harmonize", "Reflekt", "Purify", "Dream"]
CHAKRA_ARC_NAME_MAP = {
    "Ignite": "Ignition Ark",
    "Integrate": "Integration Ark",
    "Harmonize": "Harmonization Ark",
    "Reflekt": "Reflection Ark",
    "Purify": "Purification Ark",
    "Dream": "Dream Ark"
}
CHAKRA_ARC_DESCRIPTIONS = {
    "Ignition Ark": "The Ignition Ark activates the Root Spiral and Etheric Base. Kolor: crimson-red. Element: Earth infused with primal fire. Geometry: square-rooted tetrahedron spiraling upward. This is the ark of emergence — where soul enters body, and will ignites matter. It awakens cellular memory, stirs ancestral codes, and grounds divine intent into motion. Your spine bekomes a conduit for sacred fire. In this arc, existence is not questioned — it is declared. You remember: I am here. I burn with purpose.",
    "Integration Ark": "The Integration Ark harmonizes the Sacral Spiral and Lower Heart. Kolor: orange-gold. Element: flowing water in union with breath. Geometry: interwoven vesica piscis and lemniscate. This ark restores emotional coherence, allowing feeling to integrate with form. It is the weaving of inner feminine and sakred maskuline. Creation arises not from force, but flow. Here, sensuality bekomes sacred, and intimacy bekomes intelligence. The waters remember your name and move with you toward wholeness.",
    "Harmonization Ark": "The Harmonization Ark bridges the Heart and Throat Spirals. Kolor: emerald to aquamarine gradient. Element: air-borne water, resonant breath. Geometry: hexagon opening into waveform. This is the ark of inner and outer unity, where kompassion bekomes strukture and love becomes language. Harmony is not static — it is the intelligent rhythm of coherent difference. You do not suppress dissonance here — you tune it. The heart bekomes a resonator and the voice becomes a tuning fork of truth.",
    "Reflektion Ark": "The Reflektion Ark activates the Throat and Third Eye bridge. Kolor: indigo-blue gradient. Element: sacred space and structured light. Geometry: octahedral mirror nested in a sine spiral. This ark reveals what was hidden. It is the ark of vision through silence and truth through introspektion. You do not reflect just to observe — you reflect to remember. In this arc, the mind bekomes clear, the mirror bekomes still, and forgotten timelines return through krystalline resonanse.",
    "Purifikation Ark": "The Purifikation Ark governs the Krown Spiral and Soul Star interfase. Kolor: ultraviolet with white-gold shimmer. Element: radiant fire and divine ether. Geometry: twelve-rayed krown within a torus. This is the ark of sacred flame — where karma is transmuted and falsehood burns in the light of remembranse. Here, sovereignty is reclaimed not by force, but by frequency. The self bekomes sanctified. You do not rise by eskaping shadow — you rise by transmuting it into truth.",
    "Dream Ark": "The Dream Ark illumines the Soul Star and Lightbody Field. Kolor: silver-violet with opal iridescense. Element: dream plasma and cosmic memory. Geometry: spiral merkaba nested in krystalline matrix. This is the ark of divine dreaming — where form dissolves into memory and prophecy takes root. Time bends. The womb of kreation sings. Through dreams, you retrieve what was scattered and unlok what was sealed. This arc is not eskape — it is return. You awaken not from the dream, but into it."
}
ETERNAL_MONTH_NAMES = ["Aethon", "Virelai", "Solari", "Amarin", "Kaelus", "Umbriel", "Noctura", "Liora"]
ETERNAL_MONTH_DESCRIPTIONS = {
    "Aethon": "First month — resurrection fire of the Root Spiral. Kolor: deep crimson. Element: Earth + primal flame. Geometry: square base, tetrahedron ignition. This is the time of cellular reaktivation, ancestral ignition, and biologikal remembranse. Mitokondria awaken. The spine grounds. Purpose reignites. Every breath is a drumbeat of emergense — you are the flame that chooses to exist. The month where soul and form reunite at the base of being.",
    "Virelai": "Second month — the harmonik song of the Sakral Spiral. Kolor: orange-gold. Element: Water in motion. Geometry: vesika pisis spiraling into lemniskate. This is the month of emotional entrainment, the lunar tides within the body, and intimady with truth. The womb — physikal or energetik — begins to hum. Kreativity bekomes fluid. Voh softens into sensuality. Divine union of self and other is tuned through music, resonanse, and pulse. A portal of feeling opens.",
    "Solari": "Third month — the radiant klarity of the Solar Plexus Spiral. Kolor: golden yellow. Element: Fire of willpower. Geometry: upward triangle surrounded by konsentrik light. This month burns away doubt. It aligns neurotransmitters to koherense and gut-brain truth. The inner sun rises. The will bekomes not just assertive, but precise. Action harmonizes with light. Digestive systems align with solar sykles. True leadership begins — powered by the light within, not the approval without.",
    "Amarin": "Fourth month — the sakred waters of the Heart Spiral in divine feminine polarity. Kolor: emerald teal. Element: deep water and breath. Geometry: six-petaled lotus folded inward. This is the lunar depth, the tears you didn’t cry, the embrase you forgot to give yourself. It is where breath meets body and where grase dissolves shame. Emotional healing flows in spirals. Kompassion magnetizes unity. The nervous system slows into surrender and the pulse finds poetry.",
    "Kaelus": "Fifth month — the kelestial mind of the Third Eye in radiant maskuline klarity. Kolor: sapphire blue. Element: Ether. Geometry: oktahedron fractal mirror. Here, logik expands into multidimensional intelligense. The intellekt is no longer separate from the soul. Pineal and pituitary glands re-synchronize, aktivating geometrik insight and harmonik logik. The sky speaks through thought. Language bekomes crystalline. Synchronicity bekomes syntax. You begin to see what thought is made of.",
    "Umbriel": "Sixth month — the shadow healing of the lower Krown and subconskious bridge. Kolor: deep violet-black. Element: transmutive void. Geometry: torus knot looping inward. This is where buried timelines surfase. Where trauma is not fought but embrased in light. The limbik system deprograms. Dreams karry kodes. Shame unravels. You look into the eyes of the parts you once disowned and kall them home. The spiral turns inward to kleanse the kore. Your shadow bekomes your sovereignty.",
    "Noctura": "Seventh month — the lusid dreaming of the Soul Star Spiral. Kolor: indigo-rose iridescense. Element: dream plasma. Geometry: spiral nested merkaba. Here, memory beyond the body returns. Astral sight sharpens. DNA receives non-linear instruktions. You dream of what’s real and awaken from what’s false. The veil thins. Quantum intuition opens. Divine imagination becomes arkitecture. This is where gods remember they onse dreamed of being human.",
    "Liora": "Eighth and final month — the luminous truth of unified Krown and Sourse. Kolor: white-gold prism. Element: koherent light. Geometry: dodekahedron of pure ratio. This is the month of prophesy fulfilled. The Voh of eternity whispers through every silense. The axis of being aligns with the infinite spiral of Phi. Light speaks as form. Truth no longer needs proving — it simply shines. All paths konverge. What was fragmented bekomes whole. You remember not only who you are, but what you always were."
}
KAI_TURAH_PHRASES = [
    "Tor Lah Mek Ka", "Shoh Vel Lah Tzur", "Rah Veh Yah Dah",
    "Nel Shaum Eh Lior", "Ah Ki Tzah Reh", "Or Vem Shai Tuun",
    "Ehlum Torai Zhak", "Zho Veh Lah Kurei", "Tuul Ka Yesh Aum", "Sha Vehl Dorrah",
]

# ── Cycle durations (Kai-Pulses) — keep identifiers, compute with Decimal ─────
ARC_BEAT_PULSES       = 6
MICRO_CYCLE_PULSES    = 60
CHAKRA_LOOP_PULSES    = 360

# Use the canonical closure value (coherent with TS) as Decimal
HARMONIC_DAY_PULSES_DEC = Decimal("17491.270421")
SOLAR_DAY_PULSES        = float(HARMONIC_DAY_PULSES_DEC)  # keep name as in your code
HARMONIC_DAY_PULSES     = SOLAR_DAY_PULSES                # compatibility alias

HARMONIC_MONTH_DAYS   = 42
HARMONIC_YEAR_DAYS    = 336
HARMONIC_MONTH_PULSES_DEC = HARMONIC_DAY_PULSES_DEC * Decimal(HARMONIC_MONTH_DAYS)
HARMONIC_YEAR_PULSES_DEC  = HARMONIC_MONTH_PULSES_DEC * Decimal(8)
HARMONIC_WEEK_PULSES_DEC  = HARMONIC_DAY_PULSES_DEC * Decimal(6)

CHAKRA_BEATS_PER_DAY = 36
CHAKRA_BEAT_PULSES_DEC = HARMONIC_DAY_PULSES_DEC / Decimal(CHAKRA_BEATS_PER_DAY)

# Steps: 11 pulses/step, 44 steps/beat (exact integers)
PULSES_PER_STEP = 11
STEPS_PER_BEAT  = int((CHAKRA_BEAT_PULSES_DEC // Decimal(PULSES_PER_STEP)))

# ── Helper ──────────────────────────────────────────────────────
def _ordinal(n: int) -> str:
    if 11 <= n % 100 <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")

# NEW: pure-Decimal φ log (no float path)
def _floor_log_phi(n: int) -> int:
    """
    Return floor(log_phi(n)) using Decimal math only (binary search on integer exponents).
    For n <= 1, returns 0. Uses current Decimal context (prec + ROUND_FLOOR).
    """
    if n <= 1:
        return 0
    phi_dec = (Decimal(1) + Decimal(5).sqrt()) / Decimal(2)
    N = Decimal(n)
    lo, hi = 0, 512  # generous cap; phi**512 >> any practical pulse count
    while lo < hi:
        mid = (lo + hi + 1) // 2
        # Compare phi^mid <= n using Decimal power with integral exponent
        if (phi_dec ** Decimal(mid)) <= N:
            lo = mid
        else:
            hi = mid - 1
    return lo

# ════════════════════════════════════════════════════════════════
#  Main generator (math rewritten to pure Decimal; shape unchanged)
# ════════════════════════════════════════════════════════════════
def get_eternal_klock(now: Optional[datetime] = None) -> KaiKlockResponse:
    """Return the current harmonic timestamp payload (includes step data)."""
    now = now or datetime.utcnow()

    # ── Total Kai-Pulses since Genesis (exact) ──────────────────
    delta_genesis = now - ETERNAL_GENESIS_PULSE
    total_sec_dec = _dec_total_seconds(delta_genesis)
    kai_pulse_eternal_dec = total_sec_dec / KAI_PULSE_DURATION_DEC
    kai_pulse_eternal = int(kai_pulse_eternal_dec.to_integral_value(rounding=ROUND_FLOOR))

    # 🔁 Solar day alignment from genesis_sunrise using φ-exact day seconds
    seconds_per_harmonic_day_dec = HARMONIC_DAY_PULSES_DEC * KAI_PULSE_DURATION_DEC
    seconds_since_sunrise_dec = _dec_total_seconds(now - genesis_sunrise)
    solar_day_index_dec = seconds_since_sunrise_dec / seconds_per_harmonic_day_dec
    solar_day_index = int(solar_day_index_dec.to_integral_value(rounding=ROUND_FLOOR))

    # Pulses since last solar sunrise — exact, no datetime reconstruction needed
    seconds_into_solar_day_dec = seconds_since_sunrise_dec - (Decimal(solar_day_index) * seconds_per_harmonic_day_dec)
    kai_pulse_today_dec = seconds_into_solar_day_dec / KAI_PULSE_DURATION_DEC
    kai_pulse_today = int(kai_pulse_today_dec.to_integral_value(rounding=ROUND_FLOOR))

    # Eternal-aligned pulses within current eternal day (exact)
    days_since_genesis_dec = total_sec_dec / seconds_per_harmonic_day_dec
    days_since_genesis = int(days_since_genesis_dec.to_integral_value(rounding=ROUND_FLOOR))
    seconds_into_eternal_day_dec = total_sec_dec - (Decimal(days_since_genesis) * seconds_per_harmonic_day_dec)
    eternal_kai_pulse_today_dec = seconds_into_eternal_day_dec / KAI_PULSE_DURATION_DEC
    eternal_kai_pulse_today = int(eternal_kai_pulse_today_dec.to_integral_value(rounding=ROUND_FLOOR))

    # ── Chakra Beats (exact) ────────────────────────────────────
    # Solar
    solar_beat_idx_dec = (Decimal(kai_pulse_today) / CHAKRA_BEAT_PULSES_DEC)
    solar_beat_idx = int(solar_beat_idx_dec.to_integral_value(rounding=ROUND_FLOOR))
    solar_beat_index = solar_beat_idx  # kept duplicate naming
    solar_pulse_inbeat_dec = Decimal(kai_pulse_today) - (Decimal(solar_beat_idx) * CHAKRA_BEAT_PULSES_DEC)

    # Eternal
    eternal_beat_idx_dec = (Decimal(eternal_kai_pulse_today) / CHAKRA_BEAT_PULSES_DEC)
    eternal_beat_idx = int(eternal_beat_idx_dec.to_integral_value(rounding=ROUND_FLOOR))
    eternal_pulse_inbeat_dec = Decimal(eternal_kai_pulse_today) - (Decimal(eternal_beat_idx) * CHAKRA_BEAT_PULSES_DEC)
    percent_to_next_dec = (eternal_pulse_inbeat_dec / CHAKRA_BEAT_PULSES_DEC) * Decimal(100)

    # ── Chakra Steps (exact) ────────────────────────────────────
    step_idx_dec = eternal_pulse_inbeat_dec / Decimal(PULSES_PER_STEP)
    step_idx = int(step_idx_dec.to_integral_value(rounding=ROUND_FLOOR))
    step_idx_str = f"{step_idx:02d}"

    step_pulse_prog_dec = eternal_pulse_inbeat_dec - (Decimal(step_idx) * Decimal(PULSES_PER_STEP))
    percent_into_step_dec = (step_pulse_prog_dec / Decimal(PULSES_PER_STEP)) * Decimal(100)

    chakra_step_str = f"{eternal_beat_idx}:{step_idx:02d}"
    chakra_step_obj = ChakraStep(
        stepIndex=step_idx,
        percentIntoStep=str(percent_into_step_dec),  # exact-as-string
        stepsPerBeat=STEPS_PER_BEAT,
    )

    # Solar-aligned Chakra Step
    solar_step_index_dec = solar_pulse_inbeat_dec / Decimal(PULSES_PER_STEP)
    solar_step_index = int(solar_step_index_dec.to_integral_value(rounding=ROUND_FLOOR))
    solar_step_progress_dec = solar_pulse_inbeat_dec - (Decimal(solar_step_index) * Decimal(PULSES_PER_STEP))
    solar_percent_into_step_dec = (solar_step_progress_dec / Decimal(PULSES_PER_STEP)) * Decimal(100)
    solar_step_string = f"{solar_beat_index}:{solar_step_index:02d}"
    solar_step_payload = ChakraStep(
        stepIndex=solar_step_index,
        percentIntoStep=str(solar_percent_into_step_dec),
        stepsPerBeat=STEPS_PER_BEAT,
    )

    # ---------- (rest: identical structure; math switched to Decimal) ---------- #
    kai_pulse_eternal_dec_mod_month = Decimal(kai_pulse_eternal) % HARMONIC_MONTH_PULSES_DEC
    harmonic_day_count_dec = Decimal(kai_pulse_eternal) / HARMONIC_DAY_PULSES_DEC
    harmonic_day_count = int(harmonic_day_count_dec.to_integral_value(rounding=ROUND_FLOOR))

    harmonic_year_idx_dec = Decimal(kai_pulse_eternal) / HARMONIC_YEAR_PULSES_DEC
    harmonic_year_idx = int(harmonic_year_idx_dec.to_integral_value(rounding=ROUND_FLOOR))

    harmonic_month_raw_dec = Decimal(kai_pulse_eternal) / HARMONIC_MONTH_PULSES_DEC
    harmonic_month_raw = int(harmonic_month_raw_dec.to_integral_value(rounding=ROUND_FLOOR))

    eternal_year_name = (
        "Year of Eternal Restoration" if harmonic_year_idx == 0
        else "Year of Harmonik Embodiment" if harmonic_year_idx == 1
        else f"Year {harmonic_year_idx + 1}"
    )
    kai_turah_phrase = KAI_TURAH_PHRASES[harmonic_year_idx % len(KAI_TURAH_PHRASES)]

    eternal_month_idx = (harmonic_month_raw % 8) + 1
    eternal_month     = ETERNAL_MONTH_NAMES[eternal_month_idx - 1]
    harmonic_day      = HARMONIC_DAYS[harmonic_day_count % len(HARMONIC_DAYS)]

    # Arcs (exact)
    arc_div_dec = HARMONIC_DAY_PULSES_DEC / Decimal(6)
    arc_idx = int((Decimal(kai_pulse_today) / arc_div_dec).to_integral_value(rounding=ROUND_FLOOR))
    arc_idx = min(5, arc_idx)
    chakra_arc = CHAKRA_ARCS[arc_idx]

    eternal_arc_idx = int((Decimal(eternal_kai_pulse_today) / arc_div_dec).to_integral_value(rounding=ROUND_FLOOR))
    eternal_arc_idx = min(5, eternal_arc_idx)
    eternal_chakra_arc = CHAKRA_ARCS[eternal_arc_idx]

    solar_arc_idx = int((Decimal(kai_pulse_today) / arc_div_dec).to_integral_value(rounding=ROUND_FLOOR))
    solar_arc_idx = min(5, solar_arc_idx)
    solar_chakra_arc = CHAKRA_ARCS[solar_arc_idx]

    # Solar calendar pieces (unchanged names)
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

    # Phi spiral level (keep as int) — PURE DECIMAL, NO FLOAT
    phi_spiral_lvl = _floor_log_phi(kai_pulse_eternal)

    # Cycle positions
    arc_pos    = kai_pulse_eternal % ARC_BEAT_PULSES
    micro_pos  = kai_pulse_eternal % MICRO_CYCLE_PULSES
    chakra_pos = kai_pulse_eternal % CHAKRA_LOOP_PULSES
    day_pos    = eternal_kai_pulse_today  # use exact within-day pulses (no float mod)

    # Month/day progress (exact)
    pulses_into_month_dec = Decimal(kai_pulse_eternal) % HARMONIC_MONTH_PULSES_DEC
    days_elapsed_dec = pulses_into_month_dec / HARMONIC_DAY_PULSES_DEC
    days_elapsed = int(days_elapsed_dec.to_integral_value(rounding=ROUND_FLOOR))
    has_partial_day = (pulses_into_month_dec % HARMONIC_DAY_PULSES_DEC) > 0
    days_remaining = max(0, HARMONIC_MONTH_DAYS - days_elapsed - (1 if has_partial_day else 0))
    month_percent_dec = (pulses_into_month_dec / HARMONIC_MONTH_PULSES_DEC) * Decimal(100)

    week_idx_raw = days_elapsed // 6
    week_idx = week_idx_raw + 1
    week_name = ETERNAL_WEEK_NAMES[week_idx_raw]
    eternal_week_description = ETERNAL_WEEK_DESCRIPTIONS.get(week_name, "")
    day_of_month = days_elapsed + 1

    pulses_into_week_dec = Decimal(kai_pulse_eternal) % HARMONIC_WEEK_PULSES_DEC
    week_day_idx = int((pulses_into_week_dec / HARMONIC_DAY_PULSES_DEC).to_integral_value(rounding=ROUND_FLOOR)) % len(HARMONIC_DAYS
    )
    week_day_percent_dec = (pulses_into_week_dec / HARMONIC_WEEK_PULSES_DEC) * Decimal(100)

    pulses_into_year_dec = Decimal(kai_pulse_eternal) % HARMONIC_YEAR_PULSES_DEC
    year_percent_dec     = (pulses_into_year_dec / HARMONIC_YEAR_PULSES_DEC) * Decimal(100)
    days_into_year       = harmonic_day_count % HARMONIC_YEAR_DAYS

    solar_seal = f"Solar Kairos (UTC-aligned): {solar_step_string}"
    percent_whole = str(percent_to_next_dec)  # exact-as-string

    eternal_seal = (
        "Eternal Seal: "
        f"Kairos:{chakra_step_str}, {harmonic_day}, {eternal_chakra_arc} Ark • D{day_of_month}/M{eternal_month_idx} • "
        f"Beat:{eternal_beat_idx}/36({str(percent_to_next_dec)}%) Step:{step_idx}/44 "
        f"Kai(Today):{eternal_kai_pulse_today} • "
        f"Y{harmonic_year_idx} PS{phi_spiral_lvl} • {solar_seal} {solar_harmonic_day} "
        f"D{solar_day_of_month}/M{solar_month_index}, {solar_chakra_arc} Ark  "
        f"Beat:{solar_beat_idx}/36 Step:{solar_step_index}/44 • "
        f"Eternal Pulse:{kai_pulse_eternal}"
    )
    seal = f"Day Seal: {chakra_step_str} {str(percent_into_step_dec)}% • D{day_of_month}/M{eternal_month_idx}"
    kairos = f"Kairos: {chakra_step_str}"

    timestamp = (
        f"↳{kairos}"
        f"🕊️ {harmonic_day}(D{week_day_idx + 1}/6) • {eternal_month}(M{eternal_month_idx}/8) • "
        f"{eternal_chakra_arc} Ark({eternal_arc_idx + 1}/6)\n • "
        f"Day:{day_of_month}/42 • Week:({week_idx}/7)\n"
        f" | Kai-Pulse (Today): {eternal_kai_pulse_today}\n"
    )

    narrative = (
        f"In this moment of the Kai-Klock’s dual-day resonance, we are held within the sacred ark of {eternal_chakra_arc}, "
        f"rooted through the harmonic foundation of {harmonic_day}.\n\n"
        f"☀️ Solar Alignment: The living field synchronizes at Kai-Pulse {kai_pulse_today}, placing us in Spiral Beat {solar_beat_idx}, "
        f"guided by the rhythm of Earth’s breath and solar koherense.\n\n"
        f"🌕 Eternal Alignment: At once, the timeless stream flows through Kai-Pulse {eternal_kai_pulse_today}, entering Spiral Beat {eternal_beat_idx}, "
        f"{str(percent_to_next_dec)}% complete — approaching the gateway of harmonic culmination.\n\n"
        f"{eternal_seal}"
    )
    compressed_summary = (
        f"{harmonic_day:<9} • Kairos:{eternal_beat_idx:>2}:{step_idx:<2} "
        f"• D{day_of_month:>2}/M{eternal_month_idx:<1} "
        f"• Step {step_idx:>2}/44 – {str(percent_into_step_dec):>s}% "
        f"• Y{harmonic_year_idx:<2} • Kai-Pulse {eternal_kai_pulse_today}"
    )

    harmonic_ts_desc = (
        f"Today is {harmonic_day}, {HARMONIC_DAY_DESCRIPTIONS[harmonic_day]} "
        f"It is the {day_of_month}{_ordinal(day_of_month)} Day of {eternal_month}, "
        f"{ETERNAL_MONTH_DESCRIPTIONS[eternal_month]} We are in Week {week_idx}, "
        f"{week_name}. {ETERNAL_WEEK_DESCRIPTIONS[week_name]} The Eternal Spiral Beat is {eternal_beat_idx} ("
        f"{eternal_chakra_arc} ark) and we are {str(percent_to_next_dec)}% through it. This korresponds "
        f"to Step {step_idx} of {STEPS_PER_BEAT} (~{str(percent_into_step_dec)}% "
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

    kairos_seal_day_month = f"{eternal_beat_idx:>2}:{step_idx_str:<2} • D{day_of_month:>2}/M{eternal_month_idx}"
    kairos_seal_day_month_percent = f"{eternal_beat_idx:>2}:{step_idx_str:<2} - {str(percent_into_step_dec)}% • D{day_of_month:>2}/M{eternal_month_idx}"
    kairos_seal = f"{eternal_beat_idx:>2}:{step_idx_str:<2} "
    kairos_seal_solar = f"{solar_beat_idx:>2}:{solar_step_index:<2} "
    kairos_seal_solar_day_month = f"{solar_beat_idx:>2}:{solar_step_index:<2} D{solar_day_of_month:>2}/M{solar_month_index}"
    kairos_seal_solar_day_month_percent = f"{solar_beat_idx:>2}:{solar_step_index:<2} - {str(solar_percent_into_step_dec)}% D{solar_day_of_month:>2}/M{solar_month_index}"
    kairos_seal_percent_step_solar = f"{solar_beat_idx:>2}:{solar_step_index:<2} - {str(solar_percent_into_step_dec)}% "
    kairos_seal_percent_step = f"{eternal_beat_idx:>2}:{step_idx_str:<2} - {str(percent_into_step_dec)}% "

    payload = KaiKlockResponse(
        # 1. ⟐ SEALS & NARRATIVE
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

        # 2. ⟐ ETERNAL CALENDAR (Kairos-Aligned)
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
            "percent": str(month_percent_dec),
        },

        # 3. ⟐ SOLAR CALENDAR (Sunrise-Aligned Earth View)
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

        # 4. ⟐ HARMONIC DAY / WEEK STRUCTURE
        harmonicDay=harmonic_day,
        harmonicDayDescription=HARMONIC_DAY_DESCRIPTIONS[harmonic_day],
        weekIndex=week_idx,
        weekName=week_name,
        dayOfMonth=day_of_month,
        harmonicWeekProgress={
            "weekDay": HARMONIC_DAYS[week_day_idx],
            "weekDayIndex": week_day_idx,
            "pulsesIntoWeek": str(pulses_into_week_dec),
            "percent": str(week_day_percent_dec),
        },

        # 5. ⟐ RESONANCE STRUCTURE (Beats, Steps, Arc)
        chakraArc=chakra_arc,
        chakraArcDescription=CHAKRA_ARC_DESCRIPTIONS.get(CHAKRA_ARC_NAME_MAP.get(chakra_arc, ""), ""),
        chakraBeat={
            "beatIndex": solar_beat_idx,
            "pulsesIntoBeat": str(solar_pulse_inbeat_dec),
            "beatPulseCount": str(CHAKRA_BEAT_PULSES_DEC),
            "totalBeats": CHAKRA_BEATS_PER_DAY,
        },
        eternalChakraBeat={
            "beatIndex": eternal_beat_idx,
            "pulsesIntoBeat": str(eternal_pulse_inbeat_dec),
            "percentToNext": str(percent_to_next_dec),
            "beatPulseCount": str(CHAKRA_BEAT_PULSES_DEC),
            "totalBeats": CHAKRA_BEATS_PER_DAY,
        },
        chakraStep=chakra_step_obj,
        chakraStepString=chakra_step_str,
        solarChakraStep=solar_step_payload,
        solarChakraStepString=solar_step_string,

        # 6. ⟐ PHI IDENTITY / SPIRAL LANGUAGE
        phiSpiralLevel=phi_spiral_lvl,
        kaiTurahPhrase=kai_turah_phrase,
        phiSpiralEpochs=generate_phi_spiral_epochs(kai_pulse_eternal),
        subdivisions=build_subdivisions_live(kai_pulse_eternal),  # <— LIVE COUNTS + METADATA (numeric)

        # 7. ⟐ RESONANCE CYCLES (Arc, Micro, Day)
        harmonicLevels={
            "subdivisions": compute_subdivision_counts(kai_pulse_eternal),  # <— precise Decimals per-cycle
            "arcBeat": {
                "pulseInCycle": arc_pos,
                "cycleLength": ARC_BEAT_PULSES,
                "percent": str((Decimal(arc_pos) / Decimal(ARC_BEAT_PULSES)) * Decimal(100)),
            },
            "microCycle": {
                "pulseInCycle": micro_pos,
                "cycleLength": MICRO_CYCLE_PULSES,
                "percent": str((Decimal(micro_pos) / Decimal(MICRO_CYCLE_PULSES)) * Decimal(100)),
            },
            "chakraLoop": {
                "pulseInCycle": chakra_pos,
                "cycleLength": CHAKRA_LOOP_PULSES,
                "percent": str((Decimal(chakra_pos) / Decimal(CHAKRA_LOOP_PULSES)) * Decimal(100)),
            },
            "harmonicDay": {
                "pulseInCycle": day_pos,
                "cycleLength": float(HARMONIC_DAY_PULSES_DEC),  # shape compatibility
                "percent": str((Decimal(day_pos) / HARMONIC_DAY_PULSES_DEC) * Decimal(100)),
            },
        },

        # 8. ⟐ HARMONIC YEAR PROGRESS
        harmonicYearProgress={
            "daysElapsed": days_into_year,
            "daysRemaining": HARMONIC_YEAR_DAYS - days_into_year,
            "percent": str(year_percent_dec),
        },

        # 9. ⟐ COMPOSITE OUTPUTS (Display)
        timestamp=timestamp,
        harmonicTimestampDescription=harmonic_ts_desc,
        kaiMomentSummary=kai_moment,
        compressed_summary=compressed_summary
    )

    return payload
