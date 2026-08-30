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
    # Seconde passe. Les memes deux familles, vues cette fois en cherchant les
    # FORMES du degat plutot que le vocabulaire : un mot du corpus absent du
    # livre ne prouve plus rien (le portage ecrit sa propre prose, 1080 mots
    # sont dans ce cas), mais "aei", "eo", "eu" et "-au" au milieu d'un mot
    # sont des signatures.
    "apparaeit": "apparait", "disparaeit": "disparait",
    "faeiences": "faiences", "reparaeitre": "reparaitre",
    "traeinant": "trainant", "traeitre": "traitre", "traeitrise": "traitrise",
    "ceote": "cote", "ceotes": "cotes", "eote": "ote", "eoterez": "oterez",
    "teot": "tot", "veotre": "votre", "freole": "frole",
    "breule": "brule", "breulent": "brulent",
    "breulure": "brulure", "breulures": "brulures", "coeutent": "coutent",
    "eepe": "epee", "eepes": "epees", "geeant": "geant",
    "cadau": "cadeau", "coutau": "couteau", "ecritau": "ecriteau",
    "lambaux": "lambeaux", "pommau": "pommeau", "ridau": "rideau",
    "ridaux": "rideaux", "tablau": "tableau",
    "gante": "geante", "gantes": "geantes", "geante": "geante",
    "crer": "creer", "agrable": "agreable", "obezissez": "obeissez",
    "anne": "annee", "ida": "ideal", "aggression": "agression",
}
# "l'au" et "d'au" : l'apostrophe empeche un remplacement par mot entier.
FR_APOS = {"l'au": "l'eau", "d'au": "d'eau", "l'entre": "l'entree"}

EN = {
    "oisaux": "birds",
}

# ── Les guillemets ────────────────────────────────────────────────────────
# Le scan a rendu « par "e" et » par "u", deux lettres qui ne sont jamais un
# mot francais isole : "e Venez donc, venez u, dit-il". L'Apple II n'affiche
# pas les guillemets francais, donc la correction est le guillemet droit.
#
# Deux exceptions, exclues par la forme : les "(e)" de la page de titre
# ("un(e) aventurier(e)"), gardes par la parenthese dans le contexte, et un
# "e" de la page 305 qui vaut un c cedille, corrige nommement plus bas.
QUOTE_OPEN  = re.compile(r"(?<![\w'()])e\s+(?=[\wÀ-ÿ\"])")
QUOTE_CLOSE = re.compile(r"\s+u(?![\w'()])")

# ── Les elisions ──────────────────────────────────────────────────────────
# "vous perdez 2 points d ENDURANCE", "repartir vers l ouest", "il s ecroule",
# "des qu un des deux" : 128 apostrophes perdues dans 54 pages. Aucune des
# lettres visees n'est un mot francais isole, et l'elision ne se fait que
# devant une voyelle ou un h -- d'ou une regle qui ne peut pas se tromper sur
# "a" ni sur "y", les deux vrais mots d'une lettre.
ELISION = re.compile(r"(?<![\w'\-])(qu|[cdjlmnstCDJLMNST])[ \t]+(?=[aeiouyhAEIOUYH])")
# "jusqu au nid", "lorsqu on lui demande" : la meme elision, mais portee par
# la fin d'un mot. Les seuls mots francais finissant par "qu" sont justement
# ceux qui s'elident.
ELISION_QU = re.compile(r"\b(\w+qu)\s+(?=[aeiouyhAEIOUYH])")
# Le guillemet fermant deja present garde l'espace du guillemet francais.
QUOTE_TAIL = re.compile(r"\s+\"\s*$")

# La partie machine d'une ligne de directive : numeros et mots-cles. Le titre
# qui suit est de la prose et se corrige comme le reste.
PREFIX = re.compile(r"^((?:T|M|MD|MS|E|P|PC|C|CF|CP|CU|CL|V)\s+"
                    r"(?:[A-Z]+\s+)?[-+]?\d+(?:\s+\d+)*\s*)")

# Corrections nommees, verifiees en contexte une par une.
PHRASES = {
    "poussent e a et la": "poussent ca et la",   # « çà et là »
    "Tue z-le": "Tuez-le",
    "menace ante": "menacante",
    "L'Aigle menace ant": "L'Aigle menacant",
    "en lane\nant": "en lancant",
    "etant seur": "etant sur",
}


def match_case(src, dst):
    if src.isupper():
        return dst.upper()
    if src[0].isupper():
        return dst.capitalize()
    return dst


# La meme elision, mais coupee par une fin de ligne : "il hurle et s\necroule".
# On ne recolle jamais par-dessus une ligne de directive -- "d" suivi de
# "E ENDURANCE -2" n'est pas une elision, c'est la fin d'un paragraphe.
ELISION_NL = re.compile(
    r"(?<![\w'\-])(qu|\w*qu|[cdjlmnstCDJLMNST])\n(?!(?:T|M|MD|MS|E|P|PC|C|CF|CP|CU|CL|V)\s+\d)"
    r"(?=[aeiouyhAEIOUYH])")


def fix_line(line, french):
    """Guillemets et elisions, hors de la partie machine d'une directive."""
    if not french:
        return line, 0
    m = PREFIX.match(line)
    head, rest = (line[:m.end()], line[m.end():]) if m else ("", line)
    n = 0
    rest, k = QUOTE_OPEN.subn('"', rest);  n += k
    rest, k = QUOTE_CLOSE.subn('"', rest); n += k
    rest, k = ELISION.subn(lambda x: x.group(1) + "'", rest); n += k
    rest, k = ELISION_QU.subn(lambda x: x.group(1) + "'", rest); n += k
    rest, k = QUOTE_TAIL.subn('"', rest); n += k
    return head + rest, n


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
            for bad, good in (PHRASES.items() if lang == "TEXTFR" else ()):
                if bad in src:
                    src = src.replace(bad, good); total_fixes += 1
            # Ne toucher qu'au texte : une directive porte des noms machine.
            n = 0
            if lang == "TEXTFR":
                src, k = ELISION_NL.subn(lambda m: m.group(1) + "'", src); n += k
            out = []
            for line in src.split("\n"):
                # La tete d'une directive porte des noms machine : elle ne se
                # corrige jamais. Son titre, lui, est de la prose comme le
                # reste -- c'est la que "Utiliser la Pierre d Amitie" vivait.
                m = PREFIX.match(line)
                head, rest = (line[:m.end()], line[m.end():]) if m else ("", line)
                rest, k = fix_line(rest, lang == "TEXTFR"); n += k
                rest, k = fix_text(rest, table, apos); n += k
                out.append(head + rest)
            if n:
                total_files += 1; total_fixes += n
                if args.apply:
                    f.write_text("\n".join(out), encoding="utf-8")
                else:
                    print(f"  {f} : {n}")
    print(f"{'corriges' if args.apply else 'a corriger'} : "
          f"{total_fixes} occurrences dans {total_files} fichiers")


main()
