#!/usr/bin/env python3
"""Build the deterministic image-generation manifest for SCOSWAMP."""

from __future__ import annotations

import argparse
import re
import json
from pathlib import Path


STYLE = """Use case: illustration-story
Asset type: native Apple II HGR scene illustration for SCOSWAMP
Primary request: Illustrate the numbered French gamebook scene below faithfully.
Style/medium: late-1970s sword-and-sorcery pulp illustration translated into hard-edged Apple II HGR shapes; muscular readable silhouettes, bold brush-and-ink shadows, selective flat color accents.
Composition/framing: landscape 35:24; select one decisive visual moment, never a collage of choices or backstory; one strong focal action; essential shapes remain readable at 280x192 and are at least 3-4 HGR pixels thick; keep critical content away from the extreme edges.
Color palette: use only black #000000, white #FFFFFF, violet #AA1AD1, green #6FE62C, blue #008AB5, orange #FF7247; keep violet/green regions spatially separate from blue/orange regions; 35-55% solid black negative space.
Lighting/mood: theatrical menace, adventure, immediate action.
Materials/textures: hard-edged flat fills and deliberate broad ink shadows only; no random grain.
Text (verbatim): ""
Constraints: no visible words, letters, numbers, captions, border, UI, logo, signature, or watermark; no gradients; no anti-aliasing; no photorealistic texture; no tiny decorative detail; one coherent scene, not a collage.
Avoid: glossy modern concept art, modern objects, smooth airbrush shading, comic speech effects, noisy dithering, illegible micro-detail, extra characters or objects not supported by the scene.

French scene source:
"""


# ── Images de bataille ──────────────────────────────────────────────────────
# Le moteur bascule en mode mixte pendant un combat : l'illustration occupe les
# 20 lignes du haut, l'echange d'assauts les 4 du bas. Les 32 dernieres lignes
# de pixels sont donc RECOUVERTES par la fenetre de texte -- c'est la contrainte
# de cadrage qui distingue une image de bataille d'une illustration de scene.
BATTLE_HERO = """The hero, drawn identically in every battle image: a lean human adventurer in a hooded green cloak over chainmail, a round shield on the left arm, a straight sword raised in the right hand, a backpack on the shoulders, seen three-quarters from behind-left so the face stays hidden."""

BATTLE_STYLE = """Use case: illustration-story
Asset type: native Apple II HGR battle tableau for SCOSWAMP
Primary request: One duel, two figures. The hero faces the adversary named below; both are fully visible, mid-action, caught at the moment blades or claws are about to meet.
Composition/framing: landscape 35:24 for a 280x192 screen. CRITICAL: during play a text window covers the bottom sixth of the image, and the first attempt had the hero's feet cut off by it. Both figures must be COMPLETE — head to feet — within the upper three quarters of the frame, and the lowest quarter must be plain dark empty ground with nothing in it. Hero in the left third facing right, adversary in the right two thirds facing left, a clear gap of dark ground between them; readable silhouettes at 280x192, every essential shape at least 3-4 HGR pixels thick.
""" + BATTLE_HERO + """
Style/medium: late-1970s sword-and-sorcery pulp illustration translated into hard-edged Apple II HGR shapes; muscular readable silhouettes, bold brush-and-ink shadows, selective flat color accents.
Color palette: use only black #000000, white #FFFFFF, violet #AA1AD1, green #6FE62C, blue #008AB5, orange #FF7247; keep violet/green regions spatially separate from blue/orange regions; 35-55% solid black negative space.
Lighting/mood: theatrical menace, imminent violence.
Materials/textures: hard-edged flat fills and deliberate broad ink shadows only; no random grain.
Text (verbatim): ""
Constraints: no visible words, letters, numbers, captions, border, UI, logo, signature, or watermark; no gradients; no anti-aliasing; no photorealistic texture; no tiny decorative detail; exactly two figures, the hero and the adversary.
Avoid: glossy modern concept art, modern objects, smooth airbrush shading, comic speech effects, noisy dithering, illegible micro-detail, extra creatures or bystanders.

The adversary, and the French scene it comes from:
"""


