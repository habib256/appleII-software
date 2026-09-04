# Chaîne des images DHGR SCSWAMP

Les descriptions canoniques viennent du livre et sont consolidées dans
`characters.json`, `monsters.json`, `decors.json` et `objects.json`. Ces bibles
sont la source de vérité pour l'apparence des personnages, monstres, décors et
objets récurrents.

## Fichiers suivis

- `SCOSWAMP.MORE/REF/*.png` : références visuelles canoniques.
- `SCOSWAMP.MORE/ref_manifest.jsonl` : prompts des références.
- `SCOSWAMP.MORE/scene_manifest.jsonl` : prompts des scènes numérotées.
- `SCOSWAMP.MORE/battle_manifest.jsonl` : prompts des combats.
- `SCOSWAMP/IMG/` : images DHGR compressées intégrées au jeu (banque auxiliaire
  de 8 Ko, puis banque principale de 8 Ko).

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

La génération emploie exclusivement les quinze teintes distinctes de la
palette DHGR Apple II (les deux gris matériels ont le même rendu NTSC). La
conversion cible 140×192 pixels couleur, sans dégradés ni teintes hors palette.

Dans les scènes narratives, le héros doit être présent et mis en valeur. Dans
les combats seulement, il est à gauche, tourné vers la droite, face à son
adversaire placé à droite et regardant vers la gauche.

## Musique des clairières

Une musique est chargée et lancée uniquement quand la page fait entrer le
joueur dans une nouvelle clairière. Elle est jouée une seule fois, sans boucle.
Les pages suivantes de la même clairière, y compris les combats, ne relancent
ni ne rechargent de morceau.
