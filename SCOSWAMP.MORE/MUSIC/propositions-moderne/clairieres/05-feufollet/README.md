# Clairière 5 — Feu follet à l'orée (`hub` 218, case 1,1)

**`FEUFOLLET.MB.BIN` — 1 777 octets, 41,6 s, boucle.**

## Les pages

| Page | Titre | Ce qui s'y passe |
| ---: | --- | --- |
| 218 | Feu follet à l'orée | la faible lueur qui flotte à l'ouest, recule, et révèle un sentier boueux |
| 249 | Saut dans l'obscurité | le test de CHANCE, le bras blessé, la clairière quand même |

## La pièce

| | |
| --- | --- |
| Titre | **La Lumière qui Recule** |
| Source | composition originale, `feufollet.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | un piège qui ne menace pas. Rien n'appuie, rien ne pèse ; la lueur avance de deux pas et se dérobe |
| Mode | **sol mineur éolien** (sol la si♭ do ré mi♭ fa) |
| Tempo | **150** à la noire |
| Forme | intro (4) — A (8) — B (8) — A' (6) |
| Durée | 26 mesures à 4/4 = **41,6 s** |
| Taille | **1 777 octets** (marge 527) |
| Notes | 421 écrites, **0 abandonnée** |

## Ce qui la relie à `nord`, et ce qui l'en sépare

L'ostinato de la zone est fixe **et** carré : il tombe toujours au même endroit
de la mesure. Celui-ci est fixe en notes — ré - sol - si♭ - la - fa — et jamais
au même endroit, parce que sa cellule fait **cinq croches** dans une mesure à
quatre temps. À chaque tour la figure recule d'une croche ; elle ne retombe
d'aplomb qu'une mesure sur cinq. C'est le Feu Follet de la page 218, qui
« recule de quelques mètres » chaque fois qu'on avance.

Aux six dernières mesures la cellule passe à quatre croches et s'immobilise : la
lueur attend au bord du sentier boueux. C'est le piège, et c'est le seul endroit
du morceau où l'on sait où elle est.

Deux autres écarts, tous les deux pour alléger : l'ostinato est **détaché**
(occupation mesurée 76 %, contre 92 % pour la zone), et la basse est en
**blanches** d'un bout à l'autre — 52 notes contre 112 dans `MARAISNO.MB`. Sur
un sol pareil, rien ne marche.

## Les six voix, mesurées

`python3 ../../verifier.py feufollet.mid --bpm 150`

| voix | côté | ce qui s'y trouve | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | la mélodie, seule | G5..B♭6 | 76 |
| 1 | gauche | le contre-chant, et les notes hautes des accords | A3..B♭4 | 74 |
| 2 | **gauche** | la basse, en blanches, seule | F2..G3 | 52 |
| 3 | **droite** | **la lueur** | D4..B♭4 | 174 |
| 4 | droite | les accords tenus | F3..E♭4 | 38 |
| 5 | **droite** | le bourdon de ré, la quinte à vide de sol | D2 | 7 |

C'est la pièce la plus légère des douze : 421 notes, dont 174 pour la seule
lueur. Le reste tient de la place sans en prendre.

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/05-feufollet
python3 feufollet.py
python3 ../../../midi_to_mb.py feufollet.mid FEUFOLLET.MB.BIN \
    --bpm 150 --max 2304 --wav FEUFOLLET.wav
```
