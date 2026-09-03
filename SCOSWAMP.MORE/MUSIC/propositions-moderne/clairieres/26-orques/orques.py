#!/usr/bin/env python3
"""« Trois Arcs dans la Brume » — clairiere 26, les Orques des Marais. Re phrygien, 158.

Pages 290, 323, 352, 309. Trois orques a la peau rongee, trois arcs, et une
fleche qui frole la tete des l'entree. Le procede de la zone `danger` est garde
— le demi-ton phrygien, ici **mi bemol-re**, et le bourdon de re — mais le
caractere est **martial** : rythme pointe partout (noire pointee + croche a la
basse comme a la melodie), et une cellule de fanfare de trois notes qui est
enoncee trois fois de suite en montant d'un demi-ton (mesures 5, 6 puis 21, 22)
— trois arcs, la meme fleche.

Le bourdon est refrappe toutes les deux mesures : c'est le tambour, pas la brume.

28 mesures a 4/4, 42,5 s. Forme intro(4) - A(8) - B(8) - A' a l'octave(8).

    python3 orques.py && python3 ../../../midi_to_mb.py orques.mid \\
        ORQUES.MB.BIN --bpm 158 --max 2304 --wav ORQUES.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 158, 4, 28
LEN = BAR * BARS

CHORDS = (["Dm", "Dm", "Eb", "Eb"]
          + ["Dm", "Eb", "Dm", "Cm", "Bb", "Eb", "Dm", "Dm"]
          + ["Gm", "Eb", "Bb", "F", "Gm", "Cm", "Eb", "Dm"]
          + ["Dm", "Eb", "F", "Cm", "Bb", "Eb", "Gm", "Dm"])
assert len(CHORDS) == BARS

MEL = [
    "A5:1.5 A5:.5 D6:2",              "D6:1.5 C6:.5 A5:2",
    "Bb5:1.5 A5:.5 G5:2",             "Bb5:2 A5:2",
    "D5:1 D5:1 F5:2",                 "Eb5:1 Eb5:1 G5:2",
    "F5:1 D5:1 A5:2",                 "C6:1.5 Bb5:.5 G5:2",
    "Bb5:1 F5:1 D6:2",                "Eb6:1 Bb5:1 G5:2",
    "F6:1.5 Eb6:.5 D6:2",             "A5:2 D6:2",
    "G5:1 D6:1 Bb5:2",                "Eb6:1 G5:1 Bb5:2",
    "F6:1 D6:1 Bb5:2",                "C6:1.5 A5:.5 F6:2",
    "G6:1 D6:1 Bb5:2",                "C6:1.5 Bb5:.5 G5:2",
    "Eb6:1 G6:1 Bb6:2",               "A6:1.5 F6:.5 D6:2",
    "D6:1 D6:1 F6:2",                 "Eb6:1 Eb6:1 G6:2",
    "F6:1 C6:1 A5:2",                 "G5:1.5 Eb6:.5 C6:2",
    "Bb5:1 F6:1 D6:2",                "Eb6:1 Bb5:1 G6:2",
    "Bb6:1.5 G6:.5 D6:2",             "F6:1 Eb6:1 D6:2",
]
assert len(MEL) == BARS

CTR = [
    "A3:2 D4:2",                      "F4:2 D4:2",
    "Bb3:2 G3:2",                     "Eb4:2 D4:2",
    "A3:2 F4:2",                      "Bb3:2 G4:2",
    "A3:2 D4:2",                      "G3:2 Eb4:2",
    "Bb3:2 F4:2",                     "G4:2 Eb4:2",
    "F4:2 D4:2",                      "A3:2 D4:2",
    "G3:2 Bb3:2",                     "Eb4:2 G4:2",
    "D4:2 Bb3:2",                     "C4:2 A3:2",
    "Bb3:2 G4:2",                     "Eb4:2 C4:2",
    "G4:2 Bb3:2",                     "F4:2 D4:2",
    "A3:2 D4:2",                      "Bb3:2 G4:2",
    "C4:2 A3:2",                      "Eb4:2 G3:2",
    "D4:2 Bb3:2",                     "G4:2 Eb4:2",
    "Bb3:2 G3:2",                     "A3:2 D4:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("D", "phrygien", BPM, BAR, "Trois Arcs dans la Brume")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 0.5, (0, 1, 2, 1), lo=57))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    # la marche pointee : noire pointee, croche, puis deux noires
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 1.5), (0, 0.5), (-1, 1), (0, 1)], lo=45))
    p.add("bourdon", pedal(midi("D2"), 0, LEN, retrig=BAR * 2))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("orques.mid"))
