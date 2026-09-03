# Zone `sud` — les douze clairières au sud de la rivière

**`MARAISUD.MB.BIN` — 1 981 octets, 45,3 s, boucle.**

## Ce que la zone couvre

La plus grande zone du jeu : douze clairières, dont celle du départ.

| # | `hub` | Titre | (x,y) | Pages |
| ---: | ---: | --- | :---: | --- |
| 16 | 304 | Le Perroquet / Maîtresse des Oiseaux | (0,4) | 304, 149, 217 |
| 17 | 094 | La brume fétide | (1,4) | 94 |
| 18 | 179 | Le pique-nique suspect | (2,4) | 66, 192, 179 |
| 20 | 047 | Trois chemins herbeux | (4,4) | 47 |
| 21 | 031 | Bassin de cristal | (5,4) | 31, 77, 394 |
| 23 | 348 | La Licorne | (1,5) | 320, 265, 348 |
| 24 | 227 | La clairière des combats | (2,5) | 10, 142, 227 |
| 30 | 230 | Clairière des grenouilles | (4,6) | 53, 329, 230 |
| 32 | 314 | Clairière du Maître des Loups | (1,8) | 398, 239, 314 |
| **33** | **058** | **Le large rond-point (départ)** | (2,8) | **195**, 24, 208, 58, 404, 405 |
| 34 | 390 | Pierres et tronc | (3,8) | 105, 330, 390 |
| 35 | 082 | Bête du bassin | (4,8) | 209, 82, 308, 397 |

Les pages **394** et **330** appartiennent aux clairières 21 et 34, non aux 20
et 25 (`CARTOGRAPHIE.md:810-820`). La page 208 porte en plus la musique de
`village` (sortie du Marais).

## La pièce

| | |
| --- | --- |
| Titre | **Sentiers Verts** |
| Source | composition originale, `sud.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | marcher longtemps sans savoir où : la zone la plus vaste a la musique la plus large, et la moins pressée de conclure |
| Mode | **ré éolien** (ré mi fa sol la **si♭** do) |
| Tempo | **150** à la noire |
| Forme | intro (4) — A (8) — B (8) — A' à l'octave (8) |
| Durée | 28 mesures à 4/4 = **45,3 s** |
| Taille | **1 981 octets** |
| Notes | 504 écrites, 0 abandonnée |

L'harmonie est la marche i-VI-III-VII (Dm-B♭-F-C), celle de tous les thèmes de
voyage — mais posée sur un bourdon de ré qui ne bouge jamais, si bien que chaque
accord se lit comme une couleur du même lieu et non comme un départ. Le si
bémol la sépare du ré dorien de l'accueil : **c'est la même tonique, et on a
changé de monde.** Le joueur qui sort du Marais (page 208) réentend le si
bécarre du village ; c'est le seul repère tonal du jeu, et il est gratuit.

## Les six voix

| voix | côté | rôle | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | mélodie | D5..A6 | 77 |
| 1 | **gauche** | médiane (contre-chant) | G3..A4 | 74 |
| 2 | **gauche** | basse, marche de noires | E2..G3 | 112 |
| 3 | **droite** | arpège fondamentale-quinte en croches | A♯3..D5 | 141 |
| 4 | **droite** | médiane (accords tenus) | F3..G4 | 93 |
| 5 | **droite** | bourdon de ré | D2 | 7 |

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/sud
python3 sud.py
python3 ../../midi_to_mb.py sud.mid MARAISUD.MB.BIN \
    --bpm 150 --max 2400 --wav MARAISUD.wav
```
