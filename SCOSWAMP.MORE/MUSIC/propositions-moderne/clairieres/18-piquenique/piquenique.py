#!/usr/bin/env python3
"""« Le Repas du Voleur » — clairiere 18, le pique-nique suspect. Fa dorien, 176.

Variation dans la couleur `sud` : **bourdon de tonique immobile**, marche modale
large — mais a **3/4**, la seule des trente-cinq clairieres a ne pas etre a
quatre temps. Le petit homme joyeux de la page 066 mange son fromage adosse a un
chene ; il faut une valse.

La gaite est fausse, et le mode le dit : fa dorien a un **si bemol majeur** au
quatrieme degre — c'est la couleur riante de la piece — mais la section B fait
entrer un **sol bemol majeur**, le second degre abaisse, qui n'appartient pas au
mode. C'est le demi-ton phrygien de la zone `danger`, cite ici a decouvert :
l'Anneau de Cuivre chauffe, et l'on comprend qu'il s'agit d'un VOLEUR. Le sol
bemol revient trois fois, dont une dans la reprise : la valse ne s'en remet pas.

40 mesures a 3/4, 40,9 s. Forme intro(4) - A(12) le repas - B(12) l'Anneau
chauffe - A'(12) la reprise empoisonnee.

    python3 piquenique.py && python3 ../../../midi_to_mb.py piquenique.mid \\
        PIQUENIQUE.MB.BIN --bpm 176 --max 2304 --wav PIQUENIQUE.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 176, 3, 40
LEN = BAR * BARS

CHORDS = (["Fm", "Fm", "Bb", "Bb"]
          + ["Fm", "Ab", "Bb", "Fm", "Cm", "Eb", "Bb", "Fm",
             "Db", "Eb", "Cm", "Fm"]
          + ["Bb", "Fm", "Eb", "Cm", "Db", "Bb", "Ab", "Eb",
             "Gb", "Fm", "Gb", "Cm"]
          + ["Fm", "Ab", "Bb", "Fm", "Cm", "Eb", "Db", "Bb",
             "Gb", "Cm", "Fm", "Fm"])
assert len(CHORDS) == BARS

MEL = [
    "C5:3",                 "C5:1 F5:2",            "D5:1 F5:2",
    "Bb4:1 D5:2",
    "F5:1 Ab5:1 C6:1",      "Bb5:2 Ab5:1",          "D6:1 Bb5:1 F5:1",
    "Ab5:2 F5:1",           "G5:1 C6:1 Eb6:1",      "D6:2 Bb5:1",
    "F5:1 Bb5:1 D6:1",      "C6:2 Ab5:1",           "F5:1 Ab5:1 Db6:1",
    "C6:2 G5:1",            "Eb5:1 G5:1 C6:1",      "F5:3",
    "D6:1 F6:1 D6:1",       "C6:2 Ab5:1",           "Bb5:1 G5:1 Eb5:1",
    "G5:2 C6:1",            "Ab5:1 F5:1 Db5:1",     "D5:1 F5:1 Bb5:1",
    "C6:2 Ab5:1",           "Bb5:1 G5:1 Eb5:1",     "Gb5:1 Bb5:1 Db6:1",
    "C6:1 Ab5:1 F5:1",      "Db6:1 Bb5:1 Gb5:1",    "C6:2 G5:1",
    "F5:1 C6:1 Ab5:1",      "Eb6:2 C6:1",           "D6:1 F6:1 D6:1",
    "C6:2 Ab5:1",           "G5:1 Eb6:1 C6:1",      "Bb5:1 G5:1 Eb5:1",
    "F5:1 Ab5:1 Db6:1",     "D6:2 Bb5:1",           "Db6:1 Bb5:1 Gb5:1",
    "C6:1 G5:1 Eb5:1",      "F5:1 Ab5:1 C6:1",      "F5:3",
]
assert len(MEL) == BARS

CTR = [
    "Ab3:2 C4:1",           "F4:2 C4:1",            "Bb3:2 D4:1",
    "F4:2 Bb3:1",
    "C4:2 Ab3:1",           "Eb4:2 C4:1",           "D4:2 Bb3:1",
    "C4:2 Ab3:1",           "Eb4:2 G3:1",           "Bb3:2 Eb4:1",
    "D4:2 Bb3:1",           "Ab3:2 C4:1",           "F4:2 Db4:1",
    "G3:2 Eb4:1",           "C4:2 Eb4:1",           "Ab3:2 C4:1",
    "D4:2 F4:1",            "C4:2 Ab3:1",           "Bb3:2 Eb4:1",
    "G3:2 C4:1",            "Db4:2 Ab3:1",          "Bb3:2 D4:1",
    "C4:2 Eb4:1",           "Bb3:2 G3:1",           "Db4:2 Bb3:1",
    "Ab3:2 C4:1",           "Bb3:2 Db4:1",          "C4:2 G3:1",
    "Ab3:2 C4:1",           "Eb4:2 C4:1",           "D4:2 F4:1",
    "C4:2 Ab3:1",           "Eb4:2 G3:1",           "Bb3:2 Eb4:1",
    "F4:2 Db4:1",           "D4:2 Bb3:1",           "Db4:2 Bb3:1",
    "C4:2 Eb4:1",           "Ab3:2 C4:1",           "F4:2 C4:1",
]
assert len(CTR) == BARS


def build():
    p = Piece("F", "dorien", BPM, BAR, "Le Repas du Voleur")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    # trois noires par mesure : la valse, un son d'accord par temps
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 1.0, (0, 1, 2), lo=54))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    p.add("basse", progression(CHORDS, 0, BAR, [(0, 2), (-1, 1)], lo=48))
    p.add("bourdon", pedal(midi("F2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("piquenique.mid"))
