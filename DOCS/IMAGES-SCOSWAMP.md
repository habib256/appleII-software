# Chaîne des images SCSWAMP

Les descriptions canoniques viennent du livre et sont consolidées dans
`characters.json`, `monsters.json`, `decors.json` et `objects.json`. Ces bibles
sont la source de vérité pour l'apparence des personnages, monstres, décors et
objets récurrents.

## Fichiers suivis

- `SCOSWAMP.MORE/REF/*.png` : références visuelles canoniques.
- `SCOSWAMP.MORE/ref_manifest.jsonl` : prompts des références.
- `SCOSWAMP.MORE/scene_manifest.jsonl` : prompts des scènes numérotées.
- `SCOSWAMP.MORE/battle_manifest.jsonl` : prompts des combats.
- `SCOSWAMP/IMG/` : images HGR intégrées au jeu.

Les manifestes sont suivis afin que toute modification des règles visuelles
soit relue comme du code. `GENERATED`, `HGR-PREVIEW`, les WAV et les répertoires
de build sont des sorties temporaires ignorées par Git.

## Régénération

```sh
python3 SCOSWAMP.MORE/TOOLS/build_manifest.py --root . --output SCOSWAMP.MORE/ref_manifest.jsonl --refs
python3 SCOSWAMP.MORE/TOOLS/build_manifest.py --root . --output SCOSWAMP.MORE/scene_manifest.jsonl --all
python3 SCOSWAMP.MORE/TOOLS/build_manifest.py --root . --output SCOSWAMP.MORE/battle_manifest.jsonl --battle
SCOSWAMP.MORE/TOOLS/generate_images.sh SCOSWAMP.MORE/scene_manifest.jsonl 0 3
SCOSWAMP.MORE/TOOLS/generate_images.sh SCOSWAMP.MORE/battle_manifest.jsonl 0 3
SCOSWAMP.MORE/TOOLS/convert_images.sh
```

Dans les scènes narratives, le héros doit être présent et mis en valeur. Dans
les combats seulement, il est à gauche, tourné vers la droite, face à son
adversaire placé à droite et regardant vers la gauche.
