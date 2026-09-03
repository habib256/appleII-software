# Clairière 25 — Herbe à Pinces (`hub` 187)

**`PINCES.MB.BIN` — 2 038 octets, 44,1 s, boucle.**

## Ce que la clairière raconte

| Page | Ce qu'on y lit |
| ---: | --- |
| 388 | l'entrée : une agréable clairière envahie d'herbes — puis « des pinces apparaissent aux extrémités de ses tiges » |
| 263 | le retour : des taches brunes là où les lianes se sont refermées |
| 033 | la traversée en courant : « l'herbe pousse plus vite encore » |
| 187 | le carrefour à trois chemins, sud, est le long de la rivière, ouest |

Zone de référence : **`danger`** (`DANGER.MB`, *Ce qui Attend Sous l'Eau*).

## La pièce

| | |
| --- | --- |
| Titre | **L'Herbe qui Serre** |
| Source | composition originale, `pinces.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | ça pousse plus vite que vous : la plus rapide des onze clairières, et la seule dont l'accompagnement claque au lieu de couler |
| Mode | **mi phrygien** (mi **fa** sol la si do ré) |
| Tempo | **176** à la noire |
| Forme | intro (4) — A (8) — B (8) — A' à l'octave (8) — coda (4) |
| Durée | 32 mesures à 4/4 = **44,1 s** |
| Taille | **2 038 octets** (tampon de zone : 2 304) |
| Notes | 523 écrites, **0 abandonnée** |

Ce qui la rattache à `danger` : le **demi-ton phrygien**, ici fa–mi, et le
bourdon de mi qui ne bouge pas d'un bout à l'autre. Ce qui n'appartient qu'à
elle : la **pince**. L'arpège joue trois croches puis se tait à la quatrième
(`0, 2, 1, silence`), si bien que l'accompagnement mord la mesure au lieu de la
remplir ; et la mélodie repart huit fois sur la seconde mineure fa–mi en
croches, la tenaille qui se referme. La coda (mesures 29-32) est la seule
respiration : deux mesures de la mineur, puis fa qui retombe sur mi.

## Les six voix (mesurées par `verifier.py`)

| voix | côté | rôle | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | mélodie | D5..G6 | 99 |
| 1 | gauche | médiane (contre-chant) | G3..A4 | 76 |
| 2 | **gauche** | basse, quatre noires par mesure | E2..G3 | 128 |
| 3 | **droite** | l'arpège à pinces | A3..D5 | 162 |
| 4 | droite | médiane (accords tenus) | F3..G4 | 50 |
| 5 | **droite** | bourdon de mi | E2 | 8 |

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/25-pinces
python3 pinces.py
python3 ../../../midi_to_mb.py pinces.mid PINCES.MB.BIN \
    --bpm 176 --max 2304 --wav PINCES.wav
```
