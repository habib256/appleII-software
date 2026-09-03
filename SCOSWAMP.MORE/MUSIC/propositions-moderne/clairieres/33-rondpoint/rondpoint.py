#!/usr/bin/env python3
"""« Le Coeur du Marais » — clairiere 33, le large rond-point. Re eolien, 158.

C'est la premiere clairiere du Marais : le joueur y arrive page 195, le sol est
instable, trois sentiers partent de la et le brouillard monte. La piece est donc
le theme du Marais lui-meme, et elle prend la tonalite exacte de la zone `sud`
(re eolien) et son procede (la marche i-VI-III-VII posee sur un bourdon de re qui
ne bouge jamais) — mais son theme est a elle : une **montee de trois notes**
(re-mi-fa) qui redemande son chemin, enoncee trois fois dans la partie B, a trois
hauteurs, pour les trois sentiers. Le la mineur du mode (v mineur, pas de
sensible) est le sol qui se derobe : aucune cadence ne conclut vraiment, la
derniere mesure retombe sur le re et la boucle repart.

32 mesures a 4/4, 48,6 s. Forme intro(4) - A(8) - B(8) - A' a l'octave(8) - coda(4).

    python3 rondpoint.py && python3 ../../../midi_to_mb.py rondpoint.mid \\
        RONDPOINT.MB.BIN --bpm 158 --max 2304 --wav RONDPOINT.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 158, 4, 32
LEN = BAR * BARS

CHORDS = (["Dm", "Dm", "Gm", "Am"]
          + ["Dm", "F", "C", "Gm", "Dm", "Bb", "C", "Dm"]
          + ["Bb", "F", "Gm", "Dm", "Bb", "C", "Am", "Am"]
          + ["Dm", "F", "C", "Gm", "Bb", "Gm", "C", "Dm"]
          + ["Dm", "Gm", "C", "Dm"])
assert len(CHORDS) == BARS

MEL = [
    "A5:4",                           "A5:2 D6:2",
    "Bb5:2 A5:2",                     "G5:2 A5:2",
    "D5:1 E5:1 F5:2",                 "A5:1 C6:1 A5:2",
    "G5:1 E5:1 G5:2",                 "Bb5:2 A5:2",
    "D6:1 A5:1 F5:2",                 "Bb5:1 D6:1 F6:2",
    "E6:1.5 C6:.5 G5:2",              "A5:1 F5:1 D5:2",
    "F5:1 Bb5:1 D6:2",                "C6:1 A5:1 F5:2",
    "G5:1 D6:1 Bb5:2",                "A5:1 F5:1 D6:2",
    "Bb5:1 F6:1 D6:2",                "C6:1 G6:1 E6:2",
    "A5:1 E6:1 C6:2",                 "C6:2 A5:2",
    "D6:1 E6:1 F6:2",                 "A6:1 F6:1 C6:2",
    "G6:1 E6:1 C6:2",                 "D6:2 Bb5:2",
    "F6:1 D6:1 Bb5:2",                "G6:1 D6:1 Bb5:2",
    "E6:1.5 C6:.5 G5:2",              "F6:2 D6:2",
    "A5:1 D6:1 F6:2",                 "G5:1 Bb5:1 D6:2",
    "E6:2 C6:2",                      "D6:4",
]
assert len(MEL) == BARS

CTR = [
    "A3:2 D4:2",                      "F4:2 D4:2",
    "Bb3:2 D4:2",                     "C4:2 A3:2",
    "A3:2 F4:2",                      "C4:2 A3:2",
    "G3:2 E4:2",                      "Bb3:2 G3:2",
    "A3:2 D4:2",                      "D4:2 Bb3:2",
    "C4:2 E4:2",                      "A3:2 F4:2",
    "D4:2 Bb3:2",                     "C4:2 A3:2",
    "Bb3:2 G3:2",                     "A3:2 D4:2",
    "F4:2 D4:2",                      "E4:2 G3:2",
    "C4:2 A3:2",                      "E4:2 C4:2",
    "A3:2 F4:2",                      "C4:2 A3:2",
    "G3:2 E4:2",                      "Bb3:2 D4:2",
    "F4:2 D4:2",                      "G3:2 Bb3:2",
    "E4:2 C4:2",                      "A3:2 F4:2",
    "D4:2 A3:2",                      "Bb3:2 G3:2",
    "C4:2 E4:2",                      "D4:2 A3:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("D", "eolien", BPM, BAR, "Le Coeur du Marais")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 0.5, (0, 2, 1, 2), lo=57))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 2), (-1, 1), (0, 1)], lo=45))
    p.add("bourdon", pedal(midi("D2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("rondpoint.mid"))
