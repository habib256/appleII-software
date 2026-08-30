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
  CU <PIERRE> <id> <Titre>  choix qui exige et consomme une Pierre
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
DIRECTIVE = re.compile(r"^(M|MD|MS|E|P|PC|CF|CP|CU|CL|V) ")
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


# Les douze Pierres, dans les deux langues, telles que le corpus les nomme.
STONE_NAMES = {
    "FEU": "FEU", "FIRE": "FEU",
    "GLACE": "GLACE", "ICE": "GLACE",
    "ILLUSION": "ILLUSION",
    "AMITIE": "AMITIE", "FRIENDSHIP": "AMITIE",
    "CROISSANCE": "CROISSANCE", "GROWTH": "CROISSANCE",
    "BENEDICTION": "BENEDICTION", "BLESSING": "BENEDICTION",
    "TERREUR": "TERREUR", "FEAR": "TERREUR", "TERROR": "TERREUR",
    "FLETRISSURE": "FLETRISSURE", "FETRISSURE": "FLETRISSURE",
    "WITHERING": "FLETRISSURE",
    "MALEDICTION": "MALEDICTION", "CURSE": "MALEDICTION",
    "HABILETE": "HABILETE", "SKILL": "HABILETE",
    "ENDURANCE": "ENDURANCE", "STAMINA": "ENDURANCE",
    "CHANCE": "CHANCE", "LUCK": "CHANCE",
}
# "Utiliser une Pierre de Feu", "Use a Magic Fire Stone", "Pierre d'Amitie",
# "Throw an Ice Magic Stone" : le nom peut preceder ou suivre le mot Pierre.
STONE_IN_TITLE = re.compile(
    # "d Amitie" : le corpus ecrit parfois l'elision avec une espace au
    # lieu d'une apostrophe.
    r"\bPierres?\b(?:\s+Magiques?)?\s+(?:de\s+la\s+|de\s+|d[e']\s*|d\s+)([A-Za-zÀ-ÿ]+)"
    r"|\b([A-Za-z]+)\s+(?:Magic\s+)?Stone\b"
    r"|\bStone\s+of\s+([A-Za-z]+)\b", re.I)


def stone_of_title(title):
    """La Pierre qu'un choix depense, ou None."""
    m = STONE_IN_TITLE.search(title)
    if not m:
        return None
    word = next(g for g in m.groups() if g)
    key = (word.upper()
              .replace("É", "E").replace("È", "E").replace("Ê", "E"))
    return STONE_NAMES.get(key)


# Une liste de Pierres s'ecrit souvent en ellipse : "Une Pierre de Terreur /
# d'Illusion / Aucune de celles-ci". Les suivantes ne repetent pas le mot.
ELLIPSIS = re.compile(r"^(?:de\s+la\s+|de\s+|d[e']\s*)?([A-Za-zÀ-ÿ]+)\s*$", re.I)


def derive_stone_use(choices, already):
    """Un choix qui nomme une Pierre l'EXIGE et la consomme (ligne CU).

    Sans ca, 37 choix du corpus depensaient une Pierre sans toucher au sac, et
    rien n'empechait d'en lancer une qu'on n'avait pas.

    `already` dit si la page porte deja un CU : dans ce cas seulement, un titre
    qui n'est QU'un nom de Pierre est lu comme la suite de la liste. Hors de ce
    contexte la regle serait trop large -- "Illusion" peut etre un mot ordinaire.
    """
    rest, lines = [], []
    listing = already
    for cid, title in choices:
        stone = stone_of_title(title)
        if stone is None and listing:
            m = ELLIPSIS.match(title.strip())
            if m:
                key = (m.group(1).upper().replace("É", "E")
                       .replace("È", "E").replace("Ê", "E"))
                stone = STONE_NAMES.get(key)
        if stone:
            lines.append(f"CU {stone} {cid:03d} {title}")
            listing = True
        else:
            rest.append((cid, title))
    return rest, lines


