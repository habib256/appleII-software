# dev — TODO

Backlog du développement **logiciel Apple II** (les jeux). L'émulateur qui
les fait tourner a le sien, dans `../pom2/TODO.md`. Même convention que lui :
`🟠 haute · 🟡 moyenne · 🟢 basse`, effort indicatif en *italique*, fichier en
`backticks`.

État au 2026-08-29. Cible : Apple //e enhanced, cc65 `apple2enh`, ProDOS 8.

---

## Priorité : débloquer la mémoire pour le système de combat

C'est la contrainte qui bloque le reste. Carte mémoire **mesurée** sur
`SCOSWAMP.BIN` tel qu'il est construit aujourd'hui (fichier `.map` du linker,
pas une estimation) :

| Zone | État |
| --- | --- |
| `$0800-$0BFF` | tampon d'E/S ProDOS (via `apple2enh-iobuf-0800.o`) |
| `$0C00-$1FFF` | **5 Ko libres, inutilisés** |
| `$2000-$3FFF` | HGR page 1 (et le lanceur `SCOSWAMP.SYSTEM`, mort après le saut) |
| `$4000-$97xx` | code + données |
| `$97xx-$A3D9` | BSS |
| `$B700-$BF00` | pile C (2 Ko) — **tas ≈ 4 900 octets** |
| `$D000-$FFFF` | Language Card — **16 Ko inutilisés** |
| AUX 64 Ko | seul `$400-$7FF` sert (page texte 80 col) — **~46 Ko libres** |

Par ordre de rendement décroissant :

- ✅ **1. `__HIMEM__ = $BF00`** — **fait le 2026-08-29**, pour faire entrer le
  moteur de combat. Le gain est **deja consomme** : apres le mode carte il
  reste **21 octets** avant la pile. La fenetre `$4000-$BF00` est pleine, et
  tout ce qui suit demandera le point 2 ou le point 4.
  Deux contreparties, dont une seule était prévue :
  - la prévue : plus de retour à BASIC, on sort par le QUIT ProDOS ;
  - **l'imprévue** : le binaire fait maintenant 22 Ko et s'étend jusqu'à
    `$97xx`, donc **BASIC.SYSTEM ne peut plus le lancer** — il place ses
    tampons de fichier juste sous `$9600` et refuse, avec un
    `NO BUFFERS AVAILABLE` suivi d'un `BREAK`. D'où `SCOSWAMP.SYSTEM`
    (`SRC/loader.c`), un fichier ProDOS SYS chargé en `$2000` par ProDOS
    lui-même, qui lit le jeu en `$4000` et lui saute dedans. BASIC.SYSTEM et
    STARTUP.BAS ne sont plus sur le disque : ProDOS exécute le premier fichier
    `.SYSTEM` du répertoire, et `B` vient avant `S`.

  **Piège du fichier de lien**, à connaître avant de retoucher `__HIMEM__` :
  `apple2enh.cfg` calcule la taille du BSS par
  `__HIMEM__ - __STACKSIZE__ - __ONCE_RUN__`. Quand le code déborde, cette
  soustraction passe en négatif et déborde en entier non signé : **ld65 ne
  signale rien et le binaire écrase la RAM d'à côté**. Un lien qui réussit ne
  prouve donc pas que le programme tient — vérifier l'adresse de fin du BSS
  dans le `.map`.

- 🟠 **2. Les ~46 Ko de RAM auxiliaire** — *2-3 j.* Le vrai gisement, et
  l'endroit naturel pour les données de combat (stats de monstres, tables de
  résolution, sprites) : ce sont des données en **lecture seule**, donc le
  cas d'usage exact de l'AUX. cc65 n'en sait rien et n'a pas besoin d'en savoir :
  un petit mover suffit, soit l'appel firmware `AUXMOVE` (`$C311`), soit un
  basculement `RAMRD`/`RAMWRT` autour d'une copie. Attention à ne pas marcher
  sur `$400-$7FF` (page texte 80 colonnes).

- 🟡 **3. `$0C00-$1FFF`** — *1 h.* 5 Ko déjà libres en RAM principale, entre le
  tampon ProDOS et HGR page 1. Utilisables immédiatement pour un buffer de
  travail sans rien réarchitecturer.

- 🟡 **4. La Language Card** — *1 j.* 16 Ko à `$D000-$FFFF`, avec un segment
  `LC` déjà prévu par `apple2enh.cfg` (`__LCADDR__ = $D400`). Demande un
  basculement de banque explicite.

