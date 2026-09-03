# Clairière 35 — Bête du bassin (`hub` 082)

**`BASSIN.MB.BIN` — 1 969 octets, 47,4 s, boucle.**

## Ce que la clairière raconte

| Page | Ce qu'on y lit |
| ---: | --- |
| 209 | « une créature énorme à la peau brune et caoutchouteuse émerge soudain du bassin et tente de vous saisir d'un tentacule » — un magnifique Bijou Violet brille à son front |
| 082 | le duel au bord de l'eau (cette page-là passe en `+COMBAT.MB`, la surcouche) |
| 308 | la Bête morte, le Bijou Violet détaché du front, et l'unique chemin qui ramène vers l'ouest |
| 397 | la fuite : le même unique chemin |

Zone de référence : **`sud`** (`MARAISUD.MB`, *Sentiers Verts*).

## La pièce

| | |
| --- | --- |
| Titre | **Ce qui Monte du Bassin** |
| Source | composition originale, `bassin.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | quelque chose sort de l'eau à chaque mesure et n'y retourne pas — et quelque chose brille, que le joueur vient chercher |
| Mode | **fa éolien** (fa sol la♭ si♭ do ré♭ mi♭) |
| Tempo | **143** à la noire |
| Forme | intro (4) — A (8) — B (8) — A' à l'octave (8) |
| Durée | 28 mesures à 4/4 = **47,4 s** |
| Taille | **1 969 octets** (tampon de zone : 2 304) |
| Notes | 500 écrites, **0 abandonnée** |

Ce qui la rattache à `sud` : la marche **i-VI-III-VII** (Fm-D♭-A♭-E♭) sur un
bourdon de fa immobile. Deux choses n'appartiennent qu'à elle.

**Ce qui monte.** La basse ne descend jamais. Chaque mesure elle part de la
quinte grave et remonte l'accord — quinte, fondamentale, tierce, quinte — au
lieu de tourner autour de sa fondamentale comme dans les dix autres clairières.
C'est la seule basse ascendante des onze, et elle recommence à chaque mesure.

**Le Bijou Violet.** Le ré bémol (VI), seul accord majeur éclatant du morceau,
porte aux mesures 13, 18 et 22 la note la plus haute de la pièce, tenue une
blanche. C'est la seule chose qui brille dans le bassin.

## Les six voix (mesurées par `verifier.py`)

| voix | côté | rôle | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | mélodie, et le Bijou aux mesures 13, 18, 22 | F5..A♭6 | 73 |
| 1 | gauche | médiane (contre-chant) | A♭3..B♭4 | 71 |
| 2 | **gauche** | basse ascendante | F2..E♭4 | 106 |
| 3 | **droite** | arpège en croches | B♭3..E♭5 | 169 |
| 4 | droite | médiane (accords tenus) | G3..A♭4 | 74 |
| 5 | **droite** | bourdon de fa | F2 | 7 |

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/35-bassin
python3 bassin.py
python3 ../../../midi_to_mb.py bassin.mid BASSIN.MB.BIN \
    --bpm 143 --max 2304 --wav BASSIN.wav
```
