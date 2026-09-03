# Clairière 22 — Les Fleurs d'Angoisse

**`ANGOISSE.MB.BIN` — 1 589 octets, 40,5 s, boucle.**

## La clairière

| | |
| --- | --- |
| `hub` | **367** |
| Pages | 204 (les Fleurs), 250 (la clairière des Fleurs), 367 (deux chemins) |
| Case | (0,5) |
| Zone de référence | `danger` (`DANGER.MB`) |
| Sorties | N → 304 (les Oiseaux, sens unique), E → 265 (la Licorne) |
| Effet | `E HABILETE -1`, et −1 de plus si l'on fuit (269) |

« Le sentier s'élargit, et des fleurs colorées bordent le chemin. Mais soudain,
un frisson vous parcourt : quelque chose ne va pas. Votre Anneau de Cuivre
devient brûlant. Autour de vous, ces fleurs semblent trop belles... Leur pollen
inspire la terreur et vous sentez vos mains trembler. »

## La pièce

| | |
| --- | --- |
| Titre | **Les Fleurs d'Angoisse** |
| Source | composition originale, `angoisse.py` |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | trop beau, puis la main qui tremble |
| Mode | **mi phrygien** (mi **fa** sol la si do ré) |
| Tempo | **144** à la noire |
| Forme | intro (4) — A (8) les fleurs — B (8) le tremblement — A' (4) |
| Durée | 24 mesures à 4/4 = **40,5 s** |
| Taille | **1 589 octets** (tampon de zone : 2 304) |
| Notes | 402 écrites, **0 abandonnée** |

**Ce qu'elle garde de la zone `danger` :** le mode **phrygien** — fa contre mi,
le demi-ton posé juste au-dessus de la tonique — le **bourdon de tonique** qui
ne bouge pas, et le crescendo obtenu **par la densité** et non par le volume,
exactement comme `DANGER.MB` : arpège en noires pendant l'intro puis en
croches, basse en blanches jusqu'à la mesure 12 puis en noires. Le lecteur n'a
pas de volume par note ; le morceau se resserre au lieu de monter.

**Ce qui lui appartient :** le contraste. La section A est en tierces douces, la
ligne la plus consonante des douze pièces — les fleurs sont belles. Puis
l'Anneau devient brûlant, et la section B introduit le **tremblement** :
fa-mi-fa en doubles croches, quatre fois (mes. 13, 14, 17, 19), la main qui
tremble et le point d'HABILETÉ perdu. La dernière mesure ne garde que le motto,
fa puis mi, et rien d'autre.

## Les six voix, mesurées

`python3 ../../verifier.py clairieres/22-angoisse/angoisse.mid --bpm 144`

| voix | côté | rôle | registre | notes | occupation |
| ---: | :---: | --- | --- | ---: | ---: |
| 0 | **gauche** | mélodie, tierces puis tremblement | B4..F6 | 76 | 95 % |
| 1 | gauche | médiane (contre-chant) | G3..A4 | 69 | 95 % |
| 2 | **gauche** | basse, blanches puis noires | G2..A3 | 70 | 96 % |
| 3 | **droite** | arpège, noires puis croches | B3..C5 | 120 | 92 % |
| 4 | droite | médiane (accords tenus) | F3..E4 | 61 | 96 % |
| 5 | **droite** | bourdon de mi (la tonique) | E2 | 6 | 100 % |

## Refabriquer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/22-angoisse
python3 angoisse.py
python3 ../../../midi_to_mb.py angoisse.mid ANGOISSE.MB.BIN \
    --bpm 144 --max 2304 --wav ANGOISSE.wav
```