# Une page qui annonce une perte de caracteristique doit l'appliquer : sans
# ligne E, "vous perdez 3 points d'HABILETE" n'etait que du decor.
# Le verbe qualifie la PHRASE ; les valeurs se lisent ensuite partout dedans.
# "vous perdez 3 points d'HABILETE et 1 point d'ENDURANCE" ne porte qu'un seul
# verbe pour deux effets, et le second passait a la trappe.
EFFECT_VERB = re.compile(
    r"\b(perdez|perdrez|coutent|coute|regagnez|gagnez|ajoutez"
    r"|lose|loses|cost|costs|regain|regains|gain|gains)\b", re.I)
# Les deux langues n'ordonnent pas pareil : "3 points d'HABILETE" contre
# "3 SKILL points". Et l'elision s'ecrit parfois avec une espace.
EFFECT_VALUE = re.compile(
    r"(\d+)\s*(?:points?\s*(?:d[e']\s*|d\s+|of\s+))?"
    r"(ENDURANCE|HABILETE|CHANCE|STAMINA|SKILL|LUCK)", re.I)
# Ce qui rend une perte conditionnelle ou deja prise en charge ailleurs.
EFFECT_GUARD = re.compile(
    r"\b(si|sinon|supplementaire|au lieu de|chaque|initial"
    r"|if|otherwise|instead|additional|each)\b", re.I)
CARAC = {"ENDURANCE": "ENDURANCE", "STAMINA": "ENDURANCE",
         "HABILETE": "HABILETE", "SKILL": "HABILETE",
         "CHANCE": "CHANCE", "LUCK": "CHANCE"}
GAIN = ("regagnez", "gagnez", "ajoutez", "regain", "gain")


def derive_effects(body, directives):
    """Rend (lignes E, avertissements) pour les pertes annoncees par la page.

    Une perte prise dans une branche de jet (CL) ou dans une regle de combat
    (MD) est deja appliquee ailleurs : on ne la compte pas deux fois. Et une
    phrase qui porte "si", "sinon" ou "supplementaire" n'est pas une perte
    seche -- on la signale plutot que de la deviner.
    """
    if any(d.startswith(("E ", "CL ", "MD ")) for d in directives):
        return [], []
    lines, warns = [], []
    for sentence in re.split(r"(?<=[.!?])\s+", " ".join(body)):
        verb = EFFECT_VERB.search(sentence)
        if not verb:
            continue
        hits = EFFECT_VALUE.findall(sentence)
        if not hits:
            continue
        if EFFECT_GUARD.search(sentence):
            warns.append("perte de caracteristique sous condition, "
                         "a trancher a la main : " + " ".join(sentence.split())[:70])
            continue
        sign = "+" if verb.group(1).lower() in GAIN else "-"
        for n, carac in hits:
            lines.append(f"E {CARAC[carac.upper()]} {sign}{int(n)}")
    return lines, warns


# "Si vous y etes deja venu, rendez-vous au 142. Sinon, lisez ce qui suit."
# Le livre confie ce comptage au joueur ; le moteur le tient, donc la phrase
# n'a plus rien a faire dans le texte -- la laisser demanderait au joueur de
# faire a la main ce que la page vient de faire pour lui.
#
# Tous les blancs sont des \s+ : la phrase enjambe une fin de ligne dans sept
# pages sur quatorze, et une version a espace litteral n'en voyait que la
# moitie -- des deux cotes differents, ce qui a saute aux yeux au recoupement
# FR/EN. Les cesures du scan ont par ailleurs mange des espaces ("au238",
# "rendez- vous").
REVISIT = re.compile(
    r"\s*(?:Si\s+vous\s+(?:y\s+)?etes\s+deja\s+venu[^.]*?,\s*rendez-\s*vous\s*au\s*(\d+)\."
    r"(?:\s*(?:Sinon|Autrement)[^.]*\.)?"
    r"|If\s+you(?:'ve|\s+have)\s+been\s+[^.]*?before,\s*go\s+to\s*(\d+)\."
    r"(?:\s*Otherwise[^.]*\.)?)")

