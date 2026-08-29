#!/usr/bin/env python3
"""Remet les pages TXT de SCOSWAMP au format attendu par le moteur.

  T  <id> <Titre>     titre de scene, une seule ligne, barre inversee ligne 1
  <corps>             replie a 78 colonnes, tient dans les lignes 2 a 20
  M  <hab> <end> <nom>  la creature de la clairiere
  MD <n>              ses coups coutent n ENDURANCE (defaut 2)
  MS <n>              le combat cesse a n ENDURANCE (defaut 0)
  E  <CARAC> <delta>  effet applique en entrant dans la clairiere
  P  <PIERRE> <n>     Pierres Magiques recues
  PC <n> <cats>       n Pierres a choisir parmi les categories N, B, M
  CF <id> <Titre>     la Fuite, quand la page l'autorise
  CL <ok> <ko> [<dok> <dko>]  Tentez votre Chance : ou l'on va, et ce que
                      chaque branche coute en ENDURANCE
  CP <PIERRE> <id> <Titre>  choix qui remet une Pierre Magique
  C  <id> <Titre>     choix, rendus dans les 4 lignes du bas

Ne touche pas aux mots : seuls les retours a la ligne changent. Les lignes
purement decoratives (----- / =====) sautent, la barre de titre les remplace.
"""
import re, sys, textwrap
from pathlib import Path

BODY_ROWS   = 19   # lignes 2..20
CHOICE_ROWS = 4    # lignes 21..24
MAX_FOES    = 3    # doit suivre MAX_FOES dans scoswamp.c
COL         = 39   # largeur d'une colonne de choix (2 par ligne)
WRAP        = 78

RULE = re.compile(r"^[-=_*~#]{4,}\s*$")
# Les directives de jeu : ni titre, ni corps, ni choix. Elles ne se replient
# pas -- une ligne M coupee en deux ne veut plus rien dire.
DIRECTIVE = re.compile(r"^(M|MD|MS|E|P|PC|CF|CP) ")
LEGACY_TITLE = re.compile(r"^\s*(\d{1,3})\s*:\s*(.+?)\s*$")

# ── Derivation des combats depuis la prose ──────────────────────────────────
#
# Les pages ecrivent deja le combat en toutes lettres : "BETE DU BASSIN
# HABILETE: 8 ENDURANCE: 10". Personne ne devrait avoir a le retaper en ligne
# `M`. La derivation se fait ICI, a la construction, et pas dans le moteur :
# l'Apple II n'a plus la place d'un analyseur de prose, la tolerance aux
# variations d'ecriture y serait fragile, et surtout le resultat serait
# invisible -- alors qu'ici il atterrit dans le fichier, lisible dans un diff.
#
# Regle de conduite : automatique quand c'est net, signale sinon. Une page
# qu'on ne sait pas lire garde sa prose et sort dans le rapport.

STATS = {
    "TEXTFR": (r"HABILETE", r"ENDURANCE"),
    "TEXTEN": (r"SKILL",    r"STAMINA"),
}
# Le nom est une suite de mots en capitales, precedee au besoin d'un ordinal
# ecrit normalement : le corpus dit "Premier LOUP HABILETE: 7 ... Deuxieme LOUP
# HABILETE: 6", et sans l'ordinal les deux loups portaient le meme nom dans le
# bandeau -- et "Premier" restait orphelin dans la prose.
NAME = (r"((?:Premier|Premiere|Deuxieme|Troisieme|Second|Seconde|"
        r"First|Second|Third)?\s*"
        r"(?:[A-ZÀ-Ý][A-ZÀ-Ý'-]*\s+){0,3}[A-ZÀ-Ý][A-ZÀ-Ý'-]*)")
