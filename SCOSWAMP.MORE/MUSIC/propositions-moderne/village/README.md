# Zone `village` — Bourbenville, le prologue, Courbensaule, la sortie

**`VILLAGE.MB.BIN` — 2 285 octets, 46,7 s, boucle.**

## Ce que la zone couvre

Une clairière et les pages hors carte du prologue.

| # | `hub` | Titre | Pages |
| ---: | ---: | --- | --- |
| **1** | 078 | **Route de Courbensaule** (ville, boutique d'Alphonse, La Lance Tordue) | 280, 355, 78, 150, 408 |

| Ensemble | Pages |
| --- | --- |
| Prologue de Bourbenville | 001, 048, 095, 122, 240, 296, 173, 009 |
| Retour des missions | 159 |
| Sortie du Marais | 208 |

**Courbensaule est ici volontairement**, et c'est le seul écart avec le plan à
onze zones : les deux villes sont le même lieu du point de vue du joueur — un
endroit où l'on achète, où l'on parle, où rien ne mord — et la clairière 1 ne
compte que cinq pages. C'est la fusion n° 1 recommandée par
`../../MUSIC/propositions/INDEX.md` § 4. Le dossier passe ainsi de onze pièces
à dix.

## La pièce

| | |
| --- | --- |
| Titre | **Les Feux de Bourbenville** |
| Source | composition originale, `village.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | le seul morceau du jeu qui n'ait pas peur : tierces majeures, basse qui balance croche pointée-croche, refrain qui revient |
| Mode | **sol mixolydien** (sol la si do ré mi **fa**) — septième mineure au lieu de la sensible : chaud sans être pompeux |
| Tempo | **166** à la noire |
| Forme | A refrain (8) — B couplet, vers do (8) — A' (8) — coda qui s'éloigne (8) |
| Durée | 32 mesures à 4/4 = **46,7 s** |
| Taille | **2 285 octets** — la plus grosse pièce du dossier |
| Notes | 584 écrites, 0 abandonnée |

Harmonie : G-F-C-G / Am-F-C-G au refrain, C-G-Dm-Am / F-C-F-G au couplet, et
une coda Em-C-F-G / Em-C-Dm-G qui prend congé au lieu de conclure — c'est la
page 009, l'entrée du Marais.

## Les six voix

| voix | côté | rôle | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | mélodie | D5..A6 | 96 |
| 1 | **gauche** | médiane (contre-chant) | G3..A4 | 84 |
| 2 | **gauche** | basse de danse | D2..F3 | 128 |
| 3 | **droite** | arpège en croches, le tambourin | C4..D5 | 184 |
| 4 | **droite** | médiane (accords tenus) | F3..G4 | 84 |
| 5 | **droite** | bourdon de sol, refrappé toutes les 4 mesures | G2 | 8 |

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/village
python3 village.py
python3 ../../midi_to_mb.py village.mid VILLAGE.MB.BIN \
    --bpm 166 --max 2400 --wav VILLAGE.wav
```
