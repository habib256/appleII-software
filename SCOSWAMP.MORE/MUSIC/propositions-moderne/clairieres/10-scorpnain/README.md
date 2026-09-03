# Clairière 10 — Scorpion et nain (`hub` 088, case 2,2)

**`SCORPNAIN.MB.BIN` — 1 866 octets, 38,2 s, boucle.**

## Les pages

| Page | Titre | Ce qui s'y passe |
| ---: | --- | --- |
| 014 | Scorpion et nain | les bruits de lutte derrière le tronc, le SCORPION GÉANT, le NAIN sans vie |
| 338 | Retour au Scorpion Géant | quelques ossements et une cuirasse |
| 088 | Quitter la clairière | la bifurcation, nord ou est |

## La pièce

| | |
| --- | --- |
| Titre | **Les Pinces et l'Os** |
| Source | composition originale, `scorpnain.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | deux choses à la fois : la bête qui se repaît, et l'homme qui ne bouge plus |
| Mode | **la mineur phrygien** (la **si♭** do ré mi fa sol) |
| Tempo | **176** à la noire, avec `SCORPNAIN` et `BRIGANDS` le plus vif des douze |
| Forme | intro (4) — A (8) — B (8) — A' (8) |
| Durée | 28 mesures à 4/4 = **38,2 s** |
| Taille | **1 866 octets** (marge 438) |
| Notes | 459 écrites, **0 abandonnée** |

## Ce qui la relie à `danger`, et ce qui l'en sépare

Même demi-ton phrygien, même bourdon immobile, même arpège en croches sur la
figure `(0, 1, 2, 1)` que `DANGER.MB`. Ce qui appartient à cette clairière-là,
c'est que la page 014 raconte **deux** choses, et que la pièce est donc en deux
matières :

- **A et A' — le Scorpion.** L'arpège court en croches *détachées* : chaque note
  ne dure que 0,42 temps au lieu de 0,5, et le silence entre deux est le
  claquement. La mélodie ouvre et ferme sur la seconde phrygienne **la - si♭ -
  la**, qui est la pince.
- **B — le Nain.** L'arpège retombe en **noires**, la basse en **blanches**, la
  mélodie tient des blanches et descend. C'est le seul endroit des douze
  clairières où la musique s'arrête de mordre. « Il vous semble peu probable que
  vos Pierres de Magie aient de l'effet ici. »

Le crescendo par la densité de la zone est donc utilisé **à l'envers** : au lieu
de se resserrer une fois pour toutes, la pièce se desserre au milieu et se
resserre à la reprise.

Le bourdon est sur **mi**, la quinte à vide de la ; le morceau ne se pose jamais
sur sa propre tonique grave.

## Les six voix, mesurées

`python3 ../../verifier.py scorpnain.mid --bpm 176`

| voix | côté | ce qui s'y trouve | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | la mélodie, seule | E5..B♭6 | 80 |
| 1 | gauche | le contre-chant | G3..A4 | 64 |
| 2 | **gauche** | la basse, seule | G2..B♭3 | 90 |
| 3 | **droite** | l'arpège, sa moitié haute | A3..D5 | 100 |
| 4 | droite | l'arpège, sa moitié basse, et les accords tenus | F3..F4 | 118 |
| 5 | **droite** | le bourdon de mi | E2 | 7 |

C'est la seule des douze où l'arpège se partage franchement entre les deux voix
médianes de droite : le détaché ouvre des trous où la répartition se rejoue.
Les 218 notes restent toutes du **même côté**, la puce 2 ; ce qui bouge est leur
place à l'intérieur d'elle, et cela s'entend comme une largeur.

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/10-scorpnain
python3 scorpnain.py
python3 ../../../midi_to_mb.py scorpnain.mid SCORPNAIN.MB.BIN \
    --bpm 176 --max 2304 --wav SCORPNAIN.wav
```
