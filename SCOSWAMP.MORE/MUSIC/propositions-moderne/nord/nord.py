#!/usr/bin/env python3
"""« Le Bois des Guetteurs » — le Marais nord. Mi eolien, 150 a la noire.

Un ostinato fixe de quatre croches, mi-si-sol-si, qui ne change jamais pendant
que les accords bougent dessous : c'est le regard qui suit le joueur d'une
clairiere a l'autre. Sur si mineur, le sol devient une sixte mineure et le
motif mord ; c'est tout le sujet de la zone.

28 mesures a 4/4, 44,8 s. Forme intro(4) - A(8) - B(8) - A'(8), le A' une
octave au-dessus.

    python3 nord.py && python3 ../../midi_to_mb.py nord.mid \\
        MARAISNO.MB.BIN --bpm 150 --max 2304 --wav MARAISNO.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 150, 4, 28
LEN = BAR * BARS

CHORDS = (["Em", "Em", "Em", "Em"]
          + ["Em", "C", "G", "D", "Em", "C", "Am", "Bm"]
          + ["C", "G", "D", "Em", "Am", "Bm", "C", "D"]
          + ["Em", "C", "G", "D", "Em", "Am", "C", "Em"])
assert len(CHORDS) == BARS

MEL = [
    "B5:4",                           "B5:2 D6:2",
    "E6:4",                           "D6:2 B5:2",
    "E5:1 G5:1 B5:2",                 "C6:1.5 B5:.5 G5:2",
    "D6:1 B5:1 G5:1 A5:1",            "F#5:2 A5:2",
    "B5:1 E6:1 D6:2",                 "C6:1 B5:1 G5:2",
    "A5:1 C6:1 E6:1 D6:1",            "B5:2 F#5:2",
    "G5:1 C6:1 E6:2",                 "D6:1.5 B5:.5 D6:2",
    "A5:1 D6:1 F#6:2",                "E6:2 B5:2",
    "C6:1 A5:1 E6:2",                 "D6:1 F#6:1 B6:2",
    "A6:1 G6:1 E6:1 C6:1",            "D6:2 A5:2",
    "E6:1 G6:1 B6:2",                 "A6:1.5 G6:.5 E6:2",
    "B5:1 D6:1 G6:1 D6:1",            "F#6:2 A6:2",
    "B5:1 E6:1 G6:2",                 "A5:1 C6:1 E6:2",
    "G6:1 E6:1 C6:1 B5:1",            "E6:4",
]
assert len(MEL) == BARS

CTR = [
    "B3:2 E4:2",                      "B3:2 D4:2",
    "E4:2 G4:2",                      "F#4:2 D4:2",
    "E4:2 G4:2",                      "E4:2 C4:2",
    "D4:2 B3:2",                      "A3:2 D4:2",
    "B3:2 E4:2",                      "G4:2 E4:2",
    "A3:2 C4:2",                      "B3:2 D4:2",
    "C4:2 E4:2",                      "B3:2 G4:2",
    "A3:2 F#4:2",                     "G4:2 E4:2",
    "A3:2 C4:2",                      "D4:2 F#4:2",
    "G4:2 E4:2",                      "F#4:2 A4:2",
    "B3:2 E4:2",                      "C4:2 G4:2",
    "B3:2 D4:2",                      "A3:2 F#4:2",
    "G4:2 E4:2",                      "A3:2 C4:2",
    "G4:2 E4:2",                      "B3:2 E4:2",
]
assert len(CTR) == BARS

WATCH = [midi("E4"), midi("B4"), midi("G4"), midi("B4")]       # les guetteurs


def build():
    p = Piece("E", "eolien", BPM, BAR, "Le Bois des Guetteurs")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    p.add("ostinato", ostinato(WATCH, 0.5, 0, LEN))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 1), (0, 1), (-1, 1), (0, 1)], lo=45))
    p.add("bourdon", pedal(midi("E2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("nord.mid"))
