# Clairière 27 — Cul-de-sac de la Bête (`hub` 125)

**`BETE.MB.BIN` — 1 176 octets, 45,8 s, boucle.**

## Ce que la clairière raconte

| Page | Ce qu'on y lit |
| ---: | --- |
| 011 | « le rocher bouge : ce n'était pas de la pierre » — une BÊTE IMMONDE à six pattes griffues, sa respiration lourde fait vibrer le bois |
| 210 | le retour : le sol porte encore les traces du combat, un silence lourd |
| 299 | la Pierre de Terreur : la Bête se réfugie derrière les rochers en gémissant |
| 125 | les griffes coupées en souvenir — et aucun autre chemin pour sortir |
| 228 | les graines d'Arbres-Épées semées devant elle |
| 243 | la charogne et les insectes charognards |

Zone de référence : **`danger`** (`DANGER.MB`, *Ce qui Attend Sous l'Eau*).

## La pièce

| | |
| --- | --- |
| Titre | **Le Rocher qui Respire** |
| Source | composition originale, `bete.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | lourd, boiteux, sans issue : quelque chose de très grand se lève et il n'y a qu'un chemin, celui par lequel on est venu |
| Mode | **sol phrygien** (sol **la♭** si♭ do ré mi♭ fa) |
| Tempo | **143** à la noire |
| Forme | intro (2) — A (6) — B (6) — A' (4) |
| Durée | 18 mesures à **6/4** = **45,8 s** |
| Taille | **1 176 octets** (tampon de zone : 2 304) |
| Notes | 301 écrites, **0 abandonnée** |

Ce qui la rattache à `danger` : le **demi-ton phrygien**, ici la♭–sol, et le
bourdon de sol. Deux choses n'appartiennent qu'à elle, et les deux sortent de la
page 011.

**Six pattes.** C'est la seule des trente-cinq clairières qui ne soit pas à
quatre temps : elle est à **6/4**, et l'arpège y boite en 1 + ½ + ½ + 1 + 1½ +
1½ — six appuis qui ne tombent jamais régulièrement.

**La respiration lourde.** Le bourdon est refrappé à **chaque mesure** au lieu
de toutes les quatre : dix-huit inspirations sur les quarante-cinq secondes.

C'est un cul-de-sac : l'harmonie ne module jamais et la dernière mesure retombe
exactement sur la première. La pièce est aussi la plus légère des onze en
octets — la texture est volontairement clairsemée, comme la clairière.

## Les six voix (mesurées par `verifier.py`)

| voix | côté | rôle | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | mélodie | B♭4..A♭6 | 50 |
| 1 | gauche | médiane (contre-chant en blanches pointées) | G3..B♭4 | 34 |
| 2 | **gauche** | basse, foulée à six temps | B♭2..C4 | 69 |
| 3 | **droite** | l'arpège boiteux | D4..E♭5 | 95 |
| 4 | droite | médiane (accords tenus) | G3..G4 | 35 |
| 5 | **droite** | bourdon de sol, refrappé à chaque mesure | G2 | 18 |

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/27-bete
python3 bete.py
python3 ../../../midi_to_mb.py bete.mid BETE.MB.BIN \
    --bpm 143 --max 2304 --wav BETE.wav
```
