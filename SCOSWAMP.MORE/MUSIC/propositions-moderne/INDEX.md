# Propositions musicales — style **fantasy moderne**, six voix, stéréo

Ce dossier est un **atelier**, pas le disque. Rien n'est copié dans
`SCOSWAMP/MUSIC/` tant que le propriétaire n'a pas écouté et tranché. Il propose
une alternative complète au dossier voisin `../propositions/`, qui suit la même
carte des zones mais avec un répertoire Renaissance à trois voix.

**Dix pièces, toutes des compositions originales** écrites en Python sans
dépendance (`compose.py` + un script par zone), donc sous la **GPL v3** comme le
reste du dépôt. Aucune œuvre tierce, aucune licence à vérifier, aucune
attribution à porter. Les recherches de MIDI CC0/CC-BY n'ont pas été menées :
elles n'auraient rien apporté qu'une composition maison ne donne pas ici, et
elles auraient rouvert la question de compatibilité que `DOCS/MUSIQUE.md § 6.5`
demande de trancher pièce par pièce.

Le `.wav` de chaque dossier **est** ce que la Mockingboard jouera : six ondes
carrées, deux puces, la même réduction, le même tempo, la même stéréo. C'est le
seul objet à écouter pour juger. Il n'est pas suivi par git
(`.gitignore:76`).

---

## 1. Les dix musiques

| Zone | Fichier disque | Pièce | Mode | bpm | Durée | Octets | Tampon |
| --- | --- | --- | --- | ---: | ---: | ---: | :---: |
| `accueil` | `ACCUEIL.MB` | **L'Appel du Marais** | ré dorien | 136 | 49,9 s | 2 070 | zone |
| `village` | `VILLAGE.MB` | **Les Feux de Bourbenville** | sol mixolydien | **166** | 46,7 s | 2 285 | zone |
| `nord` | `MARAISNO.MB` | **Le Bois des Guetteurs** | mi éolien | 150 | 45,3 s | 1 978 | zone |
| `riviere` | `RIVIERE.MB` | **Le Pont sur la Croupie** | la dorien | 125 | 54,2 s | 1 861 | zone |
| `sud` | `MARAISUD.MB` | **Sentiers Verts** | ré éolien | 150 | 45,3 s | 1 981 | zone |
| `danger` | `DANGER.MB` | **Ce qui Attend Sous l'Eau** | do phrygien | 136 | 49,9 s | 1 764 | zone |
| `tour` | `TOUR.MB` | **La Tour de Stratagus** | sol mineur harm. | 125 | 46,5 s | 1 056 | zone |
| `combat` | `COMBAT.MB` | **Le Fer et la Pince** | si éolien | **200** | 24,5 s | 1 215 | **surcouche** |
| `mort` | `MORT.MB` | **Le Marais Referme** | do éolien | 125 | 31,2 s | 659 | **surcouche** |
| `victoire` | `VICTOIRE.MB` | **Par la Trouée de Ciel** | ré mixolydien | 150 | 26,1 s | 1 141 | **surcouche** |

**Total sur le volume : 16 010 octets**, sur ~28 Mo libres — le nombre de pièces
ne coûte rien.

⚠ **Ce qui coûte, c'est la plus grosse de chaque tampon.** Le moteur en a deux,
et chaque pièce doit tenir dans le sien :

| Tampon | Limite | Pièces | La plus grosse | Marge |
| --- | ---: | --- | ---: | ---: |
| **zone** | 2 304 o | `accueil`, `village`, `nord`, `riviere`, `sud`, `danger`, `tour` | `VILLAGE.MB`, 2 285 o | 19 o |
| **surcouche** | 1 280 o | `COMBAT`, `MORT`, `VICTOIRE` | `COMBAT.MB`, 1 215 o | 65 o |

Les commandes des `README.md` passent donc `--max 2304` pour les thèmes de zone
et `--max 1280` pour les trois surcouches : la conversion **échoue** au lieu de
livrer un flux qui déborderait à l'exécution.

`village` est à 19 octets de la limite de zone. Toute retouche de cette pièce
doit être reconvertie avant d'être crue ; les six autres thèmes de zone ont
entre 234 et 1 248 octets de marge.

`mort` et `victoire` se convertissent en plus avec **`--no-loop`** : elles se
jouent une fois et laissent le silence.

---

## 2. Les 35 clairières → leur zone → leur fichier

