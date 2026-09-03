#!/usr/bin/env python3
"""« Quatre Chemins » — clairiere 6, le croisement (page 121, une seule page).

Variation de la couleur `nord`, et la plus litterale : meme mode que la zone —
**mi eolien** — meme bourdon de mi, meme basse en noires. Le croisement est le
centre du Marais nord, il n'avait aucune raison de changer de couleur ; il avait
une raison de changer de forme.

Le procede de la zone est l'ostinato fixe. Ici il est fixe **a l'interieur d'un
panneau** et il change a chaque panneau : quatre cellules de quatre croches,
une par direction, chacune batie sur d'autres degres du meme mode. La piece est
donc intro(4) - nord(6) - sud(6) - est(6) - ouest(6), et la meme tete de melodie
revient au debut de chaque panneau, transposee : c'est la meme question posee
quatre fois, « laquelle allez-vous choisir ? ».

Dans l'intro la cellule est en noires : on est arrete au milieu du carrefour.
Elle passe en croches des le premier panneau, et ne s'arrete plus.

28 mesures a 4/4, 46,7 s.

    python3 croisement.py && python3 ../../../midi_to_mb.py croisement.mid \\
        CROISEMENT.MB.BIN --bpm 144 --max 2304 --wav CROISEMENT.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 144, 4, 28
LEN = BAR * BARS

CHORDS = (["Em", "Em", "C", "D"]                               # intro — l'arret
          + ["Em", "G", "D", "Em", "C", "Bm"]                  # nord
          + ["Am", "Em", "C", "G", "Am", "Bm"]                 # sud
          + ["G", "D", "Em", "C", "G", "D"]                    # est
          + ["C", "Am", "Bm", "Em", "D", "Em"])                # ouest
assert len(CHORDS) == BARS

MEL = [
    "E5:2 B5:2",                      "G5:1 B5:1 E6:2",
    "D6:1 B5:1 G5:2",                 "A5:1 F#5:1 D5:2",
    "E6:1 B5:1 D6:2",                 "B5:2 G5:2",           # nord — la tete
    "D6:1 F#6:1 A6:2",                "G6:1 E6:1 B5:2",
    "C6:1 E6:1 G6:2",                 "F#6:1 D6:1 B5:2",
    "A5:1 E5:1 G5:2",                 "E5:2 D5:2",           # sud — la tete
    "C6:1 G5:1 E5:2",                 "D6:1 B5:1 G5:2",
    "A5:1 C6:1 E6:2",                 "D6:1 B5:1 F#5:2",
    "G5:1 D6:1 B5:2",                 "D6:2 A5:2",           # est — la tete
    "E6:1 B5:1 G6:2",                 "E6:1 C6:1 G5:2",
    "B5:1 D6:1 G6:2",                 "F#6:1 A6:1 D6:2",
    "C6:1 G5:1 E6:2",                 "A5:2 E5:2",           # ouest — la tete
    "F#6:1 D6:1 B5:2",                "G6:1 E6:1 B5:2",
    "D6:1 A5:1 F#5:2",                "E6:4",
]
assert len(MEL) == BARS

CTR = [
    "G4:2 B3:2",                      "E4:2 G4:2",
    "C4:2 E4:2",                      "F#4:2 A3:2",
    "B3:2 E4:2",                      "D4:2 B3:2",
    "A3:2 F#4:2",                     "G4:2 E4:2",
    "E4:2 C4:2",                      "D4:2 F#4:2",
    "C4:2 A3:2",                      "E4:2 B3:2",
    "G4:2 E4:2",                      "B3:2 D4:2",
    "A3:2 C4:2",                      "F#4:2 D4:2",
    "B3:2 G4:2",                      "A3:2 D4:2",
    "E4:2 G4:2",                      "C4:2 E4:2",
    "D4:2 B3:2",                      "F#4:2 A3:2",
    "E4:2 G4:2",                      "C4:2 A3:2",
    "D4:2 F#4:2",                     "B3:2 E4:2",
    "A3:2 F#4:2",                     "E4:2 B3:2",
]
assert len(CTR) == BARS

# une cellule par direction, toutes dans le meme mode et la meme bande
NORD = [midi("B4"), midi("G4"), midi("A4"), midi("E4")]
SUD = [midi("A4"), midi("E4"), midi("F#4"), midi("D4")]
EST = [midi("D4"), midi("G4"), midi("B4"), midi("G4")]
OUEST = [midi("E4"), midi("A4"), midi("C5"), midi("A4")]


def build():
    p = Piece("E", "eolien", BPM, BAR, "Quatre Chemins")
    p.add("melodie", lines(MEL, 0, bar=BAR))

    # l'intro en noires : on est arrete. Puis un panneau de six mesures par route.
    aig = ostinato(NORD, 1.0, 0, BAR * 4)
    for k, cell in enumerate((NORD, SUD, EST, OUEST)):
        aig += ostinato(cell, 0.5, BAR * (4 + 6 * k), BAR * 6)
    p.add("ostinato", aig)

    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 1), (0, 1), (-1, 1), (0, 1)], lo=45))
    p.add("bourdon", pedal(midi("E2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("croisement.mid"))
