#!/usr/bin/env python3
"""« L'Amulette de Fleur » — clairiere 3, le Maitre des Jardins.

Variation de la couleur `nord` : meme famille mineure, meme ostinato fixe de
quatre croches. Mais c'est le seul endroit amical de tout le Marais nord — « le
seul chemin qui y mene est celui que vous avez emprunte », et l'Anneau de Cuivre
reste froid. Le mode passe donc de l'eolien au **re dorien** : une seule note
change, la sixte majeure, le si becarre, et c'est elle la fleur. L'ostinato la
touche a chaque tour (la - fa - **si** - sol) et la melodie la pose sur le sol
majeur des mesures 2, 4, 15, 20 : l'accord que le mode eolien du nord ne peut
pas faire.

L'ostinato est joue detache (`gap`), a la maniere du secateur ; la basse tient
la fondamentale une blanche au lieu de marcher, parce qu'ici on ne fuit pas.

26 mesures a 4/4, 45,2 s. Forme intro(2) - A(8) - B(8) - A'(8).

    python3 jardins.py && python3 ../../../midi_to_mb.py jardins.mid \\
        JARDINS.MB.BIN --bpm 138 --max 2304 --wav JARDINS.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 138, 4, 26
LEN = BAR * BARS

CHORDS = (["Dm", "G"]                                          # intro — l'allee
          + ["Dm", "G", "Dm", "Am", "F", "C", "G", "Dm"]       # A — le jardin
          + ["F", "C", "Dm", "Am", "G", "Em", "C", "G"]        # B — l'amulette
          + ["Dm", "G", "F", "C", "Am", "G", "Em", "Dm"])      # A' — l'adieu
assert len(CHORDS) == BARS

MEL = [
    "D5:2 F5:2",                      "G5:1 B5:1 A5:2",
    "A5:1 D6:1 C6:2",                 "B5:1.5 A5:.5 G5:2",
    "F5:1 A5:1 D6:2",                 "C6:1 A5:1 E5:2",
    "F5:1 C6:1 A5:2",                 "G5:1 E6:1 C6:2",
    "B5:1 D6:1 G6:2",                 "F6:1 D6:1 A5:2",
    "A5:1 C6:1 F6:2",                 "E6:1 C6:1 G5:2",
    "D6:1 F6:1 A6:2",                 "G6:1 E6:1 C6:2",
    "B5:1 D6:1 B5:1 G5:1",            "E6:1 B5:1 G5:2",
    "C6:1 E6:1 G6:1.5 E6:.5",         "D6:2 B5:2",
    "A5:1 D6:1 F6:2",                 "B5:1 G5:1 D6:2",
    "C6:1 A5:1 F5:2",                 "E6:1 G6:1 C6:2",
    "A5:1 C6:1 E6:2",                 "D6:1 B5:1 G5:2",
    "E6:1 D6:1 B5:1 G5:1",            "D6:4",
]
assert len(MEL) == BARS

CTR = [
    "F4:2 A3:2",                      "B3:2 D4:2",
    "A3:2 D4:2",                      "G4:2 B3:2",
    "F4:2 D4:2",                      "E4:2 C4:2",
    "A3:2 F4:2",                      "G4:2 E4:2",
    "B3:2 D4:2",                      "D4:2 F4:2",
    "C4:2 A3:2",                      "E4:2 G4:2",
    "F4:2 A3:2",                      "C4:2 E4:2",
    "D4:2 B3:2",                      "G4:2 E4:2",
    "E4:2 C4:2",                      "B3:2 D4:2",
    "A3:2 F4:2",                      "B3:2 G4:2",
    "A3:2 C4:2",                      "E4:2 G4:2",
    "C4:2 A3:2",                      "B3:2 D4:2",
    "G4:2 B3:2",                      "F4:2 A3:2",
]
assert len(CTR) == BARS

for _s in MEL + CTR:                                # chaque mesure fait 4 temps
    assert abs(sum(float(_t.rpartition(":")[2]) for _t in _s.split()) - BAR) < 1e-6, _s

# la - fa - si - sol : le si becarre est la sixte majeure du mode, la fleur
GARDEN = [midi("A4"), midi("F4"), midi("B4"), midi("G4")]


def build():
    p = Piece("D", "dorien", BPM, BAR, "L'Amulette de Fleur")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    p.add("ostinato", ostinato(GARDEN, 0.5, 0, LEN, gap=0.12))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 2), (-1, 1), (0, 1)], lo=45))
    p.add("bourdon", pedal(midi("D2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("jardins.mid"))
