# kai_klock.py  •  v2.4 “Step Resonance”  (KKS v1 grid parity)
from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, Union, List
from decimal import Decimal, getcontext, ROUND_FLOOR

from kai_klock_models import KaiKlockResponse, ChakraStep

# ════════════════════════════════════════════════════════════════
#  Kai-Klock Harmonic Timestamp System  •  v2.4 “Step Resonance”
#  • KKS v1 parity: beat/step indexing & percents on μ-pulse grid:
#      36 beats/day × 44 steps/beat × 11 pulses/step = 17,424 pulses/day
#  • Exact φ breath for time (3 + √5) in Decimal; no float rounding in core.
#  • Deterministic floor for all implicit integer conversions.
#  • FIX: project φ-day μpulses → 17,424-grid before beat/step math (TS parity)
# ════════════════════════════════════════════════════════════════

# ── Constants ───────────────────────────────────────────────────
PHI = (1 + math.sqrt(5)) / 2  # compatibility

getcontext().prec = 60
getcontext().rounding = ROUND_FLOOR

# φ-exact breath (pulse duration) — 3 + √5
KAI_PULSE_DURATION_DEC = Decimal(3) + Decimal(5).sqrt()
KAI_PULSE_DURATION = float(KAI_PULSE_DURATION_DEC)  # compatibility only

# Sunrise anchor
SOLAR_GENESIS_UTC_MS = 1715400806000  # 2024-05-11T04:13:26.000Z
ETERNAL_GENESIS_PULSE = datetime(2024, 5, 10, 6, 45, 41, 888000, tzinfo=timezone.utc)  # 1715323541888 ms
genesis_sunrise       = datetime(2024, 5, 11, 4, 13, 26, 0, tzinfo=timezone.utc)

# ── μpulse canon (1 pulse = 1,000,000 μpulses) ──────────────────
UPULSES_PER_PULSE = 1_000_000
UPULSES_PER_DAY   = 17_491_270_421  # exact μpulses/day (φ-exact daily closure)

# 17,424-grid (exact integers)
GRID_PULSES_PER_STEP = 11
GRID_STEPS_PER_BEAT  = 44
GRID_PULSES_PER_BEAT = GRID_PULSES_PER_STEP * GRID_STEPS_PER_BEAT  # 484
GRID_BEATS_PER_DAY   = 36
GRID_PULSES_PER_DAY  = GRID_PULSES_PER_BEAT * GRID_BEATS_PER_DAY   # 17,424

UPULSES_PER_GRID_STEP = GRID_PULSES_PER_STEP * UPULSES_PER_PULSE
UPULSES_PER_GRID_BEAT = GRID_PULSES_PER_BEAT * UPULSES_PER_PULSE
UPULSES_PER_GRID_DAY  = GRID_PULSES_PER_DAY  * UPULSES_PER_PULSE

# φ day and derived periods (Decimal) — used for calendar/epochs/etc (not beats/steps)
HARMONIC_DAY_PULSES_DEC   = Decimal("17491.270421")
HARMONIC_MONTH_DAYS       = 42
HARMONIC_YEAR_DAYS        = 336
HARMONIC_MONTH_PULSES_DEC = HARMONIC_DAY_PULSES_DEC * Decimal(HARMONIC_MONTH_DAYS)
HARMONIC_YEAR_PULSES_DEC  = HARMONIC_MONTH_PULSES_DEC * Decimal(8)
HARMONIC_WEEK_PULSES_DEC  = HARMONIC_DAY_PULSES_DEC * Decimal(6)

# Steps (grid truth)
PULSES_PER_STEP = GRID_PULSES_PER_STEP    # 11
STEPS_PER_BEAT  = GRID_STEPS_PER_BEAT     # 44
CHAKRA_BEATS_PER_DAY = GRID_BEATS_PER_DAY # 36

# ── Helpers ─────────────────────────────────────────────────────
def _ensure_utc(dt: datetime) -> datetime:
    return dt if dt.tzinfo is not None else dt.replace(tzinfo=timezone.utc)

def _dec_total_seconds(d: timedelta) -> Decimal:
    return (Decimal(d.days) * Decimal(86400)
            + Decimal(d.seconds)
            + (Decimal(d.microseconds) / Decimal(1_000_000)))

