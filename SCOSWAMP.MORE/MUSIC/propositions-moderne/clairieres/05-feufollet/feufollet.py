#!/usr/bin/env python3
"""« La Lumiere qui Recule » — clairiere 5, le Feu Follet a l'oree.

Variation de la couleur `nord`. L'ostinato de la zone est fixe et tombe toujours
au meme endroit de la mesure ; celui-ci est fixe **en notes** et jamais au meme
endroit, parce que sa cellule fait **cinq croches** dans une mesure a quatre
temps. A chaque tour la figure recule d'une croche, exactement comme le Feu
Follet « recule de quelques metres » chaque fois qu'on avance. Elle ne retombe
d'aplomb qu'une fois toutes les cinq mesures.

Aux six dernieres mesures la cellule passe a quatre croches : la lueur s'arrete
et attend au bord du sentier boueux — c'est le piege, et c'est la seule fois du
morceau ou l'on sait ou elle est.

Sol mineur eolien, 150 a la noire, 26 mesures a 4/4, 41,6 s.
Forme intro(4) - A(8) - B(8) - A'(6), la basse en blanches d'un bout a l'autre
pour que rien ne pese.

    python3 feufollet.py && python3 ../../../midi_to_mb.py feufollet.mid \\
        FEUFOLLET.MB.BIN --bpm 150 --max 2304 --wav FEUFOLLET.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 150, 4, 26
LEN = BAR * BARS
STOP = BAR * 20                            # la lueur s'immobilise, mesure 21

CHORDS = (["Gm", "Eb", "Cm", "Dm"]                             # intro — l'oree
          + ["Gm", "Bb", "Eb", "Dm", "Gm", "Cm", "Eb", "Dm"]   # A — la lueur
          + ["Cm", "Gm", "Eb", "Bb", "F", "Dm", "Eb", "Dm"]    # B — le sentier
          + ["Gm", "Eb", "Cm", "F", "Dm", "Gm"])               # A' — le piege
assert len(CHORDS) == BARS

MEL = [
    "G5:2 Bb5:2",                     "D6:1 Bb5:1 G5:2",
    "Eb6:1 C6:1 G5:2",                "A5:1 D6:1 F6:2",
    "D6:1 Bb5:1 G5:1 Bb5:1",          "D6:1.5 F6:.5 D6:2",
    "Bb5:1 Eb6:1 G6:2",               "F6:1 D6:1 A5:2",
    "G5:1 D6:1 Bb5:2",                "Eb6:1 C6:1 G5:2",
    "Bb5:1 G6:1 Eb6:2",               "D6:2 A5:2",
    "C6:1 Eb6:1 G6:2",                "F6:1 D6:1 Bb5:2",
    "G6:1 Eb6:1 Bb5:2",               "D6:1 F6:1 Bb6:2",
    "A6:1 F6:1 C6:2",                 "D6:1 A5:1 F6:2",
    "Bb5:1 Eb6:1 G6:1.5 F6:.5",       "D6:2 A5:2",
    "G6:1 D6:1 Bb5:2",                "Eb6:1 Bb5:1 G5:2",
    "C6:1 Eb6:1 G6:2",                "F6:1 C6:1 A5:2",
    "D6:1 F6:1 A5:1 D6:1",            "G5:4",
]
assert len(MEL) == BARS

CTR = [
    "Bb3:2 D4:2",                     "G4:2 Eb4:2",
    "C4:2 Eb4:2",                     "A3:2 D4:2",
    "D4:2 Bb3:2",                     "F4:2 D4:2",
    "Eb4:2 G4:2",                     "F4:2 A3:2",
    "Bb3:2 G4:2",                     "Eb4:2 C4:2",
    "G4:2 Bb3:2",                     "A3:2 F4:2",
    "C4:2 G4:2",                      "D4:2 Bb3:2",
    "Eb4:2 G4:2",                     "D4:2 F4:2",
    "C4:2 A3:2",                      "F4:2 D4:2",
    "G4:2 Eb4:2",                     "A3:2 D4:2",
    "Bb3:2 D4:2",                     "G4:2 Eb4:2",
    "C4:2 Eb4:2",                     "A3:2 C4:2",
    "D4:2 F4:2",                      "Bb3:2 G4:2",
]
assert len(CTR) == BARS

for _s in MEL + CTR:                                # chaque mesure fait 4 temps
    assert abs(sum(float(_t.rpartition(":")[2]) for _t in _s.split()) - BAR) < 1e-6, _s

# cinq croches : la lueur ne retombe jamais deux fois sur le meme temps
LUEUR = [midi("D4"), midi("G4"), midi("Bb4"), midi("A4"), midi("F4")]
ATTENTE = [midi("D4"), midi("G4"), midi("Bb4"), midi("G4")]


def build():
    p = Piece("G", "eolien", BPM, BAR, "La Lumiere qui Recule")
    p.add("melodie", lines(MEL, 0, bar=BAR))

    p.add("ostinato", ostinato(LUEUR, 0.5, 0, STOP, gap=0.1)
                      + ostinato(ATTENTE, 0.5, STOP, LEN - STOP, gap=0.1))

    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))

    # basse en blanches : le sol est mou, rien ne marche
    p.add("basse", progression(CHORDS, 0, BAR, [(0, 2), (-1, 2)], lo=45))

    p.add("bourdon", pedal(midi("D2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("feufollet.mid"))
