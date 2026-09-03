#!/usr/bin/env python3
"""« Trois Chemins Herbeux » — clairiere 20. Re dorien, 145.

Variation dans la couleur `sud` : **bourdon de tonique immobile** sur le meme re
que `MARAISUD.MB`, mais en dorien — le si naturel a la place du si bemol. C'est
la seule difference de mode, et elle suffit : la page 047 dit « rien
d'interessant n'y apparait a premiere vue ; l'air est lourd et calme ». Une
clairiere ou il n'arrive rien doit sonner comme la zone, en plus clair et en
plus vide.

La forme n'est pas intro-A-B-A' mais **intro et trois phrases de six mesures**,
une par sentier, dans l'ordre du texte :

- le **sud** (mes. 5-10), « plus humide » : la melodie descend, Dm-F-C-Am-Dm ;
- l'**est** (mes. 11-16), « une lueur d'horizon » : elle monte, et c'est la
  seule section a poser le sol majeur, le quatrieme degre majeur du dorien ;
- l'**ouest** (mes. 17-22), « etroit et borde d'arbres serres » : elle se
  resserre dans une sixte et retombe sur la tonique.

Chaque phrase finit sur son accord de depart : trois cadences, trois chemins,
aucun choix impose.

22 mesures a 4/4, 36,4 s.

    python3 herbeux.py && python3 ../../../midi_to_mb.py herbeux.mid \\
        HERBEUX.MB.BIN --bpm 145 --max 2304 --wav HERBEUX.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 145, 4, 22
LEN = BAR * BARS

CHORDS = (["Dm", "Dm", "C", "C"]
          + ["Dm", "F", "C", "Am", "Dm", "Dm"]
          + ["G", "C", "G", "Am", "C", "G"]
          + ["Dm", "Am", "C", "G", "Dm", "Dm"])
assert len(CHORDS) == BARS

MEL = [
    "A4:4",                           "A4:2 D5:2",
    "C5:2 E5:2",                      "G4:2 A4:2",
    "D5:1 F5:1 A5:2",                 "G5:2 F5:2",
    "E5:1 C5:1 G5:2",                 "E5:2 C5:2",
    "D5:1 A4:1 F5:2",                 "D5:4",
    "B4:1 D5:1 G5:2",                 "C6:2 G5:2",
    "B5:1 G5:1 D6:2",                 "C6:1 A5:1 E5:2",
    "G5:1 C6:1 E6:2",                 "D6:2 B5:2",
    "A5:1 F5:1 D5:2",                 "C5:1 E5:1 A5:2",
    "G5:1 E5:1 C5:2",                 "D5:1 B4:1 G5:2",
    "F5:1 A5:1 D6:2",                 "D5:4",
]
assert len(MEL) == BARS

CTR = [
    "D4:2 F4:2",                      "A3:2 D4:2",
    "C4:2 E4:2",                      "G3:2 C4:2",
    "D4:2 A3:2",                      "F4:2 C4:2",
    "E4:2 G3:2",                      "A3:2 C4:2",
    "D4:2 F4:2",                      "A3:2 D4:2",
    "B3:2 D4:2",                      "G3:2 C4:2",
    "D4:2 B3:2",                      "E4:2 A3:2",
    "C4:2 G3:2",                      "B3:2 D4:2",
    "F4:2 D4:2",                      "A3:2 C4:2",
    "E4:2 G3:2",                      "D4:2 B3:2",
    "F4:2 A3:2",                      "D4:2 A3:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("D", "dorien", BPM, BAR, "Trois Chemins Herbeux")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 0.5, (0, 2, 1, 2), lo=54))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    # deux blanches : l'air est lourd et calme
    p.add("basse", progression(CHORDS, 0, BAR, [(0, 2), (-1, 2)], lo=48))
    p.add("bourdon", pedal(midi("D2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("herbeux.mid"))
