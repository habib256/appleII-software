#!/usr/bin/env python3
"""« Ce qui Sort du Bassin » — clairiere 9, le bassin de Vase.

Variation de la couleur `danger`. Les deux marques de la zone sont le demi-ton
phrygien pose au-dessus de la tonique et le crescendo obtenu par la densite, la
carte n'ayant pas de volume par note. Ici les deux ne font qu'une seule chose :
la cellule **re - mi bemol - re - fa** ne change pas une note de tout le
morceau, et se resserre trois fois — blanches pendant six mesures, noires
pendant dix, croches pendant dix. C'est la fange qui « parait se contracter,
puis se soulever et se repandre sur le sentier ».

La melodie prend le meme demi-ton a son compte a partir de la mesure 19 (mi
bemol - re en croches) et la piece se ferme dessus : mi bemol sur re, une
blanche, sans resolution ailleurs. Le bourdon de re ne bouge pas d'un bout a
l'autre — deux metres de vase qui rampent lentement ne changent pas d'avis.

Re phrygien, 132 a la noire, 26 mesures a 4/4, 47,3 s.
Forme intro(4) - A(8) - B(8) - A'(6).

    python3 vase.py && python3 ../../../midi_to_mb.py vase.mid \\
        VASE.MB.BIN --bpm 132 --max 2304 --wav VASE.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 132, 4, 26
LEN = BAR * BARS
SERRE = (BAR * 6, BAR * 16)                # les deux resserrements

CHORDS = (["Dm", "Dm", "Eb", "Dm"]                             # intro — le bassin
          + ["Dm", "Eb", "Dm", "Cm", "Bb", "Eb", "Dm", "Dm"]   # A — la Vase
          + ["Gm", "Eb", "Bb", "F", "Gm", "Cm", "Eb", "Dm"]    # B — elle se souleve
          + ["Dm", "Eb", "Cm", "Bb", "Eb", "Dm"])              # A' — elle rampe
assert len(CHORDS) == BARS

MEL = [
    "A5:4",                           "A5:2 F5:2",
    "Bb5:2 G5:2",                     "A5:2 F5:2",
    "D6:2 A5:2",                      "Eb6:1 D6:1 Bb5:2",
    "A5:1 D6:1 F6:2",                 "Eb6:1 C6:1 G5:2",
    "F6:1 D6:1 Bb5:2",                "Eb6:1 Bb5:1 G5:2",
    "A5:1 F5:1 D6:2",                 "D6:2 A5:2",
    "G5:1 Bb5:1 D6:2",                "Eb6:1 Bb5:1 G6:2",
    "F6:1 D6:1 Bb6:2",                "A6:1 F6:1 C6:2",
    "D6:1 G6:1 Bb6:2",                "G6:1 Eb6:1 C6:2",
    "Eb6:.5 D6:.5 Bb5:1 G5:2",        "D6:2 A5:2",
    "A5:.5 Bb5:.5 A5:1 F5:2",         "Eb6:.5 D6:.5 Bb5:1 G5:2",
    "Eb6:1 C6:1 G5:2",                "F6:1 D6:1 Bb5:2",
    "Eb6:.5 D6:.5 Bb5:1 F6:2",        "Eb6:1 D6:3",
]
assert len(MEL) == BARS

CTR = [
    "F4:2 A3:2",                      "D4:2 F4:2",
    "Eb4:2 G4:2",                     "D4:2 A3:2",
    "A3:2 D4:2",                      "G4:2 Eb4:2",
    "F4:2 D4:2",                      "Eb4:2 C4:2",
    "D4:2 Bb3:2",                     "G4:2 Eb4:2",
    "F4:2 A3:2",                      "D4:2 F4:2",
    "Bb3:2 G4:2",                     "Eb4:2 Bb3:2",
    "F4:2 D4:2",                      "C4:2 A3:2",
    "D4:2 Bb3:2",                     "Eb4:2 G4:2",
    "G4:2 Eb4:2",                     "F4:2 D4:2",
    "A3:2 D4:2",                      "Eb4:2 G4:2",
    "C4:2 Eb4:2",                     "D4:2 F4:2",
    "G4:2 Eb4:2",                     "D4:2 A3:2",
]
assert len(CTR) == BARS

for _s in MEL + CTR:                                # chaque mesure fait 4 temps
    assert abs(sum(float(_t.rpartition(":")[2]) for _t in _s.split()) - BAR) < 1e-6, _s

# re - mi bemol - re - fa : le demi-ton phrygien, et rien d'autre
FANGE = [midi("D4"), midi("Eb4"), midi("D4"), midi("F4")]


def build():
    p = Piece("D", "phrygien", BPM, BAR, "Ce qui Sort du Bassin")
    p.add("melodie", lines(MEL, 0, bar=BAR))

    a, b = SERRE
    p.add("ostinato", ostinato(FANGE, 2.0, 0, a)               # elle respire
                      + ostinato(FANGE, 1.0, a, b - a)         # elle se contracte
                      + ostinato(FANGE, 0.5, b, LEN - b))      # elle se repand

    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))

    # la basse se resserre au meme endroit que la fange
    p.add("basse", progression(CHORDS[:16], 0, BAR, [(0, 2), (-1, 2)], lo=45)
                   + progression(CHORDS[16:], b, BAR,
                                 [(0, 1), (0, 1), (-1, 1), (0, 1)], lo=45))

    p.add("bourdon", pedal(midi("D2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("vase.mid"))
