#!/usr/bin/env python3
"""« La Route des Trois Auberges » — clairiere 1, Route de Courbensaule.

Variation de la couleur `village` : mode majeur a septieme mineure, arpege de
croches en guise de tambourin, basse balancee croche pointee - croche. Mais on
n'est plus SUR la place du village : on y ARRIVE. Le mode passe de sol a **re
mixolydien**, le tempo monte a 172, et la piece est batie sur une seule idee,
la marche qui s'elargit — l'intro monte du re grave a l'aigu en quatre mesures,
et le B enchaine trois phrases de deux mesures, une par auberge (l'Ours Noir,
la Lance Tordue, le Cheval Volant), avant la cadence du marchand de potions.

28 mesures a 4/4, 39,1 s. Forme intro(4) - A(8) - B(8) - A'(8).

    python3 courbens.py && python3 ../../../midi_to_mb.py courbens.mid \\
        COURBENS.MB.BIN --bpm 172 --max 2304 --wav COURBENS.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 172, 4, 28
LEN = BAR * BARS

CHORDS = (["D", "C", "G", "D"]                                 # intro — la route
          + ["D", "G", "C", "G", "D", "Am", "C", "D"]          # A — la ville
          + ["G", "D", "Em", "Bm", "C", "G", "Am", "D"]        # B — les auberges
          + ["D", "G", "C", "G", "Am", "C", "G", "D"])         # A' — la boutique
assert len(CHORDS) == BARS

MEL = [
    "D5:1 F#5:1 A5:2",                "G5:1 E5:1 C6:2",
    "B5:1 G5:1 D6:2",                 "A5:2 F#5:2",
    "A5:1 D6:1 C6:1 A5:1",            "B5:1.5 G5:.5 B5:2",
    "C6:1 E6:1 G6:1 E6:1",            "D6:2 B5:2",
    "A5:1 D6:1 F#6:2",                "E6:1 C6:1 A5:2",
    "G5:1 A5:1 C6:1.5 B5:.5",         "A5:2 D6:2",
    "B5:1 D6:1 G6:2",                 "F#6:1 D6:1 A5:2",
    "G5:1 B5:1 E6:2",                 "D6:1.5 B5:.5 F#5:2",
    "E6:1 G6:1 C6:2",                 "B5:1 D6:1 G5:2",
    "C6:1 E6:1 A5:1 C6:1",            "D6:2 A5:2",
    "D6:1 F#6:1 A6:2",                "G6:1 E6:1 B5:2",
    "C6:1 E6:1 G6:1.5 E6:.5",         "D6:2 B5:2",
    "E6:1 C6:1 A5:2",                 "G6:1 E6:1 C6:2",
    "B5:1 A5:1 F#5:1 A5:1",           "D6:4",
]
assert len(MEL) == BARS

CTR = [
    "F#4:2 A4:2",                     "E4:2 G4:2",
    "D4:2 B3:2",                      "A3:2 F#4:2",
    "F#4:2 D4:2",                     "B3:2 G4:2",
    "E4:2 C4:2",                      "D4:2 B3:2",
    "F#4:2 A4:2",                     "E4:2 C4:2",
    "G4:2 E4:2",                      "A3:2 F#4:2",
    "B3:2 D4:2",                      "A3:2 F#4:2",
    "G4:2 E4:2",                      "F#4:2 D4:2",
    "E4:2 G4:2",                      "D4:2 B3:2",
    "C4:2 E4:2",                      "F#4:2 A3:2",
    "A4:2 F#4:2",                     "G4:2 D4:2",
    "E4:2 G4:2",                      "B3:2 D4:2",
    "C4:2 E4:2",                      "G4:2 E4:2",
    "B3:2 D4:2",                      "F#4:2 A3:2",
]
assert len(CTR) == BARS

for _s in MEL + CTR:                                # chaque mesure fait 4 temps
    assert abs(sum(float(_t.rpartition(":")[2]) for _t in _s.split()) - BAR) < 1e-6, _s


def build():
    p = Piece("D", "mixolydien", BPM, BAR, "La Route des Trois Auberges")
    p.add("melodie", lines(MEL, 0, bar=BAR))

    # le tambourin du village, transpose ici : fondamentale - quinte - tierce
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 0.5, (0, 2, 1, 2), lo=57))

    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))

    # basse de danse : croche pointee - croche, puis la quinte grave
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 1.5), (0, .5), (-1, 1), (0, 1)], lo=45))

    p.add("bourdon", pedal(midi("D2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("courbens.mid"))
