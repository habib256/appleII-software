#!/usr/bin/env python3
"""« La Licorne Blessee » — clairiere 23. Fa eolien, 138.

Variation dans la couleur `sud` : c'est la piece des douze qui reprend le plus
franchement le procede de la zone — la marche i-VI-III-VII (Fm-Db-Ab-Eb, celle
de `MARAISUD.MB` transposee) sur un **bourdon de tonique** qui ne bouge pas. Le
Marais est le meme ; l'animal, non.

Ce qui appartient a la clairiere, c'est la **noblesse** : la section A est en
blanches, sans une croche a la melodie, chose qu'aucune autre des douze ne fait
— l'animal blanc est couche au centre de la clairiere, page 320. Puis « elle se
releve cependant et baisse sa corne vers vous en lancant un grognement qui
ressemble fort a un defi » : la section B passe au **rythme pointe**, la meme
melodie redressee, et monte jusqu'au sol aigu de la mesure 19. La reprise
retrouve les blanches : la Licorne se recouche, ou s'en va (page 265).

24 mesures a 4/4, 41,7 s. Forme intro(4) - A(8) l'animal couche - B(8) le defi -
A'(4).

    python3 licorne.py && python3 ../../../midi_to_mb.py licorne.mid \\
        LICORNE.MB.BIN --bpm 138 --max 2304 --wav LICORNE.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 138, 4, 24
LEN = BAR * BARS

CHORDS = (["Fm", "Fm", "Db", "Db"]
          + ["Fm", "Db", "Ab", "Eb", "Fm", "Bbm", "Cm", "Fm"]
          + ["Db", "Ab", "Eb", "Bbm", "Db", "Eb", "Cm", "Fm"]
          + ["Fm", "Db", "Eb", "Fm"])
assert len(CHORDS) == BARS

MEL = [
    "C5:4",                           "C5:2 F5:2",
    "Ab4:2 C5:2",                     "Db5:2 C5:2",
    "F5:2 C6:2",                      "Ab5:2 F5:2",
    "Eb6:2 C6:2",                     "Bb5:1.5 G5:.5 Eb5:2",
    "C6:1 Ab5:1 F5:2",                "Db6:2 Bb5:2",
    "Eb6:1 C6:1 G5:2",                "F5:2 C6:2",
    "Ab5:1.5 Bb5:.5 Db6:2",           "C6:1.5 Eb6:.5 Ab5:2",
    "Bb5:1.5 G5:.5 Eb6:2",            "F6:1.5 Db6:.5 Bb5:2",
    "Ab5:1 Db6:1 F6:2",               "Eb6:1.5 Bb5:.5 G5:2",
    "C6:1 Eb6:1 G6:2",                "F6:1.5 C6:.5 Ab5:2",
    "C6:2 F6:2",                      "Ab5:2 Db6:2",
    "Bb5:1 G5:1 Eb5:2",               "F5:4",
]
assert len(MEL) == BARS

CTR = [
    "C4:2 Ab3:2",                     "F4:2 C4:2",
    "Db4:2 Ab3:2",                    "F4:2 Ab3:2",
    "C4:2 Ab3:2",                     "Db4:2 F4:2",
    "Eb4:2 C4:2",                     "Bb3:2 G3:2",
    "Ab3:2 C4:2",                     "Db4:2 Bb3:2",
    "G3:2 Eb4:2",                     "C4:2 Ab3:2",
    "F4:2 Db4:2",                     "Eb4:2 C4:2",
    "Bb3:2 G3:2",                     "Db4:2 F4:2",
    "Ab3:2 Db4:2",                    "G3:2 Bb3:2",
    "Eb4:2 C4:2",                     "Ab3:2 F4:2",
    "C4:2 Ab3:2",                     "F4:2 Db4:2",
    "Bb3:2 Eb4:2",                    "C4:2 Ab3:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("F", "eolien", BPM, BAR, "La Licorne Blessee")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 0.5, (0, 1, 2, 1), lo=54))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 2), (-1, 1), (0, 1)], lo=48))
    p.add("bourdon", pedal(midi("F2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("licorne.mid"))