FLEE  = re.compile(r"\b(fuite|fuir|enfuir|flee|fleeing)\b", re.I)
DMG   = re.compile(r"\((\d+)\s*(?:au lieu de|instead of)\s*2\)", re.I)
STOP  = re.compile(r"(?:r[eé]duis\w*|reduce\w*)[^.]{0,30}?\b(?:a|to)\s+(\d+)", re.I)
# Une page qui tend des Pierres sans ligne PC : le moteur ne les donnera pas.
# La formulation varie trop (un chiffre, un nombre en lettres, une categorie
# nommee ou sous-entendue) pour deviner sans risque -- on signale.
STONES_GIVEN = re.compile(
    r"\b(?:donne|donnerai|offre|remet|prenez|prendre|choisissez|choisir)\b"
    r"[^.]{0,80}?\bPierres?\b(?![^.]{0,20}\bdesintegre)", re.I)


def derive_combat(text, choices, lang):
    """Rend (texte_nettoye, directives, avertissements)."""
    hab, end = STATS[lang]
    # Le corpus ecrit le bloc de trois facons : "NOM HABILETE: 9 ENDURANCE: 6",
    # "NOM HABILETE : 5 / ENDURANCE : 17", et "NOM - HABILETE : 12 ...". Le
    # tiret separateur est la raison pour laquelle trois pages passaient au
    # travers.
    block = re.compile(NAME + r"\s*(?:[-–—]\s*)?" + hab + r"\s*:?\s*(\d+)\s*/?\s*"
                       + end + r"\s*:?\s*(\d+)")
    hits = list(block.finditer(text))
    if not hits:
        return text, [], []
    warnings = []
    if len(hits) > MAX_FOES:
        return text, [], [f"{len(hits)} adversaires, le moteur en gere "
                          f"{MAX_FOES} : page laissee en prose"]

    # "Parfois, vous les affronterez comme si elles n'etaient qu'un seul
    # monstre ; parfois, vous les combattrez une par une." Les deux rencontres
    # a plusieurs du Marais sont du second type : une ligne M par adversaire,
    # dans l'ordre de la page.
    directives = []
    for m in hits:
        name = " ".join(m.group(1).split())[:23]
        directives.append(f"M {int(m.group(2))} {int(m.group(3))} {name}")

    # Les blocs de stats sortent de la prose : le bandeau les affiche. On
    # retire de la fin vers le debut pour ne pas decaler les positions.
    for m in reversed(hits):
        text = text[:m.start()] + text[m.end():]
    text = text.replace("  ", " ").strip()
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)

    d = DMG.search(text)
    if d: directives.append(f"MD {int(d.group(1))}")

    for cid, ctitle in choices:
        st = STOP.search(ctitle)
        if st:
            directives.append(f"MS {int(st.group(1))}")
            break

    return text, directives, warnings


# Les deux langues : le corpus anglais dit "Lucky" / "Unlucky". Sans elles,
# TEXTEN restait en choix libres pendant que TEXTFR passait au jet -- deux
# regles du jeu differentes selon la langue choisie.
LUCKY   = re.compile(r"\b(?:chanceux|lucky)\b", re.I)
UNLUCKY = re.compile(r"\b(?:malchanceux|unlucky)\b", re.I)
# "vous perdez 2 points d'ENDURANCE" -- le livre attache parfois un cout a une
# branche du jet, et il appartient a la TRANSITION, pas a la page d'arrivee :
# celle du 270 est atteinte depuis cinq pages, une seule fait perdre 2 points.
LOSS = re.compile(r"\b(?:perdez|perdrez|lose)\s+(\d+)\s*(?:points?\s*d[e']\s*ENDURANCE"
                  r"|STAMINA\s*points?)", re.I)


def branch_loss(text, unlucky):
    """Cout en ENDURANCE attache a la branche Chanceux ou Malchanceux."""
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        has_un = UNLUCKY.search(sentence) is not None
        has_lu = LUCKY.search(sentence) is not None and not has_un
        if unlucky and not has_un:
            continue
        if not unlucky and not has_lu:
            continue
        m = LOSS.search(sentence)
        if m:
            return -int(m.group(1))
    return 0


