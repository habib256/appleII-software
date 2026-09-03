#!/usr/bin/env python3
"""« Le Bassin de Cristal » — clairiere 21. Do dorien, 152.

Variation dans la couleur `sud` : **bourdon de tonique immobile**, marche modale
large, mais le mode est dorien et la **sixte majeure** (le la naturel, sur
l'accord de fa) revient a chaque phrase. C'est elle qui fait la difference entre
une eau croupie et « une eau pure comme du cristal » : la meme famille modale que
la zone, eclairee d'un seul degre.

Deux procedes propres a la clairiere :

- **l'eclat**, section A' : l'arpege passe seul en doubles croches (mesures
  21-26) tandis que tout le reste garde ses valeurs. Rien ne s'accelere, la
  lumiere seule change — c'est le bassin qui prend le jour ;
- **le Lezard**, section B (page 394) : la melodie se pose en blanches et la
  basse marche lentement de re a do, « une demarche chaloupee », puis il s'en
  retourne et la piece se rouvre.

26 mesures a 4/4, 41,1 s. Forme intro(4) - A(8) l'eau pure - B(8) le Lezard -
A'(6) l'eclat.

    python3 cristal.py && python3 ../../../midi_to_mb.py cristal.mid \\
        CRISTAL.MB.BIN --bpm 152 --max 2304 --wav CRISTAL.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 152, 4, 26
LEN = BAR * BARS
ECLAT = 20                                 # la mesure ou l'arpege s'illumine

CHORDS = (["Cm", "Cm", "Bb", "Bb"]
          + ["Cm", "Eb", "F", "Gm", "Cm", "Bb", "F", "Cm"]
          + ["Eb", "Bb", "F", "Dm", "Gm", "Eb", "Bb", "Cm"]
          + ["Cm", "F", "Bb", "Gm", "Eb", "Cm"])
assert len(CHORDS) == BARS

MEL = [
    "C5:4",                           "C5:2 G5:2",
    "Bb4:2 D5:2",                     "F5:4",
    "C5:1 Eb5:1 G5:2",                "Bb5:1 G5:1 Eb5:2",
    "A5:1 C6:1 F6:2",                 "D6:1.5 Bb5:.5 G5:2",
    "Eb6:1 C6:1 G5:2",                "F6:2 D6:2",
    "C6:1 A5:1 F5:2",                 "G5:1 C6:1 Eb6:2",
    "Bb5:2 G5:2",                     "F5:2 D5:2",
    "A5:2 C6:2",                      "D6:1 A5:1 F5:2",
    "G5:1 Bb5:1 D6:2",                "Eb6:2 Bb5:2",
    "D6:1 F6:1 Bb5:2",                "G5:1 Eb5:1 C5:2",
    "C6:1 Eb6:1 G6:2",                "A6:1.5 F6:.5 C6:2",
    "D6:1 Bb5:1 F6:2",                "G6:1 D6:1 Bb5:2",
    "Eb6:2 G5:2",                     "C6:4",
]
assert len(MEL) == BARS

CTR = [
    "C4:2 Eb4:2",                     "G3:2 C4:2",
    "Bb3:2 D4:2",                     "F4:2 Bb3:2",
    "C4:2 G3:2",                      "Eb4:2 Bb3:2",
    "A3:2 C4:2",                      "D4:2 G3:2",
    "Eb4:2 C4:2",                     "F4:2 D4:2",
    "C4:2 A3:2",                      "G3:2 Eb4:2",
    "Bb3:2 G3:2",                     "D4:2 F4:2",
    "C4:2 A3:2",                      "D4:2 F4:2",
    "G3:2 Bb3:2",                     "Eb4:2 G3:2",
    "F4:2 D4:2",                      "Eb4:2 C4:2",
    "G3:2 Eb4:2",                     "A3:2 C4:2",
    "D4:2 Bb3:2",                     "Bb3:2 G3:2",
    "Eb4:2 Bb3:2",                    "C4:2 G3:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("C", "dorien", BPM, BAR, "Le Bassin de Cristal")
    p.add("melodie", lines(MEL, 0, bar=BAR))

    # l'arpege seul s'illumine a la reprise : doubles croches, rien d'autre ne bouge
    arp = arpeggio(CHORDS[:ECLAT], 0, BAR, 0.5, (0, 2, 1, 2), lo=54)
    arp += arpeggio(CHORDS[ECLAT:], BAR * ECLAT, BAR, 0.25,
                    (0, 1, 2, 1), lo=54)
    p.add("arpege", arp)

    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 2), (-1, 1), (0, 1)], lo=48))
    p.add("bourdon", pedal(midi("C2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("cristal.mid"))
