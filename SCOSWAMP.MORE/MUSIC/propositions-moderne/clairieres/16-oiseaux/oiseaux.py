#!/usr/bin/env python3
"""« La Maitresse des Oiseaux » — clairiere 16. Mi dorien, 168.

Variation dans la couleur `sud` : le **bourdon de tonique qui ne bouge jamais**
et la large marche modale de la zone, mais en dorien au lieu d'eolien — le do
diese eclaircit tout, et c'est exactement ce que dit la page 304 : « le Marais
devient moins lugubre et ressemble de plus en plus a une jungle tropicale ».

Le procede propre a la clairiere est l'**arpege en sauts** : au lieu de monter
son accord degre par degre, il bondit de la fondamentale a la quinte et retombe
— des oiseaux, pas de l'eau. La melodie repond en croches breves accolees
(mesures 5, 6, 8, 10, 21-24), le babil du Perroquet rouge et jaune.

La section B est la page 149 : la clairiere ou la Maitresse n'est pas, les
plumes eparses, « un silence leger ». Tout s'y allonge en blanches, l'arpege
seul continue, et le tempo ne change pas — c'est la seule facon d'avoir du
silence quand on n'a que six ondes carrees.

28 mesures a 4/4, 40,0 s. Forme intro(4) - A(8) - B(8) - A'(8).

    python3 oiseaux.py && python3 ../../../midi_to_mb.py oiseaux.mid \\
        OISEAUX.MB.BIN --bpm 168 --max 2304 --wav OISEAUX.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 168, 4, 28
LEN = BAR * BARS

CHORDS = (["Em", "Em", "D", "D"]
          + ["Em", "G", "A", "Bm", "Em", "D", "A", "Em"]
          + ["G", "D", "Bm", "A", "G", "A", "Em", "F#m"]
          + ["Em", "G", "A", "Bm", "Em", "A", "D", "Em"])
assert len(CHORDS) == BARS

MEL = [
    "B4:4",                           "B4:2 E5:2",
    "D5:2 F#5:2",                     "A4:2 B4:2",
    "E5:.5 G5:.5 B5:1 A5:2",          "G5:.5 B5:.5 D6:1 B5:2",
    "A5:1 C#6:1 E6:2",                "D6:.5 B5:.5 F#5:1 B5:2",
    "E5:1 G5:1 B5:2",                 "F#5:.5 A5:.5 D6:1 A5:2",
    "C#6:1 E6:1 A6:2",                "G6:1.5 E6:.5 B5:2",
    "D6:2 B5:2",                      "A5:2 F#5:2",
    "B5:4",                           "C#6:2 A5:2",
    "B5:2 G5:2",                      "E6:2 C#6:2",
    "B5:1 D6:1 E6:2",                 "C#6:1.5 A5:.5 F#5:2",
    "E6:.5 G6:.5 B6:1 A6:2",          "G6:.5 D6:.5 B5:1 D6:2",
    "E6:1 C#6:1 A5:2",                "F#6:.5 D6:.5 B5:1 F#5:2",
    "E5:1 B5:1 G5:2",                 "A5:1 C#6:1 E6:2",
    "D6:1 A5:1 F#6:2",                "E6:2 B5:2",
]
assert len(MEL) == BARS

CTR = [
    "B3:2 E4:2",                      "G3:2 B3:2",
    "D4:2 F#4:2",                     "A3:2 D4:2",
    "E4:2 B3:2",                      "G3:2 D4:2",
    "A3:2 C#4:2",                     "F#4:2 B3:2",
    "E4:2 G3:2",                      "D4:2 A3:2",
    "C#4:2 E4:2",                     "B3:2 G3:2",
    "G3:2 D4:2",                      "F#4:2 A3:2",
    "B3:2 D4:2",                      "A3:2 E4:2",
    "G3:2 B3:2",                      "C#4:2 A3:2",
    "E4:2 B3:2",                      "F#4:2 C#4:2",
    "B3:2 E4:2",                      "D4:2 G3:2",
    "E4:2 A3:2",                      "F#4:2 D4:2",
    "G3:2 B3:2",                      "A3:2 C#4:2",
    "D4:2 F#4:2",                     "B3:2 E4:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("E", "dorien", BPM, BAR, "La Maitresse des Oiseaux")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    # l'arpege bondit a la quinte et retombe : des oiseaux, pas de l'eau
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 0.5, (0, 2, 1, 2), lo=54))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 2), (-1, 1), (0, 1)], lo=48))
    p.add("bourdon", pedal(midi("E2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("oiseaux.mid"))
