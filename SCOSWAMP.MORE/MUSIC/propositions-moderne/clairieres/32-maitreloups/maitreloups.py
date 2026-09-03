#!/usr/bin/env python3
"""« Le Cor du Maitre » — clairiere 32, le Maitre des Loups. Mi eolien, 143.

Pages 398, 239, 314. « Une petite maison en rondins. Un grognement qui ressemble
a celui d'un chien : ce n'est pas un chien, cependant, mais un Loup. Un homme
robuste, vetu comme un Garde Forestier, l'Amulette d'Argent en forme de loup sur
la poitrine. Il vous repond avec mauvaise humeur en vous ordonnant de passer
votre chemin. »

Le procede de la zone `sud` est garde : marche i-VI-III-VII (Em-C-G-D) sur un
bourdon de mi immobile. Le caractere est celui du **cor de chasse** : la melodie
est faite de quintes et de quartes a vide (mi-si-mi, do-sol-mi, la-re-fa diese),
jamais de degres conjoints dans les appels, et l'arpege sonne fondamentale-quinte
plutot que fondamentale-tierce. Un cor, un homme qui garde son bois, et deux
loups debout a cote de lui.

28 mesures a 4/4, 47,0 s. Forme intro(4) - A(8) - B(8) - A' a l'octave(8).

    python3 maitreloups.py && python3 ../../../midi_to_mb.py maitreloups.mid \\
        MAITRELOUPS.MB.BIN --bpm 143 --max 2304 --wav MAITRELOUPS.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 143, 4, 28
LEN = BAR * BARS

CHORDS = (["Em", "Em", "C", "D"]
          + ["Em", "C", "G", "D", "Em", "Am", "Bm", "Em"]
          + ["C", "G", "D", "Am", "C", "D", "Em", "Em"]
          + ["Em", "C", "G", "D", "Am", "C", "D", "Em"])
assert len(CHORDS) == BARS

MEL = [
    "B5:4",                           "B5:2 E6:2",
    "C6:2 B5:2",                      "A5:2 B5:2",
    "E5:1 B5:1 E6:2",                 "C6:1 G5:1 E6:2",
    "D6:1 G5:1 B5:2",                 "A5:1 D6:1 F#6:2",
    "E6:1 B5:1 G5:2",                 "A5:1 E6:1 C6:2",
    "B5:1 F#6:1 D6:2",                "E6:2 B5:2",
    "C6:1 G5:1 E5:2",                 "G5:1 D6:1 B5:2",
    "A5:1 D6:1 F#6:2",                "E6:1 C6:1 A5:2",
    "G6:1 E6:1 C6:2",                 "F#6:1 D6:1 A5:2",
    "B5:1 E6:1 G6:2",                 "E6:2 B5:2",
    "E6:1 B5:1 E5:2",                 "C6:1 E6:1 G6:2",
    "D6:1 B5:1 G6:2",                 "F#6:1 A6:1 D6:2",
    "E6:1 A5:1 C6:2",                 "G6:1 E6:1 C6:2",
    "F#6:1.5 D6:.5 A5:2",             "B5:2 E6:2",
]
assert len(MEL) == BARS

CTR = [
    "B3:2 E4:2",                      "G3:2 B3:2",
    "E4:2 C4:2",                      "A3:2 F#4:2",
    "B3:2 G3:2",                      "C4:2 E4:2",
    "B3:2 D4:2",                      "A3:2 F#4:2",
    "G3:2 B3:2",                      "A3:2 C4:2",
    "F#4:2 D4:2",                     "E4:2 B3:2",
    "G3:2 E4:2",                      "D4:2 B3:2",
    "A3:2 F#4:2",                     "C4:2 A3:2",
    "E4:2 G4:2",                      "F#4:2 D4:2",
    "B3:2 G3:2",                      "E4:2 B3:2",
    "G3:2 B3:2",                      "C4:2 G4:2",
    "D4:2 B3:2",                      "A3:2 F#4:2",
    "C4:2 E4:2",                      "G4:2 E4:2",
    "D4:2 A3:2",                      "B3:2 E4:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("E", "eolien", BPM, BAR, "Le Cor du Maitre")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    # fondamentale-quinte, le pavillon du cor : aucune tierce dans l'arpege
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 0.5, (0, 2, 0, 2), lo=57))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 1), (0, 1), (-1, 1), (0, 1)], lo=45))
    p.add("bourdon", pedal(midi("E2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("maitreloups.mid"))
