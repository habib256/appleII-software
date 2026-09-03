# Clairière 34 — Pierres et tronc creux (`hub` 390)

**`TRONC.MB.BIN` — 1 888 octets, 45,3 s, boucle.**

## Ce que la clairière raconte

| Page | Ce qu'on y lit |
| ---: | --- |
| 105 | « le sol y est ferme ; vous pouvez y pénétrer d'un pas assuré » — des pierres plates de grande taille, un tronc creux massif, deux chemins |
| 330 | le retour : « le sentier est calme, mais vous savez que le tronc a déjà abrité autre chose que des ossements » |
| 390 | les trois sentiers marécageux, tous peu sûrs |

Zone de référence : **`sud`** (`MARAISUD.MB`, *Sentiers Verts*).

## La pièce

| | |
| --- | --- |
| Titre | **Pierres Plates** |
| Source | composition originale, `tronc.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | la seule clairière sûre des onze — et elle le dit par le vide, pas par la joie |
| Mode | **do éolien** (do ré mi♭ fa sol la♭ si♭) |
| Tempo | **150** à la noire |
| Forme | intro (4) — A (8) — B (8) — A' (8) |
| Durée | 28 mesures à 4/4 = **45,3 s** |
| Taille | **1 888 octets** (tampon de zone : 2 304) |
| Notes | 473 écrites, **0 abandonnée** |

Ce qui la rattache à `sud` : la marche **i-VI-III-VII** (Cm-A♭-E♭-B♭) sur un
bourdon de do immobile. Deux choses n'appartiennent qu'à elle.

**Le tronc est creux.** L'arpège ne joue que des **quintes à vide** — la liste
`CREUX` du script remplace chaque accord par sa quinte nue, fondamentale-quinte-
octave. La seule voix qui possède encore une tierce, et donc qui dise le mode,
est le lit d'accords tenus. L'harmonie sonne de l'extérieur ; il n'y a rien
dedans.

**Le coup sur le bois.** La mélodie frappe deux noires sur la même hauteur aux
mesures 5, 6, 17, 18 et 21 : on frappe le tronc pour savoir s'il est habité.
C'est le seul motif de note répétée des onze clairières.

## Les six voix (mesurées par `verifier.py`)

| voix | côté | rôle | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | mélodie, et le coup sur le bois | C5..G6 | 74 |
| 1 | gauche | médiane (contre-chant) | A♭3..E♭5 | 84 |
| 2 | **gauche** | basse | D2..F3 | 84 |
| 3 | **droite** | arpège de quintes à vide, sans aucune tierce | C4..A♭5 | 140 |
| 4 | droite | médiane (accords tenus, la seule tierce) | G3..C5 | 84 |
| 5 | **droite** | bourdon de do | C2 | 7 |

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/34-tronc
python3 tronc.py
python3 ../../../midi_to_mb.py tronc.mid TRONC.MB.BIN \
    --bpm 150 --max 2304 --wav TRONC.wav
```
