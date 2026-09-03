# Zone `riviere` — la rivière Croupie et son pont

**`RIVIERE.MB.BIN` — 1 861 octets, 54,2 s, boucle.**

## Ce que la zone couvre

| # | `hub` | Titre | (x,y) | Pages |
| ---: | ---: | --- | :---: | --- |
| 13 | 295 | La Rivière Croupie | (1,3) | 295 |
| 14 | 183 | Sommet de la falaise | (2,3) | 183 |
| **15** | **045** | **Le pont sur la rivière Croupie** | (3,3) | 138, 45, 101 |
| 31 | 044 | La rivière profonde | (1,7) | 90, 44, 254, 370 |

Quatre clairières seulement, mais le pont est **le seul passage** entre les
douze clairières du nord et les vingt-trois du sud (`CARTOGRAPHIE.md` § 1). Une
zone de quatre pages qui porte le seuil du jeu mérite sa musique.

## La pièce

| | |
| --- | --- |
| Titre | **Le Pont sur la Croupie** |
| Source | composition originale, `riviere.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | l'eau : un arpège de croches qui ne s'arrête jamais, une mélodie en blanches au-dessus, tout en suspension |
| Mode | **la dorien** (la si do ré mi **fa♯** sol) |
| Tempo | **125** à la noire |
| Forme | intro (4) — A (8) — B (8) — A' (8) |
| Durée | 28 mesures à 4/4 = **54,2 s** — la plus longue boucle du dossier |
| Taille | **1 861 octets** |
| Notes | 464 écrites, 0 abandonnée |

Le bourdon est sur **mi**, la quinte, et non sur la tonique : rien ne se pose,
tout coule. Le ré majeur du mode dorien (mesures 8, 12, 18, 24) est la seule
lumière franche de la pièce — c'est le pont lui-même, et il revient quatre fois.

## Les six voix

| voix | côté | rôle | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | mélodie, en valeurs longues | D5..A6 | 65 |
| 1 | **gauche** | médiane (contre-chant) | G3..B4 | 88 |
| 2 | **gauche** | basse, blanche puis deux noires | G2..B3 | 84 |
| 3 | **droite** | arpège en croches, le courant | A3..D5 | 123 |
| 4 | **droite** | médiane (accords tenus) | F♯3..G4 | 97 |
| 5 | **droite** | bourdon de mi (la quinte) | E2 | 7 |

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/riviere
python3 riviere.py
python3 ../../midi_to_mb.py riviere.mid RIVIERE.MB.BIN \
    --bpm 125 --max 2400 --wav RIVIERE.wav
```
