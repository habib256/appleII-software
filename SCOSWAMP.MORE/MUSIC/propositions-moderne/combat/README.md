# Zone `combat` — surcouche, 32 pages

**`COMBAT.MB.BIN` — 1 860 octets, 34,1 s, boucle.**

## Ce que la zone couvre

Ce n'est pas une zone de la carte : c'est une **surcouche**. Les 32 pages qui
portent une ligne `M` (combat) prennent ce thème le temps du combat, puis la
musique de la clairière revient toute seule.

| Pages | 012, 026, 028, 064, 079, 082, 120, **124**, 134, 146, 171, 176, 200, 211, 215, 221, 222, 224, 225, 235, 261, 267, 281, 284, 301, 312, 341, 355, 378, 379, 392, 402 |
| --- | --- |

Cinq d'entre elles appartiennent aussi à une clairière (082 → clairière 35,
355 → clairière 1) ou à la tour (124, 222, 225, 402) : la surcouche prime pour
la page, la mémoire de zone n'est pas effacée.

## La pièce

| | |
| --- | --- |
| Titre | **Le Fer et la Pince** |
| Source | composition originale, `combat.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | l'accompagnement court, pas le thème : l'arpège martèle fondamentale-quinte en croches, la basse frappe le contretemps, la mélodie n'a que des notes longues |
| Mode | **si éolien** (si do♯ ré mi fa♯ sol la) |
| Tempo | **200** à la noire — **15 ticks par temps**, la valeur la plus rapide qui tombe juste sur l'horloge de 50 Hz |
| Forme | intro (4) — A (8) — B (8) — A' (8) |
| Durée | 28 mesures à 4/4 = **34,1 s** — assez court pour reboucler sans lasser pendant les quatre ou cinq assauts d'un combat |
| Taille | **1 860 octets** |
| Notes | 511 écrites, 0 abandonnée |

Le bourdon est sur **fa♯**, la dominante : rien ne se résout tant que le combat
dure. Les accords tournent d'une mesure chacun (Bm-G-D-A, Bm-G-A-F♯m) — c'est
le seul morceau du dossier où l'harmonie va plus vite que la mélodie.

## Les six voix

| voix | côté | rôle | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | mélodie, en valeurs longues | F♯5..B6 | 84 |
| 1 | **gauche** | médiane (contre-chant) | G3..A4 | 61 |
| 2 | **gauche** | basse, coup et contretemps | A2..B3 | 92 |
| 3 | **droite** | **quintes à vide martelées en croches** | B3..D5 | 147 |
| 4 | **droite** | médiane (accords tenus) | D3..F♯4 | 120 |
| 5 | **droite** | bourdon de fa♯ (la dominante) | F♯2 | 7 |

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/combat
python3 combat.py
python3 ../../midi_to_mb.py combat.mid COMBAT.MB.BIN \
    --bpm 200 --max 2400 --wav COMBAT.wav
```
