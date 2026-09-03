# Clairière 6 — Le croisement (`hub` 121, case 2,1)

**`CROISEMENT.MB.BIN` — 1 901 octets, 46,7 s, boucle.**

## Les pages

| Page | Titre | Ce qui s'y passe |
| ---: | --- | --- |
| 121 | Le croisement | quatre directions ; nord 170, sud 014, est 275, ouest 218 |

Une seule page, et c'est la clairière la plus traversée du Marais nord : c'est
par elle qu'on passe pour aller du Patrouilleur au Géant, du Feu Follet au
Scorpion.

## La pièce

| | |
| --- | --- |
| Titre | **Quatre Chemins** |
| Source | composition originale, `croisement.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | l'hésitation, pas la peur. On est arrêté au milieu, et la même question se pose quatre fois |
| Mode | **mi éolien** (mi fa♯ sol la si do ré) — celui de la zone, délibérément |
| Tempo | **144** à la noire |
| Forme | intro (4) — nord (6) — sud (6) — est (6) — ouest (6) |
| Durée | 28 mesures à 4/4 = **46,7 s** |
| Taille | **1 901 octets** (marge 403) |
| Notes | 488 écrites, **0 abandonnée** |

## Ce qui la relie à `nord`, et ce qui l'en sépare

C'est la variation la plus littérale des huit clairières du nord, et c'est
voulu : le croisement est le **centre** de la zone, il n'avait aucune raison de
changer de couleur. Même mode, même bourdon de mi, même basse en noires que
`MARAISNO.MB`.

Ce qui change est la **forme**. Le procédé de la zone est l'ostinato fixe ; ici
il est fixe **à l'intérieur d'un panneau** et change à chaque panneau : quatre
cellules de quatre croches, une par direction, toutes bâties sur d'autres degrés
du même mode et toutes dans la même bande de registre, donc dans la même voix.

| Panneau | Mesures | Cellule | Harmonie |
| --- | :---: | --- | --- |
| nord | 5-10 | si - sol - la - mi | Mim - Sol - Ré - Mim - Do - Sim |
| sud | 11-16 | la - mi - fa♯ - ré | Lam - Mim - Do - Sol - Lam - Sim |
| est | 17-22 | ré - sol - si - sol | Sol - Ré - Mim - Do - Sol - Ré |
| ouest | 23-28 | mi - la - do - la | Do - Lam - Sim - Mim - Ré - Mim |

La même **tête de mélodie** de deux mesures ouvre chaque panneau, transposée à
chaque fois : c'est la question de la page 121 posée quatre fois, « laquelle
allez-vous choisir ? ».

Dans l'intro la cellule est en **noires** au lieu de croches — on est arrêté au
milieu du carrefour. Elle passe en croches dès le premier panneau et ne
s'arrête plus.

## Les six voix, mesurées

`python3 ../../verifier.py croisement.mid --bpm 144`

| voix | côté | ce qui s'y trouve | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | la mélodie, seule | D5..A6 | 77 |
| 1 | gauche | le contre-chant | A3..C5 | 78 |
| 2 | **gauche** | la basse en noires, seule | E2..G3 | 112 |
| 3 | **droite** | **les quatre cellules** | D4..C5 | 180 |
| 4 | droite | les accords tenus | F♯3..B4 | 34 |
| 5 | **droite** | le bourdon de mi | E2 | 7 |

Les quatre cellules restent dans la même voix, donc du même côté : quand
l'ostinato change, c'est la clairière qui tourne, pas la stéréo.

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/06-croisement
python3 croisement.py
python3 ../../../midi_to_mb.py croisement.mid CROISEMENT.MB.BIN \
    --bpm 144 --max 2304 --wav CROISEMENT.wav
```