**Reste accessible sans rien réécrire : 5 Ko en `$0C00-$1FFF`, 16 Ko en
Language Card, ~46 Ko en auxiliaire.**

---

## Corrigé le 2026-08-29 — gardé ici pour le *pourquoi*

Quatre bugs, tous vérifiés dans l'émulateur (pas seulement au lien) :

- **Le tas faisait 270 octets.** BSS finissait à `$8CF1`, la pile commençait à
  `$8E00`. Un `fopen` ProDOS réclame un tampon de 1 Ko aligné page, soit
  ~1 280 octets contigus : **aucun `fopen` ne pouvait aboutir**. Le symptôme
  était `errno=2` avec `ProDOS=$00` — trompeur, parce qu'en cc65 `errno=2`
  vaut **`ENOMEM`, pas `ENOENT`** (`errno.h` : `ENOENT` = 1). Et `_oserror = 0`
  disait déjà que ProDOS n'avait jamais été appelé : l'échec venait de
  `iobuf_alloc` (= `posix_memalign`) dans `libsrc/apple2/open.s`, avant la
  moindre requête MLI. Correctif : lier `apple2enh-iobuf-0800.o`, qui prend les
  tampons entre `$0800` et `__MAIN_START__` au lieu du tas — et raccourcit le
  binaire de ~1 230 octets au passage.
  → `SCOSWAMP/SRC/Makefile`, `build.sh`

- **`PLX` écrasait le flag N.** `hgr_loader.s`, `get_byte` finissait par
  `plx / sec / rts` : `PLX` positionne N et Z **d'après X**, pas d'après
  l'octet lu, qui est dans A. Le `bmi repeat_token` de l'appelant testait donc
  le signe de X. Résultat : **tout token RLE répété était décodé comme un token
  littéral**, le décodage partait en vrille et s'arrêtait sur l'EOF. C'était le
  bug bloquant des images. Correctif : `pha / pla` avant le `sec` pour
  recharger N/Z depuis A (`PLA` ne touche pas C).
  → `SCOSWAMP/SRC/hgr_loader.s`

- **`PLA` écrasait le flag Z.** Même fichier, `repeat_loop` faisait
  `pha / jsr advance_dst / pla` : le `PLA` détruisait le Z que `advance_dst`
  venait de poser pour signaler la fin de la page HGR. Latent sur le corpus
  actuel — aucune image ne finit par une répétition d'octet non nul — mais il
  aurait mordu au premier ré-encodage. L'octet répété passe maintenant par une
  case RAM (`rep_byte`) au lieu de la pile.

- **80STORE coupé et jamais restauré.** Le loader faisait
  `sta $C000/$C002/$C004` avant de décoder et ne remettait rien. Après une
  image, `cprintf` n'écrivait plus qu'en banque principale : une colonne sur
  deux perdue. Le loader mémorise maintenant `RD80STORE` (`$C018`) et le
  rétablit sur les deux chemins de sortie.

- **La sauvegarde d'écran ne gardait que la moitié de l'écran.**
  `memory_swap.c` copiait 1 Ko de `$400-$7FF`, mais en 80 colonnes l'écran est
  **à cheval sur deux banques** : colonnes impaires en RAM principale, paires
  en auxiliaire. La moitié auxiliaire n'était jamais sauvée — et c'est
  exactement ce que donnait le flash « 40 colonnes buggé » au retour de HGR.
  Deux tampons maintenant, atteints en basculant `PAGE2` sous 80STORE. De plus
  `switch_to_text()` faisait `TXTSET` **avant** `restore_text_screen()`,
  exposant une frame à moitié écrite : l'ordre est inversé, on repeint avant de
  rendre visible.
  → `SCOSWAMP/SRC/memory_swap.c`

