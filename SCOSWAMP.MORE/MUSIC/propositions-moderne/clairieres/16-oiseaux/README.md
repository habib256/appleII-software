# Clairière 16 — Le Perroquet et la Maîtresse des Oiseaux

**`OISEAUX.MB.BIN` — 1 900 octets, 40,5 s, boucle.**

## La clairière

| | |
| --- | --- |
| `hub` | **304** |
| Pages | 304 (le Perroquet), 149 (la clairière aux oiseaux), 217 (retour forcé) |
| Case | (0,4) |
| Zone de référence | `sud` (`MARAISUD.MB`) |
| Sorties | aucune orientée — cul-de-sac tropical, on ressort par 217 → 250 |

« Le Marais change d'aspect. Il devient moins lugubre et ressemble de plus en
plus à une jungle tropicale. Des oiseaux aux couleurs éclatantes volent parmi
les arbres. » Un gros Perroquet rouge et jaune parle. Page 149 : la Maîtresse
n'est pas là, il ne reste que des plumes éparses et « un silence léger ».

## La pièce

| | |
| --- | --- |
| Titre | **La Maîtresse des Oiseaux** |
| Source | composition originale, `oiseaux.py` |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | la poche tropicale : la seule clairière claire du Marais sud |
| Mode | **mi dorien** (mi fa♯ sol la si **do♯** ré) |
| Tempo | **168** à la noire |
| Forme | intro (4) — A (8) les oiseaux — B (8) le silence léger — A' (8) |
| Durée | 28 mesures à 4/4 = **40,5 s** |
| Taille | **1 900 octets** (tampon de zone : 2 304) |
| Notes | 477 écrites, **0 abandonnée** |

**Ce qu'elle garde de la zone `sud` :** le **bourdon de tonique immobile** —
mi, d'un bout à l'autre — et la marche modale large qui fait lire chaque accord
comme une couleur du même lieu.

**Ce qui lui appartient :** le mode est dorien et non éolien, et ce seul **do♯**
éclaircit toute la zone d'un degré, exactement comme le texte éclaircit le
Marais. Le procédé propre à la clairière est l'**arpège en sauts** : au lieu de
monter son accord degré par degré, il bondit de la fondamentale à la quinte et
retombe — des oiseaux, pas de l'eau. La mélodie répond en croches brèves
accolées (mesures 5, 6, 8, 10, 21-24), le babil du Perroquet. La section B est
la page 149 : tout s'allonge en blanches, l'arpège seul continue, le tempo ne
change pas — c'est la seule façon de faire du silence avec six ondes carrées.

## Les six voix, mesurées

`python3 ../../verifier.py clairieres/16-oiseaux/oiseaux.mid --bpm 168`

| voix | côté | rôle | registre | notes | occupation |
| ---: | :---: | --- | --- | ---: | ---: |
| 0 | **gauche** | mélodie, le babil | A4..B6 | 78 | 96 % |
| 1 | gauche | médiane (contre-chant) | G3..A4 | 79 | 96 % |
| 2 | **gauche** | basse | A2..B3 | 84 | 95 % |
| 3 | **droite** | arpège en sauts de quinte | G3..B4 | 136 | 92 % |
| 4 | droite | médiane (accords tenus) | F♯3..F♯4 | 93 | 95 % |
| 5 | **droite** | bourdon de mi (la tonique) | E2 | 7 | 100 % |

## Refabriquer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/16-oiseaux
python3 oiseaux.py
python3 ../../../midi_to_mb.py oiseaux.mid OISEAUX.MB.BIN \
    --bpm 168 --max 2304 --wav OISEAUX.wav
```
