#!/usr/bin/env python3
"""« Ce qui Monte du Bassin » — clairiere 35, la Bete du bassin. Fa eolien, 143.

Pages 209, 082, 308, 397. « Une creature enorme a la peau brune et caoutchouteuse
emerge soudain du bassin et tente de vous saisir d'un tentacule. Un magnifique
Bijou Violet brille a son front. »

Le procede de la zone `sud` est garde : marche i-VI-III-VII (Fm-Db-Ab-Eb) sur un
bourdon de fa immobile. Deux choses sont a cette clairiere seule.

**Ce qui monte** : la basse ne descend jamais. Chaque mesure elle part de la
quinte grave et remonte l'accord — quinte, fondamentale, tierce, quinte — au
lieu de tourner autour de sa fondamentale comme partout ailleurs. Quelque chose
sort de l'eau a chaque mesure et n'y retourne pas.

**Le Bijou Violet** : le seul accord majeur eclatant du morceau, le re bemol
(VI), porte aux mesures 13, 18 et 22 la note la plus haute de la piece, tenue une
blanche. C'est la seule chose qui brille dans le bassin, et c'est ce que le
joueur vient chercher.

28 mesures a 4/4, 47,0 s. Forme intro(4) - A(8) - B(8) - A' a l'octave(8).

    python3 bassin.py && python3 ../../../midi_to_mb.py bassin.mid \\
        BASSIN.MB.BIN --bpm 143 --max 2304 --wav BASSIN.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 143, 4, 28
LEN = BAR * BARS

CHORDS = (["Fm", "Fm", "Db", "Fm"]
          + ["Fm", "Db", "Ab", "Eb", "Fm", "Bbm", "Cm", "Fm"]
          + ["Db", "Ab", "Bbm", "Eb", "Fm", "Db", "Eb", "Fm"]
          + ["Fm", "Db", "Ab", "Bbm", "Eb", "Db", "Eb", "Fm"])
assert len(CHORDS) == BARS

MEL = [
    "C6:4",                           "C6:2 F6:2",
    "Db6:2 C6:2",                     "Ab5:2 C6:2",
    "F5:1 Ab5:1 C6:2",                "Db6:2 Ab5:2",
    "C6:1 Eb6:1 Ab5:2",               "Bb5:1 G5:1 Eb6:2",
    "F6:1 C6:1 Ab5:2",                "Bb5:1 Db6:1 F6:2",
    "Eb6:1 C6:1 G5:2",                "F5:2 C6:2",
    "Db6:1 F6:1 Ab6:2",               "Eb6:1 C6:1 Ab5:2",
    "Bb5:1 F6:1 Db6:2",               "Eb6:2 Bb5:2",
    "C6:1 Ab5:1 F6:2",                "Db6:1 Ab6:1 F6:2",
    "Eb6:1 Bb5:1 G5:2",               "F5:2 Ab5:2",
    "F6:1 Ab6:1 C6:2",                "Db6:2 Ab6:2",
    "C6:1 Eb6:1 Ab6:2",               "Bb5:1 F6:1 Db6:2",
    "Eb6:1 G5:1 Bb5:2",               "Db6:1 Ab5:1 F6:2",
    "Eb6:1.5 C6:.5 Ab5:2",            "F6:2 C6:2",
]
assert len(MEL) == BARS

CTR = [
    "F4:2 C4:2",                      "Ab3:2 C4:2",
    "F4:2 Db4:2",                     "C4:2 Ab3:2",
    "C4:2 Ab3:2",                     "F4:2 Db4:2",
    "Eb4:2 C4:2",                     "Bb3:2 G4:2",
    "Ab3:2 C4:2",                     "Db4:2 Bb3:2",
    "Eb4:2 G4:2",                     "C4:2 Ab3:2",
    "F4:2 Ab4:2",                     "C4:2 Eb4:2",
    "Db4:2 Bb3:2",                    "G4:2 Eb4:2",
    "Ab3:2 C4:2",                     "F4:2 Db4:2",
    "Bb3:2 G4:2",                     "C4:2 Ab3:2",
    "C4:2 F4:2",                      "Ab4:2 Db4:2",
    "C4:2 Eb4:2",                     "F4:2 Db4:2",
    "Bb3:2 Eb4:2",                    "Db4:2 Ab3:2",
    "G4:2 Eb4:2",                     "C4:2 Ab3:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("F", "eolien", BPM, BAR, "Ce qui Monte du Bassin")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 0.5, (0, 2, 1, 2), lo=57))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    # la bete emerge : la basse remonte l'accord et ne redescend qu'a la mesure
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(-1, 1), (0, 1), (1, 1), (2, 1)], lo=46))
    p.add("bourdon", pedal(midi("F2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("bassin.mid"))
