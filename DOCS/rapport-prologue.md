# L'entrée dans le jeu — prologue de Bourbenville

Branche : `feat/scoswamp-prologue`
Date : 2026-09-04

Ce rapport couvre la mise en place de l'entrée dans SCOSWAMP : la Feuille
d'Aventure qui présente au lieu d'aligner trois nombres, et le village de
Bourbenville rendu parcourable avant qu'on choisisse un employeur.

---

## 1. Ce qui a été livré

### 1.1 La Feuille d'Aventure présente

`roll_character` (SCOSWAMP/SRC/scoswamp.c) affichait un titre, trois lignes de
chiffres, l'équipement, la règle du plafond, puis « [ESPACE] entrer dans le
Marais ». Le joueur entrait dans le Marais sans savoir ce qu'est l'Anneau de
Cuivre — qu'il porte pourtant au doigt depuis l'introduction du livre — ni
pourquoi trois hommes l'attendent au village.

Deux lignes ont été ajoutées, en données, par le catalogue de messages :

```
Vous etes un aventurier : l'Anneau de Cuivre a votre doigt montre le nord
et chauffe devant le Mal. Trois hommes de Bourbenville cherchent un heros.
```

```
You are an adventurer: the Copper Ring on your finger points north
and warms before Evil. Three men of Marshville are seeking a hero.
```

Les deux faits viennent de l'introduction du livre (« La Sorcière et
l'Anneau ») et du paragraphe 240. Le détail complet de l'Anneau vit sur une
page (417), pas dans le catalogue : une page ne coûte rien à la RAM.

**Coût mémoire — zéro octet de code, et même huit de moins.** Les quatre
`gotoxy` + `cprintf` de l'écran qui n'avaient pas d'argument de format sont
devenus des appels à `print_at()`, qui existait déjà : un appel au lieu de
deux. `roll_character` vit dans la Language Card (`#pragma code-name "LC"`),
où il ne restait que 42 octets — la première version, en `gotoxy` + `cprintf`,
débordait le segment de 8 octets et le lien échouait.

Le catalogue a par ailleurs été allégé : `M_CHANCEUX2` et `M_MALCHANCEUX2`
portaient mot pour mot le même texte que `M_CHANCEUX` et `M_MALCHANCEUX`. Les
deux doublons sont supprimés et les deux points d'appel pointent sur les
originaux (25 octets rendus côté français, la langue qui dimensionne
`MSG_BYTES`).

Bilan au lien :

| | avant | après |
| --- | --- | --- |
| marge mémoire principale | 184 o | 67 o |
| segment LC ($D400, 3 072 o) | 3 030 o | 3 040 o |
| `MSG_BYTES` | 1 413 | 1 537 |

Les 117 octets consommés sont **tous** des données : +124 de catalogue, +1 de
mémoire des clairières, −8 de code. `check-memory.sh` répond « OK : tient en
mémoire ».

### 1.2 Le prologue jouable — pages 412 à 418

Sept pages nouvelles, en français et en anglais, un fichier par page dans
`TEXTFR/N400/` et `TEXTEN/N400/` :

| Page | Titre | Rôle |
| --- | --- | --- |
| 412 | La place de Bourbenville | le carrefour, description longue, porte `V 413` |
| 413 | Bourbenville | la même place en deux lignes, à la deuxième visite |
| 414 | La salle de la taverne | les clients, le colosse aux deux loups, Grognard dans son coin |
| 415 | La boutique du vieil homme | il dit où habitent Gayolard et Pompatarte, et se tait sur la tour |
| 416 | Le bout du village | Gayolard à son tour de potier, la maison de Pompatarte, la tour de Stratagus au nord |
| 417 | L'Anneau de Cuivre | les deux pouvoirs de l'Anneau, mot pour mot d'après l'introduction |
| 418 | Ce qu'on dit des trois hommes | les trois missions, telles que le village les raconte |

