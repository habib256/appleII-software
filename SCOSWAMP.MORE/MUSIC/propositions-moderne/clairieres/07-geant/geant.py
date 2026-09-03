#!/usr/bin/env python3
"""« Il Est Interdit de Passer » — clairiere 7, le Geant.

Variation de la couleur `nord`. L'ostinato de la zone est fixe et court en
croches ; celui-ci est fixe et marche en **noires** — quatre pas par mesure,
do - sol - mi bemol - sol, l'empreinte de cinquante centimetres de la page 275.
Il ne double en croches que dans le B, quand la massue tourne (mesures 13 a 18),
et il retombe en noires pour le A'. C'est tout le crescendo du morceau, et il ne
coute rien : le lecteur n'a pas de volume par note, on ne peut serrer que la
densite.

Do mineur eolien, 132 a la noire — le tempo le plus lent des douze, parce qu'un
geant ne court pas, mais quatre noires a 132 restent une marche, pas un
adagio. Le bourdon est sur do grave, la corde la plus basse de la table.

24 mesures a 4/4, 43,6 s. Forme intro(4) - A(8) - B(6) - A'(6).

    python3 geant.py && python3 ../../../midi_to_mb.py geant.mid \\
        GEANT.MB.BIN --bpm 132 --max 2304 --wav GEANT.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 132, 4, 24
LEN = BAR * BARS
MASSUE = (BAR * 12, BAR * 18)              # les six mesures ou la massue tourne

CHORDS = (["Cm", "Cm", "Ab", "Gm"]                             # intro — l'empreinte
          + ["Cm", "Ab", "Eb", "Bb", "Cm", "Fm", "Ab", "Gm"]   # A — le Geant
          + ["Eb", "Bb", "Fm", "Cm", "Ab", "Gm"]               # B — la massue
          + ["Cm", "Ab", "Eb", "Bb", "Fm", "Cm"])              # A' — le passage
assert len(CHORDS) == BARS

MEL = [
    "C5:2 G5:2",                      "Eb5:1 C5:1 G5:2",
    "Ab5:2 Eb5:2",                    "G5:1 D5:1 Bb4:2",
    "C6:2 G5:2",                      "Eb6:1 C6:1 Ab5:2",
    "G5:1 Bb5:1 Eb6:2",               "D6:1 Bb5:1 F5:2",
    "C6:1 Eb6:1 G6:2",                "F6:1 C6:1 Ab5:2",
    "Eb6:2 C6:2",                     "D6:1 Bb5:1 G5:2",
    "Eb6:1 G6:1 Bb6:2",               "F6:1 D6:1 Bb5:2",
    "Ab6:1 F6:1 C6:2",                "G6:1 Eb6:1 C6:2",
    "Ab5:1 C6:1 Eb6:2",               "D6:2 G5:2",
    "C6:2 Eb6:2",                     "Ab5:2 C6:2",
    "Bb5:1 G5:1 Eb5:2",               "F5:1 D5:1 Bb4:2",
    "Ab5:1 F5:1 C5:2",                "C5:4",
]
assert len(MEL) == BARS

CTR = [
    "Eb4:2 G3:2",                     "C4:2 Eb4:2",
    "Ab3:2 C4:2",                     "Bb3:2 D4:2",
    "G3:2 Eb4:2",                     "C4:2 Ab3:2",
    "Bb3:2 G3:2",                     "D4:2 F4:2",
    "Eb4:2 C4:2",                     "Ab3:2 F4:2",
    "C4:2 Eb4:2",                     "Bb3:2 G3:2",
    "G3:2 Bb3:2",                     "F4:2 D4:2",
    "C4:2 Ab3:2",                     "Eb4:2 G3:2",
    "Ab3:2 Eb4:2",                    "D4:2 Bb3:2",
    "C4:2 G3:2",                      "Eb4:2 C4:2",
    "G3:2 Bb3:2",                     "D4:2 F4:2",
    "Ab3:2 C4:2",                     "G3:2 Eb4:2",
]
assert len(CTR) == BARS

for _s in MEL + CTR:                                # chaque mesure fait 4 temps
    assert abs(sum(float(_t.rpartition(":")[2]) for _t in _s.split()) - BAR) < 1e-6, _s

PAS = [midi("C4"), midi("G4"), midi("Eb4"), midi("G4")]        # l'empreinte


def build():
    p = Piece("C", "eolien", BPM, BAR, "Il Est Interdit de Passer")
    p.add("melodie", lines(MEL, 0, bar=BAR))

    a, b = MASSUE
    p.add("ostinato", ostinato(PAS, 1.0, 0, a)                 # les pas
                      + ostinato(PAS, 0.5, a, b - a)           # la massue
                      + ostinato(PAS, 1.0, b, LEN - b))        # les pas

    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))

    # basse pesante : la fondamentale une blanche, puis deux appuis
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 2), (-1, 1), (0, 1)], lo=45))

    p.add("bourdon", pedal(midi("C2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("geant.mid"))
