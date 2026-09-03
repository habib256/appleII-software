# Clairières 1 à 12 — une musique par clairière

Douze compositions originales, écrites avec `../compose.py`, converties par
`../../midi_to_mb.py`, sous **GPL v3** comme le reste du dépôt. Chacune est une
**variation dans la couleur de sa zone** — même famille de mode, même procédé
identifiable — mais avec son propre thème, son propre caractère tiré des pages
de la clairière, et sa propre forme.

Le `.wav` de chaque dossier **est** ce que la Mockingboard jouera : six ondes
carrées, deux puces, la même réduction, le même tempo, la même stéréo. C'est le
seul objet à écouter pour juger ; il n'est pas suivi par git.

---

## 1. Les douze pièces

| # | `hub` | Clairière | Zone | Fichier disque | Pièce | Mode | bpm | Durée | Octets |
| ---: | ---: | --- | --- | --- | --- | --- | ---: | ---: | ---: |
| 1 | 078 | Route de Courbensaule | `village` | `COURBENS.MB` | **La Route des Trois Auberges** | ré mixolydien | **172** | 39,1 s | 1 999 |
| 2 | 234 | Le Patrouilleur vert | `nord` | `PATROUIL.MB` | **La Question du Patrouilleur** | la éolien | 156 | 43,1 s | 1 993 |
| 3 | 084 | Le Maître des Jardins | `nord` | `JARDINS.MB` | **L'Amulette de Fleur** | ré dorien | 138 | 45,2 s | 1 883 |
| 4 | 232 | Les deux loups | `nord` | `LOUPS.MB` | **Deux Paires d'Yeux** | si éolien | 168 | 40,0 s | **2 124** |
| 5 | 218 | Feu follet à l'orée | `nord` | `FEUFOLLET.MB` | **La Lumière qui Recule** | sol éolien | 150 | 41,6 s | 1 777 |
| 6 | 121 | Le croisement | `nord` | `CROISEMENT.MB` | **Quatre Chemins** | mi éolien | 144 | 46,7 s | 1 901 |
| 7 | 161 | Le Géant | `nord` | `GEANT.MB` | **Il Est Interdit de Passer** | do éolien | **132** | 43,6 s | **1 260** |
| 8 | 019 | Clairière aux brigands | `nord` | `BRIGANDS.MB` | **Cinq Voix derrière l'Arbre** | ré éolien | **176** | 38,2 s | 1 928 |
| 9 | 153 | Le bassin de Vase | `danger` | `VASE.MB` | **Ce qui Sort du Bassin** | ré phrygien | **132** | **47,3 s** | 1 373 |
| 10 | 088 | Scorpion et nain | `danger` | `SCORPNAIN.MB` | **Les Pinces et l'Os** | la phrygien | **176** | **38,2 s** | 1 866 |
| 11 | 202 | Le nid de l'Aigle | `nord` | `AIGLE.MB` | **Le Grand Nid** | fa♯ éolien | 152 | 44,2 s | 1 437 |
| 12 | 270 | Sables mouvants | `danger` | `SABLES.MB` | **Le Sol qui Cède** | fa phrygien | 138 | 45,2 s | 1 648 |

**Total : 21 189 octets** sur le volume, pour douze fichiers. Ce qui coûte n'est
pas le nombre de pièces mais la plus grosse : **`LOUPS.MB`, 2 124 octets**, à
**180 octets** de la limite du tampon de zone (2 304). Toute retouche de
`loups.py` doit être reconvertie avant d'être crue ; les onze autres ont entre
305 et 1 044 octets de marge.

Douze modes, douze toniques, **aucun doublon** : chaque clairière a sa propre
paire mode/tonique, et aucune ne reprend celle de sa zone sauf `CROISEMENT`,
délibérément en mi éolien parce qu'il est le centre du Marais nord.

Toutes les pièces : **six voix, polyphonie maximale 6 exactement, zéro note
abandonnée par la réduction**, tempo entre 132 et 176, boucle entre 38 et 47 s.

## 2. Les procédés, zone par zone

