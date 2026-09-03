#!/usr/bin/env python3
"""« Le Pont sur la Croupie » — la riviere et son passage. La dorien, 125.

L'eau : un arpege de croches qui ne s'arrete jamais, une melodie en blanches
au-dessus, et un bourdon de **mi** — la quinte, pas la tonique — qui met tout
le morceau en suspension. Le re majeur du mode dorien (mesures 8, 12, 18, 24)
est la seule lumiere : c'est le pont, le seul passage entre les douze clairieres
du nord et les vingt-trois du sud.

28 mesures a 4/4, 53,8 s. Forme intro(4) - A(8) - B(8) - A'(8).

    python3 riviere.py && python3 ../../midi_to_mb.py riviere.mid \\
        RIVIERE.MB.BIN --bpm 125 --max 2304 --wav RIVIERE.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 125, 4, 28
LEN = BAR * BARS

CHORDS = (["Am", "Am", "G", "G"]
          + ["Am", "Em", "G", "D", "Am", "C", "G", "D"]
          + ["C", "G", "Bm", "Em", "C", "D", "Am", "Am"]
          + ["Am", "Em", "G", "D", "Am", "C", "G", "Am"])
assert len(CHORDS) == BARS

MEL = [
    "E5:4",                           "E5:2 A5:2",
    "G5:4",                           "D5:2 E5:2",
    "A5:2 C6:2",                      "B5:2 E6:2",
    "D6:1.5 B5:.5 G5:2",              "A5:1 F#5:1 D5:2",
    "E5:1 A5:1 C6:2",                 "E6:2 C6:2",
    "B5:1 D6:1 G6:2",                 "F#6:2 D6:2",
    "E6:1 C6:1 G5:2",                 "B5:1 D6:1 B5:2",
    "F#6:2 D6:2",                     "E6:1 B5:1 G5:2",
    "C6:1 E6:1 G6:2",                 "F#6:1 A6:1 D6:2",
    "E6:1.5 C6:.5 A5:2",              "B5:2 E5:2",
    "A5:2 E6:2",                      "B5:2 G5:2",
    "D6:1 B5:1 G6:2",                 "A5:2 F#6:2",
    "E6:2 C6:2",                      "G6:2 E6:2",
    "D6:1.5 B5:.5 G5:2",              "A5:4",
]
assert len(MEL) == BARS

CTR = [
    "A3:2 C4:2",                      "E4:2 A3:2",
    "B3:2 D4:2",                      "G3:2 B3:2",
    "C4:2 E4:2",                      "B3:2 G4:2",
    "D4:2 B3:2",                      "A3:2 F#4:2",
    "A3:2 C4:2",                      "G3:2 E4:2",
    "D4:2 B3:2",                      "A3:2 D4:2",
    "E4:2 G4:2",                      "D4:2 B3:2",
    "F#4:2 D4:2",                     "E4:2 B3:2",
    "G3:2 C4:2",                      "A3:2 D4:2",
    "C4:2 E4:2",                      "A3:2 E4:2",
    "A3:2 C4:2",                      "B3:2 G4:2",
    "D4:2 G3:2",                      "A3:2 F#4:2",
    "C4:2 E4:2",                      "G3:2 E4:2",
    "B3:2 D4:2",                      "A3:2 E4:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("A", "dorien", BPM, BAR, "Le Pont sur la Croupie")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 0.5, (0, 1, 2, 1), lo=57))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 2), (-1, 1), (0, 1)], lo=48))
    p.add("bourdon", pedal(midi("E2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("riviere.mid"))
