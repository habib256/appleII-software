#!/usr/bin/env python3
"""« Le Seul Passage » — clairiere 15, le pont sur la Croupie. Si bemol dorien, 150.

Variation dans la couleur `riviere` : dorien, **bourdon sur la quinte** (fa),
arpege de croches sans arret. Mais la zone regarde l'eau ; cette piece la
traverse. D'ou la basse en noires marchees, quatre pas par mesure, du debut a
la fin : c'est le seul endroit du Marais ou l'on passe du nord au sud
(`CARTOGRAPHIE.md` § 1), et la musique y marche.

La section B est la page 045 — « ce pont vous parait trop simple ; il doit sans
doute dissimuler un piege ». La melodie s'y resserre dans une quinte, repete ses
notes, tourne autour de re bemol sans oser conclure. Puis la reprise repart une
octave plus haut : on a traverse.

26 mesures a 4/4, 41,6 s. Forme intro(4) - A(8) la traversee - B(8) le soupcon -
A'(6) la reprise, a l'octave.

    python3 pont.py && python3 ../../../midi_to_mb.py pont.mid \\
        PONT.MB.BIN --bpm 150 --max 2304 --wav PONT.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 150, 4, 26
LEN = BAR * BARS

CHORDS = (["Bbm", "Bbm", "Ab", "Ab"]
          + ["Bbm", "Fm", "Db", "Eb", "Bbm", "Ab", "Eb", "Bbm"]
          + ["Db", "Ab", "Eb", "Cm", "Db", "Eb", "Fm", "Fm"]
          + ["Bbm", "Db", "Ab", "Eb", "Bbm", "Bbm"])
assert len(CHORDS) == BARS

MEL = [
    "Bb4:4",                          "Bb4:2 F5:2",
    "Ab4:2 C5:2",                     "Eb5:4",
    "Bb4:1 Db5:1 F5:2",               "Ab5:1 F5:1 C5:2",
    "Db5:1 F5:1 Ab5:2",               "Bb5:1.5 Ab5:.5 Eb5:2",
    "F5:1 Bb5:1 Db6:2",               "C6:1 Ab5:1 Eb5:2",
    "F5:1 Bb5:1 Eb6:2",               "Db6:1.5 Bb5:.5 F5:2",
    "Db5:1 F5:1 Ab5:1 F5:1",          "Eb5:1 C5:1 Ab4:2",
    "Bb4:1 Eb5:1 G5:2",               "Ab5:1 Eb5:1 C5:2",
    "Db5:1 Ab5:1 F5:2",               "Eb5:1 G5:1 Bb5:2",
    "C6:1 Ab5:1 F5:2",                "F5:2 C6:2",
    "Bb5:1 Db6:1 F6:2",               "Ab5:1 Db6:1 F6:2",
    "Eb6:1 C6:1 Ab5:2",               "Bb5:1 Eb6:1 G6:2",
    "F6:1.5 Db6:.5 Bb5:2",            "Bb5:4",
]
assert len(MEL) == BARS

CTR = [
    "Bb3:2 Db4:2",                    "F4:2 Bb3:2",
    "Ab3:2 C4:2",                     "Eb4:2 Ab3:2",
    "Bb3:2 Db4:2",                    "C4:2 Ab3:2",
    "Db4:2 F4:2",                     "Eb4:2 Bb3:2",
    "F4:2 Db4:2",                     "Ab3:2 Eb4:2",
    "Bb3:2 G4:2",                     "Db4:2 Bb3:2",
    "Ab3:2 F4:2",                     "C4:2 Eb4:2",
    "Bb3:2 G4:2",                     "Eb4:2 C4:2",
    "Db4:2 Ab3:2",                    "G4:2 Eb4:2",
    "C4:2 Ab3:2",                     "F4:2 C4:2",
    "Db4:2 Bb3:2",                    "F4:2 Ab3:2",
    "Eb4:2 C4:2",                     "Bb3:2 G4:2",
    "F4:2 Db4:2",                     "Bb3:2 F4:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("Bb", "dorien", BPM, BAR, "Le Seul Passage")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 0.5, (0, 1, 2, 1), lo=54))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    # quatre pas par mesure : on traverse
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 1), (0, 1), (-1, 1), (0, 1)], lo=48))
    p.add("bourdon", pedal(midi("F2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("pont.mid"))