Numérotation, `hub` et cases repris de `SCOSWAMP.MORE/carte.json` (35 entrées,
vérifié) et de `SCOSWAMP/DOCS/CARTOGRAPHIE.md`. La répartition en zones est
**identique** à celle de `../propositions/INDEX.md` § 2, à une exception près,
signalée en gras : `courbensaule` est fondue dans `village` (voir § 4).

| # | `hub` | Titre | (x,y) | Zone | Fichier |
| ---: | ---: | --- | :---: | --- | --- |
| 1 | 078 | Route de Courbensaule | (0,0) | **`village`** | `VILLAGE.MB` |
| 2 | 234 | Le Patrouilleur vert | (2,0) | `nord` | `MARAISNO.MB` |
| 3 | 084 | Le Maître des Jardins | (3,0) | `nord` | `MARAISNO.MB` |
| 4 | 232 | Les deux loups | (4,0) | `nord` | `MARAISNO.MB` |
| 5 | 218 | Feu follet à l'orée | (1,1) | `nord` | `MARAISNO.MB` |
| 6 | 121 | Le croisement | (2,1) | `nord` | `MARAISNO.MB` |
| 7 | 161 | Le Géant | (4,1) | `nord` | `MARAISNO.MB` |
| 8 | 019 | Clairière aux brigands | (0,2) | `nord` | `MARAISNO.MB` |
| 9 | 153 | Le bassin de Vase | (1,2) | `danger` | `DANGER.MB` |
| 10 | 088 | Scorpion et nain | (2,2) | `danger` | `DANGER.MB` |
| 11 | 202 | Le nid de l'Aigle | (3,2) | `nord` | `MARAISNO.MB` |
| 12 | 270 | Sables mouvants | (4,2) | `danger` | `DANGER.MB` |
| 13 | 295 | La Rivière Croupie | (1,3) | `riviere` | `RIVIERE.MB` |
| 14 | 183 | Sommet de la falaise | (2,3) | `riviere` | `RIVIERE.MB` |
| 15 | 045 | **Le pont sur la rivière Croupie** | (3,3) | `riviere` | `RIVIERE.MB` |
| 16 | 304 | Le Perroquet / Maîtresse des Oiseaux | (0,4) | `sud` | `MARAISUD.MB` |
| 17 | 094 | La brume fétide | (1,4) | `sud` | `MARAISUD.MB` |
| 18 | 179 | Le pique-nique suspect | (2,4) | `sud` | `MARAISUD.MB` |
| 19 | 319 | La clairière des scorpions | (3,4) | `danger` | `DANGER.MB` |
| 20 | 047 | Trois chemins herbeux | (4,4) | `sud` | `MARAISUD.MB` |
| 21 | 031 | Bassin de cristal | (5,4) | `sud` | `MARAISUD.MB` |
| 22 | 367 | Les Fleurs d'Angoisse | (0,5) | `danger` | `DANGER.MB` |
| 23 | 348 | La Licorne | (1,5) | `sud` | `MARAISUD.MB` |
| 24 | 227 | La clairière des combats | (2,5) | `sud` | `MARAISUD.MB` |
| 25 | 187 | Herbe à Pinces | (3,5) | `danger` | `DANGER.MB` |
| 26 | 309 | Orques des Marais | (4,5) | `danger` | `DANGER.MB` |
| 27 | 125 | Cul-de-sac de la Bête | (0,6) | `danger` | `DANGER.MB` |
| 28 | 022 | La clairière des Arbres-Épées | (1,6) | `danger` | `DANGER.MB` |
| 29 | 165 | Tente aux araignées | (3,6) | `danger` | `DANGER.MB` |
| 30 | 230 | Clairière des grenouilles | (4,6) | `sud` | `MARAISUD.MB` |
| 31 | 044 | La rivière profonde | (1,7) | `riviere` | `RIVIERE.MB` |
| 32 | 314 | Clairière du Maître des Loups | (1,8) | `sud` | `MARAISUD.MB` |
| 33 | 058 | **Le large rond-point (départ)** | (2,8) | `sud` | `MARAISUD.MB` |
| 34 | 390 | Pierres et tronc | (3,8) | `sud` | `MARAISUD.MB` |
| 35 | 082 | Bête du bassin | (4,8) | `sud` | `MARAISUD.MB` |

**Répartition : `sud` 12 · `danger` 10 · `nord` 8 · `riviere` 4 · `village` 1.**

