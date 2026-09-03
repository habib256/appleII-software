#!/usr/bin/env python3
"""« Le Grand Nid » — clairiere 11, le nid de l'Aigle.

Variation de la couleur `nord`. L'ostinato de la zone bat des croches egales ;
celui-ci a un rythme, et c'est tout le sujet : **noire - croche - blanche -
croche**, fa diese - la - do diese - la. Un coup d'aile, un second, puis le vol
plane sur la note du haut pendant deux temps, et l'on retombe. La cellule ne
change jamais de notes ni de place ; c'est l'Aigle « qui vole au-dessus de la
clairiere en vous observant attentivement », et il tourne au meme rythme quoi
qu'il arrive dessous.

Cette cellule est posee tres haut — jusqu'au do diese aigu — et la melodie doit
donc chanter au-dessus d'elle, en blanches : le morceau est le plus aere des
douze, quatre notes d'ostinato par mesure au lieu de huit, une basse en trois
temps, et un bourdon sur **do diese grave**, presque au fond de la table des
notes. Entre les deux, la hauteur de l'arbre.

Fa diese mineur eolien, 152 a la noire, 28 mesures a 4/4, 44,2 s.
Forme intro(4) - A(8) - B(8) - A'(8).

    python3 aigle.py && python3 ../../../midi_to_mb.py aigle.mid \\
        AIGLE.MB.BIN --bpm 152 --max 2304 --wav AIGLE.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 152, 4, 28
LEN = BAR * BARS

CHORDS = (["F#m", "D", "A", "E"]                               # intro — l'arbre
          + ["F#m", "D", "A", "E", "F#m", "Bm", "D", "C#m"]    # A — l'Aigle
          + ["A", "E", "D", "A", "Bm", "F#m", "D", "E"]        # B — le nid
          + ["F#m", "D", "A", "E", "Bm", "D", "E", "F#m"])     # A' — il s'eloigne
assert len(CHORDS) == BARS

MEL = [
    "F#5:2 C#6:2",                    "D6:2 A5:2",
    "C#6:2 E6:2",                     "B5:2 F#5:2",
    "F#5:1 A5:1 C#6:2",               "D6:2 F#6:2",
    "E6:1 C#6:1 A5:2",                "B5:1 G#5:1 E5:2",
    "C#6:1 F#6:1 A6:2",               "G#6:1 F#6:1 D6:2",
    "A5:1 D6:1 F#6:2",                "E6:1 C#6:1 G#5:2",
    "A5:2 E6:2",                      "B5:2 G#5:2",
    "D6:2 A6:2",                      "E6:1 C#6:1 A5:2",
    "B5:1 D6:1 F#6:2",                "A6:1 F#6:1 C#6:2",
    "D6:1 F#6:1 A6:1.5 G#6:.5",       "E6:2 B5:2",
    "F#6:2 C#6:2",                    "A6:1 F#6:1 D6:2",
    "E6:1 A5:1 C#6:2",                "B5:1 E6:1 G#6:2",
    "F#6:1 D6:1 B5:2",                "A5:1 D6:1 F#6:2",
    "E6:1 B5:1 G#5:2",                "F#6:4",
]
assert len(MEL) == BARS

CTR = [
    "C#4:2 A3:2",                     "D4:2 F#4:2",
    "E4:2 C#4:2",                     "B3:2 G#3:2",
    "A3:2 C#4:2",                     "F#4:2 D4:2",
    "C#4:2 E4:2",                     "G#3:2 B3:2",
    "C#4:2 A3:2",                     "D4:2 F#4:2",
    "A3:2 D4:2",                      "E4:2 C#4:2",
    "C#4:2 E4:2",                     "B3:2 G#3:2",
    "D4:2 A3:2",                      "E4:2 C#4:2",
    "F#4:2 D4:2",                     "A3:2 C#4:2",
    "D4:2 F#4:2",                     "B3:2 E4:2",
    "C#4:2 A3:2",                     "F#4:2 D4:2",
    "E4:2 C#4:2",                     "G#3:2 B3:2",
    "D4:2 F#4:2",                     "A3:2 D4:2",
    "B3:2 G#3:2",                     "A3:2 C#4:2",
]
assert len(CTR) == BARS

for _s in MEL + CTR:                                # chaque mesure fait 4 temps
    assert abs(sum(float(_t.rpartition(":")[2]) for _t in _s.split()) - BAR) < 1e-6, _s

VOL = [midi("F#4"), midi("A4"), midi("C#5"), midi("A4")]       # deux ailes, un plane


def build():
    p = Piece("F#", "eolien", BPM, BAR, "Le Grand Nid")
    p.add("melodie", lines(MEL, 0, bar=BAR))

    # noire - croche - blanche - croche : le battement puis le vol plane
    p.add("ostinato", ostinato(VOL, [1, .5, 2, .5], 0, LEN))

    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))

    # la basse ne marche pas : elle tient, puis se laisse tomber d'une quinte
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 2), (-1, 1), (0, 1)], lo=47))

    p.add("bourdon", pedal(midi("C#2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("aigle.mid"))
