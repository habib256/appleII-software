#!/usr/bin/env python3
"""« Le Rocher qui Respire » — clairiere 27, le cul-de-sac de la Bete. Sol phrygien, 143.

Pages 011, 210, 299, 125, 228, 243. « Soudain, le rocher bouge : ce n'etait pas
de la pierre. Une BETE IMMONDE a six pattes griffues s'avance. Sa respiration
lourde fait vibrer le bois. »

Deux choses la separent des autres clairieres mortelles, et les deux viennent du
texte. D'abord la **mesure a six temps** : c'est la seule piece des trente-cinq
qui ne soit pas a quatre, et l'arpege y boite en 3+3 (noire, deux croches,
noire, deux blanches pointees) — six pattes qui ne tombent pas ensemble.
Ensuite le **bourdon refrappe a chaque mesure** au lieu de toutes les quatre :
la respiration lourde, et non la brume immobile des autres.

Le procede de la zone est intact : demi-ton phrygien la bemol-sol, bourdon de
sol qui ne bouge pas. C'est un cul-de-sac : l'harmonie ne module jamais et la
derniere mesure retombe exactement sur la premiere.

18 mesures a 6/4, 45,3 s. Forme intro(2) - A(6) - B(6) - A'(4).

    python3 bete.py && python3 ../../../midi_to_mb.py bete.mid \\
        BETE.MB.BIN --bpm 143 --max 2304 --wav BETE.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 143, 6, 18
LEN = BAR * BARS

CHORDS = (["Gm", "Gm"]
          + ["Gm", "Ab", "Gm", "Fm", "Eb", "Ab"]
          + ["Cm", "Ab", "Eb", "Bb", "Cm", "Fm"]
          + ["Gm", "Ab", "Fm", "Gm"])
assert len(CHORDS) == BARS

MEL = [
    "D5:3 Eb5:3",                     "D5:3 C5:3",
    "G5:2 Bb5:1 D6:3",                "Eb6:2 D6:1 Bb5:3",
    "D6:2 Bb5:1 G5:3",                "Ab5:2 C6:1 F5:3",
    "Eb6:3 Bb5:3",                    "C6:2 Ab5:1 Eb6:3",
    "G5:2 C6:1 Eb6:3",                "Ab6:2 Eb6:1 C6:3",
    "Bb5:2 Eb6:1 G6:3",               "F6:2 D6:1 Bb5:3",
    "Eb6:2 C6:1 G5:3",                "Ab5:2 F6:1 C6:3",
    "D6:2 Bb5:1 G5:3",                "Eb6:2 C6:1 Ab5:3",
    "C6:3 Ab5:3",                     "D6:3 G5:3",
]
assert len(MEL) == BARS

CTR = [
    "G3:3 D4:3",                      "Bb3:3 G3:3",
    "D4:3 Bb3:3",                     "C4:3 Ab3:3",
    "Bb3:3 G3:3",                     "C4:3 Ab3:3",
    "G3:3 Eb4:3",                     "C4:3 Ab3:3",
    "Eb4:3 C4:3",                     "C4:3 Ab4:3",
    "G4:3 Eb4:3",                     "F4:3 D4:3",
    "Eb4:3 G3:3",                     "Ab3:3 C4:3",
    "D4:3 Bb3:3",                     "C4:3 Eb4:3",
    "Ab3:3 C4:3",                     "G3:3 D4:3",
]
assert len(CTR) == BARS


def build():
    p = Piece("G", "phrygien", BPM, BAR, "Le Rocher qui Respire")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    # la demarche a six pattes : 1 + .5 + .5 + 1 + 1.5 + 1.5, jamais reguliere
    p.add("arpege", progression(CHORDS, 0, BAR,
                                [(0, 1), (2, 0.5), (1, 0.5),
                                 (0, 1), (2, 1.5), (1, 1.5)], lo=57))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 2), (0, 1), (-1, 2), (0, 1)], lo=50))
    p.add("bourdon", pedal(midi("G2"), 0, LEN, retrig=BAR))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("bete.mid"))
