# Clairière 33 — Le large rond-point, la clairière de départ (`hub` 058)

**`RONDPOINT.MB.BIN` — 2 153 octets, 49,1 s, boucle.**

## Ce que la clairière raconte

C'est **la première clairière du Marais** : le joueur y arrive page 195, et tout
le reste de l'aventure part d'ici.

| Page | Ce qu'on y lit |
| ---: | --- |
| **195** | « il ne s'agit que d'un large rond-point d'où partent trois sentiers. Le sol est instable et détrempé, de grosses nuées d'insectes volètent au-dessus des mares stagnantes. Le brouillard humide monte en volutes. Les arbres rabougris semblent tordus, comme marqués par la corruption du marais. » |
| 024 | le Feu Follet qui danse devant vous, le trou rempli de vase, la tromperie |
| 058 | le passage prudent : une racine, une pierre, −1 ENDURANCE — puis ouest, est ou retour au sud |
| 404 | l'autre côté atteint sain et sauf, trois directions vers l'inconnu |
| 405 | la chute dans la vase, −1 HABILETÉ, et les mêmes trois directions |

La page 208 (retour vers le sud, sortie du Marais) porte la musique de
`village`, pas celle-ci.

Zone de référence : **`sud`** (`MARAISUD.MB`, *Sentiers Verts*).

## La pièce

| | |
| --- | --- |
| Titre | **Le Cœur du Marais** |
| Source | composition originale, `rondpoint.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | le thème du Marais lui-même : large, sans hâte, et sans conclusion — c'est la première chose que le joueur entend en entrant, et la dernière avant de ressortir |
| Mode | **ré éolien** (ré mi fa sol la **si♭** do) — la tonalité exacte de la zone |
| Tempo | **158** à la noire |
| Forme | intro (4) — A (8) — B (8) — A' à l'octave (8) — coda (4) |
| Durée | 32 mesures à 4/4 = **49,1 s** |
| Taille | **2 153 octets** (tampon de zone : 2 304) |
| Notes | 540 écrites, **0 abandonnée** |

C'est la plus longue et la plus grosse des onze, et c'est voulu : elle est la
seule à porter une **coda** en plus des quatre sections, parce qu'elle est le
thème du lieu et non celui d'un incident.

Elle prend de `sud` la tonique **et** le procédé — la marche i-VI-III-VII posée
sur un bourdon de ré qui ne bouge jamais — pour que le rond-point et la zone
sonnent comme le même endroit vu de plus ou moins près. Son thème, lui, n'est
qu'à elle : une **montée de trois notes**, ré-mi-fa, qui redemande son chemin.
La partie B l'énonce trois fois, à trois hauteurs (mesures 13, 15, 17) — les
trois sentiers de la page 195.

Le la mineur (v mineur, sans sensible : le mode éolien n'en a pas) est le sol
qui se dérobe. Aucune cadence ne conclut vraiment ; la dernière mesure retombe
sur le ré et la boucle repart, comme un rond-point.

## Les six voix (mesurées par `verifier.py`)

| voix | côté | rôle | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | mélodie | D5..A6 | 84 |
| 1 | gauche | médiane (contre-chant) | G3..A4 | 81 |
| 2 | **gauche** | basse | E2..G3 | 96 |
| 3 | **droite** | arpège en croches | A3..D5 | 177 |
| 4 | droite | médiane (accords tenus) | F3..G4 | 94 |
| 5 | **droite** | bourdon de ré | D2 | 8 |

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/33-rondpoint
python3 rondpoint.py
python3 ../../../midi_to_mb.py rondpoint.mid RONDPOINT.MB.BIN \
    --bpm 158 --max 2304 --wav RONDPOINT.wav
```
