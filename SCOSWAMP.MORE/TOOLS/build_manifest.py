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


def load_characters(root):
    out = []
    for name in BIBLES:
        data = json.loads((root / "SCOSWAMP.MORE" / name)
                          .read_text(encoding="utf-8"))
        out.extend(data["characters"])
    return out


def characters_in(text, characters):
    """Les fiches a injecter pour cette page, dans l'ordre de la bible."""
    out = []
    for c in characters:
        if c.get("always"):
            out.append(c["look"]); continue
        for alias in c.get("aliases", []):
            if re.search(r"\b" + re.escape(alias) + r"\b", text, re.I):
                out.append(c["look"]); break
    return out


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
    looks = characters_in(text, characters)
    if not looks:
        return ""
    return ("\n\nRecurring characters — draw them EXACTLY as described here, "
            "these descriptions are fixed across the whole series:\n"
            + "\n".join("- " + l for l in looks))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True,
                        help="apple2adventure directory")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--all", action="store_true",
                        help="toutes les pages, pas seulement celles dont "
                             "l'image manque (apres un changement de bible)")
    parser.add_argument("--battle", action="store_true",
                        help="manifeste des illustrations de bataille (une par "
                             "clairiere avec adversaire) au lieu des scenes")
    args = parser.parse_args()

    if args.battle:
        rows = battle_rows(args.root, load_characters(args.root))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8") as stream:
            for row in rows:
                stream.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"wrote {len(rows)} battle prompts to {args.output}")
        return 0

    characters = load_characters(args.root)
    all_pages = args.all
    game = args.root / "SCOSWAMP"
    more = args.root / "SCOSWAMP.MORE"
    rows = []
    for scene_id in range(402):
        sid = f"{scene_id:03d}"
        bucket = f"N{(scene_id // 50) * 50:03d}"
        text_path = game / "TEXTFR" / bucket / f"N{sid}.TXT"
        rle_path = game / "IMG" / bucket / f"N{sid}.RLE.BIN"
        # Par defaut on ne demande que les images manquantes. --all les demande
        # toutes : c'est ce qu'il faut apres une modification des bibles, sans
        # quoi les anciennes images gardent leur ancienne interpretation.
        if rle_path.exists() and not all_pages:
            continue
        scene = text_path.read_text(encoding="utf-8").strip()
        rows.append({
            "id": scene_id,
            "scene": f"N{sid}",
            "text_path": str(text_path.relative_to(args.root)),
            "source_png": str((more / "GENERATED" / f"N{sid}.png").relative_to(args.root)),
            "hgr_rle": str(rle_path.relative_to(args.root)),
            "preview_png": str((more / "HGR-PREVIEW" / f"N{sid}.png").relative_to(args.root)),
            "prompt": STYLE + scene + character_block(scene, characters),
            "status": "pending",
        })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"wrote {len(rows)} scene prompts to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
