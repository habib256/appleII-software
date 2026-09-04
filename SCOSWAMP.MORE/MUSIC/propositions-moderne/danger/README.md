# Zone `danger` — les dix clairières où l'on meurt

**`DANGER.MB.BIN` — 1 951 octets, 49,7 s, boucle.** Tampon de zone (2 304 o), 353 octets de marge.

## Ce que la zone couvre

| # | `hub` | Titre | (x,y) | Pages |
| ---: | ---: | --- | :---: | --- |
| 9 | 153 | Le bassin de Vase | (1,2) | 336, 137, 153 |
| 10 | 088 | Scorpion et nain | (2,2) | 14, 338, 88 |
| 12 | 270 | Sables mouvants | (4,2) | 41, 382, 270 |
| 19 | 319 | La clairière des scorpions | (3,4) | 118, 303, 319 |
| 22 | 367 | Les Fleurs d'Angoisse | (0,5) | 204, 250, 367 |
| 25 | 187 | Herbe à Pinces | (3,5) | 388, 263, 33, 187 |
| 26 | 309 | Orques des Marais | (4,5) | 290, 323, 352, 309 |
| 27 | 125 | Cul-de-sac de la Bête | (0,6) | 11, 210, 299, 125, 228, 243 |
| 28 | 022 | La clairière des Arbres-Épées | (1,6) | 157, 279, 22 |
| 29 | 165 | Tente aux araignées | (3,6) | 144, 345, 354, 165 |

Ces dix clairières sont réparties dans le nord comme dans le sud : la zone
n'est pas géographique, c'est un **avertissement**. Elle doit donc se
reconnaître en une seconde et ne ressembler à rien d'autre.

## La pièce

| | |
| --- | --- |
| Titre | **Ce qui Attend Sous l'Eau** |
| Source | composition originale, `danger.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | quelque chose est déjà là et ne bougera qu'au dernier moment. La batterie n'est pas un rythme : c'est un **cœur**, une grosse caisse seule, sans charleston ni caisse claire |
| Mode | **do phrygien** (do **ré♭** mi♭ fa sol la♭ si♭) |
| Tempo | **136** à la noire |
| Forme | intro (4) — A, crochet énoncé deux fois (8) — B (8) — A' (8) |
| Durée | 28 mesures à 4/4 = **49,7 s** |
| Taille | **1 951 octets** — 416 notes de hauteur, 78 coups, 0 abandonnée |

## Ce que la révision a apporté

- **Le cœur qui s'affole.** Deux coups de grosse caisse par mesure jusqu'à la mesure 12, **trois** à partir de la 13, **quatre** à partir de la 21. La pièce ne monte pas, elle accélère.
- **Crochet.** Le demi-ton do-ré bémol-do, énoncé mesure 5 et **repris à l'identique mesure 9** sur une autre basse. Aucun autre morceau du jeu n'a ce demi-ton.
- **Question et réponse.** Mesures 7, 12 et 24 : la mélodie tient, le contre-chant répond par le même demi-ton, plus bas.
- **Surprise.** Mesure 20, **tout se tait pendant deux temps**, cœur compris, et le fa mineur qui suit tombe dans le vide.
- **Ce qui a cédé sa voix.** Sous une batterie il ne reste que cinq voix de hauteur ; ici c'est la voix d'accords tenus qui part, pas le bourdon de do — il ne bouge pas d'un bout à l'autre et c'est lui qui fait la zone.
- **Arc.** L'arpège va en blanches, puis en noires mesure 5, puis en croches mesure 9 ; la basse passe des blanches aux noires au même endroit.

## Les voix

Mesuré par `../verifier.py` — c'est l'attribution réelle de
`midi_to_mb.py`, pas une intention. Voir `../INDEX.md` § 3.

| voix | côté | rôle | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | mélodie | F5..A♯6 | 72 |
| 1 | gauche | arpège, qui se resserre | D♯3..G♯4 | 179 |
| 2 | **gauche** | **bourdon de do, immobile de bout en bout** | C2 | 7 |
| 3 | **droite** | **contre-chant — la voix qui répond** | F4..D♯5 | 64 |
| 4 | droite | basse | F2..G♯3 | 94 |
| 5 | **droite** | **batterie — le cœur** : grosse caisse seule, 78 coups | bruit | 78 |

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/danger
python3 danger.py
python3 ../../midi_to_mb.py danger.mid DANGER.MB.BIN \
    --bpm 136 --max 2304 --wav DANGER.wav
```
