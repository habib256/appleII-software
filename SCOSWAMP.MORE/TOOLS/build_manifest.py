#!/usr/bin/env python3
"""Build the deterministic image-generation manifest for SCOSWAMP."""

from __future__ import annotations

import argparse
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


def battle_rows(root):
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
            "prompt": BATTLE_STYLE + "Adversary: " + ", ".join(names) + "\n\n" + text.strip(),
            "status": "pending",
        })
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True,
                        help="apple2adventure directory")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--battle", action="store_true",
                        help="manifeste des illustrations de bataille (une par "
                             "clairiere avec adversaire) au lieu des scenes")
    args = parser.parse_args()

    if args.battle:
        rows = battle_rows(args.root)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8") as stream:
            for row in rows:
                stream.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"wrote {len(rows)} battle prompts to {args.output}")
        return 0

    game = args.root / "SCOSWAMP"
    more = args.root / "SCOSWAMP.MORE"
    rows = []
    for scene_id in range(402):
        sid = f"{scene_id:03d}"
        bucket = f"N{(scene_id // 50) * 50:03d}"
        text_path = game / "TEXTFR" / bucket / f"N{sid}.TXT"
        rle_path = game / "IMG" / bucket / f"N{sid}.RLE.BIN"
        if rle_path.exists():
            continue
        scene = text_path.read_text(encoding="utf-8").strip()
        rows.append({
            "id": scene_id,
            "scene": f"N{sid}",
            "text_path": str(text_path.relative_to(args.root)),
            "source_png": str((more / "GENERATED" / f"N{sid}.png").relative_to(args.root)),
            "hgr_rle": str(rle_path.relative_to(args.root)),
            "preview_png": str((more / "HGR-PREVIEW" / f"N{sid}.png").relative_to(args.root)),
            "prompt": STYLE + scene,
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