- **L'image disque était périmée, et le bug déjà corrigé rejouait.** Le
  correctif iobuf ci-dessus était bien lié dans `SCOSWAMP.BIN` (13 334 o,
  14h34), mais `dist/SCOSWAMP.HDV` datait de 14h08 et portait l'entrée
  `SCOSWAMP` d'avant (14 371 o) : le jeu réaffichait un `errno=2 ProDOS=$00`
  qui n'existait plus dans le source. Une session de diagnostic pour une image
  pas reconstruite — le risque exact que l'entrée « un `make hdv` » du backlog
  annonçait, donc elle est faite. `make hdv` relie le binaire puis reconstruit
  le volume ; le boot loader ProDOS (1 Ko, les deux premiers blocs) est
  désormais versionné en `SCOSWAMP.MORE/TOOLS/prodos_boot.tmpl` pour que la
  cible parte d'un arbre propre, `dist/` étant ignoré par git. Le volume est
  monté depuis `SCOSWAMP/` moins `DOCS` et `SRC` : un nouvel asset n'a rien à
  déclarer.
  → `SCOSWAMP/SRC/Makefile`, `SCOSWAMP.MORE/TOOLS/prodos_boot.tmpl`

- **Mise en page fixe des pages de scène.** Le moteur affichait le fichier tel
  quel, ligne à ligne, en laissant la ligne `T <id> <titre>` s'imprimer avec
  son préfixe et en collant les choix à la suite du texte — donc à une hauteur
  qui dépendait de la longueur de la scène. Le mode mixte, qui ne montre que
  les 4 dernières lignes, n'avait donc aucune chance d'y trouver les choix.
  L'écran a maintenant trois zones fixes : **ligne 1** barre en vidéo inverse
  (titre + rappel des touches), **lignes 2-20** le texte, **lignes 21-24** les
  choix — deux par ligne quand ils tiennent dans une demi-largeur, ce qui fait
  entrer les 5 choix des 6 plus grosses scènes dans 4 lignes. Les 804 pages
  ont été repliées à 78 colonnes pour tenir dans les 19 lignes de corps (pire
  cas mesuré : 18), sans qu'un seul mot change.
  → `SCOSWAMP/SRC/scoswamp.c`, `SCOSWAMP.MORE/TOOLS/reflow_txt.py`

- **Deux pièges attrapés en câblant le moteur de combat**, tous deux invisibles
  au lien et à la compilation :

  1. **cc65 rend les structures par valeur de travers.** `combat_round()`
     rendait un `Round` ; à l'écran, un assaut à Forces d'Attaque **égales**
     blessait au lieu de faire esquiver. Le banc d'essai sur machine hôte ne
     pouvait pas l'attraper — il compile avec un vrai compilateur C. Le
     résultat passe désormais par un pointeur. À retenir pour tout le code de
     ce dépôt : sur cc65, on remplit une structure, on ne la rend pas.
  2. **Le verrou clavier arme au sortir du boot.** `dice_seed_from_keypress()`
     attendait une touche en comptant, pour semer les dés. Mais ProDOS laisse
     souvent une touche dans `$C000` avec son strobe armé : la fonction rendait
     la main aussitôt, avec un compte de zéro — **la même semence, donc le même
     personnage et la même partie à chaque lancement**. Elle vide le verrou
     avant d'attendre.
  → `SCOSWAMP/SRC/rules.c`, `SCOSWAMP/SRC/dice.c`

- **L'ecran de bataille, et le piege 80STORE qu'il a revele.** Un combat bascule
  desormais tout seul en mode mixte : l'illustration des deux adversaires
  occupe les 20 lignes du haut, l'echange d'assauts les 4 du bas, avec un
  bandeau qui porte les caracteristiques des DEUX combattants — la barre de
  titre, qui portait la Feuille d'Aventure, disparait sous l'image.
  Au premier essai, ces 4 lignes affichaient **deux textes entrelaces**, une
  colonne sur deux chacun : `enter_graphics()` coupe 80STORE, or le mixte est
  le seul mode graphique ou l'on **ecrit** du texte, et le firmware 80 colonnes
  atteint la banque auxiliaire par 80STORE + PAGE2. `switch_to_mixed()` le
  remet. L'image ne bouge pas pour autant : sous 80STORE l'ecran hi-res reste
  force sur la page 1 en banque principale.
  → `SCOSWAMP/SRC/memory_swap.c`, `SCOSWAMP/SRC/scoswamp.c`

- **Les messages de l'interface sont partis sur le disque.** 39 paires FR/EN
  en dur, 2 409 octets de litteraux, dans un binaire qui n'avait plus 21 octets
  de libre. Elles vivent maintenant dans `/SCOSWAMP/MSGFR` et `MSGEN`, et le
  jeu ne charge qu'une langue : **627 octets liberes**, et l'interface se
  traduit sans recompiler.
  `TOOLS/build_messages.py` est la source unique : il ecrit d'un meme geste
  l'enumeration C et les deux fichiers. Les editer separement decalerait tout
  le catalogue et le jeu afficherait les messages les uns pour les autres —
  d'ou le controle du nombre de lignes au chargement, qui refuse un catalogue
  incomplet en bloc plutot que de le decaler.
  → `SCOSWAMP/SRC/messages.c`, `TOOLS/build_messages.py`

