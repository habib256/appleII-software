# Clairière 21 — Bassin de cristal

**`CRISTAL.MB.BIN` — 1 982 octets, 41,5 s, boucle.**

## La clairière

| | |
| --- | --- |
| `hub` | **031** |
| Pages | 031 (le bassin), 077 (boire, `E ENDURANCE +3`), 394 (observer, le Lézard) |
| Case | (5,4) |
| Zone de référence | `sud` (`MARAISUD.MB`) |
| Sorties | O → 047 — **cul-de-sac** |
| Arbitrage | 394 rattaché à cette clairière, comme dans `../propositions/` (`CARTOGRAPHIE.md:810-820`) |

« Au centre, un bassin luit d'une eau pure comme du cristal. Une petite plage de
sable fin borde l'un des côtés du bassin. Aucun autre chemin ne permet de
sortir. » Page 394 : « Un gros Lézard vient boire à l'eau du bassin, puis s'en
retourne d'une démarche chaloupée. »

## La pièce

| | |
| --- | --- |
| Titre | **Le Bassin de Cristal** |
| Source | composition originale, `cristal.py` |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | limpide : la seule eau propre du Marais |
| Mode | **do dorien** (do ré mi♭ fa sol **la** si♭) |
| Tempo | **152** à la noire |
| Forme | intro (4) — A (8) l'eau pure — B (8) le Lézard — A' (6) l'éclat |
| Durée | 26 mesures à 4/4 = **41,5 s** |
| Taille | **1 982 octets** — la plus grosse des douze (tampon de zone : 2 304, marge 322) |
| Notes | 483 écrites, **0 abandonnée** |

**Ce qu'elle garde de la zone `sud` :** le **bourdon de tonique immobile** et la
marche modale large.

**Ce qui lui appartient :** la **sixte majeure** — le la naturel, porté par
l'accord de fa, qui revient à chaque phrase. C'est elle qui sépare une eau
croupie d'« une eau pure comme du cristal » : la même famille modale que la
zone, éclairée d'un seul degré. Deux procédés en propre :

- **l'éclat** (mes. 21-26) : l'arpège passe seul en **doubles croches** tandis
  que les cinq autres voix gardent leurs valeurs. Rien ne s'accélère, la lumière
  seule change — c'est le bassin qui prend le jour ;
- **le Lézard** (section B, page 394) : la mélodie se pose en blanches et
  l'harmonie descend lentement de ré mineur à do, la démarche chaloupée, puis
  il s'en retourne et la pièce se rouvre.

## Les six voix, mesurées

`python3 ../../verifier.py clairieres/21-cristal/cristal.mid --bpm 152`

| voix | côté | rôle | registre | notes | occupation |
| ---: | :---: | --- | --- | ---: | ---: |
| 0 | **gauche** | mélodie | A♯4..A6 | 64 | 96 % |
| 1 | gauche | médiane (contre-chant) | G3..A4 | 91 | 95 % |
| 2 | **gauche** | basse | G2..A♯3 | 78 | 96 % |
| 3 | **droite** | arpège, doubles croches à la reprise | G3..C5 | 137 | 92 % |
| 4 | droite | médiane (accords tenus) | F3..G4 | 106 | 94 % |
| 5 | **droite** | bourdon de do (la tonique) | C2 | 7 | 100 % |

## Refabriquer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/21-cristal
python3 cristal.py
python3 ../../../midi_to_mb.py cristal.mid CRISTAL.MB.BIN \
    --bpm 152 --max 2304 --wav CRISTAL.wav
```
