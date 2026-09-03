#!/usr/bin/env python3
"""« Ce qui Reste du Combat » — clairiere 24. Mi eolien, 160.

Variation dans la couleur `sud` : **bourdon de tonique immobile** et la marche
i-VI-III-VII de la zone (Em-C-G-D), mais prise a 160 et jouee **pointee**. Le
rythme long-bref du premier temps est le procede propre a la clairiere : il
revient a chaque mesure de A et de A', et c'est tout ce qui separe cette piece
d'un theme de voyage. On n'est pas dans un combat — la page 010 ne montre que
ses traces : « le sol est foule, l'herbe humide tachee de sang, et deux fleches
sont encore plantees dans un arbre ».

La section B est la fouille : la melodie quitte le pointe, monte par degres
jusqu'au sol aigu de la mesure 17 et redescend sur si mineur — le seul accord
mineur non-diatonique du tour, l'attention des ennemis caches que le texte
promet a qui s'attarde. La reprise remet le pointe et conclut sur la tonique :
on est parti.

28 mesures a 4/4, 42,0 s. Forme intro(4) - A(8) les traces - B(8) la fouille -
A'(8).

    python3 arene.py && python3 ../../../midi_to_mb.py arene.mid \\
        ARENE.MB.BIN --bpm 160 --max 2304 --wav ARENE.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 160, 4, 28
LEN = BAR * BARS

CHORDS = (["Em", "Em", "C", "C"]
          + ["Em", "C", "G", "D", "Em", "Am", "Bm", "Em"]
          + ["C", "G", "D", "Am", "C", "D", "Em", "Bm"]
          + ["Em", "C", "G", "D", "Am", "C", "D", "Em"])
assert len(CHORDS) == BARS

MEL = [
    "B4:4",                           "B4:2 E5:2",
    "C5:2 G5:2",                      "D5:2 B4:2",
    "E5:1.5 G5:.5 B5:2",              "C6:1.5 B5:.5 G5:2",
    "D6:1.5 B5:.5 G5:2",              "A5:1.5 F#5:.5 D5:2",
    "E5:1 B5:1 G5:2",                 "C6:1.5 A5:.5 E5:2",
    "F#5:1 B5:1 D6:2",                "E6:2 B5:2",
    "G5:1 C6:1 E6:2",                 "D6:1 B5:1 G5:2",
    "F#5:1 A5:1 D6:2",                "E6:1.5 C6:.5 A5:2",
    "G6:2 E6:2",                      "F#6:1.5 D6:.5 A5:2",
    "B5:1 E6:1 G6:2",                 "F#6:1.5 D6:.5 B5:2",
    "E6:1.5 G6:.5 B5:2",              "C6:1.5 E6:.5 G5:2",
    "D6:1.5 G6:.5 B5:2",              "A5:1.5 D6:.5 F#5:2",
    "E6:1 C6:1 A5:2",                 "G5:1 E6:1 C6:2",
    "D6:1 F#6:1 A6:2",                "E6:4",
]
assert len(MEL) == BARS

CTR = [
    "E4:2 B3:2",                      "G3:2 E4:2",
    "C4:2 E4:2",                      "G3:2 C4:2",
    "B3:2 E4:2",                      "C4:2 G3:2",
    "D4:2 B3:2",                      "A3:2 F#4:2",
    "E4:2 G3:2",                      "A3:2 C4:2",
    "F#4:2 D4:2",                     "B3:2 E4:2",
    "C4:2 G3:2",                      "D4:2 B3:2",
    "A3:2 F#4:2",                     "C4:2 E4:2",
    "G3:2 C4:2",                      "D4:2 A3:2",
    "E4:2 B3:2",                      "F#4:2 D4:2",
    "B3:2 E4:2",                      "G3:2 C4:2",
    "D4:2 B3:2",                      "F#4:2 A3:2",
    "C4:2 E4:2",                      "G3:2 C4:2",
    "A3:2 D4:2",                      "E4:2 B3:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("E", "eolien", BPM, BAR, "Ce qui Reste du Combat")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 0.5, (0, 1, 2, 1), lo=54))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    # quatre noires martelees : la marche de ceux qui sont passes par la
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 1), (0, 1), (-1, 1), (0, 1)], lo=48))
    p.add("bourdon", pedal(midi("E2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("arene.mid"))
