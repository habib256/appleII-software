#!/usr/bin/env python3
"""« La Nuee » — clairiere 19, la clairiere des scorpions. Re phrygien, 180.

Variation dans la couleur `danger` : le mode **phrygien**, donc le demi-ton pose
juste au-dessus de la tonique — ici mi bemol contre re — et le **bourdon de
tonique** immobile, exactement le procede de `DANGER.MB`. Ce qui change, c'est
la vitesse : 180 a la noire, le tempo le plus rapide des douze, parce que la
page 118 ne laisse pas le choix (« des dizaines de petits scorpions accourent
vers vous. Tentez votre Chance ») et que la page 319 s'appelle « Vous vous hatez
de choisir une direction ».

Le procede propre a la clairiere est le **grouillement** : la melodie attaque
presque chaque mesure par deux ou quatre doubles croches avant de se poser. Ce
sont les seules doubles du dossier ; elles ne durent qu'un temps, mais elles
suffisent a faire courir la piece. La derniere mesure lache la nuee et ne garde
que le frottement mi bemol - re, seul, tenu.

24 mesures a 4/4, 32,0 s. Forme intro(4) - A(8) - B(8) l'assaut - A'(4).

    python3 scorpions.py && python3 ../../../midi_to_mb.py scorpions.mid \\
        SCORPIONS.MB.BIN --bpm 180 --max 2304 --wav SCORPIONS.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 180, 4, 24
LEN = BAR * BARS

CHORDS = (["Dm", "Dm", "Eb", "Eb"]
          + ["Dm", "Eb", "Gm", "Cm", "Bb", "F", "Eb", "Dm"]
          + ["Gm", "F", "Eb", "Bb", "Cm", "Gm", "Eb", "Dm"]
          + ["Dm", "Eb", "Cm", "Dm"])
assert len(CHORDS) == BARS

MEL = [
    "A4:.5 Bb4:.5 A4:1 A4:2",         "A4:.5 Bb4:.5 A4:1 D5:2",
    "Bb4:.5 C5:.5 Bb4:1 G4:2",        "Eb5:2 D5:2",
    "D5:.25 F5:.25 A5:.5 D6:1 A5:2",  "Eb5:.25 G5:.25 Bb5:.5 Eb6:1 Bb5:2",
    "D6:.5 Bb5:.5 G5:1 D5:2",         "Eb5:.25 G5:.25 C6:.5 G5:1 Eb5:2",
    "F5:.5 D6:.5 Bb5:1 F5:2",         "A5:.25 C6:.25 F6:.5 C6:1 A5:2",
    "Bb5:.5 Eb6:.5 Bb5:1 G5:2",       "A5:.5 F5:.5 D5:1 A5:2",
    "G5:.25 A5:.25 Bb5:.25 D6:.25 G6:1 D6:2",
    "F6:.25 C6:.25 A5:.25 F5:.25 C6:1 A5:2",
    "Eb6:.5 Bb5:.5 G5:1 Eb6:2",
    "D6:.25 F6:.25 D6:.25 Bb5:.25 F5:1 D6:2",
    "C6:.5 Eb6:.5 G6:1 Eb6:2",
    "D6:.25 Bb5:.25 G5:.25 D5:.25 Bb5:1 G5:2",
    "Eb5:.5 G5:.5 Bb5:1 Eb6:2",       "A5:.5 D6:.5 A5:1 F5:2",
    "D5:.25 F5:.25 A5:.5 D6:1 A5:2",  "Eb6:.5 D6:.5 Eb6:1 Bb5:2",
    "G5:.5 Eb5:.5 C5:1 G5:2",         "D5:.5 Eb5:.5 D5:3",
]
assert len(MEL) == BARS

CTR = [
    "D4:2 F4:2",                      "A3:2 D4:2",
    "Bb3:2 Eb4:2",                    "G3:2 Bb3:2",
    "D4:2 A3:2",                      "Eb4:2 Bb3:2",
    "G3:2 D4:2",                      "C4:2 Eb4:2",
    "Bb3:2 F4:2",                     "A3:2 C4:2",
    "Eb4:2 Bb3:2",                    "D4:2 A3:2",
    "G3:2 Bb3:2",                     "C4:2 A3:2",
    "Eb4:2 G3:2",                     "F4:2 D4:2",
    "Eb4:2 C4:2",                     "Bb3:2 G3:2",
    "G3:2 Eb4:2",                     "A3:2 D4:2",
    "F4:2 D4:2",                      "Bb3:2 Eb4:2",
    "Eb4:2 C4:2",                     "A3:2 D4:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("D", "phrygien", BPM, BAR, "La Nuee")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 0.5, (0, 1, 2, 1), lo=54))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    # quatre noires des la premiere mesure : rien ne se met en place, on court
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 1), (0, 1), (-1, 1), (0, 1)], lo=48))
    p.add("bourdon", pedal(midi("D2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("scorpions.mid"))