def battle_rows(root, characters):
    """Une entree par clairiere portant un adversaire."""
    import re
    game = root / "SCOSWAMP"
    more = root / "SCOSWAMP.MORE"
    stat = re.compile(r"([A-Z\u00c0-\u00dd][A-Z\u00c0-\u00dd' -]{2,30}?)\s*HABILETE\s*:?\s*(\d+)\s*/?\s*ENDURANCE\s*:?\s*(\d+)")
    rows, seen = [], set()
    for path in sorted((game / "TEXTFR").rglob("N*.TXT")):
        scene_id = int(path.stem[1:])
        text = path.read_text(encoding="utf-8")
        names = [m.group(1).strip() for m in stat.finditer(text)]
        if not names and not text.startswith("T ") or scene_id in seen:
            pass
        # une page deja convertie porte une ligne "M <hab> <end> <nom>"
        for line in text.splitlines():
            if line.startswith("M ") and len(line.split()) >= 4:
                names.append(line.split(None, 3)[3].strip())
        if not names or scene_id in seen:
            continue
        seen.add(scene_id)
        sid = f"{scene_id:03d}"
        bucket = f"N{(scene_id // 50) * 50:03d}"
        rows.append({
            "id": scene_id,
            "scene": f"B{sid}",
            "adversaries": names,
            "text_path": str(path.relative_to(root)),
            "source_png": str((more / "GENERATED" / f"B{sid}.png").relative_to(root)),
            "hgr_rle": str((game / "IMG" / bucket / f"B{sid}.RLE.BIN").relative_to(root)),
            "preview_png": str((more / "HGR-PREVIEW" / f"B{sid}.png").relative_to(root)),
            "prompt": (BATTLE_STYLE + "Adversary: " + ", ".join(names)
                       + "\n\n" + text.strip()
                       + character_block(text + " " + " ".join(names), characters)),
            "refs": refs_for(text + " " + " ".join(names), characters, root),
            "bible": bible_hash(text + " " + " ".join(names), characters),
            "status": "pending",
        })
    return rows


# ── La bible des personnages ────────────────────────────────────────────────
#
# Chaque image etait generee seule, a partir de sa seule page : rien ne liait
# le Maitre des Loups d'une illustration a celui de la suivante, ni la creature
# d'une scene a celle de son image de bataille. Le heros lui-meme changeait de
# visage. La constance ne s'obtient pas en demandant "le meme personnage" : il
# faut que le MEME TEXTE decrive le personnage dans tous les prompts ou il
# apparait. C'est ce que fait cette injection.

# Trois bibles, un seul mecanisme. L'ordre compte a l'affichage du prompt :
# le decor pose le monde, les personnages et les creatures s'y tiennent.
BIBLES = ("decors.json", "characters.json", "monsters.json", "objects.json")


# Le medium et la palette etaient decrits deux fois, une fois pour les scenes
# et une fois pour les batailles : deux textes qui pouvaient deriver l'un de
# l'autre. Ils n'existent plus qu'ici.
COMMON_STYLE = """Style/medium: late-1970s sword-and-sorcery pulp illustration translated into hard-edged Apple II HGR shapes; muscular readable silhouettes, bold brush-and-ink shadows, selective flat color accents.
Color palette: use ONLY black #000000, white #FFFFFF, violet #AA1AD1, green #6FE62C, blue #008AB5, orange #FF7247 -- no other hue, no grey, no gradient; keep violet/green regions spatially separate from blue/orange regions; 35-55% solid black negative space.
Materials/textures: hard-edged flat fills and deliberate broad ink shadows only; no random grain.
Text (verbatim): ""
Constraints: no visible words, letters, numbers, captions, border, UI, logo, signature, or watermark; no anti-aliasing; no photorealistic texture; no tiny decorative detail.
Avoid: glossy modern concept art, modern objects, smooth airbrush shading, comic speech effects, noisy dithering, illegible micro-detail."""


def load_characters(root):
    out = []
    for name in BIBLES:
        data = json.loads((root / "SCOSWAMP.MORE" / name)
                          .read_text(encoding="utf-8"))
        kind = "decor" if name == "decors.json" else "figure"
        for c in data["characters"]:
            c["kind"] = kind
            out.append(c)
    return out


def matching(text, characters):
    """Les fiches qui concernent cette page, dans l'ordre des bibles."""
    out = []
    for c in characters:
        if c.get("always"):
            out.append(c); continue
        for alias in c.get("aliases", []):
            if re.search(r"\b" + re.escape(alias) + r"\b", text, re.I):
                out.append(c); break
    return out


def bible_hash(text, characters):
    """Empreinte des fiches ayant servi a ce prompt.

    Sans elle, modifier une fiche ne dit pas quelles images sont devenues
    perimees : on regenere tout, ou on oublie. Avec elle, `--stale` les nomme.
    """
    import hashlib
    blob = "\u0000".join(c["id"] + c["look"] + c.get("scale", "")
                          for c in matching(text, characters))
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()[:12]


# Un nom propre qu'aucune fiche ne couvre est une incoherence en puissance :
# rien ne le decrit, donc chaque image l'inventera.
PROPER = re.compile(r"\b([A-ZÀ-Ý][a-zà-ÿ]{3,}(?:\s+d[eu']\s*[A-ZÀ-Ýa-zà-ÿ]+)?)\b")
COMMON = {"Vous", "Cette", "Cela", "Alors", "Mais", "Dans", "Pour", "Elle",
          "Rendez", "Tentez", "Chaque", "Votre", "Deux", "Trois", "Quand",
          "Apres", "Avant", "Depuis", "Enfin", "Aucun", "Aucune", "Toute",
          "Tous", "Plus", "Bien", "Cependant", "Soudain", "Puis", "Voici"}


