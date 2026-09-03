# Clairière 7 — Le Géant (`hub` 161, case 4,1)

**`GEANT.MB.BIN` — 1 260 octets, 43,6 s, boucle.**

## Les pages

| Page | Titre | Ce qui s'y passe |
| ---: | --- | --- |
| 275 | Le Géant | l'empreinte de cinquante centimètres, la massue à pointes, « IL EST INTERDIT DE PASSER ! » |
| 342 | Retour au Géant | l'avez-vous tué ? |
| 161 | Carrefour après le Géant | trois directions |
| 103 | Le Géant | les renseignements : Courbensaule est loin à l'ouest |
| 244 | Le conseil du Géant | le buisson au nord, « prenez garde aux Loups ! » |

## La pièce

| | |
| --- | --- |
| Titre | **Il Est Interdit de Passer** |
| Source | composition originale, `geant.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | énorme, furieux, mais pas maléfique — l'Anneau de Cuivre reste froid. On n'a pas peur de lui, on ne passe pas |
| Mode | **do mineur éolien** (do ré mi♭ fa sol la♭ si♭) |
| Tempo | **132** à la noire — le plus lent des douze |
| Forme | intro (4) — A (8) — B (6) — A' (6) |
| Durée | 24 mesures à 4/4 = **43,6 s** |
| Taille | **1 260 octets** — la plus petite des douze, marge 1 044 |
| Notes | 333 écrites, **0 abandonnée** |

## Ce qui la relie à `nord`, et ce qui l'en sépare

L'ostinato de la zone court en croches. Celui-ci marche en **noires** : quatre
pas par mesure, **do - sol - mi♭ - sol**, l'empreinte de cinquante centimètres
de la page 275. Il ne change pas une note du début à la fin, comme celui de la
zone, mais il occupe deux fois moins d'espace — et c'est exactement ce qui fait
la taille d'un géant : un pas qui prend le temps d'un pas.

Il ne double en croches que dans le **B**, mesures 13 à 18, quand la massue
tourne, et il retombe en noires pour le A'. C'est tout le crescendo du morceau,
et il ne coûte rien : le lecteur MB1 n'a pas de volume par note, on ne peut
serrer que la densité. La zone `danger` utilise le même moyen ; ici il est
appliqué à un ostinato de `nord`.

La basse suit : la fondamentale une **blanche**, puis deux appuis. 72 notes
contre 112 dans la zone. Le morceau entier est plus vide que tous les autres, et
c'est le seul dont ce soit le sujet.

Le tempo est le plus lent du lot mais reste à **132** : quatre noires à 132
restent une marche, pas un adagio — la consigne du dossier est de ne jamais
descendre sous 125.

## Les six voix, mesurées

`python3 ../../verifier.py geant.mid --bpm 132`

| voix | côté | ce qui s'y trouve | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | la mélodie, seule | B♭4..B♭6 | 63 |
| 1 | gauche | le contre-chant | G3..G4 | 53 |
| 2 | **gauche** | la basse pesante, seule | F2..A♭3 | 72 |
| 3 | **droite** | **les pas**, et la massue au B | C4..G4 | 85 |
| 4 | droite | les accords tenus | G3..G4 | 54 |
| 5 | **droite** | le bourdon de do, la note la plus grave de la table | C2 | 6 |

Les deux voix médianes, 1 à gauche et 4 à droite, partagent la même octave et
s'échangent parfois : c'est audible comme une largeur, pas comme un défaut
(`../../INDEX.md § 3`).

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/07-geant
python3 geant.py
python3 ../../../midi_to_mb.py geant.mid GEANT.MB.BIN \
    --bpm 132 --max 2304 --wav GEANT.wav
```
