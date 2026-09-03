#!/usr/bin/env python3
"""Ce que la Mockingboard fera vraiment de la piece : six voix, deux cotes.

`midi_to_mb.py` ne se laisse pas dicter la voix : il attribue lui-meme, par
hauteur, en alternant les deux puces. Ce script rejoue exactement sa reduction
et rend compte, voix par voix, du nombre de notes, du registre et de la duree
sonnante — c'est le seul moyen honnete de decrire la repartition gauche/droite
dans un README.

    python3 verifier.py village/VILLAGE.mid --bpm 166
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


def name(idx):
    n = idx + mb.BASE_NOTE
    return NAMES[n % 12] + str(n // 12 - 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("midi")
    ap.add_argument("--bpm", type=float, default=150.0)
    a = ap.parse_args()
    division, notes = mb.read_midi(a.midi)
    ticks = mb.to_ticks(notes, division, a.bpm)
    voices = mb.reduce_voices(ticks, 6)
    total = max((e for v in voices for _, e, _ in v if e), default=1)
    print(f"{Path(a.midi).name} a {a.bpm:g} bpm — {len(notes)} notes ecrites, "
          f"{total / mb.TICK_HZ:.1f} s")
    print(f"{'voix':>4} {'cote':>6} {'notes':>6} {'registre':>12} {'occupation':>11}")
    for v, seq in enumerate(voices):
        if not seq:
            print(f"{v:>4} {'G' if v < 3 else 'D':>6} {0:>6}")
            continue
        lo = min(i for _, _, i in seq)
        hi = max(i for _, _, i in seq)
        busy = sum(e - s for s, e, _ in seq)
        print(f"{v:>4} {'gauche' if v < 3 else 'droite':>6} {len(seq):>6} "
              f"{name(lo) + '..' + name(hi):>12} {busy / total * 100:>10.0f}%")
    dropped = len(notes) - sum(len(v) for v in voices)
    if dropped > 0:
        print(f"!! {dropped} notes abandonnees (plus de six a la fois)")


if __name__ == "__main__":
    main()
