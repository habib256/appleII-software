#!/usr/bin/env python3
"""« Le Sol qui Cede » — clairiere 12, les Sables Mouvants.

Variation de la couleur `danger` : demi-ton phrygien, bourdon immobile,
crescendo par la densite. Ce qui appartient a cette clairiere-la, c'est le
**sens** : tout descend. L'arpege parcourt l'accord a l'envers — quinte,
tierce, fondamentale, puis la quinte une octave plus bas — et recommence en
haut a chaque changement d'accord, si bien qu'on n'arrete pas de retomber sans
jamais arriver en bas. Chaque phrase de la melodie part de sa note la plus
aigue et finit sur sa plus grave. La basse alterne fondamentale et quinte grave
au lieu de marcher.

Le sol cede a la mesure 9 : l'arpege passe de la noire a la croche et la basse
double, exactement comme le `danger` de la zone se resserre a sa mesure 9. La
seule chose qui ne bouge pas de tout le morceau est le bourdon de **do**, la
quinte a vide de fa, tenue quatre mesures d'affilee — parce qu'on s'enfonce
mais que le Marais, lui, ne s'enfonce pas.

Fa mineur phrygien, 138 a la noire, 26 mesures a 4/4, 45,2 s.
Forme intro(4) - A(8) - B(8) - A'(6).

    python3 sables.py && python3 ../../../midi_to_mb.py sables.mid \\
        SABLES.MB.BIN --bpm 138 --max 2304 --wav SABLES.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 138, 4, 26
LEN = BAR * BARS
CEDE = 8                                   # la mesure ou le terrain cede

CHORDS = (["Fm", "Gb", "Fm", "Fm"]                             # intro — le lierre
          + ["Fm", "Gb", "Fm", "Ebm", "Db", "Gb", "Fm", "Fm"]  # A — on s'enfonce
          + ["Bbm", "Db", "Ab", "Ebm", "Bbm", "Gb", "Db", "Fm"]  # B — la Chance
          + ["Fm", "Gb", "Ebm", "Db", "Gb", "Fm"])             # A' — on sombre
assert len(CHORDS) == BARS

MEL = [
    "C6:2 Ab5:2",                     "Db6:1 C6:1 Ab5:2",
    "C6:2 F5:2",                      "Ab5:2 F5:2",
    "F6:1 Eb6:1 C6:2",                "Db6:1 C6:1 Ab5:2",
    "C6:1 Ab5:1 F5:2",                "Bb5:1 Gb5:1 Eb5:2",
    "Ab5:1 F5:1 Db5:2",               "Db6:1 Bb5:1 Gb5:2",
    "C6:1 Ab5:1 F5:2",                "F5:2 C6:2",
    "Bb5:1 Db6:1 F6:2",               "Ab6:1 F6:1 Db6:2",
    "Eb6:1 C6:1 Ab5:2",               "Bb5:1 Gb5:1 Eb5:2",
    "Db6:1 Bb5:1 F5:2",               "Gb6:1 Db6:1 Bb5:2",
    "F6:1 Db6:1 Ab5:2",               "C6:.5 Db6:.5 C6:1 Ab5:2",
    "F6:1 C6:1 Ab5:2",                "Db6:.5 C6:.5 Ab5:1 Gb5:2",
    "Bb5:1 Gb5:1 Eb5:2",              "Ab5:1 F5:1 Db5:2",
    "Db6:.5 C6:.5 Bb5:1 Gb5:2",       "Db6:1 C6:3",
]
assert len(MEL) == BARS

CTR = [
    "Ab3:2 C4:2",                     "Bb3:2 Db4:2",
    "C4:2 Ab3:2",                     "F4:2 C4:2",
    "Ab3:2 F4:2",                     "Db4:2 Bb3:2",
    "C4:2 Ab3:2",                     "Gb4:2 Eb4:2",
    "F4:2 Db4:2",                     "Bb3:2 Gb4:2",
    "Ab3:2 C4:2",                     "C4:2 F4:2",
    "Db4:2 Bb3:2",                    "F4:2 Ab3:2",
    "C4:2 Eb4:2",                     "Gb4:2 Bb3:2",
    "Db4:2 F4:2",                     "Bb3:2 Db4:2",
    "Ab3:2 F4:2",                     "C4:2 Ab3:2",
    "F4:2 C4:2",                      "Db4:2 Bb3:2",
    "Gb4:2 Eb4:2",                    "F4:2 Db4:2",
    "Bb3:2 Db4:2",                    "C4:2 Ab3:2",
]
assert len(CTR) == BARS

for _s in MEL + CTR:                                # chaque mesure fait 4 temps
    assert abs(sum(float(_t.rpartition(":")[2]) for _t in _s.split()) - BAR) < 1e-6, _s

CHUTE = (2, 1, 0, -1)                      # quinte, tierce, fondamentale, quinte grave


def build():
    p = Piece("F", "phrygien", BPM, BAR, "Le Sol qui Cede")
    p.add("melodie", lines(MEL, 0, bar=BAR))

    # la chute : en noires tant que le sol tient, en croches ensuite
    p.add("arpege",
          arpeggio(CHORDS[:CEDE], 0, BAR, 1.0, CHUTE, lo=57)
          + arpeggio(CHORDS[CEDE:], BAR * CEDE, BAR, 0.5, CHUTE, lo=57))

    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))

    p.add("basse", progression(CHORDS[:CEDE], 0, BAR, [(0, 2), (-1, 2)], lo=45)
                   + progression(CHORDS[CEDE:], BAR * CEDE, BAR,
                                 [(0, 1), (-1, 1), (0, 1), (-1, 1)], lo=45))

    p.add("bourdon", pedal(midi("C2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("sables.mid"))
