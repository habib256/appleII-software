#!/usr/bin/env python3
"""« L'Appel du Marais » — theme d'accueil, page 000. Re dorien, 136 a la noire.

Le geste d'ouverture d'un film : les six voix frappent ensemble un re, un
bourdon s'installe et ne lachera plus, un appel de cor monte a la quinte.
A (le seuil) marche en Dm-C-Dm-Am, B (l'appel) flotte sur F-G-C-Am et ouvre le
registre, A' reprend le theme une octave au-dessus, la ou l'onde carree crie.
28 mesures a 4/4, 49 s de boucle.

    python3 accueil.py && python3 ../../midi_to_mb.py accueil.mid \\
        ACCUEIL.MB.BIN --bpm 136 --wav ACCUEIL.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 136, 4, 28
LEN = BAR * BARS

CHORDS = (["Dm", "Dm", "Dm", "Am"]                             # intro
          + ["Dm", "C", "Dm", "Am", "F", "C", "G", "Dm"]       # A — le seuil
          + ["F", "G", "C", "Am", "F", "G", "Dm", "Dm"]        # B — l'appel
          + ["Dm", "C", "Dm", "Am", "F", "G", "Dm", "Dm"])     # A' — a l'octave
assert len(CHORDS) == BARS

# ── voix haute : la melodie, l'appel de cor (D5..A6) ──────────────────────
MEL = [
    "D6:4",                           "D6:2 A5:2",
    "D5:1 D5:1 A5:2",                 "G5:1 F5:1 E5:2",
    "D5:1 F5:.5 G5:.5 A5:2",          "G5:1.5 E5:.5 G5:2",
    "F5:1 A5:.5 D6:.5 C6:1 A5:1",     "A5:2 G5:1 E5:1",
    "F5:1 G5:1 A5:1.5 C6:.5",         "B5:1 A5:1 G5:2",
    "A5:.5 B5:.5 D6:1 C6:1 B5:1",     "A5:2 D5:2",
    "A5:1 C6:1 D6:2",                 "B5:1 D6:1 E6:2",
    "D6:1.5 C6:.5 B5:1 G5:1",         "A5:2 E5:2",
    "F5:1 A5:1 C6:2",                 "D6:1 B5:1 G5:1 B5:1",
    "A5:1.5 F5:.5 E5:1 D5:1",         "D5:3 A5:1",
    "D6:1 F6:.5 G6:.5 A6:2",          "G6:1.5 E6:.5 G6:2",
    "F6:1 E6:.5 D6:.5 C6:1 A5:1",     "A5:1 C6:1 E6:2",
    "F6:1 E6:1 D6:1.5 C6:.5",         "B5:1 D6:1 G6:2",
    "F6:1 E6:1 D6:1 C6:1",            "D6:4",
]
assert len(MEL) == BARS

# ── voix de tenor : le contre-chant, sous l'arpege (G3..A4) ───────────────
CTR = [
    "A3:4",                           "A3:2 D4:2",
    "F4:2 G4:2",                      "A4:2 G4:2",
    "A3:2 D4:2",                      "E4:2 G4:2",
    "F4:2 A4:2",                      "E4:2 A3:2",
    "A3:2 C4:2",                      "G4:2 E4:2",
    "D4:2 G4:2",                      "F4:2 E4:2",
    "A3:2 C4:2",                      "B3:2 D4:2",
    "C4:2 B3:2",                      "C4:2 A3:2",
    "A3:2 C4:2",                      "B3:2 G4:2",
    "F4:2 E4:2",                      "D4:2 A3:2",
    "A4:1 D4:1 F4:2",                 "E4:1 C4:1 E4:2",
    "D4:2 C4:2",                      "C4:2 A3:2",
    "A3:2 C4:2",                      "B3:2 D4:2",
    "A4:2 F4:2",                      "F4:2 E4:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("D", "dorien", BPM, BAR, "L'Appel du Marais")
    p.add("melodie", lines(MEL, 0, bar=BAR))

    # arpege : croches sur l'accord, la voix qui tourne (C4..D5)
    arp = ostinato([midi("D4"), midi("A4"), midi("F4"), midi("A4")], 1.0, 0, BAR * 2)
    arp += arpeggio(CHORDS[2:], BAR * 2, BAR, 0.5, (0, 2, 1, 2), lo=57)
    p.add("arpege", arp)

    p.add("contre-chant", lines(CTR, 0, bar=BAR))

    # lit d'accords : une tenue par mesure, la tierce — trois octets la mesure
    p.add("accords", bed(CHORDS, 0, BAR, lo=52, which=1))

    # basse : fondamentale et quinte grave, marche de deux temps puis galop
    bass = progression(CHORDS[:2], 0, BAR, [(0, 2), (-1, 2)], lo=45)
    bass += progression(CHORDS[2:], BAR * 2, BAR,
                        [(0, 1), (0, .5), (-1, .5), (0, 1), (-1, 1)], lo=45)
    p.add("basse", bass)

    # bourdon de re, refrappe toutes les deux mesures
    p.add("bourdon", pedal(midi("D2"), 0, LEN, retrig=BAR * 2))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("accueil.mid"))
