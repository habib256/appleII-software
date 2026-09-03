# Clairière 15 — Le pont sur la rivière Croupie

**`PONT.MB.BIN` — 1 838 octets, 42,1 s, boucle.**

## La clairière

| | |
| --- | --- |
| `hub` | **045** |
| Pages | 138 (l'arrivée), 045 (le pont suspect), 101 (le vieux pont) |
| Case | (3,3) |
| Zone de référence | `riviere` (`RIVIERE.MB`) |
| Sorties | N → 331, S → 303 |

**Le seul passage nord ⇄ sud du Marais** (`CARTOGRAPHIE.md` § 1) : douze
clairières d'un côté, vingt-trois de l'autre, et ce pont entre les deux. « Un
pont l'enjambe, apparemment désert. » La page 045 est le refus : « ce pont vous
paraît trop simple ; il doit sans doute dissimuler un piège quelconque. »

## La pièce

| | |
| --- | --- |
| Titre | **Le Seul Passage** |
| Source | composition originale, `pont.py` |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | une marche, et une hésitation au milieu |
| Mode | **si bémol dorien** (si♭ do ré♭ mi♭ fa **sol** la♭) |
| Tempo | **150** à la noire |
| Forme | intro (4) — A (8) la traversée — B (8) le soupçon — A' (6) à l'octave |
| Durée | 26 mesures à 4/4 = **42,1 s** |
| Taille | **1 838 octets** (tampon de zone : 2 304) |
| Notes | 467 écrites, **0 abandonnée** |

**Ce qu'elle garde de la zone `riviere` :** le mode dorien, l'arpège de croches,
le **bourdon sur la quinte** — fa, pas si♭.

**Ce qui lui appartient :** la zone regarde l'eau, cette pièce la traverse.
D'où la basse en **quatre noires marchées par mesure**, du début à la fin — la
seule des trois pièces `riviere` à marcher. La section B est la page 045 : la
mélodie s'y resserre dans une quinte, répète ses notes (mesure 13), tourne
autour de ré♭ et ne conclut pas. La reprise repart une octave plus haut : on a
traversé.

## Les six voix, mesurées

`python3 ../../verifier.py clairieres/15-pont/pont.mid --bpm 150`

| voix | côté | rôle | registre | notes | occupation |
| ---: | :---: | --- | --- | ---: | ---: |
| 0 | **gauche** | mélodie | G♯4..G6 | 70 | 97 % |
| 1 | gauche | médiane (contre-chant) | G♯3..A♯4 | 81 | 96 % |
| 2 | **gauche** | basse, quatre noires marchées | G2..A♯3 | 99 | 95 % |
| 3 | **droite** | arpège de croches | G♯3..C5 | 98 | 95 % |
| 4 | droite | médiane (accords tenus) | G3..G♯4 | 112 | 95 % |
| 5 | **droite** | bourdon de fa (la quinte) | F2 | 7 | 100 % |

## Refabriquer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/15-pont
python3 pont.py
python3 ../../../midi_to_mb.py pont.mid PONT.MB.BIN \
    --bpm 150 --max 2304 --wav PONT.wav
```