- **Les Pierres Magiques se prennent au choix, depuis le texte.** Le livre ne
  les donne pas, il les fait choisir : « choisissez 6 Pierres de Magie, mais
  vous ne devrez prendre que des Pierres Malefiques ou Neutres » (Stratagus),
  six parmi les Benefiques et Neutres chez Gayolard, une Benefique chez le
  Maitre des Jardins. La ligne `PC <n> <cats>` dit cela, et l'ecran de choix
  n'offre que les categories permises — un bon sorcier ne donne pas de Pierre
  malefique. On peut prendre plusieurs fois la meme, comme le livre l'autorise.
  Les 4 pages concernees sont converties ; `reflow_txt.py --derive` **signale**
  toute page qui semble remettre une Pierre sans ligne `PC` ni `P`, parce que
  la formulation varie trop pour deviner sans risque.

- **Le verrou clavier etait lu deux fois.** `dice_seed_from_keypress` lisait
  `$C000` directement pour mesurer le temps d'attente du premier appui. Mais le
  firmware 80 colonnes du //e tient sa propre file d'entree : lire le verrou
  materiel dans son dos lui laissait la touche, et le `cgetc` suivant la rendait
  une seconde fois. Au demarrage, le `F` du choix de langue etait relu par
  l'ecran d'apres, qui passait tout seul — et l'ecran de choix des Pierres en
  prenait une sans qu'on ait appuye. La fonction passe maintenant par
  `kbhit()` / `cgetc()`.
  → `SCOSWAMP/SRC/dice.c`

- **Des bruitages sur le haut-parleur interne.** Cinq ponctuations pendant le
  combat : la lame qui touche, le coup encaisse, la double esquive, la chute
  d'une creature, la mort du heros. Tout est en assembleur (`sfx.s`) — une
  boucle C sur cc65 met plusieurs dizaines de cycles par tour, ce qui
  plafonnerait les sons dans les graves et lierait leur hauteur a l'humeur de
  l'optimiseur.
  La duree se paie : chaque palier d'un balayage coute `period * 5 * 12`
  cycles, et une chute de 60 a 200 mettait **plus d'une seconde** — une
  eternite quand la page aligne trois BRIGANDS. La plage a ete resserree.
  Le parametre qui compte est le nombre de demi-ondes par palier d'un
  balayage : peu de demi-ondes donnent un transitoire, que l'oreille entend
  comme un choc, beaucoup font chanter le balayage. C'est ce qui separe le
  coup d'epee de la chute d'un corps. Une note pure, elle, sonne comme un bip
  de terminal — c'etait le premier jet.
  Ces routines ne connaissent que `$C030`, present sur toutes les machines.
  **Le Mockingboard viendra plus tard** : il demandera une autre couche, pas
  une retouche de celle-ci.
  → `SCOSWAMP/SRC/sfx.s`

- **Les personnages changeaient de tete d'une image a l'autre.** Chaque image
  etait generee seule, a partir de sa seule page : rien ne reliait le Maitre
  des Loups d'une illustration a la suivante, ni la creature d'une scene a
  celle de son image de bataille, et le heros n'etait decrit que dans les
  prompts de bataille.

  On n'obtient pas la constance en demandant « le meme personnage » : il faut
  que **le meme texte** decrive le personnage dans tous les prompts ou il
  apparait. D'ou `SCOSWAMP.MORE/characters.json`, douze fiches ecrites une
  fois, que `build_manifest.py` injecte mot pour mot des qu'un alias est
  repere dans la page. Les 31 images de bataille sont regenerees ; le Maitre
  des Loups apparait dans trois d'entre elles et y est desormais le meme
  homme.

  Stratagus vient du livre (paragraphe 40) ; pour les autres le livre ne
  decrit presque rien, les illustrations portaient tout, et chaque fiche dit
  sa source. **Ne pas reformuler une fiche sans regenerer les images
  concernees** : c'est la constance du texte qui fait celle de l'image.

  Reste a decider : 135 pages sur 402 portent un personnage recurrent
  (Stratagus 40, Pompatarte 25, Gayolard 23, les loups 20, les brigands 20),
  et le heros est dans les 402. Les illustrations de scene n'ont pas ete
  regenerees.

  Et un detail de palette : les fiches disent « grey wolf pelts », or le gris
  n'existe pas en HGR — il ressort bleu. Les fiches gagneraient a nommer les
  six couleurs disponibles, mais les changer imposerait une regeneration.
  → `SCOSWAMP.MORE/characters.json`, `TOOLS/build_manifest.py`

