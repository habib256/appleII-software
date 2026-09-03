# Clairière 28 — La clairière des Arbres-Épées (`hub` 022)

**`ARBRESEPEES.MB.BIN` — 1 987 octets, 40,9 s, boucle.**

## Ce que la clairière raconte

| Page | Ce qu'on y lit |
| ---: | --- |
| 157 | l'entrée : des arbres petits, vert foncé, aux branches qui ressemblent à des bras — « chaque bras tient une épée à son extrémité » |
| 279 | le retour : « les branches des terribles Arbres-Épées ont déjà repoussé » |
| 022 | les pousses rapides, les graines en poche, et trois directions à choisir sans tarder |

Zone de référence : **`danger`** (`DANGER.MB`, *Ce qui Attend Sous l'Eau*).

## La pièce

| | |
| --- | --- |
| Titre | **Les Bras qui Repoussent** |
| Source | composition originale, `arbresepees.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | on coupe, ça repousse : la seule clairière des onze dont le motif revient dans une autre voix au lieu de se développer |
| Mode | **fa phrygien** (fa **sol♭** la♭ si♭ do ré♭ mi♭) |
| Tempo | **166** à la noire |
| Forme | intro (4) — A (8) — B (8) — A' à l'octave (8) |
| Durée | 28 mesures à 4/4 = **40,9 s** |
| Taille | **1 987 octets** (tampon de zone : 2 304) |
| Notes | 506 écrites, **0 abandonnée** |

Ce qui la rattache à `danger` : le **demi-ton phrygien**, ici sol♭–fa, et le
bourdon de fa. Ce qui n'appartient qu'à elle : le **canon**. La cellule de trois
notes fa–sol♭–fa que la mélodie lance mesure 5 revient au contre-chant, une
octave plus bas, mesure 6 — puis encore mesures 18 et 22. On coupe le motif, il
repousse ailleurs. C'est le seul procédé d'imitation des onze clairières, et il
est là parce que la page 279 le demande.

La basse frappe les quatre noires sans jamais s'arrêter : ce sont les lames.

## Les six voix (mesurées par `verifier.py`)

| voix | côté | rôle | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | mélodie (énonce la cellule) | F5..A♭6 | 75 |
| 1 | gauche | médiane (contre-chant, répond en canon) | F♯3..B♭4 | 89 |
| 2 | **gauche** | basse, quatre noires par mesure | F2..A♭3 | 111 |
| 3 | **droite** | arpège fondamentale-quinte-tierce | B♭3..E♭5 | 175 |
| 4 | droite | médiane (accords tenus) | F♯3..A♭4 | 49 |
| 5 | **droite** | bourdon de fa | F2 | 7 |

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/28-arbresepees
python3 arbresepees.py
python3 ../../../midi_to_mb.py arbresepees.mid ARBRESEPEES.MB.BIN \
    --bpm 166 --max 2304 --wav ARBRESEPEES.wav
```