**Le graphe.** Un seul point d'entrée : un choix ajouté à la page 240, `C 412
Faire un tour au village avant de choisir` (`C 412 Take a turn around the
village before choosing`). C'est l'endroit naturel — Grognard vient de dire
qu'il y a trois hommes dans ce village. Toutes les sorties du prologue
ramènent à la place (412) ; la place ramène au 240, où les trois offres
s'ouvrent (240 → 205 → 335 / 255 / 027). Aucune page existante ne change de
sens : la seule modification hors du prologue est cette ligne de choix
ajoutée en fin de fichier, dans les deux langues.

**La directive `V`.** La place porte `V 413`. La deuxième fois qu'on y revient
— et on y revient jusqu'à cinq fois — le moteur court-circuite la longue
description et sert la courte, avec la même liste de directions. C'est
exactement l'usage que le livre fait de « Si vous y êtes déjà venu,
rendez-vous au… », et vérifié dans l'émulateur (§ 3).

**Effet de bord nécessaire :** `SCENE_MEMORY_SIZE` passe de 52 à 53 octets
(rules.h / rules.c). À 52 octets, la mémoire des clairières s'arrêtait au
paragraphe 415 : les pages 416 à 418 n'auraient jamais été enregistrées, et
toute ligne `V` posée au-delà aurait échoué **en silence**. Coût : un octet de
BSS et un octet de sauvegarde. Les dix emplacements de `SCOSWAMP/SAVE/` sont
vides (2 octets chacun), aucune partie réelle n'est invalidée.

---

## 2. Fidélité au livre — et trois écarts assumés

Tous les faits du prologue sortent du livre, et d'aucune autre source :

- **L'Anneau de Cuivre** (page 417) : introduction « La Sorcière et l'Anneau ».
  L'anneau montre le nord et empêche de perdre son chemin ; il **se réchauffe
  en présence d'un être malfaisant, même si celui-ci fait de grandes
  démonstrations d'amitié** ; il est resté **froid** une semaine entière chez
  des brigands « rudes et brutaux » mais honnêtes à leur manière, et a
  **prévenu** devant des grottes où l'on pratiquait la magie noire. La formule
  demandée — « chaud devant le Mal, froid devant le Bien » — est donc **exacte**
  et la page la reprend telle quelle en conclusion.
- **La taverne et le colosse aux deux loups** (page 414) : paragraphe 1.
- **Le vieil homme appuyé contre la vitrine de sa boutique** (page 415) et
  **la petite maison de Gayolard en bordure du village, avec son jardin et sa
  poterie** (page 416) : paragraphe 335.
- **La grande maison de Pompatarte au bord du marché** (pages 412, 416) :
  paragraphe 27.
- **La tour de Stratagus près du marais, cernée de statues grimaçantes** (page
  416) : paragraphe 255.
- **Les trois missions** (page 418) : la baie d'Anthérique (371), la carte
  jusqu'à Courbensaule (173), les Amulettes d'argent des sorciers du Marais
  (206). Le jugement de Grognard — le premier sert le Bien, le deuxième est un
  mystère, le troisième s'est mis au service du Mal — est celui du 205.

Aucune règle nouvelle, aucun objet nouveau, aucune Pierre distribuée : le
prologue ne porte **que** des lignes `T`, `V` et `C`. Il ne touche ni à
l'ENDURANCE, ni à la CHANCE, ni au sac.

### Trois écarts par rapport à la commande

1. **« La Lance Tordue » n'est pas à Bourbenville.** Le livre la situe à
   **Courbensaule**, la ville au nord du Marais : c'est l'une de ses trois
   auberges (paragraphes 78, 214, 280, 395), on y dort au retour, pas au
   départ. La taverne du paragraphe 1, à Bourbenville, n'a pas de nom dans le
   livre. La page 414 la laisse donc sans nom. La nommer « La Lance Tordue »
   aurait déplacé un lieu du livre.
2. **La boutique d'Alphonse Mâchefer n'est pas à Bourbenville non plus.**
   Paragraphe 150 : « la rue qui mène à la sortie de la ville » — de
   Courbensaule — et c'est une scène de **retour**, où l'on troque contre des
   Pierres les objets rapportés du Marais. La page 415 met à sa place le vieil
   homme du paragraphe 335, qui est bien de Bourbenville, lui, et qui vend de
   la corde et des lanternes, rien de magique.
3. **Les trois missions sont données comme rumeur, pas comme contrat.** Le
   livre ne les révèle qu'en visitant chaque homme, et chacun y attache ses
   conditions (six Pierres bénéfiques ou neutres chez Gayolard, six maléfiques
   ou neutres et 500 Pièces d'Or par Amulette chez Stratagus, cinq Pierres
   neutres et la moitié des bénéfices chez Pompatarte). La page 418 dit ce que
   chacun **cherche** — c'est public, le 205 le dit : « tous trois ont fait
   savoir qu'ils cherchaient un aventurier » — et laisse les termes exacts aux
   pages 371, 206 et 173. Le joueur sait donc ce qu'il choisit sans que le
   prologue ait volé leur scène aux trois hommes.

Le nom anglais du village suit le corpus existant : **Marshville** (et non un
nom inventé), et Courbensaule reste Courbensaule, comme dans TEXTEN/N150/N173.

---

## 3. La musique : elle n'existe pas

La commande demandait de vérifier que les nouvelles pages portent
`MU VILLAGE.MB` et que `MU ACCUEIL.MB` ne coupe pas trop tôt sur la page 000.
**Ni la directive `MU`, ni les fichiers `.MB`, ni aucune couche musicale
n'existent dans ce dépôt.** Vérifié :

- aucun fichier `*.MB` dans l'arbre ;
- aucune occurrence de `MU `, `VILLAGE.MB` ou `ACCUEIL.MB` dans les sources,
  les outils, les manifestes ou le corpus ;
- `DIRECTIVE` dans `reflow_txt.py` et `classify_line()` dans `scoswamp.c` ne
  connaissent pas `MU` ;
- `SCOSWAMP/SRC/sfx.h` le dit en toutes lettres : « Le Mockingboard viendra
  plus tard ; ces routines ne servent que le haut-parleur », et `TODO.md`
  (lignes 229 et 553) le range dans ce qui reste à faire.

**Aucune ligne `MU` n'a donc été écrite.** C'était le point important : le
moteur ne reconnaît pas ce préfixe, et `classify_line` aurait rangé
`MU VILLAGE.MB` dans le **corps de la page** — le joueur aurait lu
« MU VILLAGE.MB » à l'écran, au milieu de la description du village. Écrire
une directive que le moteur ignore n'est pas neutre ici : elle s'affiche.

Ce qu'il faudrait pour la poser réellement, le jour venu : un préfixe `MU` dans
`DIRECTIVE` (reflow_txt.py) et dans `classify_line` (scoswamp.c), un champ dans
`AppState`, un chargeur, et une couche Mockingboard. Les sept pages du prologue
seront alors les premières à l'accueillir — elles forment un lieu unique, ce
qui est exactement le cas d'usage d'un thème de village.

De la même façon, `SCOSWAMP.MORE/carte.json` et `SCOSWAMP/DOCS/CARTOGRAPHIE.md`
n'existent pas dans le dépôt : il n'y a donc pas de clé `depart_prologue` à
mettre à jour. Les trois missions ont été relues dans le livre lui-même.

---

## 4. Côté image

Les sept pages n'ont pas d'illustration, et **ce n'est pas un blocage** : une
page sans `.RLE.BIN` retombe sur le texte plein écran, ce que le moteur fait
sans broncher — vérifié dans l'émulateur, les sept pages s'affichent en 80
colonnes. Le précédent existe déjà : les pages 407 à 411, ajoutées par un lot
antérieur, ne sont ni illustrées ni inscrites dans
`SCOSWAMP.MORE/scene_manifest.jsonl` (qui s'arrête à l'entrée 406).

`scene_manifest.jsonl` n'a donc **pas** été modifié : le pipeline ne l'exige
pas pour que le jeu tourne, et y écrire une entrée sans savoir produire la
planche donnerait un manifeste qui ment. Ce qui manque, précisément :

| Pages sans illustration | Origine |
| --- | --- |
| 407 – 411 | lot antérieur |
| 412 – 418 | ce lot (prologue) |

Soit 12 planches sur 419 (`check-project.sh` : « Images : 407 / 419 scènes
illustrées (97 %) »). Les décors utiles pour les produire sont tous déjà
décrits dans le livre : une place de bourgade en terre battue, une salle de
taverne, une devanture de boutique, un jardin de potier avec une tour noire à
l'horizon, un anneau de cuivre au doigt.

---

## 5. Tests

| Test | Résultat |
| --- | --- |
| `python3 SCOSWAMP.MORE/TOOLS/reflow_txt.py SCOSWAMP` | `problemes : 0` |
| idem `--derive` (recoupement mécanique FR ↔ EN) | `problemes : 0` |
| forme canonique | les 14 fichiers neufs et le 240 modifié sont déjà canoniques : le compteur « à réécrire » reste à 62, sa valeur d'avant le lot |
| `cd SCOSWAMP/SRC && make` | OK, marge de 67 octets |
| `make hdv` | `SCOSWAMP: 1298 files, 7371 blocks` |
| `./tools/check-project.sh` | OK — 419 FR + 419 EN |
| émulateur, parcours FR complet | 412 → 414 → 418 → 412 → 417 → 412 → 416 → 412 → 415 → 412 → 240 → 205 |
| émulateur, parcours EN | 240 → 412 → 414 → 418 → 412 |

Commande : `../pom2/build/POM2 --preset iie dist/SCOSWAMP.HDV --ai-control=6512`,
pilotage par `POST /keyboard` et lecture de l'écran 80 colonnes par `GET /mem`
(colonnes paires en banque `aux`, impaires en `main`).

### Capture 1 — la Feuille d'Aventure

```
                                                        9/9      18/18      8/8


