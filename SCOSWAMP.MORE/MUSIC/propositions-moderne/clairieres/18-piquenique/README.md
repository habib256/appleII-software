# Clairière 18 — Le pique-nique suspect

**`PIQUENIQUE.MB.BIN` — 1 548 octets, 41,4 s, boucle.**

## La clairière

| | |
| --- | --- |
| `hub` | **179** |
| Pages | 066 (le pique-nique), 192 (retour chez le Voleur), 179 (le carrefour) |
| Case | (2,4) |
| Zone de référence | `sud` (`MARAISUD.MB`) |
| Sorties | N → 183 (falaise), S → 010, E → 118 (scorpions) |
| Contenu | VOLEUR (10/9 en 267) ; **Cape Rouge** (`386 G CAPE`) |

« Un petit homme à l'air joyeux est assis par terre, le dos appuyé contre le
tronc d'un arbre. Il mange du fromage, un panier à pique-nique ouvert à côté de
lui. » Puis : « L'Anneau de Cuivre diffuse une chaleur autour de votre doigt qui
vous avertit : ne vous fiez pas. Bientôt, vous comprenez qu'il s'agit d'un
VOLEUR. »

## La pièce

| | |
| --- | --- |
| Titre | **Le Repas du Voleur** |
| Source | composition originale, `piquenique.py` |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | une valse aimable qui tourne — la seule pièce à trois temps |
| Mode | **fa dorien** (fa sol la♭ si♭ do **ré** mi♭) |
| Tempo | **176** à la noire |
| Forme | intro (4) — A (12) le repas — B (12) l'Anneau chauffe — A' (12) la reprise empoisonnée |
| Durée | 40 mesures à **3/4** = **41,4 s** |
| Taille | **1 548 octets** (tampon de zone : 2 304) |
| Notes | 429 écrites, **0 abandonnée** |

**Ce qu'elle garde de la zone `sud` :** le **bourdon de tonique immobile** (fa)
et la marche modale large.

**Ce qui lui appartient :** le **3/4**, seule des trente-cinq clairières à ne
pas être à quatre temps — il faut une valse pour un homme qui déjeune adossé à
un chêne. La gaieté est fausse, et le mode le dit : le fa dorien a un **si
bémol majeur** au quatrième degré, c'est la couleur riante de la pièce ; mais
la section B fait entrer un **sol bémol majeur**, le second degré abaissé, qui
n'appartient pas au mode. C'est le demi-ton phrygien de la zone `danger`, cité
à découvert : l'Anneau chauffe. Le sol bémol revient trois fois, dont une dans
la reprise — la valse ne s'en remet pas.

## Les six voix, mesurées

`python3 ../../verifier.py clairieres/18-piquenique/piquenique.mid --bpm 176`

| voix | côté | rôle | registre | notes | occupation |
| ---: | :---: | --- | --- | ---: | ---: |
| 0 | **gauche** | mélodie de valse | A♯4..F6 | 99 | 95 % |
| 1 | gauche | médiane (contre-chant) | G3..G♯4 | 71 | 97 % |
| 2 | **gauche** | basse, blanche + noire | G2..A♯3 | 80 | 96 % |
| 3 | **droite** | arpège, une noire par temps | A♯3..C5 | 90 | 95 % |
| 4 | droite | médiane (accords tenus) | F♯3..F4 | 79 | 96 % |
| 5 | **droite** | bourdon de fa (la tonique) | F2 | 10 | 100 % |

## Refabriquer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/18-piquenique
python3 piquenique.py
python3 ../../../midi_to_mb.py piquenique.mid PIQUENIQUE.MB.BIN \
    --bpm 176 --max 2304 --wav PIQUENIQUE.wav
```
