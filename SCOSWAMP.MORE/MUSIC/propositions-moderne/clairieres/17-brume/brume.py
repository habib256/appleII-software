#!/usr/bin/env python3
"""« La Brume Fetide » — clairiere 17. Do eolien, 128.

Variation dans la couleur `sud` : eolien comme la zone, **bourdon de tonique
immobile** comme la zone, mais transpose sur do et pris par le bas. Le procede
propre a la clairiere est la **descente** : la page 094 commence par « le sentier
descend », et la section A descend en effet, une mesure apres l'autre, do-si
bemol-la bemol-sol-fa-do, sans jamais remonter.

La section B est le moment ou l'on ne peut plus retenir son souffle : la melodie
frotte le la bemol contre le sol, la meme paire six fois, et l'atmosphere viciee
coute deux points d'ENDURANCE. La basse reste en blanches d'un bout a l'autre —
c'est la piece la plus lourde des douze, et la plus lente autorisee.

22 mesures a 4/4, 41,3 s. Forme intro(4) - A(6) la descente - B(6) l'odeur -
A'(6) la brume se referme.

    python3 brume.py && python3 ../../../midi_to_mb.py brume.mid \\
        BRUME.MB.BIN --bpm 128 --max 2304 --wav BRUME.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 128, 4, 22
LEN = BAR * BARS

CHORDS = (["Cm", "Cm", "Ab", "Ab"]
          + ["Cm", "Bb", "Ab", "Gm", "Fm", "Cm"]
          + ["Ab", "Eb", "Bb", "Fm", "Ab", "Gm"]
          + ["Cm", "Ab", "Bb", "Fm", "Gm", "Cm"])
assert len(CHORDS) == BARS

MEL = [
    "C5:4",                           "C5:2 Eb5:2",
    "C5:2 Ab4:2",                     "Eb5:2 C5:2",
    "C6:2 G5:2",                      "Bb5:2 F5:2",
    "Ab5:1 Eb5:1 C5:2",               "G5:2 D5:2",
    "F5:1 C5:1 Ab5:2",                "G5:2 Eb5:2",
    "Ab5:1 G5:1 Ab5:2",               "Bb5:1 G5:1 Eb5:2",
    "D6:1 C6:1 Bb5:2",                "C6:1 Ab5:1 F5:2",
    "Eb6:2 C6:2",                     "D6:1 Bb5:1 G5:2",
    "G5:2 C6:2",                      "Eb6:1 C6:1 Ab5:2",
    "F6:1 D6:1 Bb5:2",                "C6:1 Ab5:1 F5:2",
    "Bb5:1 G5:1 D5:2",                "C5:4",
]
assert len(MEL) == BARS

CTR = [
    "C4:2 Eb4:2",                     "G3:2 C4:2",
    "Ab3:2 C4:2",                     "Eb4:2 Ab3:2",
    "C4:2 G3:2",                      "Bb3:2 F4:2",
    "Ab3:2 Eb4:2",                    "G3:2 Bb3:2",
    "F4:2 Ab3:2",                     "Eb4:2 C4:2",
    "Ab3:2 C4:2",                     "G3:2 Eb4:2",
    "Bb3:2 D4:2",                     "F4:2 C4:2",
    "Eb4:2 Ab3:2",                    "Bb3:2 G3:2",
    "C4:2 G3:2",                      "Ab3:2 Eb4:2",
    "Bb3:2 F4:2",                     "Ab3:2 C4:2",
    "G3:2 Bb3:2",                     "Eb4:2 C4:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("C", "eolien", BPM, BAR, "La Brume Fetide")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    # l'arpege monte de trois sons et retombe : les tourbillons de brume
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 0.5, (0, 1, 2, 1), lo=54))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    # deux blanches, rien de plus : on avance a peine
    p.add("basse", progression(CHORDS, 0, BAR, [(0, 2), (-1, 2)], lo=48))
    p.add("bourdon", pedal(midi("C2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("brume.mid"))