FEUILLE D'AVENTURE

HABILETE   9   (1 de + 6)
ENDURANCE 18   (2 des + 12)
CHANCE     8   (1 de + 6)

Une epee, une cotte de mailles, un sac a dos, 20 Pieces d'Or.
Aucun de ces trois totaux ne pourra depasser sa valeur de depart.

Vous etes un aventurier : l'Anneau de Cuivre a votre doigt montre le nord
et chauffe devant le Mal. Trois hommes de Bourbenville cherchent un heros.

[ESPACE] entrer dans le Marais
```

### Capture 2 — la place, première visite (page 412)

```
  a place de  ourbenville   :       :                   9/9      18/18      8/8
Vous laissez Grognard a sa chope et poussez la porte de la taverne. Dehors,
Bourbenville s'etale au soleil : une bourgade de terre battue posee sur les
basses terres, la derniere avant le Marais. Des voyageurs y passent tous les
jours et personne ne se retourne sur votre heaume d'acier.

Sur la place, un vieil homme somnole contre la vitrine de sa boutique. Plus
loin, le marche bruit de cris et de volailles ; une grande maison en occupe
tout un cote, volets clos. La rue se termine au bout du village, sur des
jardins. Et vers le nord, la ou la terre devient molle, une tour noire se
decoupe sur le ciel.

