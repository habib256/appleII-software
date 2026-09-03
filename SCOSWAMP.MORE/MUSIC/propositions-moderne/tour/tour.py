#!/usr/bin/env python3
"""« La Tour de Stratagus » — les quatorze pages de la tour. Sol mineur
harmonique, 125 a la noire.

Une marche lente et haute : la basse ne bouge qu'a la blanche, l'arpege ne va
qu'a la noire, la melodie tient. Le fa diese du mineur harmonique — la seconde
augmentee mi bemol-fa diese — est la seule chose qui distingue cette zone de
tout le reste du jeu : c'est la magie, et elle est ecrite, pas suggeree. Le
bourdon est sur **re**, la dominante : la tour n'est jamais posee.

24 mesures a 4/4, 46,1 s. Forme intro(4) - A(8) - B(8) - coda(4).

    python3 tour.py && python3 ../../midi_to_mb.py tour.mid \\
        TOUR.MB.BIN --bpm 125 --max 2400 --wav TOUR.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 125, 4, 24
LEN = BAR * BARS

CHORDS = (["Gm", "Gm", "Eb", "D"]
          + ["Gm", "Cm", "D", "Gm", "Eb", "Cm", "D", "Gm"]
          + ["Eb", "Bb", "Cm", "D", "Eb", "Cm", "D", "D"]
          + ["Gm", "Eb", "D", "Gm"])
assert len(CHORDS) == BARS

MEL = [
    "D5:4",                           "D5:2 G5:2",
    "Bb5:2 G5:2",                     "F#5:2 A5:2",
    "G5:2 D6:2",                      "Eb6:1.5 D6:.5 C6:2",
    "A5:1 D6:1 F#6:2",                "G6:2 D6:2",
    "Bb5:1 Eb6:1 G6:2",               "Eb6:1 C6:1 G5:2",
    "A5:1 F#6:1 D6:2",                "G5:2 Bb5:2",
    "Eb6:2 Bb5:2",                    "D6:2 F6:2",
    "Eb6:1.5 D6:.5 C6:2",             "A5:1 D6:1 A6:2",
    "G6:2 Eb6:2",                     "C6:1 Eb6:1 G6:2",
    "F#6:1 A6:1 D6:2",                "A5:2 F#6:2",
    "G6:2 D6:2",                      "Bb5:1 Eb6:1 G6:2",
    "F#6:1.5 A6:.5 D6:2",             "G5:4",
]
assert len(MEL) == BARS

CTR = [
    "G3:2 Bb3:2",                     "D4:2 Bb3:2",
    "G3:2 Eb4:2",                     "F#4:2 A3:2",
    "D4:2 G3:2",                      "Eb4:2 C4:2",
    "A3:2 F#4:2",                     "G3:2 D4:2",
    "Bb3:2 Eb4:2",                    "C4:2 G3:2",
    "A3:2 D4:2",                      "Bb3:2 G3:2",
    "Eb4:2 Bb3:2",                    "D4:2 F4:2",
    "Eb4:2 C4:2",                     "A3:2 F#4:2",
    "G3:2 Eb4:2",                     "C4:2 G3:2",
    "F#4:2 A3:2",                     "D4:2 A3:2",
    "G3:2 D4:2",                      "Bb3:2 Eb4:2",
    "A3:2 F#4:2",                     "G3:2 D4:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("G", "mineur_h", BPM, BAR, "La Tour de Stratagus")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 1.0, (0, 1, 2, 1), lo=57))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    p.add("basse", progression(CHORDS, 0, BAR, [(0, 2), (-1, 2)], lo=45))
    p.add("bourdon", pedal(midi("D2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("tour.mid"))
