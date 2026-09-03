#!/usr/bin/env python3
"""« Les Feux de Bourbenville » — le village, le prologue, Courbensaule.

Sol mixolydien, 166 a la noire, 4/4, 32 mesures = 46 s. Le seul morceau du jeu
qui n'ait pas peur : septieme mineure au lieu de la sensible, tierces majeures,
une basse qui balance de la fondamentale a la quinte en croches pointees. C'est
la lumiere qu'on quitte a la page 009 et qu'on retrouve a la page 208.

Forme A(8) - B(8) - A'(8) - coda(8) : le refrain, le couplet qui module vers
do, le refrain double a la tierce, une coda qui s'eloigne.

    python3 village.py && python3 ../../midi_to_mb.py village.mid \\
        VILLAGE.MB.BIN --bpm 166 --max 2304 --wav VILLAGE.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 166, 4, 32
LEN = BAR * BARS

CHORDS = (["G", "F", "C", "G", "Am", "F", "C", "G"]            # A — le refrain
          + ["C", "G", "Dm", "Am", "F", "C", "F", "G"]         # B — le couplet
          + ["G", "F", "C", "G", "Am", "F", "C", "G"]          # A'
          + ["Em", "C", "F", "G", "Em", "C", "Dm", "G"])       # coda
assert len(CHORDS) == BARS

MEL = [
    "D5:1 G5:1 B5:1 A5:1",            "A5:1.5 F5:.5 A5:2",
    "G5:1 E5:1 G5:1 C6:1",            "B5:2 G5:2",
    "A5:1 C6:1 E6:1 D6:1",            "C6:1.5 A5:.5 F5:2",
    "G5:1 A5:1 B5:1.5 C6:.5",         "D5:2 D5:2",
    "E5:1 G5:1 C6:2",                 "D6:1 B5:1 G5:2",
    "F5:1 A5:1 D6:2",                 "C6:1 A5:1 E5:2",
    "F5:1 C6:1 A5:1 F5:1",            "E5:1 G5:1 C6:2",
    "A5:1 C6:1 F6:1.5 E6:.5",         "D6:1 B5:1 D5:2",
    "D5:1 G5:1 B5:1 D6:1",            "C6:1.5 A5:.5 C6:2",
    "B5:1 G5:1 B5:1 E6:1",            "D6:2 B5:2",
    "C6:1 E6:1 A6:1 G6:1",            "F6:1.5 C6:.5 A5:2",
    "B5:1 C6:1 D6:1.5 E6:.5",         "D5:2 G5:2",
    "B5:2 G5:2",                      "E6:2 C6:2",
    "A5:1 C6:1 F6:2",                 "D6:1 B5:1 G5:2",
    "B5:2 E5:2",                      "G5:2 C6:2",
    "A5:1 F5:1 D5:2",                 "G5:4",
]
assert len(MEL) == BARS

CTR = [
    "B3:2 D4:2",                      "C4:2 A3:2",
    "G3:2 E4:2",                      "D4:2 B3:2",
    "C4:2 E4:2",                      "A3:2 C4:2",
    "B3:2 D4:2",                      "G3:2 B3:2",
    "C4:2 G3:2",                      "B3:2 D4:2",
    "A3:2 F4:2",                      "E4:2 C4:2",
    "A3:2 C4:2",                      "G3:2 E4:2",
    "A3:2 C4:2",                      "B3:2 G3:2",
    "B3:2 G3:2",                      "A3:2 C4:2",
    "D4:2 B3:2",                      "G3:2 D4:2",
    "C4:2 E4:2",                      "A3:2 C4:2",
    "D4:2 B3:2",                      "B3:2 D4:2",
    "G3:2 B3:2",                      "E4:2 C4:2",
    "A3:2 C4:2",                      "B3:2 D4:2",
    "G3:2 B3:2",                      "E4:2 G3:2",
    "F4:2 D4:2",                      "B3:2 D4:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("G", "mixolydien", BPM, BAR, "Les Feux de Bourbenville")
    p.add("melodie", lines(MEL, 0, bar=BAR))

    # arpege en croches : le tambourin du village, une seule voix rapide
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 0.5, (0, 2, 1, 2), lo=57))

    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))

    # basse : croche pointee - croche, le balancement de danse
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 1.5), (0, .5), (-1, 1), (0, 1)],
                               lo=43))

    # bourdon de sol, refrappe toutes les quatre mesures
    p.add("bourdon", pedal(midi("G2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("village.mid"))