Les trois pages disputées (`CARTOGRAPHIE.md:810-820`) sont arbitrées comme dans
le dossier voisin : **363** → clairière 2, **394** → clairière 21, **330** →
clairière 34. Deux dossiers de propositions qui trancheraient différemment
rendraient les lignes `MU` incomparables.

Les pages hors clairière (296 sur 412) suivent la règle générale — la musique de
la dernière clairière continue — sauf les ensembles listés dans chaque
`README.md` : prologue et sortie (`village`), tour (`tour`), combats et morts
(surcouches), victoires.

---

## 3. Six voix, deux puces : comment la stéréo est obtenue

C'est la différence de fond avec `../propositions/`, et elle mérite d'être
expliquée parce qu'elle n'est **pas** un réglage.

`midi_to_mb.py` ne laisse pas choisir la voix. À chaque frontière, les notes qui
continuent gardent la leur ; les notes qui commencent sont servies **de l'aiguë
à la grave**, dans les voix libres prises dans l'ordre `0, 3, 1, 4, 2, 5`,
c'est-à-dire en alternant les deux AY. Les voix 0-2 sortent à gauche, 3-5 à
droite.

Deux conséquences, et deux règles d'écriture qui en découlent :

1. **Chaque partie doit rester dans sa bande de registre.** Si deux parties se
   croisent, elles échangent leur puce. `compose.py` fournit `voicing()` et
   `pick()` pour poser chaque figure d'accord dans une fenêtre fixe.
2. **Chaque partie doit sonner sur chaque temps fort**, en attaquant ou en
   tenant. Si une partie se tait au moment où les cinq autres attaquent, les
   cinq se décalent d'un cran et changent toutes de côté. `Piece.write()` le
   vérifie et le signale (`Piece.holes()`).

Le résultat, mesuré par `verifier.py` sur les dix pièces, est stable :

| voix | côté | ce qui s'y trouve, dans les dix pièces |
| ---: | :---: | --- |
| 0 | **gauche** | la mélodie, seule |
| 1 | gauche | une voix médiane |
| 2 | **gauche** | la basse, seule |
| 3 | **droite** | l'arpège ou l'ostinato, l'essentiel du mouvement |
| 4 | droite | une voix médiane |
| 5 | **droite** | le bourdon, seul, immobile |

Soit : **la mélodie et la basse à gauche, le mouvement et le bourdon à droite**,
les voix d'accompagnement partagées. Les trois parties médianes (contre-chant,
accords tenus, arpège) échangent parfois les voix 1, 3 et 4 selon leur hauteur
du moment — c'est audible comme une largeur, pas comme un défaut.

Vérification :

```sh
python3 verifier.py nord/nord.mid --bpm 150
```

Aucune des dix pièces n'abandonne une seule note à la réduction (polyphonie
maximale = 6 exactement, jamais 7).

---

## 4. Ce que ce style change par rapport au dossier Renaissance

| | `../propositions/` (Renaissance) | **ce dossier** (fantasy moderne) |
| --- | --- | --- |
| Sources | onze pièces XV<sup>e</sup>-XVIII<sup>e</sup>, Mutopia, domaine public | dix compositions originales, GPL v3 |
| Voix | 3, mono en pratique | **6**, stéréo écrite |
| Taille max | 1 058 o (`MARAISNO.MB`) | 2 285 o (`VILLAGE.MB`) |
| Tampons | tout tient en 1 280 o | **zone 2 304 o**, surcouche 1 280 o |
| Langage | contrepoint vocal, cadences fonctionnelles, sensible | modes (dorien, phrygien, mixolydien, éolien), bourdons, quintes à vide, ostinatos |
| Forme | celle de l'œuvre d'origine | intro - A - B - A', écrite pour boucler sans couture |
| Tempo | 120-200, celui du genre | 125-200, jamais en dessous de 125 |
| Ce qui identifie une zone | le timbre du répertoire | **un procédé** : l'ostinato fixe du `nord`, le demi-ton phrygien du `danger`, la seconde augmentée de la `tour`, le bourdon de quinte de la `riviere` |
| Zones | 11 | 10 (`courbensaule` fondu dans `village`) |

Trois différences méritent une décision, pas un goût :

- **Le tampon.** Six voix coûtent le double d'octets pour la même durée. C'est
  ce qui a fixé les deux tailles du moteur : **2 304 octets pour une zone,
  1 280 pour une surcouche.** `COMBAT` et `VICTOIRE` ont été réécrites pour la
  seconde — le combat a perdu sa reprise A' (20 mesures au lieu de 28, ce qui
  lui va : une mêlée boucle court) et la victoire sa quatrième phrase.
