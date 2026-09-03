# Clairière 30 — Clairière des grenouilles (`hub` 230)

**`GRENOUILLES.MB.BIN` — 2 029 octets, 40,9 s, boucle.**

## Ce que la clairière raconte

| Page | Ce qu'on y lit |
| ---: | --- |
| 053 | « le coassement de milliers de grenouilles vous accompagne » — d'immenses champignons, un petit homme corpulent assis sur l'un d'eux, la bouche anormalement large, deux énormes grenouilles pour le garder |
| 329 | le champignon lumineux, des traces de dents humaines sur le chapeau, une odeur agréable |
| 230 | la clairière silencieuse : les Grenouilles Géantes mortes, le Maître disparu |

Zone de référence : **`sud`** (`MARAISUD.MB`, *Sentiers Verts*).

## La pièce

| | |
| --- | --- |
| Titre | **Le Bal des Mares** |
| Source | composition originale, `grenouilles.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | la seule clairière comique des onze, et la seule où le Marais fait du bruit — mais ça rebondit lourdement, ça ne vole pas |
| Mode | **sol éolien** (sol la si♭ do ré mi♭ fa) |
| Tempo | **166** à la noire |
| Forme | intro (4) — A (8) — B (8) — A' à l'octave (8) |
| Durée | 28 mesures à 4/4 = **40,9 s** |
| Taille | **2 029 octets** (tampon de zone : 2 304) |
| Notes | 520 écrites, **0 abandonnée** |

Ce qui la rattache à `sud` : la marche **i-VI-III-VII** (Gm-E♭-B♭-F) posée sur un
bourdon de sol qui ne bouge jamais — le procédé exact de *Sentiers Verts*, dans
une autre tonique. Ce qui n'appartient qu'à elle : le **saut**. Presque chaque
phrase de la mélodie commence par deux croches écartées d'une octave ou d'une
quinte, puis retombe ; et la basse saute elle aussi, alternant fondamentale et
quinte grave à chaque temps au lieu de marcher. Le petit homme de la page 053
est corpulent : le rebond est lourd.

## Les six voix (mesurées par `verifier.py`)

| voix | côté | rôle | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | mélodie sauteuse | D5..G6 | 93 |
| 1 | gauche | médiane (contre-chant) | D3..B♭4 | 71 |
| 2 | **gauche** | basse, sauts fondamentale-quinte | A2..C4 | 100 |
| 3 | **droite** | arpège en croches | C4..D5 | 167 |
| 4 | droite | médiane (accords tenus) | D3..G4 | 82 |
| 5 | **droite** | bourdon de sol | G2 | 7 |

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/30-grenouilles
python3 grenouilles.py
python3 ../../../midi_to_mb.py grenouilles.mid GRENOUILLES.MB.BIN \
    --bpm 166 --max 2304 --wav GRENOUILLES.wav
```
