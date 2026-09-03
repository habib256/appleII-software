# Clairière 3 — Le Maître des Jardins (`hub` 084, case 3,0)

**`JARDINS.MB.BIN` — 1 883 octets, 45,2 s, boucle.**

## Les pages

| Page | Titre | Ce qui s'y passe |
| ---: | --- | --- |
| 305 | Le Maître des Jardins | le sentier taillé, l'Amulette d'Argent en forme de fleur, l'Anneau reste froid |
| 238 | Clairière du Maître des Jardins | elle est belle et complètement déserte |
| 084 | Le Maître des Jardins | il est un ami ; un seul chemin y mène |
| 117 | L'Amulette du Jardin | la Pierre d'Amitié, la paralysie, l'avertissement |
| 251 | Maître des Jardins | vous l'avez tué : −3 CHANCE, l'Amulette FLEUR |
| 283 | Le Maître des Jardins | l'Anthérique promis, une Pierre bénéfique |
| 396 | Le buisson d'Anthérique | « prenez la direction de l'ouest, puis revenez vers l'est » |

Sept pages : la clairière la plus bavarde du Marais nord.

## La pièce

| | |
| --- | --- |
| Titre | **L'Amulette de Fleur** |
| Source | composition originale, `jardins.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | le seul endroit amical du Marais nord. « Trop belle pour être entièrement naturelle, trop naturelle pour être vraiment un jardin » |
| Mode | **ré dorien** (ré mi fa sol la **si** do) |
| Tempo | **138** à la noire |
| Forme | intro (2) — A (8) — B (8) — A' (8) |
| Durée | 26 mesures à 4/4 = **45,2 s** |
| Taille | **1 883 octets** (marge 421) |
| Notes | 448 écrites, **0 abandonnée** |

## Ce qui la relie à `nord`, et ce qui l'en sépare

Même famille mineure, même ostinato fixe de quatre croches, même bourdon de
tonique. **Une seule note change de la zone à la clairière** : la sixte. Le
`nord` est en éolien, la sixte y est mineure et c'est elle qui mord ; ici le
mode est **dorien**, la sixte est majeure — le si bécarre — et c'est elle la
fleur.

Elle est partout et nulle part ailleurs :

- l'ostinato la touche à chaque tour : **la - fa - si - sol** ;
- l'harmonie s'en sert pour poser un **sol majeur** aux mesures 2, 4, 15 et 20,
  l'accord que le mode éolien du `nord` ne peut pas produire ;
- la mélodie la place au sommet de ses arches.

Deux autres écarts, tous les deux dans le sens de la douceur : l'ostinato est
joué **détaché** (`gap=0.12`) à la manière du sécateur, ce que la mesure
d'occupation confirme — 64 % au lieu des 92 % de la zone ; et la basse **tient**
la fondamentale une blanche au lieu de marcher en noires, parce qu'ici on ne
fuit pas.

## Les six voix, mesurées

`python3 ../../verifier.py jardins.mid --bpm 138`

| voix | côté | ce qui s'y trouve | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | la mélodie, seule | D5..A6 | 77 |
| 1 | gauche | le contre-chant | A3..G4 | 52 |
| 2 | **gauche** | la basse, en blanches et noires | E2..G3 | 78 |
| 3 | **droite** | **l'ostinato du jardin**, détaché | F4..B4 | 208 |
| 4 | droite | les accords tenus | F3..E4 | 26 |
| 5 | **droite** | le bourdon de ré | D2 | 7 |

La séparation est parfaite : chaque partie écrite tombe entièrement dans une
voix et une seule.

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/03-jardins
python3 jardins.py
python3 ../../../midi_to_mb.py jardins.mid JARDINS.MB.BIN \
    --bpm 138 --max 2304 --wav JARDINS.wav
```
