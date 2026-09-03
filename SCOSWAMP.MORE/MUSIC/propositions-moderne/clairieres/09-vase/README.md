# Clairière 9 — Le bassin de Vase (`hub` 153, case 1,2)

**`VASE.MB.BIN` — 1 373 octets, 47,3 s, boucle.**

## Les pages

| Page | Titre | Ce qui s'y passe |
| ---: | --- | --- |
| 336 | Le bassin de Vase | le bruit de succion, le bassin, la Vase qui se soulève et barre le passage |
| 137 | Retour face à la Vase | ses blessures sont complètement guéries |
| 153 | Fuite de la clairière | le nord ou l'ouest, le sol semble plus sec |

## La pièce

| | |
| --- | --- |
| Titre | **Ce qui Sort du Bassin** |
| Source | composition originale, `vase.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | lent, épais, et qui se resserre. Deux mètres de fange qui rampent ne changent pas d'avis |
| Mode | **ré phrygien** (ré **mi♭** fa sol la si♭ do) |
| Tempo | **132** à la noire |
| Forme | intro (4) — A (8) — B (8) — A' (6) |
| Durée | 26 mesures à 4/4 = **47,3 s** — la plus longue des douze |
| Taille | **1 373 octets** (marge 931) |
| Notes | 362 écrites, **0 abandonnée** |

## Ce qui la relie à `danger`, et ce qui l'en sépare

Les deux marques de la zone sont le **demi-ton phrygien** posé un cran au-dessus
de la tonique et le **crescendo par la densité** — la carte n'ayant pas de
volume par note, on ne peut serrer que le nombre de notes. Ici les deux ne font
qu'une seule chose.

La cellule **ré - mi♭ - ré - fa** ne change pas une note du morceau et se
resserre trois fois :

| Mesures | Valeur | Ce que ça fait |
| :---: | --- | --- |
| 1-6 | blanches | le bassin respire |
| 7-16 | noires | la fange se contracte |
| 17-26 | croches | elle se répand sur le sentier |

La basse se resserre au même endroit, de la blanche à la noire. La mélodie prend
le demi-ton à son compte à partir de la mesure 19 — mi♭ - ré en croches — et la
pièce se ferme dessus : mi♭ sur ré, une blanche, sans résolution ailleurs.

Différence avec `DANGER.MB` : la zone tient son demi-ton dans l'**harmonie**,
l'accord de ré♭ qui retombe sur do mineur. Ici il est dans une **figure de deux
notes** qu'on entend tout le temps, et l'harmonie se contente de la porter. La
zone menace ; cette clairière-ci colle.

Le bourdon de ré ne bouge pas d'un bout à l'autre — sept frappes en 47 secondes.

## Les six voix, mesurées

`python3 ../../verifier.py vase.mid --bpm 132`

| voix | côté | ce qui s'y trouve | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | la mélodie, seule | F5..B♭6 | 73 |
| 1 | gauche | le contre-chant, et les accords quand ils passent dessous | A3..F4 | 85 |
| 2 | **gauche** | la basse, seule | F2..G3 | 72 |
| 3 | **droite** | **la fange** | D4..G4 | 86 |
| 4 | droite | les accords tenus | F3..F4 | 39 |
| 5 | **droite** | le bourdon de ré, immobile | D2 | 7 |

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/09-vase
python3 vase.py
python3 ../../../midi_to_mb.py vase.mid VASE.MB.BIN \
    --bpm 132 --max 2304 --wav VASE.wav
```
