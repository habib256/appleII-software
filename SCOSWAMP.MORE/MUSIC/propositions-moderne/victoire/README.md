# Zone `victoire` — les deux fins gagnantes

**`VICTOIRE.MB.BIN` — 1 424 octets, 32,5 s, `--no-loop`.**

## Ce que la zone couvre

| Pages | Titre |
| --- | --- |
| 158 | victoire |
| 175 | victoire |

La victoire amère de Stratagus (page **358**) garde le thème de la `tour` :
elle n'en est pas une.

Comme `mort`, la pièce se joue **une seule fois** (`--no-loop`) et laisse le
silence.

## La pièce

| | |
| --- | --- |
| Titre | **Par la Trouée de Ciel** |
| Source | composition originale, `victoire.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | large, pas militaire |
| Mode | **ré mixolydien** (ré mi fa♯ sol la si **do**) — la seule pièce en majeur du dossier |
| Tempo | **150** à la noire |
| Forme | quatre phrases de quatre mesures, plus une cadence de quatre |
| Durée | 20 mesures à 4/4 = **32,5 s** |
| Taille | **1 424 octets** |
| Notes | 361 écrites, 0 abandonnée |

Le do bécarre du mixolydien supprime la sensible et donc la pompe de fanfare
classique : la cadence est C-D, pas A-D. C'est ce qui empêche la victoire de
sonner comme un générique de télévision, et ce qui la rattache au monde modal
du reste du jeu.

La mélodie monte trois fois par tierces (mesures 1, 9, 17) ; la troisième
atteint le la aigu, mesure 12, et la pièce n'y revient plus.

## Les six voix

| voix | côté | rôle | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | mélodie | D5..B6 | 56 |
| 1 | **gauche** | médiane (contre-chant) | G3..A4 | 61 |
| 2 | **gauche** | basse, marche de noires | F♯2..G3 | 78 |
| 3 | **droite** | arpège en croches, tenu du début à la fin | C4..D5 | 113 |
| 4 | **droite** | médiane (accords tenus) | F♯3..G4 | 48 |
| 5 | **droite** | bourdon de ré | D2 | 5 |

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/victoire
python3 victoire.py
python3 ../../midi_to_mb.py victoire.mid VICTOIRE.MB.BIN \
    --bpm 150 --no-loop --max 2400 --wav VICTOIRE.wav
```
