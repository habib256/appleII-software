#!/usr/bin/env python3
"""« Ce qui Attend Sous l'Eau » — les dix clairieres mortelles. Do phrygien, 136.

Le mode phrygien pose un re bemol un demi-ton au-dessus de la tonique : tout le
morceau est bati sur ce frottement, l'accord de Db qui retombe sur Cm et le
motif Db-C que la melodie repete a partir de la mesure 21. Le bourdon de do ne
bouge pas d'un bout a l'autre.

Le crescendo est fait **par la densite**, pas par le volume : le lecteur n'a pas
de volume par note. Les huit premieres mesures marchent en noires et en blanches,
les vingt suivantes en croches. Le morceau se resserre au lieu de monter.

28 mesures a 4/4, 49,4 s. Forme intro(4) - A(8) - B(8) - A'(8).

    python3 danger.py && python3 ../../midi_to_mb.py danger.mid \\
        DANGER.MB.BIN --bpm 136 --max 2400 --wav DANGER.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 136, 4, 28
LEN = BAR * BARS
CUT = 8                                    # la mesure ou les croches arrivent

CHORDS = (["Cm", "Cm", "Db", "Db"]
          + ["Cm", "Db", "Cm", "Bbm", "Ab", "Db", "Cm", "Cm"]
          + ["Fm", "Db", "Ab", "Eb", "Fm", "Bbm", "Db", "Cm"]
          + ["Cm", "Db", "Cm", "Bbm", "Ab", "Db", "Fm", "Cm"])
assert len(CHORDS) == BARS

MEL = [
    "G5:4",                           "G5:4",
    "Ab5:4",                          "G5:2 F5:2",
    "C6:2 G5:2",                      "Db6:2 C6:2",
    "G5:2 Eb6:2",                     "Db6:2 Bb5:2",
    "C6:1 Ab5:1 Eb6:2",               "F6:1 Db6:1 Ab5:2",
    "G5:1 C6:1 Eb6:1 C6:1",           "G5:2 F5:2",
    "Ab5:1 C6:1 F6:2",                "Db6:1 Ab5:1 F5:2",
    "Eb6:1 C6:1 Ab5:2",               "G5:1 Bb5:1 Eb6:2",
    "F6:1 Ab6:1 C6:2",                "Db6:1 F6:1 Bb6:2",
    "Ab6:1 F6:1 Db6:1 Ab5:1",         "G5:2 Eb6:2",
    "C6:.5 Db6:.5 C6:1 G5:2",         "Db6:.5 C6:.5 Ab5:1 F6:2",
    "Eb6:.5 Db6:.5 C6:1 G5:2",        "Bb5:1 Db6:1 F6:2",
    "Eb6:1 C6:1 Ab5:2",               "F6:1 Db6:1 Ab5:2",
    "C6:1 Ab5:1 F5:2",                "G5:2 C6:2",
]
assert len(MEL) == BARS

CTR = [
    "C4:4",                           "C4:2 Eb4:2",
    "Db4:2 C4:2",                     "Bb3:2 C4:2",
    "G3:2 Eb4:2",                     "Ab3:2 F4:2",
    "G3:2 C4:2",                      "Bb3:2 Db4:2",
    "Ab3:2 C4:2",                     "Db4:2 Ab3:2",
    "G3:2 Eb4:2",                     "C4:2 G3:2",
    "Ab3:2 C4:2",                     "F4:2 Db4:2",
    "Eb4:2 C4:2",                     "Bb3:2 G3:2",
    "Ab3:2 C4:2",                     "Db4:2 F4:2",
    "Ab3:2 Db4:2",                    "G3:2 C4:2",
    "Eb4:2 C4:2",                     "F4:2 Db4:2",
    "Eb4:2 G3:2",                     "Db4:2 Bb3:2",
    "C4:2 Ab3:2",                     "F4:2 Db4:2",
    "Ab3:2 C4:2",                     "G3:2 C4:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("C", "phrygien", BPM, BAR, "Ce qui Attend Sous l'Eau")
    p.add("melodie", lines(MEL, 0, bar=BAR))

    # l'arpege se resserre : noires jusqu'a la mesure 8, croches ensuite
    arp = arpeggio(CHORDS[:CUT], 0, BAR, 1.0, (0, 1, 2, 1), lo=57)
    arp += arpeggio(CHORDS[CUT:], BAR * CUT, BAR, 0.5, (0, 1, 2, 1), lo=57)
    p.add("arpege", arp)

    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))

    # la basse aussi : blanches, puis la marche de noires
    bass = progression(CHORDS[:CUT], 0, BAR, [(0, 2), (-1, 2)], lo=45)
    bass += progression(CHORDS[CUT:], BAR * CUT, BAR,
                        [(0, 1), (0, 1), (-1, 1), (0, 1)], lo=45)
    p.add("basse", bass)

    p.add("bourdon", pedal(midi("C2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("danger.mid"))
