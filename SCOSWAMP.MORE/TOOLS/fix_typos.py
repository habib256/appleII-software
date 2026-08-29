#!/usr/bin/env python3
"""Corrige les coquilles du corpus, en francais et en anglais.

Le corpus est volontairement sans accents -- l'Apple II n'en affiche pas --
mais la conversion qui les a retires s'est mal passee par endroits. Deux
familles de degats, toutes deux visibles a l'oeil une fois qu'on les nomme :

  - un accent circonflexe rendu par deux lettres : maitre -> "maeitre",
    aussitot -> "aussiteot", ou -> "oeu", git -> "geit" ;
  - une lettre avalee avec l'accent : geant -> "gant", creature -> "crature",
    eau -> "au", beaucoup -> "baucoup", epees -> "epes".

La liste ci-dessous a ete etablie en comparant le vocabulaire du corpus a
celui du LIVRE (le PDF d'origine, ou les accents sont intacts) : un mot du
corpus absent du livre est un suspect, et le mot du livre le plus proche donne
la correction. Chaque entree a ete verifiee en contexte -- "gant" est toujours
le Geant et jamais un gant, "vent" en revanche est bien le vent et n'est pas
corrige.

    python3 fix_typos.py --root <depot> [--apply]
"""
import argparse
import re
from pathlib import Path

# Coquilles verifiees une par une. La casse est preservee a l'application.
FR = {
    "maeitre": "maitre", "maeitres": "maitres", "paraeit": "parait",
    "aussiteot": "aussitot", "bienteot": "bientot", "pluteot": "plutot",
    "oeu": "ou", "geit": "git",
    "oisaux": "oiseaux", "gant": "geant", "gants": "geants",
    "crature": "creature", "cratures": "creatures", "crez": "creez",
    "araignes": "araignees", "araigne": "araignee",
    "pau": "peau", "baucoup": "beaucoup", "morcaux": "morceaux",
    "nivau": "niveau", "ide": "idee", "epes": "epees",
    "fetrissure": "fletrissure", "dentele": "dentelee", "menae": "menace",
}
# "l'au" et "d'au" : l'apostrophe empeche un remplacement par mot entier.
FR_APOS = {"l'au": "l'eau", "d'au": "d'eau", "l'entre": "l'entree"}

EN = {
    "oisaux": "birds",
}


def match_case(src, dst):
    if src.isupper():
        return dst.upper()
    if src[0].isupper():
        return dst.capitalize()
    return dst


def fix_text(text, table, apos):
    changed = 0

    def one(m):
        nonlocal changed
        repl = match_case(m.group(0), table[m.group(0).lower()])
        if repl != m.group(0):
            changed += 1
        return repl

    if table:
        text = re.sub(r"\b(" + "|".join(sorted(table, key=len, reverse=True)) + r")\b",
                      one, text, flags=re.I)
    for bad, good in apos.items():
        pat = re.compile(re.escape(bad) + r"\b", re.I)
        text, n = pat.subn(lambda m: match_case(m.group(0), good), text)
        changed += n
    return text, changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    total_files = total_fixes = 0
    for lang, table, apos in (("TEXTFR", FR, FR_APOS), ("TEXTEN", EN, {})):
        for f in sorted((args.root / "SCOSWAMP" / lang).rglob("N*.TXT")):
            src = f.read_text(encoding="utf-8")
            # Ne toucher qu'au texte : une directive porte des noms machine.
            out, n = [], 0
            for line in src.split("\n"):
                if re.match(r"^(M|MD|MS|E|P|PC|CF|CP|CU|CL) ", line):
                    out.append(line); continue
                fixed, k = fix_text(line, table, apos)
                out.append(fixed); n += k
            if n:
                total_files += 1; total_fixes += n
                if args.apply:
                    f.write_text("\n".join(out), encoding="utf-8")
                else:
                    print(f"  {f} : {n}")
    print(f"{'corriges' if args.apply else 'a corriger'} : "
          f"{total_fixes} occurrences dans {total_files} fichiers")


main()
