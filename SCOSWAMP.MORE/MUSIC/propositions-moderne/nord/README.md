# Zone `nord` — les huit clairières au nord de la rivière

**`MARAISNO.MB.BIN` — 1 978 octets, 45,3 s, boucle.**

## Ce que la zone couvre

| # | `hub` | Titre | (x,y) | Pages |
| ---: | ---: | --- | :---: | --- |
| 2 | 234 | Le Patrouilleur vert | (2,0) | 170, 363, 234 |
| 3 | 084 | Le Maître des Jardins | (3,0) | 305, 238, 84, 117, 251, 283, 396 |
| 4 | 232 | Les deux loups | (4,0) | 92, 232, 247, 389 |
| 5 | 218 | Feu follet à l'orée | (1,1) | 218, 249 |
| 6 | 121 | Le croisement | (2,1) | 121 |
| 7 | 161 | Le Géant | (4,1) | 275, 342, 161, 103, 244 |
| 8 | 019 | Clairière aux brigands | (0,2) | 65, 343, 19 |
| 11 | 202 | Le nid de l'Aigle | (3,2) | 350, 331, 25, 112, 202 |

La page **363** appartient à la clairière 2 et non à la 3
(`CARTOGRAPHIE.md:810-820`).

## La pièce

| | |
| --- | --- |
| Titre | **Le Bois des Guetteurs** |
| Source | composition originale, `nord.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | on est suivi. Un ostinato **fixe** de quatre croches — mi, si, sol, si — qui ne change jamais pendant que les accords bougent dessous |
| Mode | **mi éolien** (mi fa♯ sol la si do ré) |
| Tempo | **150** à la noire |
| Forme | intro (4) — A (8) — B (8) — A' une octave au-dessus (8) |
| Durée | 28 mesures à 4/4 = **45,3 s** |
| Taille | **1 978 octets** |
| Notes | 503 écrites, 0 abandonnée |

Le procédé est celui de toute la musique de jeu moderne : l'ostinato reste, la
basse tourne (Em-C-G-D, Em-C-Am-Bm), et le même motif change de sens à chaque
accord. Sur si mineur (mesure 12) le sol devient une sixte mineure et le motif
mord ; c'est le seul endroit où la pièce montre les dents, et c'est pour ça
qu'elle est écrite.

## Les six voix

| voix | côté | rôle | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | mélodie | E5..B6 | 76 |
| 1 | **gauche** | médiane (contre-chant) | A3..B4 | 92 |
| 2 | **gauche** | basse, marche de noires | E2..G3 | 112 |
| 3 | **droite** | **l'ostinato des guetteurs** | E4..B4 | 179 |
| 4 | **droite** | médiane (accords tenus) | F♯3..B4 | 37 |
| 5 | **droite** | bourdon de mi | E2 | 7 |

L'ostinato est entièrement à droite : c'est ce qui rend la zone reconnaissable
dès la première seconde, sans que la mélodie ait à se répéter.

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/nord
python3 nord.py
python3 ../../midi_to_mb.py nord.mid MARAISNO.MB.BIN \
    --bpm 150 --max 2400 --wav MARAISNO.wav
```
