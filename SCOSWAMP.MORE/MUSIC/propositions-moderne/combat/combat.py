#!/usr/bin/env python3
"""« Le Fer et la Pince » — surcouche de combat, 32 pages. Si eolien, 200.

200 a la noire, quinze ticks par temps : la valeur la plus rapide qui tombe
juste sur l'horloge de la carte. L'arpege martele fondamentale-quinte en
croches, la basse frappe le contretemps, le bourdon est sur **fa diese**, la
dominante, pour que rien ne se resolve tant que le combat dure. Les accords
tournent vite (une mesure chacun) et la melodie n'a que des notes longues :
c'est l'accompagnement qui court, pas le theme.

28 mesures a 4/4, 33,6 s — assez court pour reboucler sans lasser pendant les
quatre ou cinq assauts d'un combat.

    python3 combat.py && python3 ../../midi_to_mb.py combat.mid \\
        COMBAT.MB.BIN --bpm 200 --max 2400 --wav COMBAT.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 200, 4, 28
LEN = BAR * BARS

CHORDS = (["Bm", "Bm", "Bm", "Bm"]
          + ["Bm", "G", "D", "A", "Bm", "G", "A", "F#m"]
          + ["Em", "G", "D", "A", "Em", "G", "F#m", "F#m"]
          + ["Bm", "G", "D", "A", "Bm", "Em", "G", "Bm"])
assert len(CHORDS) == BARS

MEL = [
    "F#5:1 F#5:1 B5:2",               "F#5:1 F#5:1 D6:2",
    "B5:1 D6:1 F#6:2",                "E6:1 D6:1 B5:2",
    "B5:1 D6:.5 E6:.5 F#6:2",         "G6:1 F#6:1 D6:2",
    "A5:1 D6:1 F#6:1 A6:1",           "E6:2 C#6:2",
    "B5:1 F#6:1 D6:2",                "G5:1 B5:1 D6:2",
    "C#6:1 E6:1 A6:2",                "F#6:2 C#6:2",
    "E6:1 G6:1 B6:2",                 "A6:1 G6:1 D6:2",
    "F#6:1 A6:1 D6:2",                "E6:1 C#6:1 A5:2",
    "B5:1 E6:1 G6:2",                 "D6:1 B5:1 G5:2",
    "A5:1 C#6:1 F#6:2",               "E6:1 C#6:1 A5:2",
    "B5:1 D6:.5 E6:.5 F#6:2",         "G6:1 F#6:1 D6:2",
    "A6:1 F#6:1 D6:2",                "E6:1 A6:1 C#6:2",
    "F#6:1 D6:1 B5:2",                "G6:1 E6:1 B5:2",
    "D6:1 G6:1 B6:2",                 "F#6:2 B5:2",
]
assert len(MEL) == BARS

CTR = [
    "B3:2 F#4:2",                     "B3:2 D4:2",
    "F#4:2 B3:2",                     "D4:2 F#4:2",
    "B3:2 F#4:2",                     "G3:2 D4:2",
    "A3:2 D4:2",                      "E4:2 C#4:2",
    "B3:2 F#4:2",                     "G3:2 D4:2",
    "C#4:2 E4:2",                     "F#4:2 C#4:2",
    "E4:2 B3:2",                      "G3:2 D4:2",
    "A3:2 D4:2",                      "E4:2 C#4:2",
    "B3:2 E4:2",                      "G3:2 D4:2",
    "C#4:2 F#4:2",                    "A3:2 C#4:2",
    "B3:2 F#4:2",                     "G3:2 D4:2",
    "A3:2 F#4:2",                     "E4:2 C#4:2",
    "F#4:2 B3:2",                     "G3:2 E4:2",
    "D4:2 B3:2",                      "F#4:2 B3:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("B", "eolien", BPM, BAR, "Le Fer et la Pince")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    # quinte a vide martelee en croches : fondamentale, quinte, fondamentale...
    p.add("quintes", arpeggio(CHORDS, 0, BAR, 0.5, (0, 2, 0, 2), lo=57))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    # basse : le coup, le contretemps, puis la quinte grave tenue
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 1), (0, .5), (-1, .5), (0, 2)], lo=48))
    p.add("bourdon", pedal(midi("F#2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("combat.mid"))
