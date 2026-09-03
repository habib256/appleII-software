#!/usr/bin/env python3
"""« La Question du Patrouilleur » — clairiere 2, pages 170, 363, 234.

Variation de la couleur `nord` : le procede de la zone est l'ostinato fixe qui
ne change jamais pendant que les accords bougent dessous. Ici il change de
metrique au lieu de changer de notes : la cellule fait **trois croches** dans
une mesure a quatre temps, donc elle retombe chaque fois sur un temps
different — l'homme en vert fait sa ronde et vous le retrouvez toujours a un
autre endroit du chemin. Aux quatre dernieres mesures elle passe a quatre
croches : la ronde s'arrete, la question tombe d'aplomb.

La cellule elle-meme est un appel : la - mi - do, quarte descendante puis
sixte, la seule figure de la piece qui ne se transpose jamais. Le bourdon est
sur **mi**, la quinte a vide de la, pour que l'appel reste une question.

La mineur eolien, 156 a la noire, 28 mesures a 4/4, 43,1 s.
Forme intro(4) - A(8) - B(8) - A'(8).

    python3 patrouil.py && python3 ../../../midi_to_mb.py patrouil.mid \\
        PATROUIL.MB.BIN --bpm 156 --max 2304 --wav PATROUIL.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 156, 4, 28
LEN = BAR * BARS
HALT = BAR * 24                            # la ronde s'arrete a la mesure 25

CHORDS = (["Am", "Am", "F", "G"]                               # intro — la brume
          + ["Am", "F", "C", "G", "Am", "Dm", "Em", "Am"]      # A — l'appel
          + ["F", "C", "G", "Dm", "Am", "Em", "F", "G"]        # B — la question
          + ["Am", "F", "C", "G", "Dm", "F", "Em", "Am"])      # A' — la reponse
assert len(CHORDS) == BARS

MEL = [
    "A5:2 E5:2",                      "A5:1 C6:1 B5:2",
    "A5:2 F5:2",                      "G5:1 A5:1 B5:2",
    "E5:1 A5:1 C6:2",                 "A5:1.5 F5:.5 A5:2",
    "G5:1 C6:1 E6:2",                 "D6:1 B5:1 G5:2",
    "A5:1 E6:1 C6:2",                 "D6:1 A5:1 F5:2",
    "E5:1 G5:1 B5:1 E6:1",            "A5:2 E5:2",
    "F5:1 A5:1 C6:2",                 "E6:1 C6:1 G5:2",
    "B5:1 D6:1 G6:2",                 "F6:1 D6:1 A5:2",
    "C6:1 E6:1 A6:2",                 "G6:1 E6:1 B5:2",
    "A5:1 C6:1 F6:1.5 E6:.5",         "D6:2 B5:2",
    "A5:1 E6:1 A6:2",                 "G6:1 E6:1 C6:2",
    "E6:1 G6:1 B6:2",                 "A6:1 F6:1 D6:2",
    "E6:1 A5:1 D6:2",                 "C6:1 A5:1 F5:2",
    "G5:1 B5:1 E6:1 C6:1",            "A5:4",
]
assert len(MEL) == BARS

CTR = [
    "C4:2 E4:2",                      "A3:2 C4:2",
    "F4:2 A3:2",                      "B3:2 D4:2",
    "E4:2 C4:2",                      "A3:2 F4:2",
    "G4:2 E4:2",                      "D4:2 B3:2",
    "C4:2 A3:2",                      "F4:2 D4:2",
    "G4:2 B3:2",                      "E4:2 A3:2",
    "A3:2 C4:2",                      "E4:2 G4:2",
    "D4:2 B3:2",                      "F4:2 A3:2",
    "C4:2 E4:2",                      "B3:2 G4:2",
    "A3:2 C4:2",                      "D4:2 B3:2",
    "E4:2 C4:2",                      "A3:2 F4:2",
    "G4:2 E4:2",                      "B3:2 D4:2",
    "D4:2 F4:2",                      "C4:2 A3:2",
    "B3:2 G4:2",                      "E4:2 A3:2",
]
assert len(CTR) == BARS

for _s in MEL + CTR:                                # chaque mesure fait 4 temps
    assert abs(sum(float(_t.rpartition(":")[2]) for _t in _s.split()) - BAR) < 1e-6, _s

ROUND = [midi("A4"), midi("E4"), midi("C5")]        # l'appel, trois croches
STAND = [midi("A4"), midi("E4"), midi("A4"), midi("C5")]


def build():
    p = Piece("A", "eolien", BPM, BAR, "La Question du Patrouilleur")
    p.add("melodie", lines(MEL, 0, bar=BAR))

    # la ronde : trois croches contre quatre temps, puis quatre pour la cadence
    p.add("ostinato", ostinato(ROUND, 0.5, 0, HALT)
                      + ostinato(STAND, 0.5, HALT, LEN - HALT))

    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 1), (0, 1), (-1, 1), (0, 1)], lo=46))
    p.add("bourdon", pedal(midi("E2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("patrouil.mid"))
