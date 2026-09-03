# Clairière 23 — La Licorne

**`LICORNE.MB.BIN` — 1 605 octets, 42,2 s, boucle.**

## La clairière

| | |
| --- | --- |
| `hub` | **348** |
| Pages | 320 (la Licorne), 265 (la clairière déserte), 348 (quatre chemins) |
| Case | (1,5) |
| Zone de référence | `sud` (`MARAISUD.MB`) |
| Sorties | N → 094 (brume), S → 157, E → 010 (les combats), O → 204 (les Fleurs) |
| Contenu | LICORNE blessée (11/4 en 221) ; **Corne de Licorne** (`277 G CO`) ; bénédiction (381) |

« Un animal de couleur blanche est couché au centre de la clairière. Vous pensez
d'abord qu'il s'agit d'un cheval, mais lorsqu'il tourne la tête dans votre
direction, vous reconnaissez aussitôt une LICORNE. Elle semble blessée : des
traces de griffes sont visibles sur son flanc. Elle se relève cependant et
baisse sa corne vers vous en lançant un grognement qui ressemble fort à un
défi. »

## La pièce

| | |
| --- | --- |
| Titre | **La Licorne Blessée** |
| Source | composition originale, `licorne.py` |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | noble et blessée : elle est couchée, elle se relève, elle repart |
| Mode | **fa éolien** (fa sol la♭ si♭ do ré♭ mi♭) |
| Tempo | **138** à la noire |
| Forme | intro (4) — A (8) l'animal couché — B (8) le défi — A' (4) |
| Durée | 24 mesures à 4/4 = **42,2 s** |
| Taille | **1 605 octets** (tampon de zone : 2 304) |
| Notes | 400 écrites, **0 abandonnée** |

**Ce qu'elle garde de la zone `sud` :** c'est la plus fidèle des sept pièces
`sud` — elle reprend la **marche i-VI-III-VII** de `MARAISUD.MB` (Fm-D♭-A♭-E♭,
soit Dm-B♭-F-C transposé) sur un **bourdon de tonique** qui ne bouge pas. Le
Marais est le même ; l'animal, non.

**Ce qui lui appartient :** la **noblesse**. La section A est en blanches, sans
une seule croche à la mélodie — la seule des douze pièces à s'en priver
entièrement : l'animal blanc est couché au centre de la clairière. Puis vient
le défi, et la section B passe au **rythme pointé**, la même mélodie redressée,
qui monte jusqu'au sol aigu de la mesure 19. La reprise retrouve les blanches :
la Licorne se recouche, ou s'en va (page 265, « l'endroit est désert
maintenant ; le silence pèse »).

## Les six voix, mesurées

`python3 ../../verifier.py clairieres/23-licorne/licorne.mid --bpm 138`

| voix | côté | rôle | registre | notes | occupation |
| ---: | :---: | --- | --- | ---: | ---: |
| 0 | **gauche** | mélodie, blanches puis pointé | G♯4..G6 | 58 | 97 % |
| 1 | gauche | médiane (contre-chant) | G3..G♯4 | 58 | 96 % |
| 2 | **gauche** | basse | G2..A♯3 | 72 | 96 % |
| 3 | **droite** | arpège de croches | A♯3..C5 | 131 | 92 % |
| 4 | droite | médiane (accords tenus) | G3..G♯4 | 75 | 95 % |
| 5 | **droite** | bourdon de fa (la tonique) | F2 | 6 | 100 % |

## Refabriquer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/23-licorne
python3 licorne.py
python3 ../../../midi_to_mb.py licorne.mid LICORNE.MB.BIN \
    --bpm 138 --max 2304 --wav LICORNE.wav
```
