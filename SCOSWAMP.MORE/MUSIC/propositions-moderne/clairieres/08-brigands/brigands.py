#!/usr/bin/env python3
"""« Cinq Voix derriere l'Arbre » — clairiere 8, la clairiere aux brigands.

Variation de la couleur `nord`. L'ostinato de la zone est ici une cellule de
**cinq notes** — un homme par note, quatre croches et une noire — donc de trois
temps, dans une mesure qui en compte quatre : la figure decale d'un temps a
chaque mesure et ne retombe a sa place que toutes les quatre mesures. C'est ce
qu'on entend depuis derriere l'arbre de la page 065, cinq voix qui parlent en
meme temps sans jamais dire la meme chose au meme moment.

Aux quatre dernieres mesures la noire finale s'allonge a la blanche : la
cellule fait quatre temps, tout retombe ensemble, et les brigands se taisent —
c'est le moment ou l'on decide de les saluer ou de les charger.

L'harmonie est le tetracorde descendant Dm - Do - Si bemol - Lam, la marche de
tous les brigands de la musique modale, et la basse balance en croche pointee
comme au village : ces gens-la ne sont pas mechants, ils sont effrontes.

Re mineur eolien, 176 a la noire, 28 mesures a 4/4, 38,2 s.
Forme intro(4) - A(8) - B(8) - A'(8).

    python3 brigands.py && python3 ../../../midi_to_mb.py brigands.mid \\
        BRIGANDS.MB.BIN --bpm 176 --max 2304 --wav BRIGANDS.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 176, 4, 28
LEN = BAR * BARS
TAIRE = BAR * 24                           # les brigands se taisent, mesure 25

CHORDS = (["Dm", "Dm", "Bb", "C"]                              # intro — le champignon
          + ["Dm", "C", "Bb", "Am", "Dm", "Gm", "Bb", "C"]     # A — les cinq hommes
          + ["Gm", "Dm", "Bb", "F", "C", "Am", "Bb", "C"]      # B — la cachette
          + ["Dm", "C", "Bb", "Am", "Gm", "Bb", "C", "Dm"])    # A' — le salut
assert len(CHORDS) == BARS

MEL = [
    "D5:2 A5:2",                      "F5:1 D5:1 A5:2",
    "Bb5:1 F5:1 D6:2",                "C6:1 G5:1 E5:2",
    "D6:1 A5:1 F5:1 A5:1",            "C6:1.5 G5:.5 E5:2",
    "Bb5:1 D6:1 F6:2",                "E6:1 C6:1 A5:2",
    "D6:1 F6:1 A6:2",                 "G6:1 D6:1 Bb5:2",
    "F6:1 D6:1 Bb5:2",                "E6:1 C6:1 G5:2",
    "G5:1 Bb5:1 D6:2",                "A5:1 F5:1 D5:2",
    "Bb5:1 D6:1 F6:2",                "A5:1 C6:1 F6:2",
    "G6:1 E6:1 C6:2",                 "A5:1 E6:1 C6:2",
    "D6:1 F6:1 Bb6:1.5 A6:.5",        "G6:2 E6:2",
    "D6:1 A5:1 F6:2",                 "E6:1 C6:1 G5:2",
    "D6:1 Bb5:1 F5:2",                "C6:1 A5:1 E5:2",
    "G5:1 Bb5:1 D6:2",                "F6:1 D6:1 Bb5:2",
    "E6:1 G6:1 C6:1 E6:1",            "D6:4",
]
assert len(MEL) == BARS

CTR = [
    "F4:2 A3:2",                      "D4:2 F4:2",
    "Bb3:2 D4:2",                     "C4:2 E4:2",
    "A3:2 D4:2",                      "G4:2 E4:2",
    "F4:2 D4:2",                      "E4:2 C4:2",
    "F4:2 A3:2",                      "D4:2 Bb3:2",
    "F4:2 D4:2",                      "E4:2 G4:2",
    "Bb3:2 G4:2",                     "A3:2 F4:2",
    "D4:2 Bb3:2",                     "C4:2 A3:2",
    "E4:2 G4:2",                      "C4:2 E4:2",
    "D4:2 F4:2",                      "G4:2 E4:2",
    "A3:2 D4:2",                      "E4:2 C4:2",
    "D4:2 Bb3:2",                     "C4:2 A3:2",
    "Bb3:2 D4:2",                     "F4:2 D4:2",
    "E4:2 G4:2",                      "F4:2 A3:2",
]
assert len(CTR) == BARS

for _s in MEL + CTR:                                # chaque mesure fait 4 temps
    assert abs(sum(float(_t.rpartition(":")[2]) for _t in _s.split()) - BAR) < 1e-6, _s

CINQ = [midi("D4"), midi("F4"), midi("A4"), midi("G4"), midi("E4")]


def build():
    p = Piece("D", "eolien", BPM, BAR, "Cinq Voix derriere l'Arbre")
    p.add("melodie", lines(MEL, 0, bar=BAR))

    # cinq notes en trois temps, puis cinq notes en quatre : le silence tombe
    p.add("ostinato",
          ostinato(CINQ, [.5, .5, .5, .5, 1], 0, TAIRE, gap=0.08)
          + ostinato(CINQ, [.5, .5, .5, .5, 2], TAIRE, LEN - TAIRE, gap=0.08))

    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 1.5), (0, .5), (-1, 1), (0, 1)], lo=45))
    p.add("bourdon", pedal(midi("D2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("brigands.mid"))
