# Zone `village` — Bourbenville, le prologue et la sortie du Marais

**Fichier proposé : `VILLAGE.MB` (`VILLAGE.MB.BIN`, 916 octets, 48,0 s de boucle)**

## Ce que la zone couvre

Aucune clairière : ce sont les pages **hors carte** du prologue, avant que le
Marais ne s'ouvre, plus la page qui en ressort.

| Page | Titre | Rôle |
| --- | --- | --- |
| 001 | La taverne de Bourbenville | le village, les villageois inquiets |
| 048 / 095 | Grognard | le vieux soldat |
| 122 / 240 | Les trois missions | Gayolard, Pompatarte, Stratagus |
| 296 / 173 | la route vers le Marais | |
| 009 | L'entrée du Marais | dernière page avant le silence hostile |
| 159 | le retour des missions | carrefour de fin |
| 208 | Sortir du Marais | « un coin de ciel bleu à travers une trouée du feuillage » |

`carte.json:769` pose `"depart_prologue": 9` ; la page 208 est la porte sud
(`carte.json:771`).

## La pièce

| | |
| --- | --- |
| Œuvre | **Il Est de Bonne Heure Né** |
| Auteur | Anonyme, chanson française **c. 1470** |
| Source | Mutopia Project, [piece-info.cgi?id=198](https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=198) |
| Fichiers | `https://www.mutopiaproject.org/ftp/Anonymous/bonne_heure-song/bonne_heure-song.{ly,mid}` |
| Licence | **domaine public** (Creative Commons No Rights Reserved) |
| Effectif d'origine | quatre voix (SATB) |
| Tempo retenu | **150** à la noire (20 ticks par noire sur le tick de 50 Hz : tombe juste) |
| Durée de boucle | 48,0 s |
| Taille | 916 octets |

## Pourquoi elle convient

C'est une chanson de village, pas une pièce de cour : mélodie carrée, refrain
qui revient, aucune ombre. Elle date d'avant l'aventure — la fin du XV<sup>e</sup>
siècle contre le XVI<sup>e</sup> des trois autres pièces anglaises — ce qui donne au
prologue une couleur légèrement plus fruste que le reste du jeu, exactement le
rapport entre Bourbenville et Courbensaule.

Réduite à trois voix carrées, la ligne de dessus reste chantante et la basse
marche par degrés : c'est le cas le plus favorable pour `midi_to_mb.py`, qui
choisit à chaque instant la voix la plus haute, la plus basse et la plus proche
du milieu.

À 150 la noire elle danse au lieu de marcher — le reproche fait aux rendus à
100-120.

## Régénérer

```sh
python3 SCOSWAMP.MORE/MUSIC/midi_to_mb.py \
    SCOSWAMP.MORE/MUSIC/propositions/village/bonne_heure.mid \
    SCOSWAMP.MORE/MUSIC/propositions/village/VILLAGE.MB.BIN \
    --bpm 150 --vol 13,9,11 \
    --wav SCOSWAMP.MORE/MUSIC/propositions/village/VILLAGE.wav
```

Le `.wav` n'est pas suivi par git (`.gitignore:76`) : c'est un rendu, et il est
*exactement* ce que la carte jouera — trois ondes carrées, rien d'autre.