Trois hommes de ce village cherchent un aventurier. Rien ne presse encore :
Grognard vous attend, et sa chope est pleine.

A) La salle de la taverne               B) La boutique du vieil homme
C) Le bout du village                   D) Regarder votre Anneau
E) Retourner a la table de Grognard
```

(La barre de titre est en vidéo inverse ; les majuscules initiales manquent
dans cette transcription parce que la lecture par `/mem` rend les codes de
vidéo inverse — c'est un artefact de la capture, pas de l'affichage.)

### Capture 3 — la place, deuxième visite (la ligne `V 413` a joué)

```
  ourbenville   :       :                               9/9      18/18      8/8
Vous revenez sur la place. Le vieil homme n'a pas bouge de sa vitrine, le
marche crie toujours, et la tour noire est toujours la, au nord.

A) La salle de la taverne               B) La boutique du vieil homme
C) Le bout du village                   D) Regarder votre Anneau
E) Retourner a la table de Grognard
```

---

## 6. Ce qui reste

- **La musique.** Rien n'existe : ni directive, ni format, ni couche sonore.
  C'est un lot à part entière (§ 3), et le prologue en est le premier client
  naturel.
- **Les 12 planches manquantes** (407 à 418), § 4.
- **La marge mémoire est à 67 octets.** Le prochain lot qui ajoute une paire de
  messages devra rendre des octets ailleurs, ou déplacer du texte d'interface
  vers une page — c'est ce que fait déjà ce lot pour le détail de l'Anneau.
- **Un second point d'entrée.** Le prologue ne s'atteint que depuis le 240. Un
  joueur qui, à la page 095, refuse le conseil de Grognard (→ 122 → 296) ne
  verra jamais le village. C'était volontaire — n'ouvrir qu'une porte, et ne
  pas toucher au sens des pages existantes — mais un choix supplémentaire au
  122 serait cohérent.
