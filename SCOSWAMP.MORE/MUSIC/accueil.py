#!/usr/bin/env python3
"""« Le Marais aux Scorpions » -- theme d'accueil, proposition n°1.

Trois voix, comme les trois canaux d'une AY-3-8910 : une melodie, un
accompagnement arpege facon luth, une basse. Mode de re dorien, 96 a la
noire, 24 mesures a 4/4 = 60 s, concu pour boucler (la derniere mesure
retombe sur la premiere). Aucune dependance : bibliotheque standard seule.

    python3 accueil.py            # ecrit accueil.mid et accueil.wav a cote

- accueil.mid : trois pistes, canaux 1-3, programme 80 (square lead), a
  importer dans Arkos Tracker 3 pour en faire un AKY ;
- accueil.wav : rendu a ondes carrees, 22 050 Hz mono, pour ecouter ce que
  la Mockingboard jouera, a l'enveloppe pres.

Structure : A (16 mesures, l'appel du village, Dm-C-Am-F) puis B (8 mesures,
plus tendu, G-Dm-Am) qui revient a Dm. Voir DOCS/MUSIQUE.md pour la chaine.
"""
import math
import struct
import wave
from pathlib import Path

BPM = 96
TICKS = 480                      # ticks MIDI par noire
RATE = 22050                     # Hz du rendu WAV

NOTE_OF = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def midi(name):
    """'D5' -> 74, 'Bb3' -> 58."""
    letter, rest = name[0], name[1:]
    acc = 0
    if rest and rest[0] in "#b":
        acc = 1 if rest[0] == "#" else -1
        rest = rest[1:]
    return 12 * (int(rest) + 1) + NOTE_OF[letter] + acc


def bar(spec):
    """'D5:1 F5:1 A5:2' -> [(note, beats), ...] ; '-' = silence."""
    out = []
    for tok in spec.split():
        n, d = tok.split(":")
        out.append((None if n == "-" else midi(n), float(d)))
    return out


# ── La melodie ────────────────────────────────────────────────────────────
MELODY = [
    # A -- l'appel du village
    "D5:1 F5:1 A5:2",            "G5:.5 F5:.5 E5:1 D5:2",
    "E5:1 G5:1 C6:2",            "B5:.5 A5:.5 G5:1 E5:2",
    "D5:1 A5:1 D6:1 C6:1",       "A5:1 F5:1 D5:2",
    "E5:1 A5:1 C6:1 B5:1",       "A5:2 E5:2",
    "F5:1 A5:1 C6:2",            "D6:.5 C6:.5 A5:1 F5:2",
    "E5:1 G5:1 C6:1 D6:1",       "E6:1 D6:1 C6:2",
    "D6:1 A5:1 F5:1 A5:1",       "E5:1 C6:1 B5:1 A5:1",
    "D5:1 F5:1 E5:1 F5:1",       "D5:3 -:1",
    # B -- l'oree du Marais
    "G5:1 B5:1 D6:2",            "E6:.5 D6:.5 B5:1 G5:2",
    "F5:1 A5:1 D6:2",            "E6:.5 D6:.5 A5:1 F5:2",
    "E5:1 A5:1 C6:1 E6:1",       "D6:1 C6:1 B5:1 A5:1",
    "D6:1 C6:1 A5:1 F5:1",       "D5:3 -:1",
]

# ── Les accords, une entree par mesure : (fondamentale, tierce, quinte) ──
CHORDS = (["D4 F4 A4"] * 2 + ["C4 E4 G4"] * 2 + ["D4 F4 A4"] * 2 + ["A3 C4 E4"] * 2
          + ["F4 A4 C5"] * 2 + ["C4 E4 G4"] * 2 + ["D4 F4 A4", "A3 C4 E4", "D4 F4 A4", "D4 F4 A4"]
          + ["G4 B4 D5"] * 2 + ["D4 F4 A4"] * 2 + ["A3 C4 E4"] * 2 + ["D4 F4 A4"] * 2)
BASS = (["D3 A2"] * 2 + ["C3 G2"] * 2 + ["D3 A2"] * 2 + ["A2 E3"] * 2
        + ["F3 C3"] * 2 + ["C3 G2"] * 2 + ["D3 A2", "A2 E3", "D3 A2", "D3 D3"]
        + ["G2 D3"] * 2 + ["D3 A2"] * 2 + ["A2 E3"] * 2 + ["D3 A2", "D3 D3"])
