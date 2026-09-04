#!/usr/bin/env python3
"""Ce que la Mockingboard fera vraiment de la piece : les voix, les cotes, la batterie.

`midi_to_mb.py` ne se laisse pas dicter la voix : il attribue lui-meme, par
hauteur, en alternant les deux puces. Et si la piece a une batterie (canal MIDI
10), la voix 5 devient le canal de bruit : il ne reste que **cinq** voix de
hauteur, 0-1-2 a gauche, 3-4 a droite. Ce script rejoue exactement cette
reduction et rend compte, voix par voix, du nombre de notes, du registre et de
la duree sonnante — c'est le seul moyen honnete de decrire la repartition
gauche/droite dans un README.

    python3 verifier.py village/village.mid --bpm 166
    python3 verifier.py clairieres/15-pont/pont.mid --bpm 150 --drum-voice 5
"""
import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("midi_to_mb", HERE.parent / "midi_to_mb.py")
mb = importlib.util.module_from_spec(spec)
sys.modules["midi_to_mb"] = mb
spec.loader.exec_module(mb)

NAMES = "C C# D D# E F F# G G# A A# B".split()

# l'inverse de mb.DRUM_PERIOD : une periode de bruit -> l'instrument qui l'a produite
PERIOD_NAME = {24: "grosse caisse", 10: "caisse claire", 8: "claves",
               2: "charleston ferme", 4: "charleston ouvert",
               14: "tom grave", 12: "tom aigu", 6: "cymbale"}


def name(idx):
    n = idx + mb.BASE_NOTE
    return NAMES[n % 12] + str(n // 12 - 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("midi")
    ap.add_argument("--bpm", type=float, default=150.0)
    ap.add_argument("--drum-voice", type=int, default=5)
    a = ap.parse_args()

    division, notes = mb.read_midi(a.midi)
    ticked = mb.to_ticks(notes, division, a.bpm)
    drums = mb.drum_hits(ticked)
    pitched = [(s, e, n) for s, e, n, d in ticked if not d]
    nv = 6 - (1 if drums else 0)
    voices = mb.reduce_voices(pitched, nv)
    if drums:                       # la voix des percussions reste vide de tons
        voices = (voices[:a.drum_voice] + [[]] + voices[a.drum_voice:])[:6]

    total = max([e for v in voices for _, e, _ in v if e]
                + [e for _, e, _ in drums] or [1])
    print(f"{Path(a.midi).name} a {a.bpm:g} bpm — {len(pitched)} notes de hauteur, "
          f"{len(drums)} coups de batterie, {total / mb.TICK_HZ:.1f} s, "
          f"{nv} voix de hauteur" + (" + batterie" if drums else ""))
    print(f"{'voix':>4} {'cote':>6} {'notes':>6} {'registre':>12} {'occupation':>11}  role")

    busy_side = [0.0, 0.0]
    for v, seq in enumerate(voices):
        cote = "gauche" if v < 3 else "droite"
        if drums and v == a.drum_voice:
            busy = sum(e - s for s, e, _ in drums)
            kinds = {}
            for _, _, per in drums:
                kinds[PERIOD_NAME.get(per, f"bruit {per}")] = \
                    kinds.get(PERIOD_NAME.get(per, f"bruit {per}"), 0) + 1
            detail = ", ".join(f"{k} {n}" for k, n in
                               sorted(kinds.items(), key=lambda x: -x[1]))
            print(f"{v:>4} {cote:>6} {len(drums):>6} {'bruit':>12} "
                  f"{busy / total * 100:>10.0f}%  BATTERIE — {detail}")
            busy_side[1] += busy
            continue
        if not seq:
            print(f"{v:>4} {cote:>6} {0:>6} {'—':>12} {'—':>11}  (vide)")
            continue
        lo = min(i for _, _, i in seq)
        hi = max(i for _, _, i in seq)
        busy = sum(e - s for s, e, _ in seq)
        busy_side[0 if v < 3 else 1] += busy
        print(f"{v:>4} {cote:>6} {len(seq):>6} "
              f"{name(lo) + '..' + name(hi):>12} {busy / total * 100:>10.0f}%")

    # -- les controles ----------------------------------------------------
    bad = []
    dropped = len(pitched) - sum(len(v) for v in voices)
    if dropped > 0:
        bad.append(f"{dropped} notes abandonnees : plus de {nv} hauteurs a la fois")
    used = [v for v, seq in enumerate(voices)
            if seq or (drums and v == a.drum_voice)]
    for v in range(6):
        if v not in used:
            bad.append(f"voix {v} ({'gauche' if v < 3 else 'droite'}) inutilisee : "
                       f"une partie de moins que ce que la carte peut jouer")
    if voices[0]:
        top = max(i for _, _, i in voices[0])
        for v, seq in enumerate(voices[1:], 1):
            if seq and max(i for _, _, i in seq) > top:
                bad.append(f"la voix {v} monte plus haut que la voix 0 : "
                           f"la melodie n'est pas la partie la plus aigue")
                break
    g, d = busy_side
    if g + d and min(g, d) / max(g, d) < 0.45:
        bad.append(f"stereo desequilibree : {g / (g + d) * 100:.0f}% a gauche, "
                   f"{d / (g + d) * 100:.0f}% a droite")
    if bad:
        for b in bad:
            print("!!", b)
    else:
        print(f"OK — {len(used)} voix employees, stereo "
              f"{g / (g + d) * 100:.0f}/{d / (g + d) * 100:.0f}, aucune note abandonnee")


if __name__ == "__main__":
    main()