- **Les Pierres se depensaient sans jamais toucher au sac.** 43 choix du corpus
  disent « Utiliser une Pierre de Feu » : ils partaient en `C` ordinaire, donc
  rien ne verifiait qu'on possedait la Pierre et rien ne la consommait. D'ou
  les deux symptomes signales — l'inventaire qui ne suit pas, et le droit de
  lancer un sort qu'on n'a pas. La ligne `CU <PIERRE> <id> <titre>` exige la
  Pierre et la consomme ; un choix dont la Pierre manque **s'affiche sans
  lettre** — on le voit, le livre l'ecrit, mais on ne peut pas le prendre.

- **Cinq rencontres ne se lancaient pas du tout**, dont le Maitre des Loups et
  ses deux betes (`N120`). Ces pages posent leurs adversaires en TABLEAU —
  `HABILETE ENDURANCE Premier Loup 7 5 Deuxieme Loup 6 6 Maitre des Loups
  11 10` — que le motif en phrase ne voyait pas. **Les pages ont ete
  corrigees**, pas l'outil : le corpus a maintenant une seule facon d'ecrire un
  bloc de stats, `<NOM> HABILETE: h ENDURANCE: e`, avec les noms en capitales.
  Une deuxieme grammaire dans l'analyseur aurait ete une dette permanente pour
  cinq pages. `N281` en profite pour perdre sa coquille : `ORQUEDES MARAIS`.

- **Le recoupement FR/EN etait aveugle a la moitie des directives** : il ne
  retenait que `M`, `MD`, `MS` et `CF` a l'entree, si bien que l'extension aux
  `CU` et `CL` ne servait a rien. Il enregistre tout desormais, et c'est ce qui
  a fait sortir trois pages ou l'anglais depensait une Pierre que le francais
  gardait — le corpus francais ecrivant `Pierre d Amitie`, avec une espace au
  lieu de l'apostrophe.

- **La barre parlait francais en partie anglaise.** Les caracteristiques
  s'affichent maintenant `SKL / STA / LCK`, les trois mots de Fighting Fantasy,
  et le rappel devient `I:BAG H:HELP`.

- **A la mort, on choisit** : recommencer une aventure, ou rendre la main a
  ProDOS. Avec ProDOS 2.4 c'est Bitsy Bye qui reprend, et l'on peut lancer
  autre chose sans redemarrer la machine.

- **Le choix des Pierres ne se repeint plus a chaque prise.** La liste des
  Pierres permises ne bouge pas ; seul le compteur change. Six Pierres, c'etait
  neuf lignes redessinees neuf fois.

- **Le mode carte a ete retire.** Il avait ete construit (fichier `MAP` genere
  depuis les directions de la prose, cercles numerotes, sentiers, rayons pour
  les chemins connus mais pas empruntes) et il fonctionnait. Il coutait
  **5 019 octets** — les primitives de trace HGR, l'ecran, le bitmap des
  clairieres visitees et quatre messages — dans une fenetre programme qui n'en
  a que 32 Ko. Retire, il reste **4 981 octets libres**.
  Ce qu'il faudrait pour le reprendre : la place (RAM auxiliaire ou Language
  Card), et les numeros de clairiere du livre — la carte affichait le numero
  du PARAGRAPHE, alors que le livre demande de porter celui de la CLAIRIERE,
  et 29 des 90 seulement le donnent en clair dans la prose.
  `SCOSWAMP.MORE/TOOLS/build_map.py` derivait la carte de la prose ; il a ete
  supprime avec le reste.

- **Le sac à dos demandait deux appuis.** `wait_key_at()` affiche une invite
  *et* consomme une touche ; l'appeler avant un `cgetc()` explicite en mangeait
  une pour rien. L'affichage est maintenant séparé de l'attente (`print_at`).
  → `SCOSWAMP/SRC/scoswamp.c`

---

## Backlog

### Portage / gameplay

