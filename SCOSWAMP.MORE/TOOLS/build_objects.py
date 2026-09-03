#!/usr/bin/env python3
"""Genere le catalogue des objets et drapeaux, OBJFR.TXT / OBJEN.TXT.

Un objet (Cape Rouge) et un fait ("vous servez Gayolard") sont le meme
mecanisme : un BIT NOMME, pose par la ligne `G`, efface par `GX`, teste par
les choix `CI` (il faut l'avoir), `CN` (il ne faut pas), `GU` (il faut, et
c'est consomme). Le jeton est identique dans les deux langues -- c'est lui
que portent les pages ; seul le libelle du sac se traduit. Un jeton prefixe
d'un point est un drapeau cache : jamais montre dans le sac.

L'ORDRE FAIT FOI : la ligne N est le bit N. Ce script est la seule source.

    python3 build_objects.py --root <depot>
"""
import argparse
from pathlib import Path

# (jeton, libelle FR, libelle EN) -- jeton '.xxx' = drapeau cache.
OBJECTS = [
    ('ANNEAU',    "Anneau de Cuivre",   "Copper Ring"),
    ('CAPE',      "Cape Rouge",         "Red Cape"),
    ('CH',         "Chaine d'Or",        "Gold Chain"),
    ('AI',         "Aimant d'Or",        "Gold Magnet"),
    ('FI',         "Fiole scellee",      "Sealed Vial"),
    ('BA',         "Baie d'Antherique",  "Antherique Berry"),
    ('EP',         "Epee Magique",       "Magic Sword"),
    ('BJ',         "Bijou Violet",       "Purple Jewel"),
    ('CO',         "Corne de Licorne",   "Unicorn Horn"),
    ('PL',         "Plumes de Perroquet", "Parrot Feathers"),
    ('GR',         "Graines d'Arbre-Epee", "Sword Tree Seeds"),
    ('.T',         "", ""),   # le buisson d'Antherique est trouve
]
# Les drapeaux caches se rangent APRES les objets : le moteur montre dans le
# sac tout ce qui precede le premier d'entre eux (OBJ_HIDDEN0, rules.h).

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    args = ap.parse_args()

    assert len(OBJECTS) <= 32, "32 bits, pas un de plus"
    toks = [o[0] for o in OBJECTS]
    assert len(set(toks)) == len(toks), "jetons en double"
    for name, idx in (("OBJFR.TXT", 1), ("OBJEN.TXT", 2)):
        out = "\n".join(f"{o[0]} {o[idx]}".rstrip() for o in OBJECTS) + "\n"
        (args.root / "SCOSWAMP" / name).write_text(out, encoding="ascii")
    print(f"{len(OBJECTS)} bits ({sum(1 for o in OBJECTS if not o[0].startswith('.'))} "
          f"objets visibles, {sum(1 for o in OBJECTS if o[0].startswith('.'))} drapeaux)")
    return 0

raise SystemExit(main())
