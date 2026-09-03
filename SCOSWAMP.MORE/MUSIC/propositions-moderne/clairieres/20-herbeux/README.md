# Clairière 20 — Trois chemins herbeux

**`HERBEUX.MB.BIN` — 1 408 octets, 36,9 s, boucle.**

## La clairière

| | |
| --- | --- |
| `hub` | **047** |
| Pages | 047 |
| Case | (4,4) |
| Zone de référence | `sud` (`MARAISUD.MB`) |
| Sorties | S → 290 (orques), E → 031 (bassin de cristal), O → 118 (scorpions) |
| Contenu | rien — mais six pages y mènent (`CARTOGRAPHIE.md` § 2.3) |

« Rien d'intéressant n'y apparaît à première vue ; l'air est lourd et calme.
Trois sentiers permettent de quitter cette clairière : sud, est et ouest. Le
sentier du sud semble plus humide ; l'est offre une lueur d'horizon ; l'ouest
est étroit et bordé d'arbres serrés. »

## La pièce

| | |
| --- | --- |
| Titre | **Trois Chemins Herbeux** |
| Source | composition originale, `herbeux.py` |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | une clairière où il n'arrive rien : la zone, en plus clair et plus vide |
| Mode | **ré dorien** (ré mi fa sol la **si** do) |
| Tempo | **145** à la noire |
| Forme | intro (4) + **trois phrases de six mesures**, une par sentier |
| Durée | 22 mesures à 4/4 = **36,9 s** |
| Taille | **1 408 octets** (tampon de zone : 2 304) |
| Notes | 345 écrites, **0 abandonnée** |

**Ce qu'elle garde de la zone `sud` :** le **bourdon de tonique immobile** sur
le **même ré** que `MARAISUD.MB`, et la même marche modale. C'est la plus
proche de la zone des douze — voulu : c'est la clairière la plus neutre du jeu.

**Ce qui lui appartient :** le mode est dorien, si naturel au lieu de si bémol.
Une seule note de différence, et elle suffit à éclaircir l'air. Surtout, la
forme n'est pas intro-A-B-A' mais **trois phrases**, dans l'ordre du texte :

- le **sud** (mes. 5-10), « plus humide » : la mélodie descend, Dm-F-C-Am-Dm ;
- l'**est** (mes. 11-16), « une lueur d'horizon » : elle monte, et c'est la
  seule section à poser le **sol majeur**, le quatrième degré majeur du dorien ;
- l'**ouest** (mes. 17-22), « étroit et bordé d'arbres serrés » : elle se
  resserre dans une sixte et retombe sur la tonique.

Chaque phrase finit sur son accord de départ : trois cadences, trois chemins,
aucun choix imposé. La basse ne fait que deux blanches — l'air est lourd et
calme.

## Les six voix, mesurées

`python3 ../../verifier.py clairieres/20-herbeux/herbeux.mid --bpm 145`

| voix | côté | rôle | registre | notes | occupation |
| ---: | :---: | --- | --- | ---: | ---: |
| 0 | **gauche** | mélodie, les trois sentiers | G4..E6 | 53 | 96 % |
| 1 | gauche | médiane (contre-chant) | A3..A4 | 76 | 95 % |
| 2 | **gauche** | basse, deux blanches | G2..A3 | 44 | 97 % |
| 3 | **droite** | arpège en sauts de quinte | A3..C5 | 89 | 94 % |
| 4 | droite | médiane (accords tenus) | F3..G4 | 77 | 95 % |
| 5 | **droite** | bourdon de ré (la tonique) | D2 | 6 | 100 % |

## Refabriquer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/20-herbeux
python3 herbeux.py
python3 ../../../midi_to_mb.py herbeux.mid HERBEUX.MB.BIN \
    --bpm 145 --max 2304 --wav HERBEUX.wav
```
