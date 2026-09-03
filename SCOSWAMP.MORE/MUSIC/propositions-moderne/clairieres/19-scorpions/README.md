# Clairière 19 — La clairière des scorpions

**`SCORPIONS.MB.BIN` — 1 847 octets, 32,5 s, boucle.**

## La clairière

| | |
| --- | --- |
| `hub` | **319** |
| Pages | 118 (l'embuscade), 303 (le retour), 319 (choisir une direction) |
| Case | (3,4) |
| Zone de référence | `danger` (`DANGER.MB`) |
| Sorties | N → 138 (le pont), E → 047, O → 066 |
| Contenu | nuée de petits SCORPIONS ; `CL 070 182` — jamais de choix à prendre |

« Votre Anneau de Cuivre vous picote au doigt. En baissant les yeux, vous voyez
des dizaines de petits scorpions accourir vers vous. Tentez votre Chance. » La
page 319 s'appelle « Vous vous hâtez de choisir une direction ».

## La pièce

| | |
| --- | --- |
| Titre | **La Nuée** |
| Source | composition originale, `scorpions.py` |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | ça grouille et ça court — la plus rapide et la plus courte des douze |
| Mode | **ré phrygien** (ré **mi♭** fa sol la si♭ do) |
| Tempo | **180** à la noire |
| Forme | intro (4) — A (8) — B (8) l'assaut — A' (4) |
| Durée | 24 mesures à 4/4 = **32,5 s** |
| Taille | **1 847 octets** (tampon de zone : 2 304) |
| Notes | 472 écrites, **0 abandonnée** |

**Ce qu'elle garde de la zone `danger` :** le mode **phrygien**, donc le
demi-ton posé juste au-dessus de la tonique — mi♭ contre ré — et le **bourdon
de tonique** immobile. Le frottement est le procédé de la zone, et il est ici
la piqûre de l'Anneau.

**Ce qui lui appartient :** la vitesse, et le **grouillement**. La mélodie
attaque presque chaque mesure par deux ou quatre **doubles croches** avant de se
poser : ce sont les seules doubles croches d'attaque des douze pièces, elles ne
durent qu'un temps chacune, et elles suffisent à faire courir tout le morceau.
La basse marche en quatre noires dès la première mesure — rien ne se met en
place, contrairement à `DANGER.MB` qui prend huit mesures pour se resserrer :
ici, on n'a pas le temps. La dernière mesure lâche la nuée et ne garde que le
frottement mi♭-ré, seul, tenu.

## Les six voix, mesurées

`python3 ../../verifier.py clairieres/19-scorpions/scorpions.mid --bpm 180`

| voix | côté | rôle | registre | notes | occupation |
| ---: | :---: | --- | --- | ---: | ---: |
| 0 | **gauche** | mélodie, les doubles croches | F4..G6 | 109 | 93 % |
| 1 | gauche | médiane (contre-chant) | G3..A4 | 62 | 96 % |
| 2 | **gauche** | basse, quatre noires | G2..A♯3 | 93 | 94 % |
| 3 | **droite** | arpège de croches | G3..C5 | 140 | 91 % |
| 4 | droite | médiane (accords tenus) | F3..G4 | 62 | 96 % |
| 5 | **droite** | bourdon de ré (la tonique) | D2 | 6 | 100 % |

## Refabriquer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/19-scorpions
python3 scorpions.py
python3 ../../../midi_to_mb.py scorpions.mid SCORPIONS.MB.BIN \
    --bpm 180 --max 2304 --wav SCORPIONS.wav
```
