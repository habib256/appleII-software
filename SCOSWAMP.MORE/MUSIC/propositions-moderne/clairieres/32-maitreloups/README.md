# Clairière 32 — Clairière du Maître des Loups (`hub` 314)

**`MAITRELOUPS.MB.BIN` — 1 978 octets, 47,4 s, boucle.**

## Ce que la clairière raconte

| Page | Ce qu'on y lit |
| ---: | --- |
| 398 | une petite maison en rondins, un Loup debout à côté ; un homme robuste vêtu comme un Garde Forestier, l'Amulette d'Argent en forme de loup — « il vous répond avec mauvaise humeur en vous ordonnant de passer votre chemin » |
| 239 | la maison fermée à double tour, aucun signe de vie |
| 314 | deux directions, et un énorme escargot qui passe doucement devant vous |

Zone de référence : **`sud`** (`MARAISUD.MB`, *Sentiers Verts*).

## La pièce

| | |
| --- | --- |
| Titre | **Le Cor du Maître** |
| Source | composition originale, `maitreloups.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | un homme qui garde son bois : ni piège ni monstre, seulement quelqu'un qui vous dit de passer votre chemin |
| Mode | **mi éolien** (mi fa♯ sol la si do ré) |
| Tempo | **143** à la noire |
| Forme | intro (4) — A (8) — B (8) — A' à l'octave (8) |
| Durée | 28 mesures à 4/4 = **47,4 s** |
| Taille | **1 978 octets** (tampon de zone : 2 304) |
| Notes | 503 écrites, **0 abandonnée** |

Ce qui la rattache à `sud` : la marche **i-VI-III-VII** (Em-C-G-D) sur un bourdon
de mi immobile. Ce qui n'appartient qu'à elle : le **cor de chasse**. Les appels
de la mélodie sont faits de quintes et de quartes à vide — mi-si-mi, do-sol-mi,
la-ré-fa♯ — et jamais de degrés conjoints ; et l'arpège ne joue **aucune
tierce**, seulement fondamentale et quinte, pendant que le lit d'accords tenus
reste la seule voix qui dise le mode. C'est le son ouvert d'un pavillon, et
c'est la seule clairière des onze où l'accompagnement refuse la tierce.

## Les six voix (mesurées par `verifier.py`)

| voix | côté | rôle | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | mélodie, appels de cor | E5..A6 | 76 |
| 1 | gauche | médiane (contre-chant) | G3..A4 | 77 |
| 2 | **gauche** | basse, quatre noires par mesure | E2..G3 | 112 |
| 3 | **droite** | arpège de quintes à vide, sans tierce | A3..D5 | 151 |
| 4 | droite | médiane (accords tenus, la seule tierce) | F♯3..G4 | 80 |
| 5 | **droite** | bourdon de mi | E2 | 7 |

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/32-maitreloups
python3 maitreloups.py
python3 ../../../midi_to_mb.py maitreloups.mid MAITRELOUPS.MB.BIN \
    --bpm 143 --max 2304 --wav MAITRELOUPS.wav
```
