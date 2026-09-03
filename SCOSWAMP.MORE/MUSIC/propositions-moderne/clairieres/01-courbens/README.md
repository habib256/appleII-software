# Clairière 1 — Route de Courbensaule (`hub` 078, case 0,0)

**`COURBENS.MB.BIN` — 1 999 octets, 39,1 s, boucle.**

## Les pages

| Page | Titre | Ce qui s'y passe |
| ---: | --- | --- |
| 280 | Route de Courbensaule | le Marais s'ouvre, les gardes forestiers, les trois auberges |
| 355 | Retour à Courbensaule | la rumeur des exploits, les deux coupeurs de bourses |
| 078 | La Lance Tordue | l'auberge, +2 ENDURANCE, le sorcier voisin |
| 150 | Le marchand de potions | Alphonse Machefer, négociant en magie |
| 408 | Échange chez Alphonse | jusqu'à trois objets contre des Pierres neutres |

C'est la seule clairière **hors Marais** des trente-cinq : une ville marchande,
pas une trouée dans la fange. La zone de référence est donc `village`.

## La pièce

| | |
| --- | --- |
| Titre | **La Route des Trois Auberges** |
| Source | composition originale, `courbens.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | on arrive. Le seul morceau des douze qui n'ait rien à craindre : tierces majeures, septième mineure, un tambourin qui ne s'arrête jamais |
| Mode | **ré mixolydien** (ré mi fa♯ sol la si do) |
| Tempo | **172** à la noire |
| Forme | intro (4) — A (8) — B (8) — A' (8) |
| Durée | 28 mesures à 4/4 = **39,1 s** |
| Taille | **1 999 octets** (marge 305 sur le tampon de zone) |
| Notes | 510 écrites, **0 abandonnée** |

## Ce qui la relie à `village`, et ce qui l'en sépare

De la zone elle garde les trois marques : le **mode majeur à septième mineure**,
l'**arpège de croches** qui tient lieu de tambourin, et la **basse balancée en
croche pointée - croche**, le pas de danse. Elle en change tout le reste :

- le mode descend de sol à **ré**, une quinte plus bas — la même couleur, une
  autre lumière, et surtout une autre paire de doigts sur le manche ;
- le tempo monte de 166 à **172**, parce qu'on marche vers la ville au lieu d'y
  être déjà ;
- l'intro de quatre mesures monte du ré grave à l'aigu : c'est la route qui
  « s'élargit peu à peu » de la page 280, et elle n'existe pas dans `VILLAGE.MB` ;
- le B enchaîne trois phrases de deux mesures, une par auberge, sur la marche
  `sol - ré - mim - sim` puis `do - sol - lam - ré`, avant la cadence du
  marchand de potions.

## Les six voix, mesurées

`python3 ../../verifier.py courbens.mid --bpm 172`

| voix | côté | ce qui s'y trouve | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | la mélodie, seule, du début à la fin | D5..A6 | 83 |
| 1 | gauche | le contre-chant, et les notes basses de l'arpège | A3..B4 | 85 |
| 2 | **gauche** | la basse de danse, seule | E2..G3 | 112 |
| 3 | **droite** | l'arpège, l'essentiel du mouvement | C4..D5 | 128 |
| 4 | droite | les accords tenus, et le reste de l'arpège | F♯3..G4 | 95 |
| 5 | **droite** | le bourdon de ré, immobile | D2 | 7 |

Mélodie et basse à gauche, tambourin et bourdon à droite : la même image stéréo
que `VILLAGE.MB`, ce qui est voulu — les deux pièces se succèdent dans la
partie, page 009 puis page 280.

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/01-courbens
python3 courbens.py
python3 ../../../midi_to_mb.py courbens.mid COURBENS.MB.BIN \
    --bpm 172 --max 2304 --wav COURBENS.wav
```
