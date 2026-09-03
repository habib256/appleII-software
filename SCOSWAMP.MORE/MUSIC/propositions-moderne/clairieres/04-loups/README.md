# Clairière 4 — Les deux loups (`hub` 232, case 4,0)

**`LOUPS.MB.BIN` — 2 124 octets, 40,0 s, boucle.**

## Les pages

| Page | Titre | Ce qui s'y passe |
| ---: | --- | --- |
| 092 | Les deux loups | la forêt profonde, le silence, puis deux énormes loups qui vous fixent |
| 247 | Buisson violet | feuilles vert foncé, fleurs blanches, la grosse baie |
| 232 | La baie rangée | vous la cueillez et la rangez |
| 389 | Buisson d'Anthérique trouvé | la moitié de la mission est accomplie |

## La pièce

| | |
| --- | --- |
| Titre | **Deux Paires d'Yeux** |
| Source | composition originale, `loups.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | l'affût. « Vous tendez l'oreille, mais rien d'anormal ne trouble le silence. Puis, soudain, deux énormes loups… » |
| Mode | **si mineur éolien** (si do♯ ré mi fa♯ sol la) |
| Tempo | **168** à la noire |
| Forme | intro (4) — A (8) — B (8) — A' (8) |
| Durée | 28 mesures à 4/4 = **40,0 s** |
| Taille | **2 124 octets** — la plus grosse des douze, marge 180 |
| Notes | 514 écrites, **0 abandonnée** |

⚠ À 180 octets de la limite du tampon de zone. Toute retouche de cette pièce
doit être reconvertie avant d'être crue.

## Ce qui la relie à `nord`, et ce qui l'en sépare

Le procédé de la zone est l'ostinato fixe. Ici il est fixe et il y en a
**deux** : une cellule haute — si - fa♯ - la - fa♯ — et une cellule basse —
mi - si - ré - si — qui se relaient de mesure en mesure. Ni l'une ni l'autre ne
bouge d'une note de tout le morceau, y compris quand l'harmonie passe sous
elles ; ce sont deux bêtes qui se répondent d'un bord à l'autre de la clairière.
Sur le fa♯ mineur des mesures 4, 12, 18 et 20, le sol de la cellule basse
devient une sixte mineure appuyée sur la quinte, et le motif montre les dents —
c'est le même mécanisme que dans `MARAISNO.MB`, mais deux fois et en alternance.

Les deux cellules sont **détachées** (`gap=0.08`) : un pas dans les feuilles, pas
un bourdonnement. Occupation mesurée 77 %, contre 92 % pour la zone.

Le bourdon est sur **fa♯**, la quinte à vide de si, et il se refrappe **toutes
les deux mesures** au lieu de quatre : c'est la respiration de l'affût, quatorze
frappes au lieu de sept.

## Les six voix, mesurées

`python3 ../../verifier.py loups.mid --bpm 168`

| voix | côté | ce qui s'y trouve | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | la mélodie, seule | F♯5..A6 | 80 |
| 1 | gauche | le contre-chant, et la cellule haute quand elle passe dessous | F♯3..A4 | 91 |
| 2 | **gauche** | la basse qui rôde, fondamentale et quinte grave | A2..B3 | 108 |
| 3 | **droite** | **les deux cellules**, l'essentiel du mouvement | B3..B4 | 191 |
| 4 | droite | les accords tenus | F♯3..D4 | 30 |
| 5 | **droite** | le bourdon de fa♯, respiré | F♯2 | 14 |

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/04-loups
python3 loups.py
python3 ../../../midi_to_mb.py loups.mid LOUPS.MB.BIN \
    --bpm 168 --max 2304 --wav LOUPS.wav
```
