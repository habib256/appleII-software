#!/usr/bin/env python3
"""« Le Marais Referme » — les onze morts et l'ecran game_over. Do eolien, 125.

Ecrit en blanches et en rondes : a 125 a la noire le pouls reel est a 62, mais
l'horloge reste celle des autres pieces et les valeurs tombent juste. Pas
d'ostinato, pas de croche, aucune voix qui court — la seule chose qui bouge est
l'arpege a la noire, et il descend. La melodie ne monte qu'une fois, mesure 5,
puis retombe de sol a do en huit mesures.

16 mesures a 4/4, 30,7 s. **Sans boucle** (`--no-loop`) : elle se joue une fois
et laisse le silence, comme les pieces de mort et de victoire.

    python3 mort.py && python3 ../../midi_to_mb.py mort.mid \\
        MORT.MB.BIN --bpm 125 --no-loop --max 1280 --wav MORT.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 125, 4, 16
LEN = BAR * BARS

CHORDS = (["Cm", "Cm", "Ab", "Ab"]
          + ["Eb", "Bb", "Fm", "Cm"]
          + ["Ab", "Eb", "Fm", "Gm"]
          + ["Ab", "Bb", "Cm", "Cm"])
assert len(CHORDS) == BARS

MEL = [
    "G5:4",                           "G5:2 Eb5:2",
    "Ab5:4",                          "G5:2 F5:2",
    "Eb6:4",                          "D6:2 Bb5:2",
    "C6:2 Ab5:2",                     "G5:4",
    "Ab5:2 C6:2",                     "Bb5:2 G5:2",
    "Ab5:2 F5:2",                     "G5:4",
    "Eb6:2 C6:2",                     "D6:2 Bb5:2",
    "C6:2 G5:2",                      "C6:4",
]
assert len(MEL) == BARS

CTR = [
    "C4:4",                           "Eb4:2 C4:2",
    "C4:2 Ab3:2",                     "Eb4:4",
    "Bb3:2 G3:2",                     "D4:2 Bb3:2",
    "C4:2 Ab3:2",                     "G3:4",
    "Ab3:2 C4:2",                     "G3:2 Bb3:2",
    "Ab3:2 F4:2",                     "G3:2 D4:2",
    "C4:2 Eb4:2",                     "D4:2 Bb3:2",
    "C4:2 Eb4:2",                     "C4:4",
]
assert len(CTR) == BARS


def build():
    p = Piece("C", "eolien", BPM, BAR, "Le Marais Referme")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    # l'arpege descend : quinte, tierce, fondamentale, tierce
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 1.0, (2, 1, 0, 1), lo=57))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    p.add("basse", progression(CHORDS, 0, BAR, [(0, 2), (-1, 2)], lo=45))
    p.add("bourdon", pedal(midi("C2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("mort.mid"))
