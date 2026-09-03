#!/usr/bin/env python3
"""« Pierres Plates » — clairiere 34, les pierres et le tronc creux. Do eolien, 150.

Pages 105, 330, 390. « Le sol y est ferme ; vous pouvez y penetrer d'un pas
assure. Des pierres plates de grande taille, un tronc creux massif, et deux
chemins. » Et au retour : « le tronc a deja abrite autre chose que des
ossements. »

C'est la seule clairiere sure des onze — sol ferme, pas de monstre a l'entree —
et la musique le dit par le **vide**, pas par la joie. L'arpege ne joue que des
**quintes a vide** (fondamentale, quinte, octave : la liste `CREUX` remplace
chaque accord par sa quinte nue) ; la seule voix qui possede encore une tierce,
et donc qui dise le mode, est le lit d'accords tenus. C'est un tronc creux :
l'harmonie sonne de l'exterieur, il n'y a rien dedans.

Le **coup sur le bois** est la note repetee de la melodie, deux noires sur la
meme hauteur, aux mesures 5, 6, 17, 18 et 21 : on frappe le tronc pour savoir
s'il est habite.

28 mesures a 4/4, 44,8 s. Forme intro(4) - A(8) - B(8) - A'(8).

    python3 tronc.py && python3 ../../../midi_to_mb.py tronc.mid \\
        TRONC.MB.BIN --bpm 150 --max 2304 --wav TRONC.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 150, 4, 28
LEN = BAR * BARS

CHORDS = (["Cm", "Gm", "Ab", "Cm"]
          + ["Cm", "Ab", "Eb", "Bb", "Cm", "Fm", "Gm", "Cm"]
          + ["Ab", "Eb", "Bb", "Fm", "Ab", "Bb", "Cm", "Cm"]
          + ["Cm", "Ab", "Eb", "Bb", "Fm", "Ab", "Gm", "Cm"])
assert len(CHORDS) == BARS

# le tronc est creux : l'arpege ne connait que la quinte a vide de chaque accord
CREUX = [c.replace("m", "") + "5" for c in CHORDS]

MEL = [
    "G5:4",                           "G5:2 C6:2",
    "Eb6:2 C6:2",                     "G5:2 C5:2",
    "C6:1 C6:1 G5:2",                 "Eb6:1 Eb6:1 C6:2",
    "Bb5:1 G5:1 Eb6:2",               "F6:2 D6:2",
    "Eb6:1 C6:1 G5:2",                "Ab5:1 C6:1 F6:2",
    "G5:1 D6:1 Bb5:2",                "C6:2 G5:2",
    "Ab5:1 Eb6:1 C6:2",               "Bb5:1 G5:1 Eb6:2",
    "F6:1 D6:1 Bb5:2",                "C6:1 Ab5:1 F6:2",
    "Eb6:1 Eb6:1 C6:2",               "D6:1 D6:1 Bb5:2",
    "C6:1 G6:1 Eb6:2",                "G5:2 C6:2",
    "C6:1 C6:1 G5:2",                 "Eb6:1 C6:1 Ab5:2",
    "G6:1 Eb6:1 Bb5:2",               "F6:1 D6:1 Bb5:2",
    "Ab5:1 F6:1 C6:2",                "Eb6:1 C6:1 Ab5:2",
    "D6:1 Bb5:1 G5:2",                "C6:4",
]
assert len(MEL) == BARS

CTR = [
    "C4:2 G3:2",                      "D4:2 Bb3:2",
    "C4:2 Ab3:2",                     "Eb4:2 G3:2",
    "G3:2 Eb4:2",                     "Ab3:2 C4:2",
    "Bb3:2 G4:2",                     "F4:2 D4:2",
    "Eb4:2 C4:2",                     "Ab3:2 F4:2",
    "D4:2 Bb3:2",                     "Eb4:2 G3:2",
    "C4:2 Ab3:2",                     "G4:2 Eb4:2",
    "D4:2 F4:2",                      "Ab3:2 C4:2",
    "Eb4:2 Ab3:2",                    "F4:2 D4:2",
    "G3:2 Eb4:2",                     "C4:2 G3:2",
    "G3:2 Eb4:2",                     "C4:2 Ab3:2",
    "Bb3:2 G4:2",                     "D4:2 F4:2",
    "Ab3:2 C4:2",                     "Eb4:2 Ab3:2",
    "Bb3:2 D4:2",                     "C4:2 G3:2",
]
assert len(CTR) == BARS


def build():
    p = Piece("C", "eolien", BPM, BAR, "Pierres Plates")
    p.add("melodie", lines(MEL, 0, bar=BAR))
    p.add("arpege", arpeggio(CREUX, 0, BAR, 0.5, (0, 1, 2, 1), lo=57))
    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))
    p.add("basse", progression(CHORDS, 0, BAR,
                               [(0, 2), (-1, 1), (0, 1)], lo=43))
    p.add("bourdon", pedal(midi("C2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("tronc.mid"))
