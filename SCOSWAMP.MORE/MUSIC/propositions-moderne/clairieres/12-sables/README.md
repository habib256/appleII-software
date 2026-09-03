# Clairière 12 — Sables mouvants (`hub` 270, case 4,2)

**`SABLES.MB.BIN` — 1 648 octets, 45,2 s, boucle.**

## Les pages

| Page | Titre | Ce qui s'y passe |
| ---: | --- | --- |
| 041 | Sables mouvants | les troncs couverts de lierre, le sol qui cède, le test de Chance |
| 382 | Retour aux Sables Mouvants | la Pierre de Glace, la Pierre de Croissance |
| 270 | Deux sentiers | le nord ou l'ouest, « avec prudence » |

## La pièce

| | |
| --- | --- |
| Titre | **Le Sol qui Cède** |
| Source | composition originale, `sables.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | on tombe, et on n'arrive pas en bas. « Aucun autre chemin ne semble présent : vous êtes pris au centre » |
| Mode | **fa mineur phrygien** (fa **sol♭** la♭ si♭ do ré♭ mi♭) |
| Tempo | **138** à la noire |
| Forme | intro (4) — A (8) — B (8) — A' (6) |
| Durée | 26 mesures à 4/4 = **45,2 s** |
| Taille | **1 648 octets** (marge 656) |
| Notes | 425 écrites, **0 abandonnée** |

## Ce qui la relie à `danger`, et ce qui l'en sépare

Demi-ton phrygien, bourdon immobile, crescendo par la densité : les trois
marques de la zone sont là. Ce qui appartient à cette clairière-là, c'est le
**sens**. Tout descend.

- L'arpège parcourt l'accord à l'envers — **quinte, tierce, fondamentale, puis
  la quinte une octave plus bas** — et recommence en haut à chaque changement
  d'accord. On n'arrête donc pas de retomber sans jamais arriver en bas ; c'est
  la même illusion d'escalier que produit le sable qui coule. L'arpège de
  `DANGER.MB` monte et redescend ; celui-ci ne fait que descendre.
- Chaque phrase de la mélodie part de sa note la plus aiguë et finit sur sa plus
  grave.
- La basse alterne fondamentale et quinte grave au lieu de marcher.

Le sol cède à la **mesure 9** : l'arpège passe de la noire à la croche et la
basse double, exactement là où le `danger` de la zone se resserre. La seule
chose qui ne bouge pas est le **bourdon de do**, la quinte à vide de fa, tenue
quatre mesures d'affilée — on s'enfonce, mais le Marais, lui, ne s'enfonce pas.

## Les six voix, mesurées

`python3 ../../verifier.py sables.mid --bpm 138`

| voix | côté | ce qui s'y trouve | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | la mélodie, seule | D♭5..A♭6 | 76 |
| 1 | gauche | le contre-chant, seul | A♭3..G♭4 | 51 |
| 2 | **gauche** | la basse, seule | F2..A♭3 | 88 |
| 3 | **droite** | **la chute** | F3..E♭5 | 176 |
| 4 | droite | les accords tenus, seuls | G♭3..F4 | 27 |
| 5 | **droite** | le bourdon de do, immobile | C2 | 7 |

L'arpège descend sur près de deux octaves (fa3 à mi♭5) sans jamais sortir de sa
voix : c'est ce qui permet à la chute de rester entièrement à droite alors même
qu'elle traverse le registre du contre-chant et des accords.

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/12-sables
python3 sables.py
python3 ../../../midi_to_mb.py sables.mid SABLES.MB.BIN \
    --bpm 138 --max 2304 --wav SABLES.wav
```
