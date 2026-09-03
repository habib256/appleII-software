# Clairière 31 — La rivière profonde (`hub` 044)

**`PROFONDE.MB.BIN` — 1 873 octets, 49,9 s, boucle.**

## Ce que la clairière raconte

| Page | Ce qu'on y lit |
| ---: | --- |
| 090 | « celui qui se trouve devant vous est beaucoup plus profond. La rivière tourbillonne en remous : qui sait quelles créatures se cachent dans son lit ? » |
| 044 | la traversée à pied : sur l'autre rive, de grosses sangsues, un dé d'ENDURANCE perdu |
| 254 | la Pierre de Flétrissure : l'arbre s'abat, fait pont, puis se décompose dans le courant |
| 370 | la Pierre de Glace : un pont solide se forme à la surface |

Zone de référence : **`riviere`** (`RIVIERE.MB`, *Le Pont sur la Croupie*).

## La pièce

| | |
| --- | --- |
| Titre | **L'Eau Noire** |
| Source | composition originale, `profonde.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | on ne touche pas le fond : la plus longue boucle des onze, et la seule qui ne se pose jamais |
| Mode | **sol dorien** (sol la si♭ do ré **mi** fa) |
| Tempo | **136** à la noire |
| Forme | intro (4) — A (8) — B (8) — A' (8) |
| Durée | 28 mesures à 4/4 = **49,9 s** |
| Taille | **1 873 octets** (tampon de zone : 2 304) |
| Notes | 468 écrites, **0 abandonnée** |

Les deux marques de la zone `riviere` sont gardées : l'arpège de croches qui
**ne s'arrête jamais** d'un bout à l'autre, et le bourdon posé non sur la
tonique mais sur la **quinte** — un ré sous un sol dorien —, qui laisse tout le
morceau en suspension. Ce qui n'appartient qu'à elle : le **remous**. Au lieu de
monter et redescendre proprement comme au pont, le dessin de l'arpège revient
sur lui-même (0-2-1-2-0-1-2-1), huit croches qui tournent au lieu de couler.

Le do majeur du mode dorien — le mi bécarre sous un mode à si bémol — est la
seule clarté de la pièce : c'est la surface, vue d'en dessous.

## Les six voix (mesurées par `verifier.py`)

| voix | côté | rôle | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | mélodie en blanches | C5..G6 | 69 |
| 1 | gauche | médiane (contre-chant) | G3..A4 | 69 |
| 2 | **gauche** | basse | E2..G3 | 84 |
| 3 | **droite** | le remous : huit croches qui reviennent sur elles-mêmes | B♭3..D5 | 156 |
| 4 | droite | médiane (accords tenus) | F3..G4 | 83 |
| 5 | **droite** | bourdon de ré, la **quinte** du mode | D2 | 7 |

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/31-profonde
python3 profonde.py
python3 ../../../midi_to_mb.py profonde.mid PROFONDE.MB.BIN \
    --bpm 136 --max 2304 --wav PROFONDE.wav
```
