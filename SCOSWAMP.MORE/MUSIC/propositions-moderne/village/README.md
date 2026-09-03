# Zone `village` — Bourbenville, le prologue, Courbensaule, la sortie

**`VILLAGE.MB.BIN` — 2 254 octets, 40,8 s, boucle.** Tampon de zone (2 304 o), 50 octets de marge.

## Ce que la zone couvre

Une clairière et les pages hors carte du prologue.

| # | `hub` | Titre | Pages |
| ---: | ---: | --- | --- |
| **1** | 078 | **Route de Courbensaule** (ville, boutique d'Alphonse, La Lance Tordue) | 280, 355, 78, 150, 408 |

| Ensemble | Pages |
| --- | --- |
| Prologue de Bourbenville | 001, 048, 095, 122, 240, 296, 173, 009 |
| Retour des missions | 159 |
| Sortie du Marais | 208 |

**Courbensaule est ici volontairement**, et c'est le seul écart avec le plan à
onze zones : les deux villes sont le même lieu du point de vue du joueur — un
endroit où l'on achète, où l'on parle, où rien ne mord — et la clairière 1 ne
compte que cinq pages. C'est la fusion n° 1 recommandée par
`../../MUSIC/propositions/INDEX.md` § 4. Le dossier passe ainsi de onze pièces
à dix.

## La pièce

| | |
| --- | --- |
| Titre | **Les Feux de Bourbenville** |
| Source | composition originale, `village.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | le seul morceau du jeu qui n'ait pas peur : tierces majeures, basse qui balance croche pointée-croche, batterie de danse |
| Mode | **sol mixolydien** (sol la si do ré mi **fa**) — septième mineure au lieu de la sensible |
| Tempo | **166** à la noire |
| Forme | intro (4) — A, crochet énoncé deux fois (8) — B (8) — A' à l'octave (8) |
| Durée | 28 mesures à 4/4 = **40,8 s** |
| Taille | **2 254 octets** — 461 notes de hauteur, 117 coups, 0 abandonnée |

## Ce que la révision a apporté

- **Crochet.** Ré-sol-si-la puis la retombée la-fa-la, mesures 5-6, **repris mesures 9-10** avec un ré mineur passager à la mesure 11 qui le fait respirer autrement ; à l'octave mesure 21.
- **Question et réponse.** Mesures 7, 12 et 24 : la mélodie tient, le contre-chant répond en croches montantes.
- **Partie B contrastée.** La mélodie monte d'une tierce, l'harmonie part sur la mineur.
- **Surprise.** Mesures 17-18, un accord de **si bémol** étranger au mixolydien **et la batterie qui s'arrête net** ; elle revient mesure 19 sur un coup de cymbale. C'est le seul moment du jeu où le village se tait.
- **Rythme harmonique.** Huit temps sur sol à l'intro, quatre en A, deux aux mesures 11 et 23, huit sur la cadence.
- **Arc.** Arpège en noires à l'intro et dans la première moitié du B, en croches ailleurs ; batterie de 3 à 5 frappes par mesure.

## Les voix

Mesuré par `../verifier.py` — c'est l'attribution réelle de
`midi_to_mb.py`, pas une intention. Voir `../INDEX.md` § 3.

| voix | côté | rôle | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | mélodie | D5..B6 | 72 |
| 1 | gauche | médiane (accords tenus) | A3..B4 | 41 |
| 2 | **gauche** | basse de danse | D2..F3 | 112 |
| 3 | **droite** | **contre-chant — la voix qui répond** | B3..C5 | 69 |
| 4 | droite | arpège en croches, le tambourin | F3..G4 | 167 |
| 5 | **droite** | **batterie** — charleston 60, grosse caisse 30, caisse claire 22, cymbale 3 | bruit | 115 |

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/village
python3 village.py
python3 ../../midi_to_mb.py village.mid VILLAGE.MB.BIN \
    --bpm 166 --max 2304 --wav VILLAGE.wav
```
