# Clairière 11 — Le nid de l'Aigle (`hub` 202, case 3,2)

**`AIGLE.MB.BIN` — 1 437 octets, 44,2 s, boucle.**

## Les pages

| Page | Titre | Ce qui s'y passe |
| ---: | --- | --- |
| 350 | Le nid de l'Aigle | l'arbre immense dans un sol dur et nu, le nid gigantesque, l'AIGLE qui vous observe |
| 331 | Le nid de l'Aigle | de retour : rien que le vieil arbre et le nid |
| 025 | L'aigle s'envole | il crie, tourne en cercle, et s'éloigne |
| 112 | Le grand nid | grimper pour l'examiner, ou repartir |
| 202 | Trois directions | sud, est, ouest |

## La pièce

| | |
| --- | --- |
| Titre | **Le Grand Nid** |
| Source | composition originale, `aigle.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | de la hauteur. Pas une menace : une surveillance, très haut, qui tourne sans se presser |
| Mode | **fa♯ mineur éolien** (fa♯ sol♯ la si do♯ ré mi) |
| Tempo | **152** à la noire |
| Forme | intro (4) — A (8) — B (8) — A' (8) |
| Durée | 28 mesures à 4/4 = **44,2 s** |
| Taille | **1 437 octets** (marge 867) |
| Notes | 360 écrites, **0 abandonnée** |

## Ce qui la relie à `nord`, et ce qui l'en sépare

L'ostinato de la zone bat des croches égales ; celui-ci a un **rythme**, et
c'est tout le sujet : **noire - croche - blanche - croche**, fa♯ - la - do♯ - la.
Un coup d'aile, un second, puis le vol plané sur la note du haut pendant deux
temps, et l'on retombe. La cellule ne change jamais de notes ni de place, comme
celle de `MARAISNO.MB` ; elle ne bat que **quatre** fois par mesure au lieu de
huit, et c'est ce qui fait la différence entre courir et planer.

La cellule est posée très haut — jusqu'au do♯5 — et la mélodie doit donc chanter
au-dessus d'elle, en blanches. La basse ne marche pas non plus : elle tient la
fondamentale une blanche, puis se laisse tomber d'une quinte. Et le bourdon est
sur **do♯ grave**, presque au fond de la table des notes de la carte. Entre le
bourdon et la mélodie il y a plus de trois octaves et demie : c'est la hauteur
de l'arbre de la page 350.

C'est la pièce la plus **aérée** des douze — 360 notes en 44 secondes, contre 514
pour `LOUPS` en 40.

## Les six voix, mesurées

`python3 ../../verifier.py aigle.mid --bpm 152`

| voix | côté | ce qui s'y trouve | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | la mélodie, seule | E5..A6 | 73 |
| 1 | gauche | le contre-chant, seul | G♯3..F♯4 | 56 |
| 2 | **gauche** | la basse, seule | F♯2..A3 | 84 |
| 3 | **droite** | **le vol** | F♯4..C♯5 | 112 |
| 4 | droite | les accords tenus, seuls | F♯3..E4 | 28 |
| 5 | **droite** | le bourdon de do♯ | C♯2 | 7 |

Séparation parfaite : les six parties écrites tombent chacune dans une voix et
une seule, du début à la fin. C'est la mieux rangée des douze, et c'est l'effet
recherché — un ciel dégagé.

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/11-aigle
python3 aigle.py
python3 ../../../midi_to_mb.py aigle.mid AIGLE.MB.BIN \
    --bpm 152 --max 2304 --wav AIGLE.wav
```
