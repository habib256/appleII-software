#!/usr/bin/env python3
"""« Le Bal des Mares » — clairiere 30, les grenouilles. Sol eolien, 166.

Pages 053, 329, 230. « Le coassement de milliers de grenouilles vous accompagne.
Le sentier debouche sur une clairiere parsemee de mares. D'immenses champignons
se dressent au milieu ; un petit homme est assis sur l'un d'eux, petit et
corpulent, la bouche anormalement large, deux enormes grenouilles le gardent. »

C'est la seule clairiere comique des onze, et la seule ou le Marais fait du
bruit. Le procede de la zone `sud` est garde tel quel — la marche i-VI-III-VII
(Gm-Eb-Bb-F) posee sur un bourdon de sol qui ne bouge pas — mais la melodie
**saute** : presque chaque phrase commence par deux croches ecartees d'une
octave ou d'une quinte, et retombe. Le petit homme est corpulent : ca rebondit
lourdement, ca ne vole pas.

28 mesures a 4/4, 40,5 s. Forme intro(4) - A(8) - B(8) - A' a l'octave(8).

    python3 grenouilles.py && python3 ../../../midi_to_mb.py grenouilles.mid \\
        GRENOUILLES.MB.BIN --bpm 166 --max 2304 --wav GRENOUILLES.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 166, 4, 28
LEN = BAR * BARS

CHORDS = (["Gm", "Gm", "Bb", "Gm"]
          + ["Gm", "Eb", "F", "Cm", "Bb", "Eb", "Dm", "Gm"]
          + ["Cm", "Bb", "Eb", "F", "Gm", "Eb", "Cm", "Dm"]
          + ["Gm", "Eb", "F", "Cm", "Bb", "Eb", "Dm", "Gm"])
assert len(CHORDS) == BARS

MEL = [
    "D5:2 G5:2",                      "G5:1 D5:1 G5:2",
    "Bb5:2 A5:2",                     "G5:2 D5:2",
    "G5:.5 D6:.5 G5:1 Bb5:2",         "Eb6:.5 Bb5:.5 Eb6:1 G5:2",
    "F5:.5 F6:.5 D6:1 Bb5:2",         "C6:1 G5:1 D6:2",
    "Bb5:.5 F6:.5 D6:1 Bb5:2",        "Eb6:1 C6:1 G5:2",
    "D6:.5 A5:.5 D6:1 F6:2",          "G5:2 D6:2",
    "C6:.5 G6:.5 Eb6:1 C6:2",         "Bb5:1 F6:1 D6:2",
    "Eb6:.5 G6:.5 Eb6:1 Bb5:2",       "F6:1 D6:1 A5:2",
    "G5:.5 G6:.5 D6:1 Bb5:2",         "Eb6:1 Bb5:1 G6:2",
    "C6:.5 G6:.5 Eb6:1 C6:2",         "D6:1 A5:1 F6:2",
    "G5:.5 D6:.5 G6:1 Bb5:2",         "Eb6:.5 Bb5:.5 Eb6:1 G6:2",
    "F6:.5 C6:.5 F6:1 D6:2",          "C6:1 G6:1 Eb6:2",
    "Bb5:.5 F6:.5 D6:1 Bb5:2",        "Eb6:1 G6:1 Bb5:2",
    "D6:.5 A5:.5 D6:1 F6:2",          "G6:2 G5:2",
]
assert len(MEL) == BARS

CTR = [
    "G3:2 D4:2",                      "Bb3:2 G3:2",
    "D4:2 F4:2",                      "G3:2 Bb3:2",
    "D4:2 G3:2",                      "Bb3:2 G4:2",
    "C4:2 A3:2",                      "Eb4:2 C4:2",
    "F4:2 D4:2",                      "G4:2 Eb4:2",
    "A3:2 D4:2",                      "Bb3:2 G3:2",
    "Eb4:2 C4:2",                     "D4:2 F4:2",
    "G4:2 Bb3:2",                     "C4:2 A3:2",
    "D4:2 G3:2",                      "Bb3:2 G4:2",
    "Eb4:2 C4:2",                     "F4:2 A3:2",
    "D4:2 G3:2",                      "Bb3:2 G4:2",
    "C4:2 A3:2",                      "Eb4:2 G3:2",
    "F4:2 D4:2",                      "G4:2 Eb4:2",
    "A3:2 D4:2",                      "G3:2 D4:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("G", "eolien", BPM, BAR, "Le Bal des Mares")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 0.5, (0, 2, 1, 2), lo=57))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    # la basse rebondit elle aussi : fondamentale, saut a la quinte grave, retour
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 1), (-1, 1), (0, 1), (-1, 1)], lo=50))
    p.add("bourdon", pedal(midi("G2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("grenouilles.mid"))
