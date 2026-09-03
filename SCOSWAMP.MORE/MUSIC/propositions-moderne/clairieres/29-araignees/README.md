# Clairière 29 — Tente aux araignées, le Maître des Araignées (`hub` 165)

**`ARAIGNEES.MB.BIN` — 1 885 octets, 45,3 s, boucle.**

## Ce que la clairière raconte

| Page | Ce qu'on y lit |
| ---: | --- |
| 144 | « des milliers de fils forment des guirlandes entre les arbres » — au centre, une tente somptueuse, un homme à la barbe blanche, l'Amulette d'Argent en forme d'araignée ; l'Anneau de Cuivre se réchauffe |
| 345 | le retour : la clairière est en feu, un immense brasier, −1 ENDURANCE |
| 354 | l'Amulette arrachée au cadavre : une étincelle, et tout s'embrase |
| 165 | la petite clairière à deux chemins, à peine protégée des vents |

Zone de référence : **`danger`** (`DANGER.MB`, *Ce qui Attend Sous l'Eau*).

## La pièce

| | |
| --- | --- |
| Titre | **Le Fil d'Argent** |
| Source | composition originale, `araignees.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | une toile qui ne se referme pas, puis un incendie qui ne s'éteint pas |
| Mode | **do dièse phrygien** (do♯ **ré** mi fa♯ sol♯ la si) |
| Tempo | **150** à la noire |
| Forme | intro (4) — A (8) — B (8) — A' (8), l'incendie à la mesure 17 |
| Durée | 28 mesures à 4/4 = **45,3 s** |
| Taille | **1 885 octets** (tampon de zone : 2 304) |
| Notes | 472 écrites, **0 abandonnée** |

Ce qui la rattache à `danger` : le **demi-ton phrygien**, ici ré–do♯, et le
bourdon immobile. Deux traits viennent des pages.

**La toile.** L'arpège est une cellule de **trois** sons dans une mesure de
**quatre** temps : il ne retombe jamais deux fois au même endroit du cycle
harmonique, les fils se croisent sans jamais se superposer. C'est le seul
accompagnement des onze clairières qui ne soit pas en phase avec la mesure.

**Le feu.** À partir de la mesure 17, la basse passe de la blanche à la noire :
la densité double et ne redescend plus. Comme dans `danger`, le crescendo est
fait par la densité et non par le volume — le lecteur 6502 n'a pas de volume par
note.

## Les six voix (mesurées par `verifier.py`)

| voix | côté | rôle | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | mélodie | F♯5..B6 | 77 |
| 1 | gauche | médiane (contre-chant) | G♯3..A4 | 114 |
| 2 | **gauche** | basse, blanches puis noires (l'incendie) | E2..F♯3 | 80 |
| 3 | **droite** | la toile : trois sons dans quatre temps | A3..C♯5 | 136 |
| 4 | droite | médiane (accords tenus) | F♯3..G♯4 | 58 |
| 5 | **droite** | bourdon de do dièse | C♯2 | 7 |

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/29-araignees
python3 araignees.py
python3 ../../../midi_to_mb.py araignees.mid ARAIGNEES.MB.BIN \
    --bpm 150 --max 2304 --wav ARAIGNEES.wav
```