def uncovered_names(text, characters):
    known = " ".join(a for c in characters for a in c.get("aliases", [])).lower()
    out = set()
    for m in PROPER.finditer(text):
        name = m.group(1)
        first = name.split()[0]
        if first in COMMON or len(first) < 4:
            continue
        if first.lower() in known:
            continue
        out.add(name)
    return out


def character_block(text, characters):
    """Le bloc injecte : description, puis echelle.

    L'echelle compte autant que la description : deux images peuvent respecter
    la lettre d'une fiche et montrer le Geant a deux tailles differentes. Elle
    est toujours donnee PAR RAPPORT AU HEROS, seule mesure commune a toutes
    les images.
    """
    present = matching(text, characters)
    if not present:
        return ""
    out = []
    for c in present:
        line = "- " + c["look"]
        if c.get("scale"):
            line += " Scale: " + c["scale"] + "."
        out.append(line)
    return ("\n\nRecurring subjects — draw them EXACTLY as described here. "
            "These descriptions are fixed across the whole series; two images "
            "that share one must show the same subject.\n" + "\n".join(out))


# Une page peut citer jusqu'a dix fiches. Les joindre toutes noierait le
# modele : au-dela de quelques planches il moyenne au lieu de copier. On garde
# le heros — present partout, donc le sujet dont l'incoherence se verrait le
# plus — puis les figures nommees, puis le decor, et on s'arrete la.
REF_ATTACH_MAX = 4


def refs_for(text, characters, root):
    """Les planches a joindre au prompt, les plus utiles d'abord."""
    def rank(c):
        return 0 if c.get("always") else (1 if c["kind"] == "figure" else 2)

    out = []
    for c in sorted(matching(text, characters), key=rank):
        ref = c.get("ref")
        if ref and (root / ref).exists():
            out.append(ref)
        if len(out) == REF_ATTACH_MAX:
            break
    return out


REF_FIGURE = """Use case: reference sheet
Asset type: a single character reference for an Apple II HGR gamebook
Primary request: ONE subject alone, full figure head to foot, standing still and facing the viewer three-quarters, on a plain solid black background. No scene, no ground, no props beyond what the description names.
Composition/framing: the subject centered and complete, filling most of the frame, nothing cropped.
"""

REF_DECOR = """Use case: reference sheet
Asset type: a location reference for an Apple II HGR gamebook
Primary request: the place itself, empty of people and creatures, seen wide at eye level. It is the stage other illustrations will be set on, so its shapes and colours must read at a glance.
Composition/framing: a wide establishing view, horizon roughly a third from the top.
"""

REF_TAIL = COMMON_STYLE + """

This sheet is the CANON. Every later illustration of this subject will be drawn
from it, so the shapes and colours chosen here must be unambiguous.

The subject:
"""


def ref_rows(root, characters):
    """Une planche de reference par sujet des bibles."""
    rows = []
    for c in characters:
        look = c["look"]
        if c.get("scale"):
            look += " Scale: " + c["scale"] + "."
        base = REF_DECOR if c["kind"] == "decor" else REF_FIGURE
        rows.append({
            "id": c["id"],
            "source_png": c["ref"],
            "prompt": base + REF_TAIL + look,
            "status": "pending",
        })
    return rows


def scene_rows(root, characters, all_pages):
    """Une illustration par clairiere. Par defaut, seulement les manquantes."""
    game = root / "SCOSWAMP"
    more = root / "SCOSWAMP.MORE"
    rows = []
    for scene_id in range(402):
        sid = f"{scene_id:03d}"
        bucket = f"N{(scene_id // 50) * 50:03d}"
        text_path = game / "TEXTFR" / bucket / f"N{sid}.TXT"
        rle_path = game / "IMG" / bucket / f"N{sid}.RLE.BIN"
        # --all les demande toutes : c'est ce qu'il faut apres une modification
        # des bibles, sans quoi les anciennes images gardent leur ancienne
        # interpretation.
        if not text_path.exists():
            continue
        if rle_path.exists() and not all_pages:
            continue
        scene = text_path.read_text(encoding="utf-8").strip()
        rows.append({
            "id": scene_id,
            "scene": f"N{sid}",
            "text_path": str(text_path.relative_to(root)),
            "source_png": str((more / "GENERATED" / f"N{sid}.png").relative_to(root)),
            "hgr_rle": str(rle_path.relative_to(root)),
            "preview_png": str((more / "HGR-PREVIEW" / f"N{sid}.png").relative_to(root)),
            "prompt": STYLE + scene + character_block(scene, characters),
            "refs": refs_for(scene, characters, root),
            "bible": bible_hash(scene, characters),
            "status": "pending",
        })
    return rows


