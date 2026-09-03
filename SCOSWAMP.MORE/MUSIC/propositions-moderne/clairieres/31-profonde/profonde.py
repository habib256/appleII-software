#!/usr/bin/env python3
"""« L'Eau Noire » — clairiere 31, la riviere profonde. Sol dorien, 136.

Pages 090, 044, 254, 370. « Celui qui se trouve devant vous est beaucoup plus
profond. La riviere tourbillonne en remous et n'inspire guere confiance : qui
sait quelles creatures se cachent dans son lit ? » Et sur l'autre rive, les
sangsues.

Les deux marques de la zone `riviere` sont gardees : l'arpege de croches qui
**ne s'arrete jamais** d'un bout a l'autre de la piece, et le bourdon pose non
sur la tonique mais sur la **quinte** (re sous un sol dorien), qui laisse tout
le morceau en suspension — on ne touche pas le fond. Ce qui change, c'est le
dessin de l'arpege : au lieu de monter et redescendre proprement comme au pont,
il revient sur lui-meme (0-2-1-2-0-1-2-1), un **remous** et non un courant.

Le do majeur du mode dorien — le mi becarre sous un mode a si bemol — est la
seule clarte de la piece : c'est la surface, vue d'en dessous.

28 mesures a 4/4, 49,4 s. Forme intro(4) - A(8) - B(8) - A'(8).

    python3 profonde.py && python3 ../../../midi_to_mb.py profonde.mid \\
        PROFONDE.MB.BIN --bpm 136 --max 2304 --wav PROFONDE.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 136, 4, 28
LEN = BAR * BARS

CHORDS = (["Gm", "Gm", "F", "F"]
          + ["Gm", "Dm", "F", "C", "Gm", "Bb", "C", "Gm"]
          + ["Bb", "F", "C", "Dm", "Gm", "C", "Am", "Gm"]
          + ["Gm", "Dm", "Bb", "F", "C", "Bb", "C", "Gm"])
assert len(CHORDS) == BARS

MEL = [
    "D5:4",                           "D5:2 G5:2",
    "F5:4",                           "C5:2 D5:2",
    "G5:2 Bb5:2",                     "A5:2 D6:2",
    "C6:1.5 A5:.5 F5:2",              "G5:1 E5:1 C5:2",
    "D5:1 G5:1 Bb5:2",                "D6:2 Bb5:2",
    "C6:1 E6:1 G6:2",                 "D6:2 G5:2",
    "F5:1 Bb5:1 D6:2",                "C6:1 A5:1 F5:2",
    "E6:2 C6:2",                      "D6:1 A5:1 F6:2",
    "G6:1.5 D6:.5 Bb5:2",             "C6:1 G5:1 E6:2",
    "A5:1 C6:1 E6:2",                 "D6:2 G5:2",
    "Bb5:1 D6:1 G6:2",                "F6:1 D6:1 A5:2",
    "Bb5:1 F6:1 D6:2",                "C6:1 A5:1 F6:2",
    "E6:2 G6:2",                      "D6:1 Bb5:1 F6:2",
    "E6:1.5 C6:.5 G5:2",              "G5:4",
]
assert len(MEL) == BARS

CTR = [
    "D4:2 G3:2",                      "Bb3:2 D4:2",
    "C4:2 A3:2",                      "F4:2 D4:2",
    "G3:2 D4:2",                      "A3:2 F4:2",
    "C4:2 A3:2",                      "E4:2 G3:2",
    "D4:2 Bb3:2",                     "F4:2 D4:2",
    "E4:2 C4:2",                      "D4:2 G3:2",
    "Bb3:2 F4:2",                     "A3:2 C4:2",
    "G3:2 E4:2",                      "A3:2 D4:2",
    "Bb3:2 G3:2",                     "C4:2 E4:2",
    "A3:2 C4:2",                      "D4:2 G3:2",
    "G3:2 Bb3:2",                     "A3:2 F4:2",
    "D4:2 Bb3:2",                     "C4:2 A3:2",
    "E4:2 G4:2",                      "F4:2 D4:2",
    "C4:2 E4:2",                      "D4:2 G3:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("G", "dorien", BPM, BAR, "L'Eau Noire")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    # le remous : l'arpege revient sur lui-meme au lieu de monter
    p.add("arpege", arpeggio(CHORDS, 0, BAR, 0.5, (0, 2, 1, 2, 0, 1, 2, 1),
                             lo=57))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 2), (-1, 1), (0, 1)], lo=45))
    # le bourdon est sur la quinte, pas sur la tonique : rien ne se pose
    p.add("bourdon", pedal(midi("D2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("profonde.mid"))
