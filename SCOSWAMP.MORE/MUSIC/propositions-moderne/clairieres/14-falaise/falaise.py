#!/usr/bin/env python3
"""« Le Ciel s'Ouvre » — clairiere 14, sommet de la falaise. Si dorien, 140.

Variation dans la couleur `riviere` : dorien, et le **bourdon sur la quinte**
(fa diese), la marque de la zone. Ce qui change, c'est la direction : la riviere
coule, la falaise monte. L'arpege n'y tourne plus sur trois sons mais en atteint
**quatre**, l'octave comprise — une figure qui s'ouvre au lieu de tourner, comme
le ciel qui remplace le feuillage a la page 183.

La melodie monte pendant seize mesures jusqu'au si aigu de la mesure 18, le
point le plus haut du dossier, puis redescend d'un trait sur trois mesures : on
se penche, on voit les crocodiles paresseux dans l'eau boueuse, et le pont
inaccessible plus loin a l'est.

24 mesures a 4/4, 41,1 s. Forme intro(4) - A(8) - B(8) - A'(4).

    python3 falaise.py && python3 ../../../midi_to_mb.py falaise.mid \\
        FALAISE.MB.BIN --bpm 140 --max 2304 --wav FALAISE.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 140, 4, 24
LEN = BAR * BARS

CHORDS = (["Bm", "Bm", "A", "A"]
          + ["Bm", "F#m", "D", "A", "Bm", "E", "A", "Bm"]
          + ["D", "A", "E", "C#m", "D", "E", "Bm", "F#m"]
          + ["Bm", "D", "E", "Bm"])
assert len(CHORDS) == BARS

MEL = [
    "B4:4",                           "B4:2 F#5:2",
    "A4:2 C#5:2",                     "E5:4",
    "B4:1 D5:1 F#5:2",                "A5:1 F#5:1 C#5:2",
    "D5:1 F#5:1 A5:2",                "B5:1.5 A5:.5 E5:2",
    "F#5:1 B5:1 D6:2",                "C#6:1 B5:1 G#5:2",
    "A5:1 C#6:1 E6:2",                "D6:1.5 B5:.5 F#5:2",
    "D6:2 F#6:2",                     "E6:1 C#6:1 A5:2",
    "B5:1 E6:1 G#6:2",                "F#6:1 E6:1 C#6:2",
    "D6:1 A5:1 F#6:2",                "E6:1 G#6:1 B6:2",
    "A6:1.5 F#6:.5 D6:2",             "C#6:1 A5:1 F#5:2",
    "B5:1 F#5:1 D5:2",                "F#5:1 A5:1 D6:2",
    "G#5:1 B5:1 E6:2",                "B5:4",
]
assert len(MEL) == BARS

CTR = [
    "B3:2 D4:2",                      "F#4:2 B3:2",
    "A3:2 C#4:2",                     "E4:2 A3:2",
    "B3:2 D4:2",                      "C#4:2 A3:2",
    "D4:2 F#4:2",                     "E4:2 C#4:2",
    "F#4:2 B3:2",                     "G#3:2 E4:2",
    "A3:2 C#4:2",                     "D4:2 B3:2",
    "F#4:2 D4:2",                     "E4:2 A3:2",
    "B3:2 G#3:2",                     "C#4:2 E4:2",
    "D4:2 A3:2",                      "G#3:2 B3:2",
    "D4:2 F#4:2",                     "C#4:2 A3:2",
    "B3:2 F#4:2",                     "D4:2 A3:2",
    "G#3:2 E4:2",                     "F#4:2 B3:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("B", "dorien", BPM, BAR, "Le Ciel s'Ouvre")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    # quatre sons, l'octave comprise : la figure s'ouvre au lieu de tourner
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 0.5, (0, 1, 2, 3), lo=54))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    # deux blanches ouvertes : rien ne marche, on est en haut
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 2), (-1, 2)], lo=48))
    p.add("bourdon", pedal(midi("F#2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("falaise.mid"))
