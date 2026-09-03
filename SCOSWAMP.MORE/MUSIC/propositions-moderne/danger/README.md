# Zone `danger` — les dix clairières où l'on meurt

**`DANGER.MB.BIN` — 1 764 octets, 49,9 s, boucle.**

## Ce que la zone couvre

| # | `hub` | Titre | (x,y) | Pages |
| ---: | ---: | --- | :---: | --- |
| 9 | 153 | Le bassin de Vase | (1,2) | 336, 137, 153 |
| 10 | 088 | Scorpion et nain | (2,2) | 14, 338, 88 |
| 12 | 270 | Sables mouvants | (4,2) | 41, 382, 270 |
| 19 | 319 | La clairière des scorpions | (3,4) | 118, 303, 319 |
| 22 | 367 | Les Fleurs d'Angoisse | (0,5) | 204, 250, 367 |
| 25 | 187 | Herbe à Pinces | (3,5) | 388, 263, 33, 187 |
| 26 | 309 | Orques des Marais | (4,5) | 290, 323, 352, 309 |
| 27 | 125 | Cul-de-sac de la Bête | (0,6) | 11, 210, 299, 125, 228, 243 |
| 28 | 022 | La clairière des Arbres-Épées | (1,6) | 157, 279, 22 |
| 29 | 165 | Tente aux araignées | (3,6) | 144, 345, 354, 165 |

Ces dix clairières sont réparties dans le nord comme dans le sud : la zone
n'est pas géographique, c'est un **avertissement**. Elle doit donc se
reconnaître en une seconde et ne ressembler à rien d'autre.

## La pièce

| | |
| --- | --- |
| Titre | **Ce qui Attend Sous l'Eau** |
| Source | composition originale, `danger.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | quelque chose est déjà là et ne bougera qu'au dernier moment |
| Mode | **do phrygien** (do **ré♭** mi♭ fa sol la♭ si♭) |
| Tempo | **136** à la noire |
| Forme | intro (4) — A (8) — B (8) — A' resserré (8) |
| Durée | 28 mesures à 4/4 = **49,9 s** |
| Taille | **1 764 octets** |
| Notes | 453 écrites, 0 abandonnée |

Le phrygien pose un ré bémol **un demi-ton au-dessus de la tonique**, et toute
la pièce est bâtie sur ce frottement : l'accord de D♭ qui retombe sur Cm
(mesures 6-7, 22-23), et le motif ré♭-do que la mélodie martèle à partir de la
mesure 21. Aucun autre morceau du jeu n'a ce demi-ton.

**Le crescendo est fait par la densité, pas par le volume** : le lecteur
Mockingboard n'a pas de volume par note (`SCOSWAMP/SRC/music.s` ne pose `VOL`
qu'en tête de flux). Les huit premières mesures marchent en blanches et en
noires, les vingt suivantes en croches. La pièce se resserre au lieu de monter,
et c'est plus efficace sur une onde carrée.

## Les six voix

| voix | côté | rôle | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | mélodie | F5..A♯6 | 75 |
| 1 | **gauche** | médiane (contre-chant) | G3..G♯4 | 97 |
| 2 | **gauche** | basse, blanches puis noires | F2..G♯3 | 95 |
| 3 | **droite** | arpège, noires puis croches | A♯3..D♯5 | 102 |
| 4 | **droite** | médiane (accords tenus) | G3..G♯4 | 77 |
| 5 | **droite** | bourdon de do, immobile de bout en bout | C2 | 7 |

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/danger
python3 danger.py
python3 ../../midi_to_mb.py danger.mid DANGER.MB.BIN \
    --bpm 136 --max 2400 --wav DANGER.wav
```