- 🟠 **Convertir les 402 pages au nouveau format** — le moteur de combat et
  d'objets existe et tourne (voir plus bas), mais **le corpus ne s'en sert
  presque pas** : deux pages converties sur 402. C'est désormais le seul
  travail qui sépare le jeu du livre. Détail chiffré ci-dessous.
- 🟡 **SPACETRIP** — au point 0.1alpha, n'a pas reçu les correctifs mémoire de
  SCOSWAMP. Il utilise `fopen` de la même façon (`SPACETRIP/spacetrip.c:43,95`)
  et a donc **le même tas de 270 octets** : à vérifier en priorité, le bug est
  probablement identique et jamais diagnostiqué.
- 🟢 **`build_paths()` ignore `lang`** — `paths.c:32`, paramètre non utilisé
  (le choix de langue se fait par `chdir` dans `enter_asset_dir`). Soit le
  retirer de la signature, soit s'en servir.

### Outillage

- 🟡 **Câbler `reflow_txt.py` dans un `make check`** —
  `SCOSWAMP.MORE/TOOLS/reflow_txt.py` remet les pages au format du moteur et
  **vérifie les invariants de mise en page** : corps ≤ 19 lignes une fois
  replié à 78 colonnes, choix ≤ 4 lignes, titre ≤ 60 caractères, et pas un mot
  modifié. Il tourne à la main aujourd'hui ; sans lui dans le build, une page
  trop longue ne se verra qu'à l'écran, tronquée.

- 🟢 **Un test de non-régression du décodeur RLE** — les trois bugs 6502
  ci-dessus étaient tous invisibles au lien et n'ont été trouvés qu'en
  exécutant. `TOOLS/test_hgr_rle.c` existe : lui faire décoder tout le corpus
  `IMG/` et comparer à un rendu de référence donnerait le test qui **échoue**
  quand un flag est mal restauré.

### Le personnage et le combat : ce qui existe, ce qui reste

**Le moteur est là.** `SCOSWAMP/SRC/rules.c` porte les règles de *Défis
Fantastiques* telles que les pages liminaires du livre les énoncent, chaque
règle non évidente accompagnée de la phrase qui la fonde. Il ne connaît ni
l'écran ni ProDOS, ce qui permet de le passer au banc sur machine hôte :
`SCOSWAMP.MORE/TOOLS/test_rules.c`, cible ctest `rules`.

Ce qu'il couvre : création du personnage (1d6+6 / 2d6+12 / 1d6+6), le plafond
« jamais au-dessus du total de départ », Tentez votre Chance et son point de
CHANCE consommé, l'assaut (2d6 + HABILETÉ de chaque côté, égalité = esquive),
les blessures avec leurs quatre modificateurs de Chance, la Fuite et sa
blessure automatique, la mémoire des clairières (une créature laissée blessée
garde son ENDURANCE — le Marais est le seul livre où l'on revient sur ses pas),
les douze Pierres Magiques avec leurs trois catégories, leur consommation à
l'usage, la restitution de la moitié du total de départ pour les trois pierres
de caractéristique, le dé de la Malédiction, et l'interdiction de s'en servir
une fois le premier coup donné.

`SCOSWAMP/SRC/dice.c` fournit le hasard : un congruentiel dont on ne garde que
les bits de poids fort (un modulo 6 sur les bits bas d'un LCG donnerait des dés
biaisés), semé par le temps d'attente du premier appui de touche.

**Le format de page sait déjà dire :**

| Ligne | Effet |
| --- | --- |
| `M <hab> <end> <nom>` | la créature de la clairière |
| `MD <n>` | ses coups coûtent n ENDURANCE (défaut 2) |
| `MS <n>` | le combat cesse à n ENDURANCE (défaut 0) |
| `E <CARAC> <delta>` | effet appliqué en entrant |
| `P <PIERRE> <n>` | Pierres reçues en entrant |
| `CF <id> <titre>` | la Fuite, quand la page l'autorise |
| `CP <PIERRE> <id> <titre>` | choix qui remet une Pierre |

Et côté images : `IMG/<bucket>/B<id>.RLE` est l'illustration de bataille d'une
clairière, préférée à `N<id>.RLE` pendant le combat.

Le paragraphe 12 (le GÉANT) est converti dans les deux langues et sert de cas
d'école : il exerce `M`, `MD 4` (« vous perdez 4 points d'ENDURANCE au lieu de
2 »), `MS 6` (« si vous parvenez à réduire à 6 les points d'ENDURANCE du
Géant ») et `CF`. Le paragraphe 283 exerce `CP` : le Maître des Jardins donne
une Pierre bénéfique au choix.

