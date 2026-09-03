# Clairière 24 — La clairière des combats

**`ARENE.MB.BIN` — 1 975 octets, 42,5 s, boucle.**

## La clairière

| | |
| --- | --- |
| `hub` | **227** |
| Pages | 010 (la clairière des combats), 142 (silence après la bataille), 227 (le choix des chemins) |
| Case | (2,5) |
| Zone de référence | `sud` (`MARAISUD.MB`) |
| Sorties | N → 066 (pique-nique), E → 388, O → 320 (la Licorne) |
| Contenu | traces d'un combat, cadavre → **Aimant d'Or** (`059 G AI`, maudit : `063 GX AI`) |

« L'endroit porte les marques récentes d'un combat : le sol est foulé, l'herbe
humide tachée de sang, et deux flèches sont encore plantées dans un arbre un
peu plus loin. Vous pouvez fouiller la clairière pour découvrir indices ou
butin, mais rester risque d'attirer l'attention d'ennemis cachés. » Page 227 :
« Le silence pèse, seulement rompu par le bourdonnement des mouches. »

## La pièce

| | |
| --- | --- |
| Titre | **Ce qui Reste du Combat** |
| Source | composition originale, `arene.py` |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | martial, mais après coup : on ne se bat pas, on relève des traces |
| Mode | **mi éolien** (mi fa♯ sol la si do ré) |
| Tempo | **160** à la noire |
| Forme | intro (4) — A (8) les traces — B (8) la fouille — A' (8) |
| Durée | 28 mesures à 4/4 = **42,5 s** |
| Taille | **1 975 octets** (tampon de zone : 2 304) |
| Notes | 502 écrites, **0 abandonnée** |

**Ce qu'elle garde de la zone `sud` :** le **bourdon de tonique immobile** et la
marche i-VI-III-VII (Em-C-G-D), celle de `MARAISUD.MB`.

**Ce qui lui appartient :** le **rythme pointé**. Le long-bref du premier temps
revient à chaque mesure de A et de A', et c'est tout ce qui sépare cette pièce
d'un thème de voyage : on n'est pas dans un combat, la page 010 ne montre que
ses traces. La section B est la fouille : la mélodie quitte le pointé, monte par
degrés jusqu'au sol aigu de la mesure 17 et redescend sur **si mineur** — le
seul accord mineur non diatonique du tour, l'attention des ennemis cachés que le
texte promet à qui s'attarde. La reprise remet le pointé et conclut sur la
tonique : on est parti. La basse martèle quatre noires d'un bout à l'autre — la
marche de ceux qui sont passés par là.

## Les six voix, mesurées

`python3 ../../verifier.py clairieres/24-arene/arene.mid --bpm 160`

| voix | côté | rôle | registre | notes | occupation |
| ---: | :---: | --- | --- | ---: | ---: |
| 0 | **gauche** | mélodie, rythme pointé | B4..A6 | 75 | 96 % |
| 1 | gauche | médiane (contre-chant) | G3..A4 | 100 | 94 % |
| 2 | **gauche** | basse, quatre noires martelées | G2..B3 | 111 | 94 % |
| 3 | **droite** | arpège de croches | B3..B4 | 117 | 93 % |
| 4 | droite | médiane (accords tenus) | F♯3..G4 | 92 | 95 % |
| 5 | **droite** | bourdon de mi (la tonique) | E2 | 7 | 100 % |

## Refabriquer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/24-arene
python3 arene.py
python3 ../../../midi_to_mb.py arene.mid ARENE.MB.BIN \
    --bpm 160 --max 2304 --wav ARENE.wav
```
