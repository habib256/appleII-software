# Clairières 13 à 24 — douze musiques, une par clairière

Douze **compositions originales** (GPL v3), écrites avec `../compose.py` et
converties par `../../midi_to_mb.py` — le même code que le disque. Chacune est
une **variation dans la couleur de sa zone** : même famille de mode, même
procédé identifiable, mais son propre thème et son propre caractère, tirés des
pages de la clairière.

Le `.wav` de chaque dossier **est** ce que la Mockingboard jouera — six ondes
carrées, deux puces, la même réduction, le même tempo, la même stéréo. Il n'est
pas suivi par git.

## Le tableau

| # | `hub` | Clairière | Dossier | Fichier | Pièce | Mode | bpm | Durée | Octets |
| ---: | ---: | --- | --- | --- | --- | --- | ---: | ---: | ---: |
| 13 | 295 | La Rivière Croupie | `13-croupie` | `CROUPIE.MB.BIN` | **La Berge aux Crocodiles** | sol dorien | 132 | 44,1 s | 1 611 |
| 14 | 183 | Sommet de la falaise | `14-falaise` | `FALAISE.MB.BIN` | **Le Ciel s'Ouvre** | si dorien | 140 | 41,6 s | 1 548 |
| 15 | 045 | Le pont sur la Croupie | `15-pont` | `PONT.MB.BIN` | **Le Seul Passage** | si♭ dorien | 150 | 42,1 s | 1 838 |
| 16 | 304 | Le Perroquet / la Maîtresse des Oiseaux | `16-oiseaux` | `OISEAUX.MB.BIN` | **La Maîtresse des Oiseaux** | mi dorien | **168** | 40,5 s | 1 900 |
| 17 | 094 | La brume fétide | `17-brume` | `BRUME.MB.BIN` | **La Brume Fétide** | do éolien | **128** | 41,7 s | 1 408 |
| 18 | 179 | Le pique-nique suspect | `18-piquenique` | `PIQUENIQUE.MB.BIN` | **Le Repas du Voleur** | fa dorien | **176** | 41,4 s | 1 548 |
| 19 | 319 | La clairière des scorpions | `19-scorpions` | `SCORPIONS.MB.BIN` | **La Nuée** | ré phrygien | **180** | 32,5 s | 1 847 |
| 20 | 047 | Trois chemins herbeux | `20-herbeux` | `HERBEUX.MB.BIN` | **Trois Chemins Herbeux** | ré dorien | 145 | 36,9 s | 1 408 |
| 21 | 031 | Bassin de cristal | `21-cristal` | `CRISTAL.MB.BIN` | **Le Bassin de Cristal** | do dorien | 152 | 41,5 s | **1 982** |
| 22 | 367 | Les Fleurs d'Angoisse | `22-angoisse` | `ANGOISSE.MB.BIN` | **Les Fleurs d'Angoisse** | mi phrygien | 144 | 40,5 s | 1 589 |
| 23 | 348 | La Licorne | `23-licorne` | `LICORNE.MB.BIN` | **La Licorne Blessée** | fa éolien | 138 | 42,2 s | 1 605 |
| 24 | 227 | La clairière des combats | `24-arene` | `ARENE.MB.BIN` | **Ce qui Reste du Combat** | mi éolien | 160 | 42,5 s | 1 975 |

**Total : 20 259 octets** sur le volume. Ce qui coûte, c'est la plus grosse :
`CRISTAL.MB.BIN`, **1 982 octets**, soit **322 octets de marge** sur le tampon
de zone (2 304). Les onze autres ont entre 329 et 896 octets de marge. Aucune
des douze n'abandonne une seule note à la réduction : polyphonie maximale = 6
exactement, jamais 7, et `midi_to_mb.py` affiche « 0 abandonnées » sur les
douze.

## Ce que chaque pièce garde de sa zone, et ce qu'elle y ajoute