# Ce que le CORPUS dit de l'apparence d'un sujet. Le corpus est la verite du
# jeu : une fiche qui le contredit fait dessiner autre chose que ce que le
# joueur lit. C'est arrive deux fois -- la fiche du Maitre des Loups lui otait
# l'epee et les habits de Garde Forestier que la page 398 lui donne, et celle
# de Gayolard en faisait un vieillard barbu en robe bleue la ou la page 371
# decrit un petit homme replet en tunique blanche, au tour de potier.
DESCRIBES = re.compile(r"\b(porte|portant|vetu|vetue|couvert\w*|habill\w+"
                       r"|pend|arbore|tient|ressemble)\b", re.I)


def describe(root, characters):
    """Les phrases du corpus qui decrivent chaque sujet, pour relire sa fiche."""
    pages = sorted((root / "SCOSWAMP" / "TEXTFR").rglob("N*.TXT"))
    texts = [p.read_text(encoding="utf-8") for p in pages]
    for c in characters:
        if c.get("always"):
            continue
        seen = []
        for t in texts:
            for alias in c.get("aliases", []):
                for m in re.finditer(r"[^.]*\b" + re.escape(alias) + r"\b[^.]*\.",
                                     t, re.I):
                    line = " ".join(m.group(0).split())
                    if DESCRIBES.search(line) and line not in seen:
                        seen.append(line)
        if seen:
            print(f"--- {c['id']}")
            print(f"    FICHE : {c['look']}")
            for line in seen[:3]:
                print(f"    TEXTE : {line[:150]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True,
                        help="apple2adventure directory")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--describe", action="store_true",
                        help="ce que le corpus dit de chaque sujet, en regard "
                             "de sa fiche : a relire avant de modifier une bible")
    parser.add_argument("--stale", action="store_true",
                        help="liste les images qu'un changement de fiche a "
                             "rendues perimees")
    parser.add_argument("--record", action="store_true",
                        help="enregistre l'empreinte des fiches pour les "
                             "images presentes, apres une generation")
    parser.add_argument("--refs", action="store_true",
                        help="les planches de reference, une par sujet des "
                             "bibles : le canon dont tout le reste decoule")
    parser.add_argument("--all", action="store_true",
                        help="toutes les pages, pas seulement celles dont "
                             "l'image manque (apres un changement de bible)")
    parser.add_argument("--battle", action="store_true",
                        help="manifeste des illustrations de bataille (une par "
                             "clairiere avec adversaire) au lieu des scenes")
    args = parser.parse_args()
    characters = load_characters(args.root)

    # ── Perimees ────────────────────────────────────────────────────────
    # Modifier une fiche change le prompt de toutes les images qui la citent.
    # Sans trace, on regenere tout ou on oublie ; avec, on nomme exactement
    # celles qui ont vieilli.
    # A cote des manifestes, pas dans GENERATED/ : ce dossier est ignore par
    # git, et un registre que le depot ne garde pas ne sert a rien.
    stamp = args.root / "SCOSWAMP.MORE" / "bible.stamp.json"

    if args.describe:
        describe(args.root, characters)
        return 0

    if args.stale or args.record:
        current = {}
        for rows in (battle_rows(args.root, characters),
                     scene_rows(args.root, characters, all_pages=True)):
            for r in rows:
                current[r["source_png"]] = r["bible"]
        known = json.loads(stamp.read_text(encoding="utf-8")) if stamp.exists() else {}
        if args.record:
            kept = {k: v for k, v in current.items() if (args.root / k).exists()}
            stamp.parent.mkdir(parents=True, exist_ok=True)
            stamp.write_text(json.dumps(kept, indent=1, sort_keys=True) + "\n",
                             encoding="utf-8")
            print(f"empreinte enregistree pour {len(kept)} images")
            return 0
        stale = [k for k, v in sorted(current.items())
                 if (args.root / k).exists() and known.get(k) != v]
        never = [k for k in sorted(current) if not (args.root / k).exists()]
        print(f"{len(stale)} image(s) perimee(s) par un changement de fiche, "
              f"{len(never)} jamais generee(s)")
        for k in stale[:20]:
            print("   " + k)
        return 0

    if args.refs:
        rows = ref_rows(args.root, characters)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        (args.root / "SCOSWAMP.MORE" / "REF").mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8") as stream:
            for row in rows:
                stream.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"wrote {len(rows)} reference prompts to {args.output}")
        return 0

    if args.battle:
        rows = battle_rows(args.root, characters)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8") as stream:
            for row in rows:
                stream.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"wrote {len(rows)} battle prompts to {args.output}")
        return 0

    rows = scene_rows(args.root, characters, args.all)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"wrote {len(rows)} scene prompts to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
