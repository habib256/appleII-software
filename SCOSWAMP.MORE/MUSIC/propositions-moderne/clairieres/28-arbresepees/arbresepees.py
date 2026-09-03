#!/usr/bin/env python3
"""« Les Bras qui Repoussent » — clairiere 28, les Arbres-Epees. Fa phrygien, 166.

Pages 157, 279, 022. « Chaque bras tient une epee a son extremite. » Et si l'on
revient : « les branches des terribles Arbres-Epees ont deja repousse. »

Le procede de la zone `danger` est la : demi-ton phrygien **sol bemol-fa**,
bourdon de fa immobile. Le caractere de la clairiere, lui, est la **repousse**,
et il est ecrit comme tel : la cellule de trois notes fa-solb-fa que la melodie
lance mesure 5 revient au contre-chant, deux octaves plus bas, mesure 6 — puis
encore mesures 18 et 22. On coupe le motif, il repousse ailleurs. C'est un canon
court, le seul des onze clairieres.

La basse frappe les quatre noires sans jamais s'arreter : ce sont les lames.

28 mesures a 4/4, 40,5 s. Forme intro(4) - A(8) - B(8) - A' a l'octave(8).

    python3 arbresepees.py && python3 ../../../midi_to_mb.py arbresepees.mid \\
        ARBRESEPEES.MB.BIN --bpm 166 --max 2304 --wav ARBRESEPEES.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 166, 4, 28
LEN = BAR * BARS

CHORDS = (["Fm", "Fm", "Gb", "Gb"]
          + ["Fm", "Ab", "Gb", "Bbm", "Db", "Ebm", "Ab", "Fm"]
          + ["Bbm", "Gb", "Ab", "Db", "Ebm", "Fm", "Db", "Fm"]
          + ["Fm", "Ab", "Gb", "Bbm", "Db", "Gb", "Ab", "Fm"])
assert len(CHORDS) == BARS

MEL = [
    "C6:4",                           "C6:2 F6:2",
    "Db6:2 C6:2",                     "Bb5:2 C6:2",
    "F5:1 Gb5:1 F5:2",                "Ab5:1 C6:1 Ab5:2",
    "Gb5:1 F5:1 Db6:2",               "C6:2 Bb5:2",
    "Db6:1 Ab5:1 F5:2",               "Eb6:1 Bb5:1 Gb5:2",
    "F6:1.5 Db6:.5 Ab5:2",            "C6:1 Ab5:1 F5:2",
    "Bb5:1 F6:1 Db6:2",               "Gb6:1 Db6:1 Bb5:2",
    "Ab5:1 Eb6:1 C6:2",               "Db6:1 Ab5:1 F6:2",
    "Eb6:1 Bb5:1 Gb6:2",              "F6:1 Ab6:1 C6:2",
    "Db6:1.5 C6:.5 Ab5:2",            "C6:2 F5:2",
    "F6:1 Gb6:1 F6:2",                "Ab6:1 F6:1 C6:2",
    "Gb6:1 F6:1 Db6:2",               "C6:2 Bb5:2",
    "Db6:1 F6:1 Ab6:2",               "Gb6:1 Db6:1 Bb5:2",
    "C6:1.5 Db6:.5 C6:2",             "F6:2 C6:2",
]
assert len(MEL) == BARS

CTR = [
    "C4:2 F4:2",                      "Ab3:2 C4:2",
    "Db4:2 Ab3:2",                    "Gb3:2 Ab3:2",
    "C4:2 Ab3:2",                     "F4:1 Gb4:1 F4:2",
    "Db4:2 Ab3:2",                    "F4:2 Bb3:2",
    "Ab3:2 Db4:2",                    "Gb4:1 Bb3:1 Eb4:2",
    "C4:2 Ab3:2",                     "F4:2 C4:2",
    "Bb3:2 F4:2",                     "Db4:2 Gb3:2",
    "Eb4:2 C4:2",                     "Ab3:2 Db4:2",
    "Bb3:2 Gb4:2",                    "F4:1 Gb4:1 F4:2",
    "Ab3:2 Db4:2",                    "C4:2 Ab3:2",
    "F4:2 C4:2",                      "F4:1 Gb4:1 F4:2",
    "Db4:2 Ab3:2",                    "Gb3:2 Db4:2",
    "Ab3:2 F4:2",                     "Db4:2 Bb3:2",
    "Eb4:2 C4:2",                     "C4:2 Ab3:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("F", "phrygien", BPM, BAR, "Les Bras qui Repoussent")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 0.5, (0, 2, 1, 2), lo=57))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 1), (0, 1), (-1, 1), (0, 1)], lo=46))
    p.add("bourdon", pedal(midi("F2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("arbresepees.mid"))