# La meme regle sans son but : il est porte par un choix, que le joueur devait
# prendre lui-meme (N118).
REVISIT_MUTE = re.compile(
    r"\s*(?:Si\s+vous\s+y\s+etes\s+deja\s+venu,\s*ignorez\s+ce\s+passage\."
    r"|If\s+you(?:'ve|\s+have)\s+been\s+here\s+before,\s*ignore\s+this\s+passage\.)")
REVISIT_CHOICE = re.compile(r"deja\s+venu|already\s+been|been\s+here\s+before", re.I)


def _cut(text, m):
    """Retire la phrase et recolle sans laisser la double espace du trou."""
    return text[:m.start()].rstrip() + " " + text[m.end():].lstrip()


def derive_revisit(body, choices, directives):
    """Rend (corps, choix, ligne V) pour une clairiere a description double."""
    if any(d.startswith("V ") for d in directives):
        return body, choices, None
    text = "\n".join(body)
    m = REVISIT.search(text)
    if m:
        target = int(m.group(1) or m.group(2))
        return _cut(text, m).split("\n"), choices, f"V {target:03d}"
    m = REVISIT_MUTE.search(text)
    if not m:
        return body, choices, None
    for i, (cid, ctitle) in enumerate(choices):
        if REVISIT_CHOICE.search(ctitle):
            return _cut(text, m).split("\n"), \
                   choices[:i] + choices[i+1:], f"V {cid:03d}"
    return body, choices, None


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
    # Les blancs multiples sont ramenes a un : textwrap les conserve, et le
    # trou laisse par une phrase retiree se voyait a l'ecran.
    text = re.sub(r"\s+", " ", text)
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
    out = [f"T {scene_id:03d} {title}"]
    # La ligne V passe devant tout : le moteur court-circuite la page des
    # qu'il la lit, et une ligne E placee avant elle serait appliquee pour
    # rien -- une seconde fois, en fait, puisqu'on est deja passe par la.
    out += [d for d in directives if d.startswith("V ")]
    directives = [d for d in directives if not d.startswith("V ")]
    out += [""]
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
            if derive:
                body, choices, rv = derive_revisit(body, choices, directives)
                if rv:
                    directives = [rv] + directives
            if derive and not any(d.startswith("CL ") for d in directives):
                choices, cl = derive_luck(choices, body)
                if cl:
                    directives = directives + [cl]
            if derive:
                eff, ewarn = derive_effects(body, directives)
                directives = directives + eff
                for w in ewarn:
                    problems.append(f"{f}: {w}")
            if derive:
                has_cu = any(d.startswith("CU ") for d in directives)
                choices, cus = derive_stone_use(choices, has_cu)
                directives = directives + cus
            if derive and not any(d.startswith("PC ") for d in directives) \
                     and not any(d.startswith("P ") for d in directives) \
                     and STONES_GIVEN.search(" ".join(body)):
                problems.append(f"{f}: une Pierre semble remise ici, mais la "
                                f"page n'a ni ligne PC ni ligne P")
            if derive and directives:
                # Tout enregistrer : c'est `mechanics` qui decide ensuite ce
                # qui compte. Filtrer ici avait rendu le recoupement aveugle
                # aux CU, CL et PC -- et il a laisse passer trois pages ou
                # l'anglais depensait une Pierre que le francais ne depensait
                # pas.
                found[(lang, sid)] = list(directives)
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
            # L'Apple II n'a ni accents ni guillemets francais : un octet
            # hors ASCII sortirait en glyphe faux, et le corpus est
            # volontairement sans accents depuis le depart.
            for ch in set(re.findall(r"[^\x00-\x7f]", "\n".join(body + [title]))):
                problems.append(f"{f}: caractere non ASCII {ch!r}")
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
            KEEP = {"M": 3, "MD": 2, "MS": 2, "CL": None, "CF": 2, "PC": 3,
                    "CU": 3, "CP": 3, "E": None, "V": None}

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
