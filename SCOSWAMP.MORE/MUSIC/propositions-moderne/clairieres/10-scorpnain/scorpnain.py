#!/usr/bin/env python3
"""« Les Pinces et l'Os » — clairiere 10, le Scorpion Geant et le Nain.

Variation de la couleur `danger` : meme demi-ton phrygien, meme bourdon
immobile, meme crescendo par la densite. Mais la page 014 raconte deux choses a
la fois, la bete qui se repait et l'homme qui ne bouge plus, et la piece est
donc en deux matieres :

- le A et le A' sont le Scorpion. L'arpege court en croches **detachees**, une
  note sur trois seulement dure ; la melodie ouvre et ferme sur la seconde
  phrygienne la - si bemol - la, qui est le claquement de la pince ;
- le B est le Nain. L'arpege retombe en noires, la basse en blanches, la
  melodie tient des blanches et descend : c'est le seul endroit des douze
  clairieres ou la musique s'arrete de mordre. « Il vous semble peu probable que
  vos Pierres de Magie aient de l'effet ici. »

La mineur phrygien, 176 a la noire — le tempo le plus vif du lot, celui de la
lutte entendue derriere le tronc. Le bourdon est sur mi, la quinte a vide de la.

28 mesures a 4/4, 38,2 s. Forme intro(4) - A(8) - B(8) - A'(8).

    python3 scorpnain.py && python3 ../../../midi_to_mb.py scorpnain.mid \\
        SCORPNAIN.MB.BIN --bpm 176 --max 2304 --wav SCORPNAIN.wav
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from compose import *                                          # noqa: E402,F403

BPM, BAR, BARS = 176, 4, 28
LEN = BAR * BARS
NAIN = (12, 20)                            # les mesures du Nain, en index

CHORDS = (["Am", "Bb", "Am", "Am"]                             # intro — les bruits
          + ["Am", "Bb", "Am", "Gm", "F", "Bb", "Am", "Am"]    # A — le Scorpion
          + ["Dm", "F", "C", "Gm", "Dm", "Bb", "F", "Am"]      # B — le Nain
          + ["Am", "Bb", "Gm", "F", "Dm", "Bb", "Am", "Am"])   # A' — on s'en va
assert len(CHORDS) == BARS

MEL = [
    "A5:1 Bb5:1 A5:2",                "Bb5:2 F5:2",
    "E5:2 A5:2",                      "C6:1 A5:1 E5:2",
    "A5:.5 Bb5:.5 A5:1 E5:2",         "Bb5:1 D6:1 F6:2",
    "E6:1 C6:1 A5:2",                 "G5:1 Bb5:1 D6:2",
    "C6:1 A5:1 F5:2",                 "D6:1 Bb5:1 F5:2",
    "A5:.5 Bb5:.5 A5:1 C6:2",         "E6:2 A5:2",
    "D6:2 A5:2",                      "C6:2 A5:2",
    "G5:2 E6:2",                      "D6:1 Bb5:1 G5:2",
    "F6:2 D6:2",                      "Bb5:1 D6:1 F6:2",
    "A6:1 F6:1 C6:2",                 "E6:2 A5:2",
    "A6:.5 Bb6:.5 A6:1 E6:2",         "F6:1 D6:1 Bb5:2",
    "G6:1 D6:1 Bb5:2",                "A5:1 C6:1 F6:2",
    "D6:1 F6:1 A6:2",                 "F6:1 Bb5:1 D6:2",
    "C6:1 A5:1 E5:1 A5:1",            "A5:.5 Bb5:.5 A5:3",
]
assert len(MEL) == BARS

CTR = [
    "C4:2 E4:2",                      "D4:2 Bb3:2",
    "A3:2 C4:2",                      "E4:2 A3:2",
    "C4:2 A3:2",                      "F4:2 D4:2",
    "E4:2 C4:2",                      "Bb3:2 G3:2",
    "C4:2 A3:2",                      "D4:2 F4:2",
    "A3:2 C4:2",                      "E4:2 A3:2",
    "F4:2 D4:2",                      "A3:2 C4:2",
    "G3:2 E4:2",                      "Bb3:2 D4:2",
    "A3:2 F4:2",                      "D4:2 Bb3:2",
    "C4:2 A3:2",                      "E4:2 C4:2",
    "A3:2 E4:2",                      "D4:2 F4:2",
    "G3:2 Bb3:2",                     "C4:2 A3:2",
    "F4:2 D4:2",                      "Bb3:2 D4:2",
    "C4:2 E4:2",                      "A3:2 E4:2",
]
assert len(CTR) == BARS

for _s in MEL + CTR:                                # chaque mesure fait 4 temps
    assert abs(sum(float(_t.rpartition(":")[2]) for _t in _s.split()) - BAR) < 1e-6, _s


def build():
    p = Piece("A", "phrygien", BPM, BAR, "Les Pinces et l'Os")
    p.add("melodie", lines(MEL, 0, bar=BAR))

    i, j = NAIN
    # les pinces : croches detachees ; sur le Nain, des noires
    pinces = arpeggio(CHORDS[:i], 0, BAR, 0.5, (0, 1, 2, 1), lo=57)
    pinces += arpeggio(CHORDS[j:], BAR * j, BAR, 0.5, (0, 1, 2, 1), lo=57)
    pinces = [(n, t, 0.42) for n, t, _ in pinces]
    pinces += arpeggio(CHORDS[i:j], BAR * i, BAR, 1.0, (0, 1, 2, 1), lo=57)
    p.add("arpege", pinces)

    p.add("contre-chant", lines(CTR, 0, bar=BAR))
    p.add("accords", bed(CHORDS, 0, BAR, lo=50, which=1))

    marche = [(0, 1), (0, 1), (-1, 1), (0, 1)]
    p.add("basse", progression(CHORDS[:i], 0, BAR, marche, lo=47)
                   + progression(CHORDS[i:j], BAR * i, BAR, [(0, 2), (-1, 2)], lo=47)
                   + progression(CHORDS[j:], BAR * j, BAR, marche, lo=47))

    p.add("bourdon", pedal(midi("E2"), 0, LEN, retrig=BAR * 4))
    return p


if __name__ == "__main__":
    build().write(Path(__file__).with_name("scorpnain.mid"))
