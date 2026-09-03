# Clairière 26 — Orques des Marais (`hub` 309)

**`ORQUES.MB.BIN` — 2 017 octets, 43,0 s, boucle.**

## Ce que la clairière raconte

| Page | Ce qu'on y lit |
| ---: | --- |
| 290 | l'embuscade : « une flèche vous frôle la tête en sifflant » — trois orques à la peau rongée par la gale, arcs en main |
| 323 | le retour : s'ils vivent encore, ils gardent l'ENDURANCE qu'ils avaient |
| 352 | la remontée vers le nord, épée en main, au cas où |
| 309 | les trois chemins qui quittent la clairière |

Zone de référence : **`danger`** (`DANGER.MB`, *Ce qui Attend Sous l'Eau*).

## La pièce

| | |
| --- | --- |
| Titre | **Trois Arcs dans la Brume** |
| Source | composition originale, `orques.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | martial : la seule clairière où le Marais est tenu par une troupe, et non par une créature |
| Mode | **ré phrygien** (ré **mi♭** fa sol la si♭ do) |
| Tempo | **158** à la noire |
| Forme | intro (4) — A (8) — B (8) — A' à l'octave (8) |
| Durée | 28 mesures à 4/4 = **43,0 s** |
| Taille | **2 017 octets** (tampon de zone : 2 304) |
| Notes | 516 écrites, **0 abandonnée** |

Ce qui la rattache à `danger` : le **demi-ton phrygien**, ici mi♭–ré, et le
bourdon de ré. Ce qui n'appartient qu'à elle : le **rythme pointé**, à la basse
comme à la mélodie (noire pointée, croche, deux noires), et une cellule de
fanfare de trois notes énoncée deux fois de suite un demi-ton plus haut, ré puis
mi♭ (mesures 5-6, reprise à l'octave mesures 21-22) — trois arcs, la même
flèche. Le bourdon est refrappé **toutes les deux mesures** au lieu de toutes
les quatre : c'est un tambour, pas une brume.

## Les six voix (mesurées par `verifier.py`)

| voix | côté | rôle | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | mélodie | D5..B♭6 | 82 |
| 1 | gauche | médiane (contre-chant) | G3..B♭4 | 87 |
| 2 | **gauche** | basse, marche pointée | F2..G3 | 111 |
| 3 | **droite** | arpège fondamentale-tierce-quinte | B♭3..D5 | 168 |
| 4 | droite | médiane (accords tenus) | F3..G4 | 54 |
| 5 | **droite** | bourdon de ré, refrappé toutes les 2 mesures | D2 | 14 |

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/26-orques
python3 orques.py
python3 ../../../midi_to_mb.py orques.mid ORQUES.MB.BIN \
    --bpm 158 --max 2304 --wav ORQUES.wav
```
