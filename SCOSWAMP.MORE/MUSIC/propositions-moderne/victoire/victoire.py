#!/usr/bin/env python3
"""« Par la Trouee de Ciel » — les pages 158 et 175. Re mixolydien, 150.

La seule piece du dossier en majeur. Le do becarre du mode mixolydien evite la
sensible et donc la pompe de fanfare classique : la victoire est large, pas
militaire. La melodie monte trois fois par tierces (mesures 1, 9, 17) et la
troisieme atteint le la aigu ; l'arpege en croches tient tout du debut a la fin.

20 mesures a 4/4, 32,0 s. **Sans boucle** (`--no-loop`).

    python3 victoire.py && python3 ../../midi_to_mb.py victoire.mid \\
        VICTOIRE.MB.BIN --bpm 150 --no-loop --max 1280 --wav VICTOIRE.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 150, 4, 16
LEN = BAR * BARS

CHORDS = (["D", "D", "C", "G"]
          + ["D", "C", "G", "D"]
          + ["Bm", "G", "C", "D"]
          + ["D", "C", "G", "D"])
assert len(CHORDS) == BARS

MEL = [
    "D5:1 F#5:1 A5:2",                "D6:2 A5:2",
    "C6:1 E6:1 G6:2",                 "D6:1 B5:1 G5:2",
    "D6:1 A5:1 F#6:2",                "E6:1 C6:1 G5:2",
    "B5:1 D6:1 G6:2",                 "A5:1 D6:1 F#6:2",
    "B5:1 D6:1 F#6:2",                "G6:1 D6:1 B5:2",
    "C6:1 E6:1 G6:2",                 "A6:2 F#6:2",
    "D6:1 F#6:1 A6:2",                "G6:1 E6:1 C6:2",
    "B5:1 D6:1 G6:2",                 "D6:4",
]
assert len(MEL) == BARS

CTR = [
    "A3:2 D4:2",                      "F#4:2 A3:2",
    "C4:2 E4:2",                      "B3:2 G3:2",
    "A3:2 F#4:2",                     "E4:2 C4:2",
    "D4:2 B3:2",                      "A3:2 D4:2",
    "B3:2 F#4:2",                     "G3:2 D4:2",
    "C4:2 E4:2",                      "A3:2 D4:2",
    "D4:2 A3:2",                      "G3:2 E4:2",
    "B3:2 D4:2",                      "A3:2 D4:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("D", "mixolydien", BPM, BAR, "Par la Trouee de Ciel")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 0.5, (0, 1, 2, 1), lo=57))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 1), (0, 1), (-1, 1), (0, 1)], lo=45))
    p.add("bourdon", pedal(midi("D2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("victoire.mid"))