def derive_luck(choices, body):
    """Une paire Chanceux / Malchanceux devient un jet que le moteur joue.

    Le livre ne propose pas ces deux issues, il ORDONNE le jet et annonce ce
    qui arrive dans chaque cas ; les laisser en choix libres revenait a
    demander au joueur de tirer lui-meme les des, et de tricher.
    """
    lucky = [c for c in choices if LUCKY.search(c[1]) and not UNLUCKY.search(c[1])]
    unlucky = [c for c in choices if UNLUCKY.search(c[1])]
    if len(lucky) != 1 or len(unlucky) != 1:
        return choices, None
    text = " ".join(body)
    dok = branch_loss(text, unlucky=False)
    dko = branch_loss(text, unlucky=True)
    line = "CL %03d %03d" % (lucky[0][0], unlucky[0][0])
    if dok or dko:
        line += " %d %d" % (dok, dko)
    rest = [c for c in choices if c not in lucky and c not in unlucky]
    return rest, line


def derive_flee(choices, directives):
    """Transforme le choix de Fuite en ligne CF. Rend (choix_restants, cf)."""
    if any(d.startswith("CF ") for d in directives):
        return choices, None
    for i, (cid, ctitle) in enumerate(choices):
        if FLEE.search(ctitle):
            return choices[:i] + choices[i+1:], f"CF {cid:03d} {ctitle}"
    return choices, None


def parse(path):
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    title, body, choices, directives = None, [], [], []
    for i, l in enumerate(lines):
        if DIRECTIVE.match(l):
            directives.append(l.rstrip())
        elif l.startswith("T ") and title is None:
            rest = l[2:].strip()
            m = re.match(r"^(\d{1,3})\s+(.*)$", rest)
            title = m.group(2).strip() if m else rest
        elif l.startswith("C "):
            m = re.match(r"^(\d{1,3})\s+(.*)$", l[2:].strip())
            if m:
                choices.append((int(m.group(1)), m.group(2).strip()))
        elif RULE.match(l):
            continue
        elif title is None and not body and LEGACY_TITLE.match(l):
            title = LEGACY_TITLE.match(l).group(2)
        else:
            body.append(l)
    while body and not body[-1].strip(): body.pop()
    while body and not body[0].strip(): body.pop(0)
    return title, body, choices, directives

def _w(text, width):
    # break_on_hyphens=False : sinon "spider-shaped" est coupe en deux mots et
    # la ligne se termine sur un tiret orphelin. break_long_words=False : aucun
    # mot n'est jamais casse ; le controle de largeur ci-dessous le verifierait.
    return textwrap.wrap(text, width, break_on_hyphens=False,
                         break_long_words=False)

def wrap(body, width=WRAP):
    out, para = [], []
    for l in body:
        if not l.strip():
            if para: out += _w(" ".join(para), width); para = []
            if out and out[-1] != "": out.append("")
        elif l[0] in " \t":
            # Ligne indentee = deja mise en forme (une liste de commandes, un
            # tableau) : on la garde telle quelle, la replier la collerait en
            # un paragraphe illisible.
            if para: out += _w(" ".join(para), width); para = []
            out.append(l.rstrip()[:width])
        else:
            para.append(l.strip())
    if para: out += _w(" ".join(para), width)
    while out and out[-1] == "": out.pop()
    return out

def choice_rows(choices):
    """Simule le rendu : 2 choix par ligne s'ils tiennent tous deux en COL."""
    i, rows = 0, 0
    while i < len(choices):
        a = 3 + len(choices[i][1])
        if i + 1 < len(choices) and a <= COL and 3 + len(choices[i+1][1]) <= COL:
            i += 2
        else:
            i += 1
        rows += 1
    return rows

def render(scene_id, title, body, choices, directives):
    out = [f"T {scene_id:03d} {title}", ""]
    out += body
    out.append("")
    out += directives
    out += [f"C {cid:03d} {ctitle}" for cid, ctitle in choices]
    return "\n".join(out) + "\n"

def words(seq):
    return " ".join(" ".join(seq).split())