**Ce qui reste.**

- ✅ **`CL` : Tentez votre Chance.** 15 scènes dérivées, dans les deux langues.
  Le livre ne *propose* pas ces deux issues, il ordonne le jet et annonce ce
  qui arrive dans chaque cas ; les laisser en choix libres revenait à demander
  au joueur de tirer les dés lui-même, et de tricher. Le moteur joue le jet une
  fois la page lue, montre le résultat (« Vous jetez les deux dés : 7, contre
  une CHANCE de 8 »), consomme le point de CHANCE et saute.
  La ligne porte un effet d'ENDURANCE optionnel **par branche**, parce que le
  livre en pose deux : « si vous êtes Chanceux, vous perdez 2 points
  d'ENDURANCE et vous vous rendez au 270 ». Ce coût appartient à la
  transition, pas à la page d'arrivée — le 270 est atteint depuis cinq pages,
  une seule fait perdre ces points.

- 🟠 **Les conditions qui restent : 39 choix**, et ce ne sont plus des jets de
  dés mais de la mémoire de partie :

| Ce que la condition demande | Choix |
|---|---|
| Un fait acquis (« Si vous avez déjà trouvé le buisson », « Si vous touchez le Chef ») | 33 |
| La possession d'un objet (« Si vous possédez l'Amulette en forme de Loup ») | 4 |
| Une clairière déjà visitée | 1 |
| Un seuil de caractéristique | 1 |

  Il faut donc un jeu de **drapeaux** — quelques dizaines de bits de partie,
  posés par une directive et lus par une autre — plus un `CI <objet> <id>` pour
  l'inventaire. Le bitmap des clairières visitées existait pour la carte ; il
  est parti avec elle et reviendra ici.

