# Clairière 8 — Clairière aux brigands (`hub` 019, case 0,2)

**`BRIGANDS.MB.BIN` — 1 928 octets, 38,2 s, boucle.**

## Les pages

| Page | Titre | Ce qui s'y passe |
| ---: | --- | --- |
| 065 | Clairière aux brigands | le grand champignon, les voix, cinq hommes épiés derrière un arbre |
| 343 | Retour aux Brigands | amis, ou fuis, trompés, tués |
| 019 | Deux sentiers | le large chemin du nord, l'étroit sentier de l'est |

## La pièce

| | |
| --- | --- |
| Titre | **Cinq Voix derrière l'Arbre** |
| Source | composition originale, `brigands.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | effronté, pas méchant : « l'Anneau de Cuivre reste froid, ils ne paraissent pas malfaisants. Il serait cependant stupide de prendre des risques inutiles » |
| Mode | **ré mineur éolien** (ré mi fa sol la si♭ do) |
| Tempo | **176** à la noire |
| Forme | intro (4) — A (8) — B (8) — A' (8) |
| Durée | 28 mesures à 4/4 = **38,2 s** |
| Taille | **1 928 octets** (marge 376) |
| Notes | 466 écrites, **0 abandonnée** |

## Ce qui la relie à `nord`, et ce qui l'en sépare

L'ostinato de la zone a quatre notes ; celui-ci en a **cinq** — un homme par
note, ré - fa - la - sol - mi, quatre croches et une noire. Il fait donc trois
temps dans une mesure qui en compte quatre : la figure décale d'un temps à
chaque mesure et ne retombe à sa place que toutes les quatre mesures. C'est ce
qu'on entend depuis derrière l'arbre de la page 065, cinq voix qui parlent en
même temps sans jamais dire la même chose au même moment.

Aux quatre dernières mesures la noire finale s'allonge à la blanche : la cellule
fait quatre temps, tout retombe ensemble, **et les brigands se taisent**. C'est
le moment de la page 065 où l'on choisit — les saluer, les charger, ou repartir.

L'harmonie est le tétracorde descendant **Rém - Do - Si♭ - Lam**, la marche de
tous les brigands de la musique modale, et la basse balance en **croche pointée
- croche** comme au village : ces gens-là ne sont pas des monstres, ce sont des
voyous.

## Les six voix, mesurées

`python3 ../../verifier.py brigands.mid --bpm 176`

| voix | côté | ce qui s'y trouve | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | la mélodie, seule | D5..B♭6 | 83 |
| 1 | gauche | le contre-chant, et les notes basses de l'ostinato | A3..A4 | 90 |
| 2 | **gauche** | la basse balancée, seule | E2..G3 | 112 |
| 3 | **droite** | **les cinq voix** | D4..A4 | 136 |
| 4 | droite | les accords tenus, et le reste de l'ostinato | F3..A4 | 38 |
| 5 | **droite** | le bourdon de ré | D2 | 7 |

L'ostinato étant détaché (`gap=0.08`, occupation 84 %), quelques-unes de ses
notes basculent d'une voix médiane à l'autre selon leur hauteur du moment ;
elles restent toutes du côté droit.

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/08-brigands
python3 brigands.py
python3 ../../../midi_to_mb.py brigands.mid BRIGANDS.MB.BIN \
    --bpm 176 --max 2304 --wav BRIGANDS.wav
```
