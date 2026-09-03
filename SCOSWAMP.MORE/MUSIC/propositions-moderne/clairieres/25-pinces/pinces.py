#!/usr/bin/env python3
"""« L'Herbe qui Serre » — clairiere 25, l'Herbe a Pinces. Mi phrygien, 176.

Pages 388, 263, 033, 187. « Elle pousse si vite qu'on peut la voir bouger. Et
tandis que vous l'observez, des pinces apparaissent aux extremites de ses
tiges. » La piece garde le procede de la zone `danger` — le demi-ton phrygien,
ici **fa-mi**, et un bourdon de mi qui ne bouge jamais — mais son caractere est
la **pince** : l'arpege a un trou a chaque quatrieme croche (0, 2, 1, silence),
si bien que l'accompagnement claque au lieu de couler, et la melodie mord la
meme seconde mineure fa-mi en croches a chaque fois qu'elle repart.

C'est la plus rapide des onze clairieres : l'herbe pousse plus vite que vous.

32 mesures a 4/4, 43,6 s. Forme intro(4) - A(8) - B(8) - A' a l'octave(8) - coda(4).

    python3 pinces.py && python3 ../../../midi_to_mb.py pinces.mid \\
        PINCES.MB.BIN --bpm 176 --max 2304 --wav PINCES.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 176, 4, 32
LEN = BAR * BARS

CHORDS = (["Em", "Em", "F", "F"]
          + ["Em", "F", "Em", "Dm", "C", "F", "Em", "Em"]
          + ["Am", "F", "C", "G", "Am", "Dm", "F", "Em"]
          + ["Em", "F", "Em", "Dm", "C", "G", "F", "Em"]
          + ["Am", "F", "F", "Em"])
assert len(CHORDS) == BARS

MEL = [
    "E5:4",                           "E5:2 F5:2",
    "F5:2 E5:2",                      "G5:2 F5:2",
    "E5:.5 F5:.5 E5:1 B5:2",          "C6:.5 B5:.5 A5:1 F5:2",
    "E5:.5 F5:.5 G5:1 B5:2",          "A5:1 F5:1 D5:2",
    "C6:1 A5:1 E5:2",                 "F5:.5 E5:.5 C6:1 A5:2",
    "B5:1 G5:1 E5:2",                 "E5:.5 F5:.5 E5:1 G5:2",
    "A5:1 C6:1 E6:2",                 "F6:.5 E6:.5 C6:1 A5:2",
    "G5:1 C6:1 E6:2",                 "D6:1 B5:1 G5:2",
    "A5:1 E6:1 C6:2",                 "D6:.5 C6:.5 A5:1 F5:2",
    "F6:1 C6:1 A5:2",                 "B5:1 G5:1 E5:2",
    "E6:.5 F6:.5 E6:1 B5:2",          "C6:.5 B5:.5 A5:1 F6:2",
    "E6:.5 F6:.5 G6:1 B5:2",          "A5:1 F5:1 D6:2",
    "C6:1 A5:1 E6:2",                 "D6:1 B5:1 G6:2",
    "F6:.5 E6:.5 C6:1 A5:2",          "E6:2 B5:2",
    "A5:1 C6:1 E6:2",                 "F6:.5 E6:.5 C6:1 A5:2",
    "F6:2 E6:2",                      "E6:4",
]
assert len(MEL) == BARS

CTR = [
    "B3:2 E4:2",                      "G3:2 B3:2",
    "A3:2 C4:2",                      "C4:2 A3:2",
    "B3:2 G3:2",                      "A3:2 C4:2",
    "B3:2 E4:2",                      "A3:2 F4:2",
    "G3:2 E4:2",                      "A3:2 C4:2",
    "B3:2 G3:2",                      "E4:2 B3:2",
    "A3:2 C4:2",                      "C4:2 A3:2",
    "G3:2 E4:2",                      "B3:2 D4:2",
    "C4:2 A3:2",                      "D4:2 F4:2",
    "A3:2 C4:2",                      "B3:2 G3:2",
    "E4:2 B3:2",                      "A3:2 C4:2",
    "B3:2 E4:2",                      "F4:2 D4:2",
    "E4:2 C4:2",                      "D4:2 B3:2",
    "C4:2 A3:2",                      "B3:2 G3:2",
    "A3:2 E4:2",                      "C4:2 A3:2",
    "F4:2 C4:2",                      "E4:2 B3:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("E", "phrygien", BPM, BAR, "L'Herbe qui Serre")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    # la pince : trois croches puis un trou, huit fois par mesure
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 0.5, (0, 2, 1, None), lo=57))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 1), (0, 1), (-1, 1), (0, 1)], lo=45))
    p.add("bourdon", pedal(midi("E2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("pinces.mid"))
