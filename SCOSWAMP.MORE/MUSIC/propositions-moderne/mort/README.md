# Zone `mort` — surcouche, 11 pages et l'écran `game_over`

**`MORT.MB.BIN` — 659 octets, 31,2 s, `--no-loop`.**

Surcouche : le flux doit tenir dans le **tampon de surcouche de 1 280
octets**, la moitié de celui des thèmes de zone. Il reste 621 octets — c'est la pièce la plus au large du dossier.

## Ce que la zone couvre

| Pages | 003, 030, 098, 260, 297, 313, 332, 361, 372, 375, 401 |
| --- | --- |

Plus l'écran `game_over` du moteur. Quatre de ces pages (297, 372, 375, 401)
sont aussi des pages de la tour de Stratagus : la surcouche prime.

La pièce se joue **une seule fois** puis laisse le silence — c'est le seul
usage de `--no-loop` avec `victoire`. Une boucle sur un écran de mort serait
une punition.

## La pièce

| | |
| --- | --- |
| Titre | **Le Marais Referme** |
| Source | composition originale, `mort.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | rien ne court. Aucune croche, aucun ostinato ; la seule chose qui bouge est un arpège à la noire, et il descend |
| Mode | **do éolien** (do ré mi♭ fa sol la♭ si♭) |
| Tempo | **125** à la noire, écrit en blanches et en rondes — le pouls réel est à 62 |
| Forme | quatre phrases de quatre mesures ; la mélodie ne monte qu'une fois, mesure 5, puis retombe de sol à do en huit mesures |
| Durée | 16 mesures à 4/4 = **31,2 s** |
| Taille | **659 octets** — la plus petite pièce du dossier |
| Notes | 170 écrites, 0 abandonnée |

Harmonie : Cm-Cm-A♭-A♭ / E♭-B♭-Fm-Cm / A♭-E♭-Fm-Gm / A♭-B♭-Cm-Cm. La cadence
finale est plagale (A♭-Cm), pas dominante : elle referme au lieu de conclure.

## Les six voix

| voix | côté | rôle | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | mélodie, blanches et rondes | D♯5..D♯6 | 26 |
| 1 | **gauche** | médiane (contre-chant) | G3..F4 | 25 |
| 2 | **gauche** | basse, deux blanches par mesure | F2..G♯3 | 32 |
| 3 | **droite** | arpège **descendant** à la noire (quinte, tierce, fondamentale, tierce) | A♯3..D♯5 | 63 |
| 4 | **droite** | médiane (accords tenus) | G3..D♯4 | 20 |
| 5 | **droite** | bourdon de do | C2 | 4 |

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/mort
python3 mort.py
python3 ../../midi_to_mb.py mort.mid MORT.MB.BIN \
    --bpm 125 --no-loop --max 1280 --wav MORT.wav
```