def mu_since_genesis(at: datetime) -> int:
    """Exact Chronos→μpulses: floor((seconds / (3+√5)) * 1e6)."""
    at = _ensure_utc(at)
    delta = at - ETERNAL_GENESIS_PULSE
    sec_dec = _dec_total_seconds(delta)
    pulses_dec = sec_dec / KAI_PULSE_DURATION_DEC
    mu_dec = pulses_dec * Decimal(UPULSES_PER_PULSE)
    return int(mu_dec.to_integral_value(rounding=ROUND_FLOOR))

def mu_at(dt: datetime) -> int:
    return mu_since_genesis(_ensure_utc(dt))

def solar_window_mu(now: datetime) -> tuple[int, int, int, int]:
    """
    Return (mu_last, mu_next, mu_now, solar_day_index) for the sunrise-anchored solar day,
    all in μpulses, using the exact φ-day tiling from the stored genesis_sunrise.
    """
    now = _ensure_utc(now)
    mu_now = mu_since_genesis(now)
    mu_sunrise0 = mu_at(genesis_sunrise)
    mu_since_sunrise = mu_now - mu_sunrise0
    solar_day_index = mu_since_sunrise // UPULSES_PER_DAY
    mu_last = mu_sunrise0 + solar_day_index * UPULSES_PER_DAY
    mu_next = mu_last + UPULSES_PER_DAY
    return mu_last, mu_next, mu_now, int(solar_day_index)

