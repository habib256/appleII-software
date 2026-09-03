# Clairière 17 — La brume fétide

**`BRUME.MB.BIN` — 1 408 octets, 41,7 s, boucle.**

## La clairière

| | |
| --- | --- |
| `hub` | **094** |
| Pages | 094 |
| Case | (1,4) |
| Zone de référence | `sud` (`MARAISUD.MB`) |
| Sorties | N → 295 (la Rivière Croupie), S → 320 (la Licorne) |
| Effet | `E ENDURANCE -2` — on la traverse toujours, on la paie toujours |

« Le sentier descend et des tourbillons de brume vous entourent. Une odeur
infecte emplit l'air et vous retenez votre souffle. Mais bientôt, force vous est
de respirer de nouveau. »

## La pièce

| | |
| --- | --- |
| Titre | **La Brume Fétide** |
| Source | composition originale, `brume.py` |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | la plus lourde des douze, et la plus lente autorisée |
| Mode | **do éolien** (do ré mi♭ fa sol la♭ si♭) |
| Tempo | **128** à la noire |
| Forme | intro (4) — A (6) la descente — B (6) l'odeur — A' (6) la brume se referme |
| Durée | 22 mesures à 4/4 = **41,7 s** |
| Taille | **1 408 octets** (tampon de zone : 2 304) |
| Notes | 345 écrites, **0 abandonnée** |

**Ce qu'elle garde de la zone `sud` :** le mode éolien et le **bourdon de
tonique immobile**, ici sur do et pris tout en bas du clavier.

**Ce qui lui appartient :** la **descente**. La page commence par « le sentier
descend », et la section A descend en effet, une mesure après l'autre —
do, si♭, la♭, sol, fa, do — sans jamais remonter. La section B est le moment où
l'on ne peut plus retenir son souffle : la mélodie frotte le la♭ contre le sol,
la même paire répétée, et l'air vicié coûte ses deux points. La basse ne fait
que deux blanches par mesure d'un bout à l'autre : c'est le seul endroit des
douze où l'on avance à peine.

## Les six voix, mesurées

`python3 ../../verifier.py clairieres/17-brume/brume.mid --bpm 128`

| voix | côté | rôle | registre | notes | occupation |
| ---: | :---: | --- | --- | ---: | ---: |
| 0 | **gauche** | mélodie, la descente | G♯4..F6 | 54 | 96 % |
| 1 | gauche | médiane (accords tenus) | G3..G4 | 87 | 94 % |
| 2 | **gauche** | basse, deux blanches | G2..A♯3 | 44 | 97 % |
| 3 | **droite** | arpège, les tourbillons | G3..C5 | 69 | 95 % |
| 4 | droite | médiane (contre-chant) | G3..G4 | 85 | 94 % |
| 5 | **droite** | bourdon de do (la tonique) | C2 | 6 | 100 % |

## Refabriquer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/17-brume
python3 brume.py
python3 ../../../midi_to_mb.py brume.mid BRUME.MB.BIN \
    --bpm 128 --max 2304 --wav BRUME.wav
```
