# Zone `combat` — surcouche, 32 pages

**`COMBAT.MB.BIN` — 1 215 octets, 24,5 s, boucle.**

Surcouche : le flux doit tenir dans le **tampon de surcouche de 1 280
octets**, la moitié de celui des thèmes de zone. Il reste 65 octets.

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
| Caractère | l'accompagnement court, pas le thème : les quintes martèlent, la basse frappe le contretemps, la mélodie n'a que des notes longues |
| Mode | **si éolien** (si do♯ ré mi fa♯ sol la) |
| Tempo | **200** à la noire — **15 ticks par temps**, la valeur la plus rapide qui tombe juste sur l'horloge de 50 Hz |
| Forme | garde (4) — A (8) — B (8) |
| Durée | 20 mesures à 4/4 = **24,5 s** — la durée d'une mêlée, et assez court pour reboucler sans lasser pendant les quatre ou cinq assauts |
| Taille | **1 215 octets** |
| Notes | 329 écrites, 0 abandonnée |

Le bourdon est sur **fa♯**, la dominante : rien ne se résout tant que le combat
dure. Les accords tournent d'une mesure chacun (Bm-G-D-A, Bm-G-A-F♯m) — c'est
le seul morceau du dossier où l'harmonie va plus vite que la mélodie.

Les quintes à vide vont **à la noire pendant les quatre mesures de garde, puis
en croches dès la mesure 5** : c'est la seule montée du morceau, et elle sert
aussi le budget. La reprise A' du thème a été supprimée — un combat ne dure pas
assez pour qu'on l'entende, et la boucle courte sert le propos.

## Les six voix

| voix | côté | rôle | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | mélodie, en valeurs longues | F♯5..B6 | 60 |
| 1 | **gauche** | médiane (contre-chant) | A3..F♯4 | 39 |
| 2 | **gauche** | basse : le coup, la quinte grave au contretemps, la blanche | A2..B3 | 52 |
| 3 | **droite** | **quintes à vide martelées**, noires puis croches | B3..D5 | 103 |
| 4 | **droite** | médiane (accords tenus) | D3..F♯4 | 70 |
| 5 | **droite** | bourdon de fa♯ (la dominante) | F♯2 | 5 |

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/combat
python3 combat.py
python3 ../../midi_to_mb.py combat.mid COMBAT.MB.BIN \
    --bpm 200 --max 1280 --wav COMBAT.wav
```