def main():
    root = Path(sys.argv[1])
    apply = "--apply" in sys.argv
    derive = "--derive" in sys.argv
    found = {}          # (lang, id) -> directives, pour le recoupement FR/EN
    problems, changed = [], 0
    for lang in ("TEXTFR", "TEXTEN"):
        for f in sorted((root / lang).rglob("N*.TXT")):
            sid = int(f.stem[1:])
            title, body, choices, directives = parse(f)
            if title is None:
                problems.append(f"{f}: pas de titre"); continue

            if derive and not any(d.startswith("M ") for d in directives):
                text, found_dirs, warns = derive_combat("\n".join(body), choices, lang)
                for w in warns:
                    problems.append(f"{f}: {w}")
                if found_dirs:
                    body = text.split("\n")
                    choices, cf = derive_flee(choices, found_dirs)
                    directives = found_dirs + ([cf] if cf else [])
            if derive and not any(d.startswith("CL ") for d in directives):
                choices, cl = derive_luck(choices, body)
                if cl:
                    directives = directives + [cl]
            if derive and not any(d.startswith("PC ") for d in directives) \
                     and not any(d.startswith("P ") for d in directives) \
                     and STONES_GIVEN.search(" ".join(body)):
                problems.append(f"{f}: une Pierre semble remise ici, mais la "
                                f"page n'a ni ligne PC ni ligne P")
            if derive and directives:
                found[(lang, sid)] = [d for d in directives
                                      if d.split()[0] in ("M", "MD", "MS", "CF")]
            w = wrap(body)
            if len(w) > BODY_ROWS:
                problems.append(f"{f}: corps {len(w)} lignes > {BODY_ROWS}")
            if len(choices) > 6:
                problems.append(f"{f}: {len(choices)} choix > 6 (MAX_CHOICES)")
            r = choice_rows(choices)
            if r > CHOICE_ROWS:
                problems.append(f"{f}: choix sur {r} lignes > {CHOICE_ROWS} "
                                f"({len(choices)} choix)")
            if len(new_bytes := render(sid, title, w, choices, directives).encode("utf-8")) > 1343:
                problems.append(f"{f}: {len(new_bytes)} octets > 1343 (file_buffer)")
            if len(title) > 60:
                problems.append(f"{f}: titre {len(title)} car. > 60")
            if words(w) != words(body):
                problems.append(f"{f}: LE TEXTE A CHANGE")
            new = render(sid, title, w, choices, directives)
            if new != f.read_text(encoding="utf-8", errors="replace"):
                changed += 1
                if apply: f.write_text(new, encoding="utf-8")
    print(f"{'ecrits' if apply else 'a reecrire'} : {changed} fichiers")

    if derive:
        # Le moteur ne lit qu'une langue a la fois, mais le combat doit etre le
        # meme dans les deux : une divergence FR/EN est une erreur de contenu.
        ids = {sid for (_, sid) in found}
        for sid in sorted(ids):
            fr = found.get(("TEXTFR", sid))
            en = found.get(("TEXTEN", sid))
            # Le moteur ne lit qu'une langue, mais les regles doivent etre les
            # memes des deux cotes : on compare la MECANIQUE de chaque
            # directive, pas les titres. C'est ainsi qu'on a vu TEXTEN rester
            # en choix libres pendant que TEXTFR passait au jet de Chance.
            # Combien de champs portent de la mecanique, par directive : le
            # reste est du titre, qui se traduit.
            KEEP = {"M": 3, "MD": 2, "MS": 2, "CL": None, "CF": 2, "PC": 3}

            def mechanics(dirs):
                out = []
                for d in (dirs or []):
                    parts = d.split()
                    if parts[0] in KEEP:
                        out.append(" ".join(parts[:KEEP[parts[0]]]))
                return sorted(out)
            if mechanics(fr) != mechanics(en):
                problems.append(f"N{sid:03d}: FR et EN ne disent pas la meme "
                                f"chose ({mechanics(fr)} / {mechanics(en)})")
        combats = sorted(sid for sid in ids
                         if any(d.startswith("M ") for d in found.get(("TEXTFR", sid), [])))
        print(f"combats derives : {len(combats)}")
        for sid in combats:
            print("   N%03d  %s" % (sid, "  ".join(found[("TEXTFR", sid)])))

    print(f"problemes : {len(problems)}")
    for p in problems[:40]: print("  " + p)

main()
