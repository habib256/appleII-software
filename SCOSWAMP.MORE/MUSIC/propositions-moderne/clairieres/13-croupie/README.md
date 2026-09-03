# Clairière 13 — La Rivière Croupie

**`CROUPIE.MB.BIN` — 1 611 octets, 44,1 s, boucle.**

## La clairière

| | |
| --- | --- |
| `hub` | **295** |
| Pages | 295 |
| Case | (1,3) |
| Zone de référence | `riviere` (`RIVIERE.MB`) |
| Sorties | E → 183 (falaise), S → 094 (brume fétide) |

La berge. « La rive opposée est à 200 mètres de distance au moins et le cours
d'eau est infesté de crocodiles et d'autres créatures tout aussi peu
accueillantes. » On ne traverse pas ici ; on regarde.

## La pièce

| | |
| --- | --- |
| Titre | **La Berge aux Crocodiles** |
| Source | composition originale, `croupie.py` |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | large et lourde : une eau qui ne mène nulle part, et quelque chose dessous |
| Mode | **sol dorien** (sol la si♭ do ré **mi** fa) |
| Tempo | **132** à la noire |
| Forme | intro (4) — A (8) — B (8) — A' (4) |
| Durée | 24 mesures à 4/4 = **44,1 s** |
| Taille | **1 611 octets** (tampon de zone : 2 304) |
| Notes | 402 écrites, **0 abandonnée** |

**Ce qu'elle garde de la zone `riviere` :** le mode dorien, l'arpège de croches
qui ne s'arrête jamais, et surtout le **bourdon sur la quinte** — ré, pas sol.
C'est le procédé identifiable de la zone : la tonique n'est jamais soutenue,
donc rien ne se pose, donc tout coule.

**Ce qui lui appartient :** la basse en figure brève-longue, une mâchoire qui se
referme sous la surface, et le **mi naturel** du mode dorien (l'accord de do
majeur, mesures 8, 11, 18, 23) comme unique reflet de lumière sur une eau
boueuse. La mélodie reste en valeurs longues du début à la fin : on ne bouge
pas de la berge.

## Les six voix, mesurées

`python3 ../../verifier.py clairieres/13-croupie/croupie.mid --bpm 132`

| voix | côté | rôle | registre | notes | occupation |
| ---: | :---: | --- | --- | ---: | ---: |
| 0 | **gauche** | mélodie, valeurs longues | C5..G6 | 60 | 96 % |
| 1 | gauche | médiane (contre-chant) | G3..A4 | 72 | 96 % |
| 2 | **gauche** | basse, brève-longue | G2..A♯3 | 72 | 96 % |
| 3 | **droite** | arpège de croches, le courant | G3..C5 | 87 | 95 % |
| 4 | droite | médiane (accords tenus) | F3..G4 | 105 | 94 % |
| 5 | **droite** | bourdon de ré (la quinte) | D2 | 6 | 100 % |

## Refabriquer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/13-croupie
python3 croupie.py
python3 ../../../midi_to_mb.py croupie.mid CROUPIE.MB.BIN \
    --bpm 132 --max 2304 --wav CROUPIE.wav
```
