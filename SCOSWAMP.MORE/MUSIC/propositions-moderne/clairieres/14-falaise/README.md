# Clairière 14 — Sommet de la falaise

**`FALAISE.MB.BIN` — 1 548 octets, 41,6 s, boucle.**

## La clairière

| | |
| --- | --- |
| `hub` | **183** |
| Pages | 183 |
| Case | (2,3) |
| Zone de référence | `riviere` (`RIVIERE.MB`) |
| Sorties | S → 066, O → 295 ; **N et E = plonger = mort** (crocodile) |

« Au lieu du morne feuillage, c'est le ciel qui s'ouvre. Vous atteignez le
sommet d'une haute falaise dominant la rivière. » En contrebas, les eaux
boueuses, les crocodiles paresseux ; plus loin à l'est, le pont, inaccessible.

## La pièce

| | |
| --- | --- |
| Titre | **Le Ciel s'Ouvre** |
| Source | composition originale, `falaise.py` |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | l'altitude : ça monte seize mesures, puis on se penche |
| Mode | **si dorien** (si do♯ ré mi fa♯ **sol♯** la) |
| Tempo | **140** à la noire |
| Forme | intro (4) — A (8) — B (8) — A' (4) |
| Durée | 24 mesures à 4/4 = **41,6 s** |
| Taille | **1 548 octets** (tampon de zone : 2 304) |
| Notes | 381 écrites, **0 abandonnée** |

**Ce qu'elle garde de la zone `riviere` :** le mode dorien et le **bourdon sur
la quinte** — fa♯, pas si.

**Ce qui lui appartient :** l'arpège n'y tourne plus sur trois sons mais en
atteint **quatre, l'octave comprise** — une figure qui s'ouvre au lieu de
tourner. La mélodie monte pendant seize mesures jusqu'au **si aigu de la mesure
18**, le point le plus haut des douze pièces, puis redescend d'un trait sur
trois mesures : on se penche par-dessus le bord. La basse abandonne la marche
et se contente de deux blanches ouvertes — en haut, on ne marche plus.

## Les six voix, mesurées

`python3 ../../verifier.py clairieres/14-falaise/falaise.mid --bpm 140`

| voix | côté | rôle | registre | notes | occupation |
| ---: | :---: | --- | --- | ---: | ---: |
| 0 | **gauche** | mélodie, la montée | A4..B6 | 63 | 96 % |
| 1 | gauche | médiane (contre-chant) | G♯3..D5 | 62 | 96 % |
| 2 | **gauche** | basse, deux blanches | G♯2..B3 | 48 | 97 % |
| 3 | **droite** | arpège à l'octave, l'ouverture | A3..E5 | 102 | 94 % |
| 4 | droite | médiane (accords tenus) | F♯3..C♯5 | 100 | 94 % |
| 5 | **droite** | bourdon de fa♯ (la quinte) | F♯2 | 6 | 100 % |

## Refabriquer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/14-falaise
python3 falaise.py
python3 ../../../midi_to_mb.py falaise.mid FALAISE.MB.BIN \
    --bpm 140 --max 2304 --wav FALAISE.wav
```