| # | Zone | Procédé de la zone, conservé | Ce qui appartient à la clairière |
| ---: | --- | --- | --- |
| 13 | `riviere` | dorien, arpège continu, **bourdon sur la quinte** (ré) | basse brève-longue, la mâchoire ; le mi naturel comme seul reflet |
| 14 | `riviere` | dorien, **bourdon sur la quinte** (fa♯) | arpège à **quatre sons, l'octave comprise** ; la montée sur 16 mesures |
| 15 | `riviere` | dorien, arpège continu, **bourdon sur la quinte** (fa) | **quatre noires marchées** par mesure : on traverse ; le B qui n'ose pas |
| 16 | `sud` | **bourdon de tonique** (mi), marche modale large | dorien au lieu d'éolien ; **arpège en sauts de quinte** ; le B en blanches, le silence léger |
| 17 | `sud` | éolien, **bourdon de tonique** (do) | la **descente** mesure par mesure ; basse en blanches partout |
| 18 | `sud` | **bourdon de tonique** (fa), marche modale | le **3/4**, seule valse des 35 ; le sol♭ phrygien qui trahit le Voleur |
| 19 | `danger` | **phrygien** (mi♭ contre ré), **bourdon de tonique** | les **doubles croches** du grouillement ; la basse en noires dès la mesure 1 |
| 20 | `sud` | **bourdon de tonique** sur le même ré que la zone | dorien ; **trois phrases**, une par sentier, trois cadences |
| 21 | `sud` | **bourdon de tonique** (do), marche modale | la **sixte majeure** ; l'arpège en doubles croches à la reprise, l'éclat |
| 22 | `danger` | **phrygien** (fa contre mi), **bourdon de tonique**, crescendo **par la densité** | tierces douces en A, **tremblement** fa-mi-fa en B |
| 23 | `sud` | la **marche i-VI-III-VII** de la zone, transposée ; bourdon de tonique (fa) | A **sans une croche** ; B au **rythme pointé**, le défi |
| 24 | `sud` | la **marche i-VI-III-VII** (Em-C-G-D), bourdon de tonique (mi) | le **rythme pointé** à chaque mesure ; le si mineur de la fouille |

## Les six voix

Toutes les douze suivent le plan du dossier — la mélodie et la basse à gauche,
le mouvement et le bourdon à droite — parce qu'elles suivent ses deux règles
d'écriture : chaque partie reste dans sa bande de registre, et chaque partie
sonne sur chaque temps fort, en attaquant ou en tenant. `Piece.write()` ne
signale un trou sur aucune.

| voix | côté | ce qui s'y trouve, dans les douze pièces |
| ---: | :---: | --- |
| 0 | **gauche** | la mélodie, seule |
| 1 | gauche | une voix médiane |
| 2 | **gauche** | la basse, seule |
| 3 | **droite** | l'arpège, l'essentiel du mouvement |
| 4 | droite | une voix médiane |
| 5 | **droite** | le bourdon, seul, immobile |

## Refabriquer les douze

```sh
cd /Users/gistair/src/pom2adventure/SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres
M=../../../midi_to_mb.py
(cd 13-croupie    && python3 croupie.py    && python3 $M croupie.mid    CROUPIE.MB.BIN    --bpm 132 --max 2304 --wav CROUPIE.wav)
(cd 14-falaise    && python3 falaise.py    && python3 $M falaise.mid    FALAISE.MB.BIN    --bpm 140 --max 2304 --wav FALAISE.wav)
(cd 15-pont       && python3 pont.py       && python3 $M pont.mid       PONT.MB.BIN       --bpm 150 --max 2304 --wav PONT.wav)
(cd 16-oiseaux    && python3 oiseaux.py    && python3 $M oiseaux.mid    OISEAUX.MB.BIN    --bpm 168 --max 2304 --wav OISEAUX.wav)
(cd 17-brume      && python3 brume.py      && python3 $M brume.mid      BRUME.MB.BIN      --bpm 128 --max 2304 --wav BRUME.wav)
(cd 18-piquenique && python3 piquenique.py && python3 $M piquenique.mid PIQUENIQUE.MB.BIN --bpm 176 --max 2304 --wav PIQUENIQUE.wav)
(cd 19-scorpions  && python3 scorpions.py  && python3 $M scorpions.mid  SCORPIONS.MB.BIN  --bpm 180 --max 2304 --wav SCORPIONS.wav)
(cd 20-herbeux    && python3 herbeux.py    && python3 $M herbeux.mid    HERBEUX.MB.BIN    --bpm 145 --max 2304 --wav HERBEUX.wav)
(cd 21-cristal    && python3 cristal.py    && python3 $M cristal.mid    CRISTAL.MB.BIN    --bpm 152 --max 2304 --wav CRISTAL.wav)
(cd 22-angoisse   && python3 angoisse.py   && python3 $M angoisse.mid   ANGOISSE.MB.BIN   --bpm 144 --max 2304 --wav ANGOISSE.wav)
(cd 23-licorne    && python3 licorne.py    && python3 $M licorne.mid    LICORNE.MB.BIN    --bpm 138 --max 2304 --wav LICORNE.wav)
(cd 24-arene      && python3 arene.py      && python3 $M arene.mid      ARENE.MB.BIN      --bpm 160 --max 2304 --wav ARENE.wav)
```

Le bloc entier se recolle tel quel dans un shell. `--max 2304` est le tampon de
zone : la conversion **échoue** au lieu de livrer un flux qui déborderait à
l'exécution. `--vol` reste au défaut `13,11,11,12,11,11` sur les douze.

Vérifier la stéréo d'une pièce, voix par voix :

```sh
cd /Users/gistair/src/pom2adventure/SCOSWAMP.MORE/MUSIC/propositions-moderne
python3 verifier.py clairieres/21-cristal/cristal.mid --bpm 152
```
