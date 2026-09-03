#!/usr/bin/env python3
"""« Le Fil d'Argent » — clairiere 29, la tente aux araignees. Do diese phrygien, 150.

Pages 144, 345, 354, 165. « Des milliers de fils forment des guirlandes entre
les arbres. Au centre, une tente somptueuse : un homme de haute taille, barbe et
sourcils d'un blanc de neige, une Amulette d'Argent en forme d'araignee. » Puis,
si l'on revient : la clairiere est en feu.

Le procede de la zone `danger` est garde — demi-ton phrygien **re-do diese**,
bourdon immobile — et deux traits viennent de la page. La **toile** : l'arpege
est une cellule de **trois** sons dans une mesure de **quatre** temps, si bien
qu'il ne retombe jamais deux fois au meme endroit du cycle harmonique ; les fils
se croisent sans se superposer. Le **feu** : a partir de la mesure 17 la basse
passe de la blanche a la noire, la densite double et ne redescend plus — c'est
l'incendie de la page 345, ecrit comme dans `danger`, par la densite et non par
le volume, puisque le lecteur n'a pas de volume par note.

28 mesures a 4/4, 44,8 s. Forme intro(4) - A(8) - B(8) - A'(8), l'incendie a 17.

    python3 araignees.py && python3 ../../../midi_to_mb.py araignees.mid \\
        ARAIGNEES.MB.BIN --bpm 150 --max 2304 --wav ARAIGNEES.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 150, 4, 28
LEN = BAR * BARS
FEU = 16                                   # la mesure ou la clairiere prend feu

CHORDS = (["C#m", "C#m", "D", "D"]
          + ["C#m", "D", "C#m", "Bm", "A", "D", "C#m", "C#m"]
          + ["F#m", "D", "A", "E", "F#m", "Bm", "D", "C#m"]
          + ["C#m", "D", "F#m", "Bm", "A", "D", "E", "C#m"])
assert len(CHORDS) == BARS

MEL = [
    "G#5:4",                          "G#5:2 C#6:2",
    "A5:2 G#5:2",                     "F#5:2 G#5:2",
    "C#6:2 G#5:2",                    "D6:2 C#6:2",
    "G#5:2 E6:2",                     "D6:2 B5:2",
    "C#6:1 A5:1 E6:2",                "F#6:1 D6:1 A5:2",
    "G#5:1 C#6:1 E6:1 C#6:1",         "G#5:2 F#5:2",
    "A5:1 C#6:1 F#6:2",               "D6:1 A5:1 F#5:2",
    "E6:1 C#6:1 A5:2",                "G#5:1 B5:1 E6:2",
    "F#6:1 A6:1 C#6:2",               "D6:1 F#6:1 B6:2",
    "A6:1 F#6:1 D6:1 A5:1",           "G#5:2 E6:2",
    "C#6:.5 D6:.5 C#6:1 G#5:2",       "D6:.5 C#6:.5 A5:1 F#6:2",
    "E6:.5 D6:.5 C#6:1 A5:2",         "B5:1 D6:1 F#6:2",
    "E6:1 C#6:1 A5:2",                "F#6:1 D6:1 A5:2",
    "B5:1 G#5:1 E6:2",                "G#5:2 C#6:2",
]
assert len(MEL) == BARS

CTR = [
    "C#4:2 G#3:2",                    "E4:2 C#4:2",
    "D4:2 A3:2",                      "B3:2 C#4:2",
    "G#3:2 E4:2",                     "A3:2 F#4:2",
    "C#4:2 G#3:2",                    "B3:2 D4:2",
    "A3:2 C#4:2",                     "D4:2 A3:2",
    "G#3:2 E4:2",                     "C#4:2 G#3:2",
    "A3:2 C#4:2",                     "F#4:2 D4:2",
    "E4:2 C#4:2",                     "B3:2 G#3:2",
    "C#4:2 A3:2",                     "D4:2 F#4:2",
    "A3:2 D4:2",                      "G#3:2 E4:2",
    "C#4:2 A3:2",                     "D4:2 F#4:2",
    "C#4:2 A3:2",                     "B3:2 F#4:2",
    "E4:2 C#4:2",                     "A3:2 D4:2",
    "B3:2 G#3:2",                     "E4:2 C#4:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("C#", "phrygien", BPM, BAR, "Le Fil d'Argent")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    # la toile : trois sons dans quatre temps, le motif se decale a chaque mesure
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 0.5, (0, 2, 1), lo=57))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))

    # l'incendie : la basse passe de la blanche a la noire et n'y revient pas
    bass = progression(CHORDS[:FEU], 0, BAR, [(0, 2), (-1, 2)], lo=45)
    bass += progression(CHORDS[FEU:], BAR * FEU, BAR,
                        [(0, 1), (0, 1), (-1, 1), (0, 1)], lo=45)
    p.add("basse", bass)

    p.add("bourdon", pedal(midi("C#2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("araignees.mid"))