assert len(MELODY) == len(CHORDS) == len(BASS) == 24


def voices():
    """Trois listes de (note MIDI ou None, debut en temps, duree en temps)."""
    mel, acc, bass = [], [], []
    t = 0.0
    for m, c, b in zip(MELODY, CHORDS, BASS):
        for n, d in bar(m):
            mel.append((n, t, d)); t += d
        t0 = t - 4.0
        r, third, fifth = (midi(x) for x in c.split())
        for k, n in enumerate([r, fifth, third, fifth, r, fifth, third, fifth]):
            acc.append((n, t0 + k * 0.5, 0.3))          # detache, comme un luth
        lo, hi = (midi(x) for x in b.split())
        bass.append((lo, t0, 2.0)); bass.append((hi, t0 + 2.0, 2.0))
    return mel, acc, bass


# ── MIDI ──────────────────────────────────────────────────────────────────
def vlq(n):
    out = [n & 0x7F]
    n >>= 7
    while n:
        out.append(0x80 | (n & 0x7F)); n >>= 7
    return bytes(reversed(out))


def track(events, channel, extra=b""):
    """events : (tick, bytes) tries ; produit un chunk MTrk."""
    events.sort(key=lambda e: e[0])
    data = bytearray(extra)
    last = 0
    for tick, msg in events:
        data += vlq(tick - last) + msg; last = tick
    data += vlq(0) + b"\xFF\x2F\x00"
    return b"MTrk" + struct.pack(">I", len(data)) + bytes(data)


def write_midi(path, parts):
    tempo = b"\x00\xFF\x51\x03" + struct.pack(">I", 60_000_000 // BPM)[1:]
    chunks = [track([], 0, tempo + b"\x00\xFF\x58\x04\x04\x02\x18\x08")]
    for ch, (notes, vol) in enumerate(parts):
        ev = [(0, bytes([0xC0 | ch, 80]))]                      # square lead
        for n, t, d in notes:
            if n is None: continue
            a, b = int(t * TICKS), int((t + d) * TICKS)
            ev.append((a, bytes([0x90 | ch, n, vol])))
            ev.append((b, bytes([0x80 | ch, n, 0])))
        chunks.append(track(ev, ch))
    hdr = b"MThd" + struct.pack(">IHHH", 6, 1, len(chunks), TICKS)
    Path(path).write_bytes(hdr + b"".join(chunks))


# ── Rendu a ondes carrees ─────────────────────────────────────────────────
def render_wav(path, parts):
    beat = 60.0 / BPM
    total = int((96 * beat + 0.5) * RATE)
    mix = [0.0] * total
    for notes, vol in parts:
        g = vol / 127.0 * 0.45
        for n, t, d in notes:
            if n is None: continue
            f = 440.0 * 2 ** ((n - 69) / 12.0)
            s0, s1 = int(t * beat * RATE), int((t + d) * beat * RATE)
            length = s1 - s0
            half = RATE / f / 2.0
            for i in range(length):
                # enveloppe : attaque 5 ms, decroissance vers 0,6, relache 25 ms
                x = i / RATE
                env = min(1.0, x / 0.005)
                env *= 0.6 + 0.4 * math.exp(-x * 12.0)
                rem = (length - i) / RATE
                if rem < 0.025: env *= rem / 0.025
                sq = 1.0 if int(i / half) % 2 == 0 else -1.0
                mix[s0 + i] += sq * env * g
    frames = bytearray()
    for v in mix:
        v = max(-1.0, min(1.0, v))
        frames += struct.pack("<h", int(v * 32000))
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
        w.writeframes(bytes(frames))


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    mel, acc, bass = voices()
    parts = [(mel, 100), (acc, 55), (bass, 80)]
    write_midi(here / "accueil.mid", parts)
    render_wav(here / "accueil.wav", parts)
    print("accueil.mid et accueil.wav ecrits :", len(mel), "notes de melodie,",
          len(acc), "d'accompagnement,", len(bass), "de basse ; 60 s a", BPM, "bpm")
