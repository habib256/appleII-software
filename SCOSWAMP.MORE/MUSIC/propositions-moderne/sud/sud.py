#!/usr/bin/env python3
"""« Sentiers Verts » — le Marais sud, douze clairieres. Re eolien, 150.

La zone la plus vaste du jeu a la musique la plus large : la marche
i-VI-III-VII (Dm-Bb-F-C), celle de tous les themes de voyage, mais posee sur
un bourdon de re qui ne bouge jamais, si bien que chaque accord se lit comme une
couleur du meme lieu plutot que comme un depart. Le si bemol la separe du re
dorien de l'accueil : on est entre dans le Marais.

28 mesures a 4/4, 44,8 s. Forme intro(4) - A(8) - B(8) - A'(8), A' a l'octave.

    python3 sud.py && python3 ../../midi_to_mb.py sud.mid \\
        MARAISUD.MB.BIN --bpm 150 --max 2400 --wav MARAISUD.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 150, 4, 28
LEN = BAR * BARS

CHORDS = (["Dm", "Dm", "Bb", "Bb"]
          + ["Dm", "Bb", "F", "C", "Dm", "Gm", "C", "Dm"]
          + ["Bb", "F", "C", "Gm", "Bb", "C", "Dm", "Am"]
          + ["Dm", "Bb", "F", "C", "Gm", "Bb", "C", "Dm"])
assert len(CHORDS) == BARS

MEL = [
    "A5:4",                           "A5:2 D6:2",
    "F5:2 A5:2",                      "D5:2 F5:2",
    "D5:1 F5:1 A5:2",                 "Bb5:1 A5:1 F5:2",
    "A5:1 C6:1 F6:2",                 "E6:1.5 C6:.5 G5:2",
    "F5:1 A5:1 D6:2",                 "Bb5:1 G5:1 D6:2",
    "C6:1 E6:1 G6:1 E6:1",            "D6:2 A5:2",
    "F5:1 Bb5:1 D6:2",                "C6:1 A5:1 F5:2",
    "G5:1 C6:1 E6:2",                 "D6:1 Bb5:1 G5:2",
    "F6:2 D6:2",                      "E6:1 G6:1 C6:2",
    "A5:1 D6:1 F6:2",                 "E6:1.5 C6:.5 A5:2",
    "D6:1 F6:1 A6:2",                 "G6:1.5 F6:.5 D6:2",
    "C6:1 F6:1 A6:2",                 "G6:1 E6:1 C6:2",
    "D6:1 Bb5:1 G6:2",                "F6:1 D6:1 Bb5:2",
    "C6:1 E6:1 G6:1 E6:1",            "D6:4",
]
assert len(MEL) == BARS

CTR = [
    "A3:2 D4:2",                      "F4:2 D4:2",
    "Bb3:2 D4:2",                     "F4:2 A3:2",
    "A3:2 F4:2",                      "D4:2 Bb3:2",
    "C4:2 A3:2",                      "G3:2 E4:2",
    "A3:2 D4:2",                      "Bb3:2 G3:2",
    "C4:2 E4:2",                      "A3:2 F4:2",
    "D4:2 Bb3:2",                     "C4:2 A3:2",
    "G3:2 E4:2",                      "D4:2 Bb3:2",
    "F4:2 D4:2",                      "E4:2 G3:2",
    "A3:2 D4:2",                      "C4:2 E4:2",
    "A3:2 F4:2",                      "D4:2 Bb3:2",
    "C4:2 A3:2",                      "G3:2 E4:2",
    "Bb3:2 D4:2",                     "F4:2 D4:2",
    "E4:2 C4:2",                      "A3:2 D4:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("D", "eolien", BPM, BAR, "Sentiers Verts")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 0.5, (0, 2, 1, 2), lo=57))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 1), (0, 1), (-1, 1), (0, 1)], lo=45))
    p.add("bourdon", pedal(midi("D2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("sud.mid"))
