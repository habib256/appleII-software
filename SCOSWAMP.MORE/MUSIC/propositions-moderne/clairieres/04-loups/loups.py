""" « Deux Paires d'Yeux » — clairiere 4, les deux loups.

Variation de la couleur `nord`. Le procede de la zone est l'ostinato fixe ; ici
il est fixe mais il y en a **deux**, une cellule haute et une cellule basse, et
elles se relaient de mesure en mesure. Aucune des deux ne bouge de tout le
morceau : ce sont deux betes qui se repondent d'un bord a l'autre de la
clairiere pendant que les accords, eux, se deplacent. Le texte le dit sans
detour : « vous tendez l'oreille, mais rien d'anormal ne trouble le silence.
Puis, soudain, deux enormes loups... »

Les deux cellules sont detachees (`gap`) — un pas dans les feuilles, pas un
bourdonnement — et le bourdon est sur **fa diese**, la quinte a vide de si, qui
se refrappe toutes les deux mesures : la respiration de l'affut.

Si mineur eolien, 168 a la noire, 28 mesures a 4/4, 40,0 s.
Forme intro(4) - A(8) - B(8) - A'(8).

    python3 loups.py && python3 ../../../midi_to_mb.py loups.mid \\
        LOUPS.MB.BIN --bpm 168 --max 2304 --wav LOUPS.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 168, 4, 28
LEN = BAR * BARS

CHORDS = (["Bm", "Bm", "G", "F#m"]                             # intro — le silence
          + ["Bm", "G", "D", "A", "Bm", "Em", "G", "F#m"]      # A — les deux betes
          + ["Em", "Bm", "G", "D", "A", "F#m", "G", "F#m"]     # B — le buisson
          + ["Bm", "G", "D", "A", "Em", "G", "F#m", "Bm"])     # A' — on recule
assert len(CHORDS) == BARS

MEL = [
    "F#5:2 B5:2",                     "D6:1 B5:1 F#5:2",
    "G5:2 D6:2",                      "C#6:1 A5:1 F#5:2",
    "B5:1 F#5:1 D6:2",                "B5:1 G5:1 D6:2",
    "F#6:1 D6:1 A5:2",                "E6:1 C#6:1 A5:2",
    "B5:1 D6:1 F#6:2",                "G6:1 E6:1 B5:2",
    "D6:1 B5:1 G5:2",                 "A5:1 F#5:1 C#6:2",
    "E6:2 B5:2",                      "F#6:1 D6:1 B5:2",
    "G6:1 D6:1 B5:2",                 "A5:1 D6:1 F#6:2",
    "E6:1 A5:1 C#6:2",                "F#6:1 C#6:1 A5:2",
    "B5:1 D6:1 G6:1.5 F#6:.5",        "F#6:2 C#6:2",
    "B5:1 F#6:1 D6:2",                "B5:1 G6:1 D6:2",
    "F#6:1 A6:1 D6:2",                "E6:1 C#6:1 A5:2",
    "G6:1 E6:1 B5:2",                 "D6:1 B5:1 G5:2",
    "C#6:1 A5:1 F#5:1 A5:1",          "B5:4",
]
assert len(MEL) == BARS

CTR = [
    "D4:2 F#4:2",                     "B3:2 D4:2",
    "G4:2 B3:2",                      "A4:2 F#4:2",
    "F#4:2 D4:2",                     "B3:2 G4:2",
    "F#4:2 A4:2",                     "E4:2 C#4:2",
    "D4:2 B3:2",                      "G4:2 E4:2",
    "B3:2 D4:2",                      "C#4:2 A4:2",
    "E4:2 G4:2",                      "F#4:2 D4:2",
    "B3:2 G4:2",                      "A4:2 F#4:2",
    "A4:2 E4:2",                      "C#4:2 F#4:2",
    "D4:2 B3:2",                      "A4:2 C#4:2",
    "F#4:2 B3:2",                     "D4:2 G4:2",
    "F#4:2 A4:2",                     "E4:2 C#4:2",
    "G4:2 B3:2",                      "D4:2 B3:2",
    "A4:2 F#4:2",                     "D4:2 B3:2",
]
assert len(CTR) == BARS

for _s in MEL + CTR:                                # chaque mesure fait 4 temps
    assert abs(sum(float(_t.rpartition(":")[2]) for _t in _s.split()) - BAR) < 1e-6, _s

HAUT = [midi("B4"), midi("F#4"), midi("A4"), midi("F#4")]      # le premier loup
BAS = [midi("E4"), midi("B3"), midi("D4"), midi("B3")]         # le second


def build():
    p = Piece("B", "eolien", BPM, BAR, "Deux Paires d'Yeux")
    p.add("melodie", lines(MEL, 0, bar=BAR))

    # les deux betes se relaient une mesure sur deux, sans jamais bouger
    yeux = []
    for b in range(BARS):
        yeux += ostinato(HAUT if b % 2 == 0 else BAS, 0.5, b * BAR, BAR, gap=0.08)
    p.add("ostinato", yeux)

    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))

    # la basse rode : fondamentale et quinte grave, en noires
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 1), (-1, 1), (0, 1), (-1, 1)], lo=48))

    p.add("bourdon", pedal(midi("F#2"), 0, LEN, retrig=BAR * 2))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("loups.mid"))
