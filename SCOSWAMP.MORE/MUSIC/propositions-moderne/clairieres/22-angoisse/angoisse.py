#!/usr/bin/env python3
"""« Les Fleurs d'Angoisse » — clairiere 22. Mi phrygien, 144.

Variation dans la couleur `danger` : le mode **phrygien**, donc le demi-ton pose
juste au-dessus de la tonique — ici fa contre mi — le **bourdon de tonique** qui
ne bouge pas, et le crescendo obtenu **par la densite** et non par le volume,
comme dans `DANGER.MB` : la basse passe en blanches jusqu'a la mesure 12, en
noires ensuite.

Ce que la clairiere ajoute est le contraste de la page 204. Les fleurs sont
belles : la section A est en tierces douces, la ligne la plus consonante des
douze pieces. Puis « votre Anneau de Cuivre devient brulant », et la section B
introduit le **tremblement** — fa-mi-fa en doubles croches, quatre fois, la main
qui tremble et le point d'HABILETE perdu. La derniere mesure ne garde que le
motto : fa, mi, et rien d'autre.

24 mesures a 4/4, 40,0 s. Forme intro(4) - A(8) les fleurs - B(8) le
tremblement - A'(4).

    python3 angoisse.py && python3 ../../../midi_to_mb.py angoisse.mid \\
        ANGOISSE.MB.BIN --bpm 144 --max 2304 --wav ANGOISSE.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 144, 4, 24
LEN = BAR * BARS
CUT = 12                                   # la mesure ou la basse passe en noires

CHORDS = (["Em", "Em", "F", "F"]
          + ["Em", "C", "Am", "F", "Em", "G", "F", "Em"]
          + ["Am", "F", "C", "G", "Am", "Dm", "F", "Em"]
          + ["Em", "F", "Am", "Em"])
assert len(CHORDS) == BARS

MEL = [
    "B4:4",                           "B4:2 E5:2",
    "C5:2 F5:2",                      "F5:2 E5:2",
    "E5:1 G5:1 B5:2",                 "C6:1 G5:1 E5:2",
    "A5:1 C6:1 E6:2",                 "F6:1.5 E6:.5 C6:2",
    "B5:1 G5:1 E6:2",                 "D6:2 B5:2",
    "C6:1 A5:1 F5:2",                 "G5:1 E5:1 B4:2",
    "E6:.25 F6:.25 E6:.5 C6:1 A5:2",  "F6:.25 E6:.25 F6:.5 A5:1 C6:2",
    "G5:1 E6:1 C6:2",                 "D6:.25 C6:.25 B5:.5 G5:1 D6:2",
    "E6:.25 F6:.25 E6:.5 A5:1 C6:2",  "F6:1 D6:1 A5:2",
    "C6:.25 D6:.25 C6:.5 A5:1 F5:2",  "B5:1 G5:1 E5:2",
    "E6:1 B5:1 G5:2",                 "F6:1 C6:1 A5:2",
    "E6:1 C6:1 A5:2",                 "F5:.5 E5:.5 E5:3",
]
assert len(MEL) == BARS

CTR = [
    "E4:2 G3:2",                      "B3:2 E4:2",
    "F4:2 A3:2",                      "C4:2 A3:2",
    "E4:2 B3:2",                      "C4:2 G3:2",
    "A3:2 E4:2",                      "F4:2 C4:2",
    "B3:2 G3:2",                      "D4:2 B3:2",
    "C4:2 A3:2",                      "G3:2 E4:2",
    "A3:2 C4:2",                      "F4:2 A3:2",
    "G3:2 C4:2",                      "B3:2 D4:2",
    "C4:2 E4:2",                      "D4:2 F4:2",
    "A3:2 C4:2",                      "B3:2 G3:2",
    "E4:2 B3:2",                      "F4:2 C4:2",
    "A3:2 E4:2",                      "G3:2 E4:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("E", "phrygien", BPM, BAR, "Les Fleurs d'Angoisse")
    p.add("melodie", lines(MEL, 0, bar=BAR))

    # l'arpege marche en noires tant que les fleurs sont belles
    arp = arpeggio(CHORDS[:4], 0, BAR, 1.0, (0, 1, 2, 1), lo=54)
    arp += arpeggio(CHORDS[4:], BAR * 4, BAR, 0.5, (0, 1, 2, 1), lo=54)
    p.add("arpege", arp)

    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))

    # le crescendo est fait par la densite : blanches, puis noires
    bass = progression(CHORDS[:CUT], 0, BAR, [(0, 2), (-1, 2)], lo=48)
    bass += progression(CHORDS[CUT:], BAR * CUT, BAR,
                        [(0, 1), (0, 1), (-1, 1), (0, 1)], lo=48)
    p.add("basse", bass)

    p.add("bourdon", pedal(midi("E2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("angoisse.mid"))