# ── Subdivisions (derived from φ breath) ────────────────────────
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
RESONANT_NAMES = {
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

def compute_subdivision_counts(kai_pulse_eternal: int) -> dict[str, dict[str, Decimal]]:
    seconds_elapsed = Decimal(kai_pulse_eternal) * KAI_PULSE_DURATION_DEC
    out: dict[str, dict[str, Decimal]] = {}
    for name, duration in SUBDIVISIONS.items():
        out[name] = {"duration": duration, "count": seconds_elapsed / duration}
    return out

def build_subdivisions_live(kai_pulse_eternal: int) -> Dict[str, Dict[str, Union[float, str]]]:
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

# ── Epoch scaffolding ───────────────────────────────────────────
def _floor_log_phi(n: int) -> int:
    if n <= 1:
        return 0
    phi_dec = (Decimal(1) + Decimal(5).sqrt()) / Decimal(2)
    N = Decimal(n)
    lo, hi = 0, 512
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if (phi_dec ** Decimal(mid)) <= N:
            lo = mid
        else:
            hi = mid - 1
    return lo

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
    powers = [0, 1, 2, 3, 5, 8, 13, 21]
    labels = ["Eternal Year","Phi Epok","Phi Resonanse Epok","Tri-Spiral Gate",
              "Great Harmonic Ring","Kai-Cycle of Return","Solar Spiral Era","One Breath of Erah Voh"]
    descriptions = [e[2] for e in EPOCHS_PHI]
    base = HARMONIC_YEAR_PULSES_DEC
    phi_dec = (Decimal(1) + Decimal(5).sqrt()) / Decimal(2)
    spiral_epochs: List[Dict] = []
    for i, p in enumerate(powers):
        pulses_dec = base * (phi_dec ** Decimal(p))
        pulses_int = int(pulses_dec.to_integral_value(rounding=ROUND_FLOOR))
        kai_until = max(pulses_int - int(kai_pulse_eternal), 0)
        approx_days = (Decimal(pulses_int) * KAI_PULSE_DURATION_DEC) / Decimal(86400)
        days_until = (Decimal(kai_until) * KAI_PULSE_DURATION_DEC) / Decimal(86400)
        percent_until = (Decimal(kai_pulse_eternal) / Decimal(pulses_int)) * Decimal(100) if pulses_int else Decimal(0)
        spiral_epochs.append({
            "name": labels[i], "phiPower": p, "kaiPulses": pulses_int,
            "approxDays": str(approx_days), "description": descriptions[i],
            "kaiUntil": kai_until, "daysUntil": str(days_until), "percentUntil": str(percent_until),
        })
    return spiral_epochs

# ── Calendar text ───────────────────────────────────────────────
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

# ── Cycle durations (Kai-Pulses) ────────────────────────────────
ARC_BEAT_PULSES       = 6
MICRO_CYCLE_PULSES    = 60
CHAKRA_LOOP_PULSES    = 360

# ── Utility ─────────────────────────────────────────────────────
def _ordinal(n: int) -> str:
    if 11 <= n % 100 <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")

# ── Grid projection helper (φ-day μ → 17,424-grid μ; exact integer math) ─────
def _mu_project_to_grid(mu_in_phi_day: int) -> int:
    """
    Project μpulses within a φ-day (length = UPULSES_PER_DAY) onto the semantic
    17,424-grid (length = UPULSES_PER_GRID_DAY) exactly, matching SovereignSolar.ts:
        muGrid = (muInto * MU_PER_GRID_DAY) / MU_PER_DAY
    """
    return (mu_in_phi_day * UPULSES_PER_GRID_DAY) // UPULSES_PER_DAY

# ════════════════════════════════════════════════════════════════
#  Main generator (KKS v1 grid parity for beats/steps)
# ════════════════════════════════════════════════════════════════
def get_eternal_klock(now: Optional[datetime] = None) -> KaiKlockResponse:
    now = _ensure_utc(now or datetime.utcnow())

    # μpulse windowing
    mu_last, mu_next, mu_now, solar_day_index = solar_window_mu(now)
    mu_span = UPULSES_PER_DAY
    mu_into_solar_day   = mu_now - mu_last
    mu_days_since_genesis = mu_now // mu_span
    mu_into_eternal_day = mu_now - mu_days_since_genesis * mu_span

    # Whole-pulse counters
    kai_pulse_eternal       = int(mu_now // UPULSES_PER_PULSE)
    kai_pulse_today         = int(mu_into_solar_day // UPULSES_PER_PULSE)
    eternal_kai_pulse_today = int(mu_into_eternal_day // UPULSES_PER_PULSE)

    # ── GRID (KKS v1) beat + step indexing (μ-pulse lattice with projection) ───
    # Eternal grid (project φ-day μ → 17,424-grid μ, then index)
    mu_grid_eternal    = _mu_project_to_grid(mu_into_eternal_day)
    mu_in_beat_eternal = mu_grid_eternal % UPULSES_PER_GRID_BEAT
    mu_in_step_eternal = mu_in_beat_eternal % UPULSES_PER_GRID_STEP

    eternal_beat_idx = int(mu_grid_eternal // UPULSES_PER_GRID_BEAT)          # 0..35
    eternal_step_idx = int(mu_in_beat_eternal // UPULSES_PER_GRID_STEP)       # 0..43

    eternal_grid_pulses_into_beat_dec = Decimal(mu_in_beat_eternal) / Decimal(UPULSES_PER_PULSE)  # 0..484
    eternal_percent_into_step_dec     = (Decimal(mu_in_step_eternal) / Decimal(UPULSES_PER_GRID_STEP)) * Decimal(100)
    eternal_percent_of_beat_dec       = (Decimal(mu_in_beat_eternal) / Decimal(UPULSES_PER_GRID_BEAT)) * Decimal(100)

    # Solar grid (sunrise-anchored lattice; same projection)
    mu_grid_solar    = _mu_project_to_grid(mu_into_solar_day)
    mu_in_beat_solar = mu_grid_solar % UPULSES_PER_GRID_BEAT
    mu_in_step_solar = mu_in_beat_solar % UPULSES_PER_GRID_STEP

    solar_beat_idx = int(mu_grid_solar // UPULSES_PER_GRID_BEAT)              # 0..35
    solar_step_idx = int(mu_in_beat_solar // UPULUSES_PER_GRID_STEP)          # 0..43

    solar_grid_pulses_into_beat_dec = Decimal(mu_in_beat_solar) / Decimal(UPULSES_PER_PULSE)      # 0..484
    solar_percent_into_step_dec     = (Decimal(mu_in_step_solar) / Decimal(UPULSES_PER_GRID_STEP)) * Decimal(100)
    solar_percent_of_beat_dec       = (Decimal(mu_in_beat_solar) / Decimal(UPULSES_PER_GRID_BEAT)) * Decimal(100)

    # Clamp + tidy percentages
    q = Decimal("0.000001")
    eternal_percent_into_step_dec = min(Decimal("99.999999"), max(Decimal(0), eternal_percent_into_step_dec)).quantize(q)
    eternal_percent_of_beat_dec   = min(Decimal("99.999999"), max(Decimal(0), eternal_percent_of_beat_dec)).quantize(q)
    solar_percent_into_step_dec   = min(Decimal("99.999999"), max(Decimal(0), solar_percent_into_step_dec)).quantize(q)
    solar_percent_of_beat_dec     = min(Decimal("99.999999"), max(Decimal(0), solar_percent_of_beat_dec)).quantize(q)

    # Strings / objects
    chakra_step_str   = f"{eternal_beat_idx}:{eternal_step_idx:02d}"
    solar_step_string = f"{solar_beat_idx}:{solar_step_idx:02d}"

    chakra_step_obj = ChakraStep(
        stepIndex=eternal_step_idx,
        percentIntoStep=str(eternal_percent_into_step_dec),
        stepsPerBeat=STEPS_PER_BEAT,
    )
    solar_step_payload = ChakraStep(
        stepIndex=solar_step_idx,
        percentIntoStep=str(solar_percent_into_step_dec),
        stepsPerBeat=STEPS_PER_BEAT,
    )

    # ── Calendrics (φ durations; independent of grid) ───────────
    harmonic_day_count_dec = Decimal(kai_pulse_eternal) / HARMONIC_DAY_PULSES_DEC
    harmonic_day_count     = int(harmonic_day_count_dec.to_integral_value(rounding=ROUND_FLOOR))
    harmonic_year_idx      = int((Decimal(kai_pulse_eternal) / HARMONIC_YEAR_PULSES_DEC).to_integral_value(rounding=ROUND_FLOOR))
    harmonic_month_raw     = int((Decimal(kai_pulse_eternal) / HARMONIC_MONTH_PULSES_DEC).to_integral_value(rounding=ROUND_FLOOR))

    eternal_year_name = ("Year of Eternal Restoration" if harmonic_year_idx == 0
                         else "Year of Harmonik Embodiment" if harmonic_year_idx == 1
                         else f"Year {harmonic_year_idx + 1}")
    kai_turah_phrase  = KAI_TURAH_PHRASES[harmonic_year_idx % len(KAI_TURAH_PHRASES)]

    eternal_month_idx = (harmonic_month_raw % 8) + 1
    eternal_month     = ETERNAL_MONTH_NAMES[eternal_month_idx - 1]
    harmonic_day      = HARMONIC_DAYS[harmonic_day_count % len(HARMONIC_DAYS)]

    arc_div_dec = HARMONIC_DAY_PULSES_DEC / Decimal(6)
    arc_idx         = int((Decimal(kai_pulse_today)         / arc_div_dec).to_integral_value(rounding=ROUND_FLOOR))
    eternal_arc_idx = int((Decimal(eternal_kai_pulse_today) / arc_div_dec).to_integral_value(rounding=ROUND_FLOOR))
    arc_idx = min(5, arc_idx); eternal_arc_idx = min(5, eternal_arc_idx)
    chakra_arc        = CHAKRA_ARCS[arc_idx]
    eternal_chakra_arc= CHAKRA_ARCS[eternal_arc_idx]
    solar_chakra_arc  = chakra_arc

    # Solar calendar pieces
    solar_day_of_month      = (solar_day_index % HARMONIC_MONTH_DAYS) + 1
    solar_month_index       = ((solar_day_index // HARMONIC_MONTH_DAYS) % 8) + 1
    solar_month_name        = ETERNAL_MONTH_NAMES[solar_month_index - 1]
    solar_day_name          = HARMONIC_DAYS[solar_day_index % len(HARMONIC_DAYS)]
    solar_month_description = ETERNAL_MONTH_DESCRIPTIONS[solar_month_name]
    solar_day_description   = HARMONIC_DAY_DESCRIPTIONS[solar_day_name]
    solar_harmonic_day      = HARMONIC_DAYS[solar_day_index % len(HARMONIC_DAYS)]
    solar_week_index        = ((solar_day_index // 6) % 7) + 1
    solar_week_name         = ETERNAL_WEEK_NAMES[(solar_day_index // 6) % 7]
    solar_week_description  = ETERNAL_WEEK_DESCRIPTIONS[solar_week_name]

    # Phi spiral level
    phi_spiral_lvl = _floor_log_phi(kai_pulse_eternal)

    # Month/day progress (φ durations)
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
    week_day_idx = int((pulses_into_week_dec / HARMONIC_DAY_PULSES_DEC).to_integral_value(rounding=ROUND_FLOOR)) % len(HARMONIC_DAYS)
    week_day_percent_dec = ((pulses_into_week_dec / HARMONIC_WEEK_PULSES_DEC) * Decimal(100)).quantize(q)

    pulses_into_year_dec = Decimal(kai_pulse_eternal) % HARMONIC_YEAR_PULSES_DEC
    year_percent_dec     = (pulses_into_year_dec / HARMONIC_YEAR_PULSES_DEC) * Decimal(100)
    days_into_year       = harmonic_day_count % HARMONIC_YEAR_DAYS

    # Seals / strings (grid beats)
    solar_seal = f"Solar Kairos (UTC-aligned): {solar_step_string}"
    eternal_seal = (
        "Eternal Seal: "
        f"Kairos:{chakra_step_str}, {harmonic_day}, {eternal_chakra_arc} Ark • D{day_of_month}/M{eternal_month_idx} • "
        f"Beat:{eternal_beat_idx}/36({str(eternal_percent_of_beat_dec)}%) Step:{eternal_step_idx}/44 "
        f"Kai(Today):{eternal_kai_pulse_today} • "
        f"Y{harmonic_year_idx} PS{phi_spiral_lvl} • {solar_seal} {solar_harmonic_day} "
        f"D{solar_day_of_month}/M{solar_month_index}, {solar_chakra_arc} Ark  "
        f"Beat:{solar_beat_idx}/36 Step:{solar_step_idx}/44 • "
        f"Eternal Pulse:{kai_pulse_eternal}"
    )
    seal = f"Day Seal: {chakra_step_str} {str(eternal_percent_into_step_dec)}% • D{day_of_month}/M{eternal_month_idx}"
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
        f"guided by Earth’s breath and solar koherense.\n\n"
        f"🌕 Eternal Alignment: The timeless stream flows through Kai-Pulse {eternal_kai_pulse_today}, entering Spiral Beat {eternal_beat_idx}, "
        f"{str(eternal_percent_of_beat_dec)}% complete — approaching the gateway of harmonic culmination.\n\n"
        f"{eternal_seal}"
    )

    compressed_summary = (
        f"{harmonic_day:<9} • Kairos:{eternal_beat_idx:02d}:{eternal_step_idx:02d} "
        f"• D{day_of_month:>2}/M{eternal_month_idx} "
        f"• Step {eternal_step_idx:>2}/44 – {str(eternal_percent_into_step_dec)}% "
        f"• Y{harmonic_year_idx:<2} • Kai-Pulse {eternal_kai_pulse_today}"
    )

    harmonic_ts_desc = (
        f"Today is {harmonic_day}, {HARMONIC_DAY_DESCRIPTIONS[harmonic_day]} "
        f"It is the {day_of_month}{_ordinal(day_of_month)} Day of {eternal_month}, "
        f"{ETERNAL_MONTH_DESCRIPTIONS[eternal_month]} We are in Week {week_idx}, "
        f"{week_name}. {ETERNAL_WEEK_DESCRIPTIONS[week_name]} The Eternal Spiral Beat is {eternal_beat_idx} ("
        f"{eternal_chakra_arc} ark) and we are {str(eternal_percent_of_beat_dec)}% through it. This korresponds "
        f"to Step {eternal_step_idx} of 44 (~{str(eternal_percent_into_step_dec)}% into the step). "
        f"This is the {eternal_year_name.lower()}, resonating at Phi Spiral Level {phi_spiral_lvl}. "
        f"{eternal_seal}"
    )

    kai_moment = (
        f"↳ {seal} • Kai-Pulse {eternal_kai_pulse_today}, Beat {eternal_beat_idx}, Step {eternal_step_idx} "
        f"{harmonic_day} Day, Month of {eternal_month}, Week of {week_name.split()[-1]}, Spiral Level {phi_spiral_lvl}."
    )

    # ── OUTPUT (grid beats for beat/step; φ for calendar) ───────
    kairos_seal_day_month = f"{eternal_beat_idx:02d}:{eternal_step_idx:02d} • D{day_of_month:02d}/M{eternal_month_idx}"
    kairos_seal_day_month_percent = f"{eternal_beat_idx:02d}:{eternal_step_idx:02d} - {str(eternal_percent_into_step_dec)}% • D{day_of_month:02d}/M{eternal_month_idx}"
    kairos_seal = f"{eternal_beat_idx:02d}:{eternal_step_idx:02d}"
    kairos_seal_solar = f"{solar_beat_idx:02d}:{solar_step_idx:02d}"
    kairos_seal_solar_day_month = f"{solar_beat_idx:02d}:{solar_step_idx:02d} D{solar_day_of_month:02d}/M{solar_month_index}"
    kairos_seal_solar_day_month_percent = f"{solar_beat_idx:02d}:{solar_step_idx:02d} - {str(solar_percent_into_step_dec)}% D{solar_day_of_month:02d}/M{solar_month_index}"
    kairos_seal_percent_step_solar = f"{solar_beat_idx:02d}:{solar_step_idx:02d} - {str(solar_percent_into_step_dec)}%"
    kairos_seal_percent_step = f"{eternal_beat_idx:02d}:{eternal_step_idx:02d} - {str(eternal_percent_into_step_dec)}%"

    payload = KaiKlockResponse(
        # 1) Seals & narrative
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

        # 2) Eternal calendar (φ durations)
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

        # 3) Solar calendar (φ durations)
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

        # 4) Harmonic day/week structure
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

        # 5) Resonance structure (GRID beats/steps ONLY)
        chakraArc=chakra_arc,
        chakraArcDescription=CHAKRA_ARC_DESCRIPTIONS.get(CHAKRA_ARC_NAME_MAP.get(chakra_arc, ""), ""),
        chakraBeat={
            "beatIndex": solar_beat_idx,
            "pulsesIntoBeat": str(solar_grid_pulses_into_beat_dec),  # 0..484 (grid pulses)
            "beatPulseCount": str(GRID_PULSES_PER_BEAT),             # "484"
            "totalBeats": CHAKRA_BEATS_PER_DAY,                      # 36
        },
        eternalChakraBeat={
            "beatIndex": eternal_beat_idx,
            "pulsesIntoBeat": str(eternal_grid_pulses_into_beat_dec),# 0..484 (grid pulses)
            "percentToNext": str(eternal_percent_of_beat_dec),       # beat % on grid
            "beatPulseCount": str(GRID_PULSES_PER_BEAT),             # "484"
            "totalBeats": CHAKRA_BEATS_PER_DAY,                      # 36
        },
        chakraStep=chakra_step_obj,
        chakraStepString=chakra_step_str,
        solarChakraStep=solar_step_payload,
        solarChakraStepString=solar_step_string,

        # 6) Phi identity / spiral language
        phiSpiralLevel=phi_spiral_lvl,
        kaiTurahPhrase=kai_turah_phrase,
        phiSpiralEpochs=generate_phi_spiral_epochs(kai_pulse_eternal),
        subdivisions=build_subdivisions_live(kai_pulse_eternal),

        # 7) Resonance cycles (φ day progress for these aggregates is fine)
        harmonicLevels={
            "subdivisions": compute_subdivision_counts(kai_pulse_eternal),
            "arcBeat": {
                "pulseInCycle": kai_pulse_eternal % ARC_BEAT_PULSES,
                "cycleLength": ARC_BEAT_PULSES,
                "percent": str((Decimal(kai_pulse_eternal % ARC_BEAT_PULSES) / Decimal(ARC_BEAT_PULSES)) * Decimal(100)),
            },
            "microCycle": {
                "pulseInCycle": kai_pulse_eternal % MICRO_CYCLE_PULSES,
                "cycleLength": MICRO_CYCLE_PULSES,
                "percent": str((Decimal(kai_pulse_eternal % MICRO_CYCLE_PULSES) / Decimal(MICRO_CYCLE_PULSES)) * Decimal(100)),
            },
            "chakraLoop": {
                "pulseInCycle": kai_pulse_eternal % CHAKRA_LOOP_PULSES,
                "cycleLength": CHAKRA_LOOP_PULSES,
                "percent": str((Decimal(kai_pulse_eternal % CHAKRA_LOOP_PULSES) / Decimal(CHAKRA_LOOP_PULSES)) * Decimal(100)),
            },
            "harmonicDay": {
                "pulseInCycle": eternal_kai_pulse_today,
                "cycleLength": float(HARMONIC_DAY_PULSES_DEC),
                "percent": str((Decimal(eternal_kai_pulse_today) / HARMONIC_DAY_PULSES_DEC) * Decimal(100)),
            },
        },

        # 8) Harmonic year progress
        harmonicYearProgress={
            "daysElapsed": days_into_year,
            "daysRemaining": HARMONIC_YEAR_DAYS - days_into_year,
            "percent": str(year_percent_dec),
        },

        # 9) Composite outputs (display)
        timestamp=timestamp,
        harmonicTimestampDescription=harmonic_ts_desc,
        kaiMomentSummary=kai_moment,
        compressed_summary=compressed_summary
    )

    return payload