| Zone | Procédé de la zone | Ce que les clairières en font |
| --- | --- | --- |
| `village` | arpège de croches, basse en croche pointée | **1** garde les deux, descend d'une quinte et ajoute l'intro qui s'élargit |
| `nord` | un ostinato **fixe** sous des accords qui bougent | **2** le met à trois croches (il décale), **3** lui donne la sixte majeure du dorien, **4** en fait deux qui se relaient, **5** le met à cinq croches, **6** en met un par direction, **7** le met en noires, **8** lui donne cinq notes, **11** lui donne un rythme de vol plané |
| `danger` | demi-ton phrygien, bourdon immobile, crescendo par la densité | **9** fait du demi-ton la cellule et la resserre trois fois, **10** desserre au milieu au lieu de resserrer, **12** retourne l'arpège vers le bas |

## 3. Refabriquer les douze

Depuis `SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres` :

```sh
M=../../../midi_to_mb.py
(cd 01-courbens   && python3 courbens.py   && python3 $M courbens.mid   COURBENS.MB.BIN   --bpm 172 --max 2304 --wav COURBENS.wav)
(cd 02-patrouil   && python3 patrouil.py   && python3 $M patrouil.mid   PATROUIL.MB.BIN   --bpm 156 --max 2304 --wav PATROUIL.wav)
(cd 03-jardins    && python3 jardins.py    && python3 $M jardins.mid    JARDINS.MB.BIN    --bpm 138 --max 2304 --wav JARDINS.wav)
(cd 04-loups      && python3 loups.py      && python3 $M loups.mid      LOUPS.MB.BIN      --bpm 168 --max 2304 --wav LOUPS.wav)
(cd 05-feufollet  && python3 feufollet.py  && python3 $M feufollet.mid  FEUFOLLET.MB.BIN  --bpm 150 --max 2304 --wav FEUFOLLET.wav)
(cd 06-croisement && python3 croisement.py && python3 $M croisement.mid CROISEMENT.MB.BIN --bpm 144 --max 2304 --wav CROISEMENT.wav)
(cd 07-geant      && python3 geant.py      && python3 $M geant.mid      GEANT.MB.BIN      --bpm 132 --max 2304 --wav GEANT.wav)
(cd 08-brigands   && python3 brigands.py   && python3 $M brigands.mid   BRIGANDS.MB.BIN   --bpm 176 --max 2304 --wav BRIGANDS.wav)
(cd 09-vase       && python3 vase.py       && python3 $M vase.mid       VASE.MB.BIN       --bpm 132 --max 2304 --wav VASE.wav)
(cd 10-scorpnain  && python3 scorpnain.py  && python3 $M scorpnain.mid  SCORPNAIN.MB.BIN  --bpm 176 --max 2304 --wav SCORPNAIN.wav)
(cd 11-aigle      && python3 aigle.py      && python3 $M aigle.mid      AIGLE.MB.BIN      --bpm 152 --max 2304 --wav AIGLE.wav)
(cd 12-sables     && python3 sables.py     && python3 $M sables.mid     SABLES.MB.BIN     --bpm 138 --max 2304 --wav SABLES.wav)
```

Le bloc entier se recolle tel quel dans un shell ; avec `set -e` il s'arrête à la
première erreur. `--max 2304` fait **échouer** la conversion au lieu de livrer un
flux qui déborderait le tampon de zone à l'exécution. `--vol` reste au défaut
`13,11,11,12,11,11` partout, comme pour les dix pièces de zone.

Pour vérifier ce que la carte fera réellement d'une pièce, voix par voix et
côté par côté :

```sh
python3 ../verifier.py 11-aigle/aigle.mid --bpm 152
```

## 4. Ce que l'adoption demanderait

Aucun texte, aucun code, aucun `Makefile` n'a été touché : ce dossier est un
atelier. Adopter une de ces douze pièces demanderait, **pour chaque page de la
clairière**, de remplacer sa ligne `MU MARAISNO.MB` / `MU DANGER.MB` /
`MU VILLAGE.MB` par le fichier de la clairière, et de copier le `.MB.BIN` sur le
volume. Les pages concernées sont listées en tête de chaque `README.md`.

Trente-cinq musiques de clairière remplaceraient les cinq thèmes de zone par
trente-cinq fichiers d'environ deux kilo-octets, soit de l'ordre de 70 Ko sur les
~28 Mo libres : le volume n'est pas la question. La question est le tampon, qui
reste de **2 304 octets par zone** et qu'aucune de ces douze pièces ne dépasse.