- **L'unité.** Le dossier Renaissance emprunte onze langages à onze
  compositeurs ; celui-ci en a un seul, décliné. Le premier a plus de variété
  et moins de cohérence ; le second l'inverse. La question est de savoir si le
  Marais doit sonner comme une anthologie ou comme un lieu.
- **L'époque.** *Le Marais aux Scorpions* est un livre de 1984 et l'Apple IIe
  une machine de 1983 ; le style moderne assume l'anachronisme du portage, le
  style Renaissance assume celui du récit. Aucun des deux n'a tort.

Les deux dossiers sont **interchangeables fichier par fichier** : les noms de
disque (`MARAISNO.MB`, `DANGER.MB`, …) et la carte des zones sont les mêmes.
On peut prendre `DANGER.MB` ici et `TOUR.MB` là.

---

## 5. Refabriquer tout le dossier

```sh
cd /Users/gistair/src/pom2adventure/SCOSWAMP.MORE/MUSIC/propositions-moderne
M=../../midi_to_mb.py
(cd accueil  && python3 accueil.py   && python3 $M accueil.mid   ACCUEIL.MB.BIN  --bpm 136 --max 2304 --wav ACCUEIL.wav)
(cd village  && python3 village.py   && python3 $M village.mid   VILLAGE.MB.BIN  --bpm 166 --max 2304 --wav VILLAGE.wav)
(cd nord     && python3 nord.py      && python3 $M nord.mid      MARAISNO.MB.BIN --bpm 150 --max 2304 --wav MARAISNO.wav)
(cd riviere  && python3 riviere.py   && python3 $M riviere.mid   RIVIERE.MB.BIN  --bpm 125 --max 2304 --wav RIVIERE.wav)
(cd sud      && python3 sud.py       && python3 $M sud.mid       MARAISUD.MB.BIN --bpm 150 --max 2304 --wav MARAISUD.wav)
(cd danger   && python3 danger.py    && python3 $M danger.mid    DANGER.MB.BIN   --bpm 136 --max 2304 --wav DANGER.wav)
(cd tour     && python3 tour.py      && python3 $M tour.mid      TOUR.MB.BIN     --bpm 125 --max 2304 --wav TOUR.wav)
(cd combat   && python3 combat.py    && python3 $M combat.mid    COMBAT.MB.BIN   --bpm 200 --max 1280 --wav COMBAT.wav)
(cd mort     && python3 mort.py      && python3 $M mort.mid      MORT.MB.BIN     --bpm 125 --no-loop --max 1280 --wav MORT.wav)
(cd victoire && python3 victoire.py  && python3 $M victoire.mid  VICTOIRE.MB.BIN --bpm 150 --no-loop --max 1280 --wav VICTOIRE.wav)
```

Chaque ligne entre dans son sous-dossier, d'où le `../../midi_to_mb.py` : c'est
aussi la forme utilisée dans les `README.md`. Le bloc entier se recolle tel quel
dans un shell ; il s'arrête à la première erreur si l'on a fait `set -e`.

`--vol` reste au défaut `13,11,11,12,11,11` partout : mélodie et arpège un cran
devant, le reste au même niveau. Rien ne justifie d'en changer avant d'avoir
écouté sur la carte.

---

## 6. Les fichiers de l'atelier

| Fichier | Rôle |
| --- | --- |
| `compose.py` | le module : noms de notes, modes, accords, `voicing`, `ostinato`, `pedal`, `bed`, `progression`, `arpeggio`, `double`, la classe `Piece` qui écrit le MIDI et diagnostique |
| `verifier.py` | rejoue la réduction de `midi_to_mb.py` et dit, voix par voix, ce qui sortira à gauche et à droite |
| `<zone>/<zone>.py` | la pièce, en notation texte lisible |
| `<zone>/<zone>.mid` | le MIDI à six pistes, entrée de `midi_to_mb.py` |
| `<zone>/<NOM>.MB.BIN` | le flux MB1 que le lecteur 6502 joue |
| `<zone>/<NOM>.wav` | le rendu, non suivi par git |

`compose.py` généralise `../accueil.py`, qui mêlait composition, MIDI, MB1 et
rendu dans un seul fichier pour trois voix. Il n'écrit **que** du MIDI : le MB1
et le WAV viennent de `midi_to_mb.py`, donc du même code que le disque.