- ✅ **Les combats sont dérivés de la prose.** `reflow_txt.py --derive` lit le
  bloc de stats que les pages écrivent déjà en toutes lettres — `BETE DU
  BASSIN HABILETE: 8 ENDURANCE: 10` — et en fait une ligne `M`, puis retire le
  bloc du texte (le bandeau de combat l'affiche désormais). **24 combats
  dérivés sur 26**, plus les `MD` (« 3 au lieu de 2 »), les `MS`
  (« si vous réduisez à 6 ») et les `CF` (un choix qui parle de Fuite).

  **Pourquoi à la construction et pas dans le moteur** : l'Apple II n'a plus la
  place d'un analyseur de prose, la tolérance aux trois façons dont le corpus
  écrit un bloc de stats y serait fragile, et surtout le résultat serait
  invisible — alors qu'ici il atterrit dans le fichier, lisible dans un diff.
  L'auteur écrit toujours de la prose ; personne ne tape de directive.

  L'outil **recoupe FR et EN** : une divergence de stats entre les deux langues
  est une erreur de contenu, il la signale. Et il refuse de deviner : les 2
  pages à plusieurs adversaires (`N224` deux LOUPS, `N235` trois BRIGANDS)
  gardent leur prose et sortent dans le rapport, en attendant que le moteur
  sache mener un combat contre plusieurs créatures.

- 🟠 **La conversion du corpus**, chiffrée sur `TEXTFR/` :

| À convertir | Scènes |
|---|---|
| Un combat / un adversaire à affronter | 88 |
| ~~Un bloc de stats en clair → `M`~~ | ~~26~~ **26 faits** |
| Choix écrits comme une condition → `CL` / `CS` | 68 |
| Les Pierres Magiques (12 noms) → `P` / `CP` | 53 |
| Une variation chiffrée (« perdez 2 points d'ENDURANCE ») → `E` | 14 |
| Provisions / repas | 8 |
| Pièces d'Or | 7 |

  Le PDF du livre est la source : c'est lui qui donne les exceptions par page
  (dégâts doublés, seuils, fuites autorisées) que le corpus actuel a perdues en
  route ou noyées dans la prose.

- 🟠 **Les images de bataille.** Le moteur cherche `IMG/<bucket>/B<id>.RLE`
  quand la clairière porte un adversaire, et retombe sur l'illustration
  ordinaire `N<id>.RLE` quand elle manque. La chaîne complète :

  ```
  build_manifest.py --battle  ->  SCOSWAMP.MORE/battle_manifest.jsonl   (26 prompts)
  codex exec                  ->  SCOSWAMP.MORE/GENERATED/B<id>.png
  TOOLS/convert_images.sh     ->  SCOSWAMP/IMG/<bucket>/B<id>.RLE.BIN
  SRC/make hdv                ->  dist/SCOSWAMP.HDV
  ```

  Les 26 clairières sont celles dont la page porte un bloc de stats ; le
  manifeste les extrait tout seul, y compris depuis une ligne `M` déjà
  convertie.

  **Deux contraintes de cadrage**, apprises sur le premier essai et écrites
  dans le prompt :
  - le héros doit être **le même sur les 26 images** — capuche et cape vertes,
    cotte de mailles, bouclier rond, sac à dos, épée levée, vu de trois quarts
    dos ;
  - le **quart inférieur** doit rester du sol sombre et vide : la fenêtre de
    texte du mode mixte recouvre le sixième du bas, et au premier essai elle
    coupait les pieds du héros.

  `convert_images.sh` ne reconvertit qu'un PNG plus récent que son RLE : les
  400 illustrations de scène ne sont pas refaites à chaque passage.

- 🟠 **La fenetre programme reste etroite.** Le catalogue de messages a rendu
  627 octets, l'ecran de choix des Pierres en a repris une partie. Les deux
  pistes suivantes sont structurelles :
  1. **La RAM auxiliaire** (point 2 de la carte memoire), ~46 Ko.
  2. **La Language Card** (point 4), 16 Ko.

  Deux choses attendent cette place, toutes deux visibles a l'ecran :
  effacer le fond d'un cercle de la carte avant d'y ecrire son numero (le
  numero est pour l'instant remonte au-dessus du diametre pour eviter les
  sentiers horizontaux), et le combat contre plusieurs creatures.

- 🟡 **La sauvegarde.** Une partie de *Défis Fantastiques* se joue en plusieurs
  fois. `Character` fait une trentaine d'octets, la mémoire des clairières 120 :
  un fichier ProDOS de rien du tout.

- ✅ **Combat contre plusieurs créatures.** « Parfois, vous les affronterez
  comme si elles n'étaient qu'un seul monstre ; parfois, vous les combattrez
  une par une. » Les deux rencontres à plusieurs du Marais sont du second
  type — `N224` (deux LOUPS, « à tour de rôle »), `N235` (trois BRIGANDS, « un
  seul à la fois ») — et une page porte désormais autant de lignes `M` que
  d'adversaires. Le suivant se présente entier dès que le précédent tombe, et
  le héros garde l'ENDURANCE qui lui reste : aucun répit entre deux.
  La mémoire des clairières retient **lequel** de la file était en cours, pas
  seulement son ENDURANCE — sans quoi fuir devant le deuxième LOUP puis
  revenir ferait recommencer au premier. Pinné par `test_rules`.
  Le mode « comme un seul monstre » n'existe pas dans ce livre-ci ; il faudra
  une directive le jour où un autre le demandera.

  Au passage, le motif de dérivation absorbe l'ordinal : le corpus écrit
  « Premier LOUP » et « Deuxieme LOUP », et sans lui les deux portaient le
  même nom dans le bandeau — « Premier » restant orphelin dans la prose.

- 🟢 **Les Provisions et l'or** existent dans `Character` mais aucune page ne
  les touche encore.

- 🟢 **Que faire de `COMBAT/SRC/combat.c`.** Ces 847 lignes ne sont **pas**
  réutilisables : c'est le système de SPACETRIP (HP / ATK / DEF / niveaux / XP,
  monstres de science-fiction), pas celui de *Défis Fantastiques*. Son
  générateur aléatoire est en plus semé sur une constante (`srand(0x1234)`) :
  toutes les parties seraient identiques. À garder pour SPACETRIP, ou à
  supprimer.

- 🟢 **Coquille dans le corpus** : `Fetrissure` apparaît 2 fois pour
  `Fletrissure` 10 — à corriger avant d'en faire une clé d'inventaire.

### Documentation

- 🟢 Consigner dans `DOCS/` les deux pièges cc65/ProDOS payés ici : `errno`
  n'est **pas** numéroté comme en POSIX, et `_oserror == 0` est le signal que
  l'échec est côté runtime C, pas côté ProDOS. C'est ce qui a fait chercher un
  fichier manquant pendant longtemps alors que le problème était le tas.
