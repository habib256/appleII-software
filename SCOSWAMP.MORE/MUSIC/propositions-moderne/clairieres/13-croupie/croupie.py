#!/usr/bin/env python3
"""« La Berge aux Crocodiles » — clairiere 13, la Riviere Croupie. Sol dorien, 132.

Variation dans la couleur `riviere` : meme famille modale (dorien), meme procede
identifiable — le **bourdon sur la quinte**, jamais sur la tonique, si bien que
rien ne se pose et que tout coule. Ici la quinte est **re**, le mode est sol
dorien, et la piece regarde l'eau au lieu de la franchir.

La page 295 dit deux choses : la rive opposee est a deux cents metres, et le
cours d'eau est infeste de crocodiles. D'ou la largeur — melodie en valeurs
longues, arpege de croches qui ne s'interrompt pas — et la basse en figure
breve-longue, une machoire qui se referme sous la surface. Le **mi naturel** du
mode dorien (l'accord de do majeur, mesures 8, 11, 18, 23) est le seul reflet de
lumiere sur une eau boueuse.

24 mesures a 4/4, 43,6 s. Forme intro(4) - A(8) - B(8) - A'(4).

    python3 croupie.py && python3 ../../../midi_to_mb.py croupie.mid \\
        CROUPIE.MB.BIN --bpm 132 --max 2304 --wav CROUPIE.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 132, 4, 24
LEN = BAR * BARS

CHORDS = (["Gm", "Gm", "F", "F"]
          + ["Gm", "Dm", "Bb", "C", "Gm", "F", "C", "Gm"]
          + ["Bb", "F", "C", "Dm", "Bb", "C", "Gm", "Am"]
          + ["Gm", "Bb", "C", "Gm"])
assert len(CHORDS) == BARS

MEL = [
    "D5:4",                           "D5:2 G5:2",
    "F5:4",                           "C5:2 D5:2",
    "D5:1 G5:1 Bb5:2",                "A5:1 F5:1 D5:2",
    "Bb5:2 D6:2",                     "C6:1.5 A5:.5 E5:2",
    "D5:1 Bb5:1 G5:2",                "C6:2 A5:2",
    "G5:1 C6:1 E6:2",                 "D6:1.5 Bb5:.5 G5:2",
    "Bb5:1 D6:1 F6:2",                "C6:1 A5:1 F5:2",
    "G5:1 C6:1 E6:2",                 "F6:1 D6:1 A5:2",
    "Bb5:2 F6:2",                     "E6:1 C6:1 G5:2",
    "D6:1 Bb5:1 G6:2",                "F6:1.5 E6:.5 C6:2",
    "D6:1 G5:1 Bb5:2",                "D6:2 Bb5:2",
    "C6:1 E6:1 G6:2",                 "G5:4",
]
assert len(MEL) == BARS

CTR = [
    "G3:2 Bb3:2",                     "D4:2 G3:2",
    "A3:2 C4:2",                      "F4:2 A3:2",
    "G3:2 Bb3:2",                     "A3:2 F4:2",
    "Bb3:2 D4:2",                     "C4:2 E4:2",
    "D4:2 Bb3:2",                     "A3:2 C4:2",
    "G3:2 E4:2",                      "Bb3:2 G3:2",
    "D4:2 F4:2",                      "C4:2 A3:2",
    "E4:2 G3:2",                      "F4:2 D4:2",
    "Bb3:2 F4:2",                     "G3:2 E4:2",
    "D4:2 Bb3:2",                     "C4:2 A3:2",
    "G3:2 D4:2",                      "Bb3:2 F4:2",
    "E4:2 C4:2",                      "D4:2 G3:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("G", "dorien", BPM, BAR, "La Berge aux Crocodiles")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 0.5, (0, 1, 2, 1), lo=54))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    # breve-longue : la machoire qui se referme
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 2), (-1, 1), (0, 1)], lo=48))
    p.add("bourdon", pedal(midi("D2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("croupie.mid"))
