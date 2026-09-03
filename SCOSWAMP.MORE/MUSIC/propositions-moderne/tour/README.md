# Zone `tour` — la tour de Stratagus

**`TOUR.MB.BIN` — 1 056 octets, 46,5 s, boucle.**

## Ce que la zone couvre

Aucune clairière : quatorze pages hors carte, plus la victoire amère.

| Ensemble | Pages |
| --- | --- |
| Tour de Stratagus | 226, 225, 402, **124**, 222, 297, 298, 327, 349, 372, 373, 375, 401 |
| Victoire amère de Stratagus | 358 |

Les pages **124**, **222**, **225**, **402** portent aussi une ligne de combat,
et **297**, **372**, **375**, **401** sont aussi des pages de mort : la
surcouche `MU +COMBAT.MB` ou `MU +MORT.MB` remplace le thème pour une page sans
effacer la mémoire de la zone, qui revient à la page suivante.

## La pièce

| | |
| --- | --- |
| Titre | **La Tour de Stratagus** |
| Source | composition originale, `tour.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | marche lente et haute : la basse ne bouge qu'à la blanche, l'arpège qu'à la noire, la mélodie tient |
| Mode | **sol mineur harmonique** (sol la si♭ do ré mi♭ **fa♯**) |
| Tempo | **125** à la noire |
| Forme | intro (4) — A (8) — B (8) — coda (4) |
| Durée | 24 mesures à 4/4 = **46,5 s** |
| Taille | **1 056 octets** — la plus légère des huit pièces à boucle |
| Notes | 279 écrites, 0 abandonnée |

La seconde augmentée mi♭-fa♯ du mineur harmonique est la seule chose qui
distingue cette zone de tout le reste du jeu : **c'est la magie, et elle est
écrite, pas suggérée.** Aucun autre morceau du dossier n'a de sensible.

Le bourdon est sur **ré**, la dominante, pas sur sol : la tour n'est jamais
posée, et la cadence D-Gm des mesures 20-21 est la seule fois où elle le
paraît.

À 125 à la noire avec une basse en blanches, le pouls réel est à 62 : la
lenteur vient de l'écriture, pas du tempo, et le tempo reste sur les 24 ticks
par temps qui tombent juste.

## Les six voix

| voix | côté | rôle | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | mélodie, en valeurs longues | D5..A6 | 57 |
| 1 | **gauche** | médiane (contre-chant) | G3..G4 | 47 |
| 2 | **gauche** | basse, deux blanches par mesure | F2..G3 | 48 |
| 3 | **droite** | arpège à la noire | D4..D5 | 85 |
| 4 | **droite** | médiane (accords tenus) | F♯3..F4 | 36 |
| 5 | **droite** | bourdon de ré (la dominante) | D2 | 6 |

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/tour
python3 tour.py
python3 ../../midi_to_mb.py tour.mid TOUR.MB.BIN \
    --bpm 125 --max 2400 --wav TOUR.wav
```
