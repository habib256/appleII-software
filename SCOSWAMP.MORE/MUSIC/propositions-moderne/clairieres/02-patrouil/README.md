# Clairière 2 — Le Patrouilleur vert (`hub` 234, case 2,0)

**`PATROUIL.MB.BIN` — 1 993 octets, 43,1 s, boucle.**

## Les pages

| Page | Titre | Ce qui s'y passe |
| ---: | --- | --- |
| 170 | Le Patrouilleur vert | la brume se lève, l'homme en vert sur son rocher, la question |
| 363 | Retour au Patrouilleur | ami, mort, ou fui ? |
| 234 | Deux sentiers | l'est ou le sud |

La page **363** appartient à cette clairière et non à la 3
(`CARTOGRAPHIE.md:810-820`), comme dans les deux dossiers de propositions.

## La pièce

| | |
| --- | --- |
| Titre | **La Question du Patrouilleur** |
| Source | composition originale, `patrouil.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | on est interrogé, pas suivi. « Es-tu au service du Bien ou du Mal ? » — une figure d'appel qui revient toujours, et jamais au même endroit de la mesure |
| Mode | **la mineur éolien** (la si do ré mi fa sol) |
| Tempo | **156** à la noire |
| Forme | intro (4) — A (8) — B (8) — A' (8) |
| Durée | 28 mesures à 4/4 = **43,1 s** |
| Taille | **1 993 octets** (marge 311) |
| Notes | 508 écrites, **0 abandonnée** |

## Ce qui la relie à `nord`, et ce qui l'en sépare

Le procédé de la zone est l'**ostinato fixe** : quatre notes qui ne changent
jamais pendant que les accords bougent dessous. Celui-ci ne change jamais de
notes non plus — **la - mi - do**, une quarte descendante puis une sixte, un
appel de cor — mais sa cellule fait **trois croches** dans une mesure à quatre
temps. Elle retombe donc chaque fois sur un temps différent, et ne revient à sa
place qu'une mesure sur trois. C'est la ronde : l'homme en vert est toujours
là, jamais au même endroit du chemin.

Aux quatre dernières mesures la cellule passe à quatre croches. Tout retombe
d'aplomb, et la question tombe avec — c'est la cadence, et c'est le seul moment
du morceau où l'on sait où il est.

Le bourdon est sur **mi**, la quinte à vide de la, et non sur la tonique comme
dans `MARAISNO.MB` : une quinte ouverte ne conclut pas, elle attend une réponse.

## Les six voix, mesurées

`python3 ../../verifier.py patrouil.mid --bpm 156`

| voix | côté | ce qui s'y trouve | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | la mélodie, seule | E5..B6 | 81 |
| 1 | gauche | le contre-chant | A3..C5 | 61 |
| 2 | **gauche** | la basse en noires | G2..A3 | 111 |
| 3 | **droite** | **la ronde**, en entier | E4..C5 | 218 |
| 4 | droite | les accords tenus | F3..E4 | 30 |
| 5 | **droite** | le bourdon de mi | E2 | 7 |

218 des 508 notes sont dans une seule voix, à droite : la ronde occupe presque
la moitié du morceau et toute une puce. C'est ce qui rend la clairière
reconnaissable en deux secondes, exactement comme l'ostinato de la zone.

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/02-patrouil
python3 patrouil.py
python3 ../../../midi_to_mb.py patrouil.mid PATROUIL.MB.BIN \
    --bpm 156 --max 2304 --wav PATROUIL.wav
```
