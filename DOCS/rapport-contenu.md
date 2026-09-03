# Les impasses de contenu, tranchees livre en main

Branche : `feat/scoswamp-contenu`. Corpus touche : 63 fichiers, tous dans
`SCOSWAMP/TEXTFR` et `SCOSWAMP/TEXTEN`. Aucune ligne de code, aucun octet du
catalogue d'objets, aucun binaire.

L'arbitre est le livre lui-meme : `SCOSWAMP.MORE/Defis Fantastiques 08 - Le
Marais aux Scorpions.pdf`, dont le texte s'extrait proprement (400
paragraphes, aucun trou). Chaque decision ci-dessous cite le paragraphe qui la
fonde.

---

## 1. L'Amulette d'Oiseau exigee au 350

**Ce que dit le livre.** Le paragraphe 350 demande « Avez-vous une Amulette
d'Argent en forme d'oiseau ? Rendez-vous au 25 ». La vraie amulette est au cou
de la Maitresse des Oiseaux (288). Les quatre facons de l'aborder ne la
donnent jamais :

| voie | paragraphe | issue |
| --- | --- | --- |
| l'attaquer | 391 | les oiseaux l'emportent, -2 CHANCE, retour au 217 |
| Pierre d'Amitie | 111 | « Vous avez sottement gache votre Pierre », renvoi au 184 |
| Pierre de Terreur | 201 | les oiseaux la protegent, elle disparait, retour au 217 |
| Pierre de Malediction | 260 | mort du heros |
| lui parler | 184 | elle **forge une fausse amulette** |

La vraie Amulette d'Oiseau n'est donc **jamais** obtenable. Le livre le dit
lui-meme au 184 : « Je vais fabriquer une fausse Amulette en forme d'oiseau.
**Quiconque la verra pensera qu'elle est authentique.** » L'Aigle du 350 est
precisement quelqu'un qui la verra.

**Avant** (`N350.TXT`, FR et EN) :

    CI OISEAU 025 Une Amulette d'Argent en forme d'oiseau

**Apres** :

    CI FAUX 025 Une Amulette d'Argent en forme d'oiseau

Le libelle ne change pas -- pour l'Aigle comme pour Stratagus, la fausse *est*
l'amulette. On a prefere remplacer plutot qu'ajouter une seconde ligne :
`render_choices` affiche aussi les choix indisponibles, marques `-`, et deux
lignes identiques dont l'une morte a jamais auraient encombre l'ecran a chaque
passage.

`AMULET_OISEAU` reste dans l'enumeration de `rules.h` : le bit sert encore au
comptage des amulettes (`GA`, `CA` -- Stratagus paie 500 Pieces d'Or par
amulette rapportee, et le livre veut qu'il soit dupe).

## 2. Le drapeau `.T`, pose et jamais relu

**Ce que dit le livre.** Deux paragraphes interrogent la decouverte du
buisson :

- **36** — « Si vous avez deja decouvert le buisson d'Antherique, rendez-vous
  au 283, sinon, rendez-vous au 396. »
- **76** — « Si vous avez deja trouve le buisson d'Antherique, rendez-vous au
  166. Sinon, rendez-vous au 333. »

Le portage laissait ces deux pages en choix libres, sans condition, et le
drapeau `.T` du 389 ne servait a rien.

**Ou poser le drapeau.** Le 389 n'est atteint que par 232, lui-meme atteint
par 247 -- et c'est au **247** que le livre fait decouvrir le buisson (« un
buisson de forme inhabituelle... En haut de ce buisson, vous remarquez une
grosse baie violette »). Le 232 bifurque ensuite selon le sorcier servi : un
heros au service de Pompatarte a vu le buisson mais ne passe jamais par le
389. Le drapeau appartient donc au 247.

**Avant / apres** :

| page | avant | apres |
| --- | --- | --- |
| 247 | (rien) | `G .T` ajoute |
| 389 | `G .T` | inchange (descendant strict du 247, la ligne y reste sans effet nouveau) |
| 036 | `C 283` / `C 396` | `CI .T 283` / `CN .T 396` |
| 076 | `C 166` / `C 333` | `CI .T 166` / `CN .T 333` |

C'est exactement la forme que le corpus emploie deja au 092 (`CI LOUP 344` /
`CN LOUP 068`).

## 3. Les trois pages ou l'anglais en disait plus

| page | le livre | verdict | correction |
| --- | --- | --- | --- |
| 124 | « C'est un combat a mort et il n'est pas question d'essayer de prendre la fuite. » | l'anglais avait raison | phrase ajoutee au FR ; aucune ligne `CF` des deux cotes, la mecanique etait deja juste |
| 126 | « C'est le seul effet que vous obteniez. » | l'anglais avait raison | phrase ajoutee au FR |
| 140 | « vous vous rendez compte aussitot qu'il s'agit la d'une **Epee Magique qui donne 2 points d'HABILETE supplementaire** a celui qui s'en sert au combat » | l'anglais avait raison, **et les deux langues avaient tort sur la mecanique** | phrase ajoutee au FR, `G EP` et `E BONUS +2` ajoutes **dans les deux langues** |

Le 140 etait le vrai trou : la page 340 (l'autre mort de Stratagus, celle du
duel final) portait bien `G EP` + `E BONUS +2`, la 140 -- celle du Stratagus
9/10 du paragraphe 225 -- ne donnait rien. Le heros ramassait une epee que le
moteur ne lui mettait pas dans les mains.

## 4. Les sept fins vivantes non victorieuses

La liste de l'enonce est exacte : **049, 052, 100, 141, 298, 327, 349**. Le
recensement complet des pages sans issue donne 21 pages en FR, dont 11 morts
(003, 030, 098, 260, 297, 313, 332, 361, 372, 375, 401) et 3 victoires (158,
175, 358).

Toutes les sept portaient deja la phrase de cloture du livre, mais aucune
n'annoncait la fin comme le 175 (« FIN DE L'AVENTURE - SUCCES COMPLET ») ou le
260 (« FIN DE L'AVENTURE. ») le font. Chacune recoit desormais la meme
derniere ligne, dans les deux langues :

    FIN DE L'AVENTURE.        /        END OF ADVENTURE.

Trois accords fautifs sont corriges au passage, sur la foi du livre :

| page | avant | apres |
| --- | --- | --- |
| 049 | « plusieurs annes », « votre aventure s'acheve ici » | « plusieurs annees », « votre aventure s'acheve **donc avant d'avoir commence** » (livre, 49) |
| 100 | « votre aventure est termine » | « votre aventure est terminee » |
| 141 | « Pierres Magiques inutilises », « est termine » | « inutilisees », « est terminee » |
| 298 | « votre aventure est termine » | « votre aventure est terminee » |

**La musique n'a pas ete touchee, faute d'exister.** Il n'y a dans ce depot ni
dossier `SCOSWAMP.MORE/MUSIC`, ni ligne `MU` dans le corpus (0 occurrence sur
824 fichiers), ni traitement d'une telle directive dans `scoswamp.c`, ni
fichier `.MB`. Pire : `DIRECTIVE`, dans `reflow_txt.py`, n'accepte `M` que
suivi d'une espace, donc une ligne `MU -` serait repliee **dans le corps** et
s'afficherait telle quelle a l'ecran. Ajouter ces lignes aurait abime les sept
pages au lieu de les soigner. Voir la liste d'arbitrage ci-dessous.

## 5. Relecture ciblee : objets, Pierres et amulettes de la prose

`reflow_txt.py --derive` ne signale rien (« problemes : 0 »). Le balayage par
grep sur les dix libelles du catalogue et les six amulettes rend quinze pages,
toutes verifiees une a une contre le livre :

- **descriptives, aucune directive attendue** : 053, 144, 209, 288, 305, 398
  (l'amulette pend au cou d'un PNJ), 184 (`G FAUX` deja present), 150 (la
  liste d'Alphonse ; l'echange se fait au 408 par `TR`, dont le masque
  `0x018C` couvre bien Chaine d'Or, Aimant d'Or, Bijou Violet et Corne de
  Licorne, plus les amulettes) ;
- **035 et 357** (l'Aimant d'Or maudit) : le livre ne le retire pas du sac, le
  portage non plus. Fidele ;
- **117 et 292** (le Maitre des Jardins passe son Amulette a Fleur autour de
  votre cou) : « Il reprend son Amulette et s'en va ». Aucun `G FLEUR` a
  poser, l'amulette ne change pas de main. C'est au 251, quand on le tue,
  qu'on s'en empare -- et le `G FLEUR` y est ;
- **Anneau de Cuivre** : aucun `G ANNEAU` dans le corpus, mais aucun n'est
  necessaire -- `character_roll` pose le bit de depart (`c->objects = (1u <<
  OBJ_ANNEAU)`), conformement au prologue du livre (la vieille femme de la
  route du Roi).

Aucun manque a corriger de ce cote : ce point-la etait sain.

## 6. Les pages synthetiques 402-411

Structure FR/EN identique pour les onze (401 compris), et chacune se rattache
a un paragraphe du livre :

| page | source | ce que le livre dit |
| --- | --- | --- |
| 401 | 315 | la trappe, branche Malchanceux |
| 402 | 373 | « vous parvenez a blesser le sorcier... vous oterez 2 points au total d'ENDURANCE de votre adversaire » — d'ou `M 9 8` au lieu de `M 9 10`, et `MV 140` comme au 225 |
| 403 | 257 | « Augmentez de 2 points votre total de CHANCE et rendez-vous au 153 » |
| 404 / 405 | 91 | le saut reussi / rate (-1 HABILETE), puis 398 / 105 / 208 |
| 406 | 377 | « Vous perdrez alors 3 points d'ENDURANCE... rendez-vous au 319 » |
| 407 | 128 | « donnez-lui un objet de votre choix » — `PO` |
| 408 | 150 | l'echange chez Alphonse — `TR` |
| 409 / 410 / 411 | 164 | la potion de la Maitresse des Oiseaux, « choisissez vous-meme le total que vous souhaitez voir revenir a son niveau de depart », puis 248 |

Rien a corriger.

---

## Ce que la relecture a trouve en plus (et corrige)

En verifiant les points ci-dessus, un defaut plus large est apparu : **douze
pages du corpus n'avaient aucun lien entrant**, alors que le livre les atteint
toutes. Elles sont desormais toutes joignables (`orphelines: []` dans les deux
langues).

### a) Douze lignes `V` manquantes

`rules.h` annonce « Quatorze pages du livre ouvrent sur cette phrase ». Le
livre en compte en realite **vingt-trois** ; le portage n'en avait que
quatorze. La prose condensee du portage avait perdu la phrase « Si vous y etes
deja venu, rendez-vous au... », et avec elle la derivation automatique.

Ajoutees (FR et EN), en tete de page comme l'exige `classify_line` :

    V 210 au 011   V 338 au 014   V 364 au 031   V 382 au 041
    V 329 au 053   V 343 au 065   V 108 au 092   V 330 au 105
    V 345 au 144   V 363 au 170   V 250 au 204   V 168 au 209

C'est la memoire des clairieres que `rules.h` appelle « le seul Defis
Fantastiques ou l'on revient sur ses pas » : sans ces douze lignes, la moitie
du mecanisme dormait.

### b) Deux boucles fermees par la ligne `V`

Une page `V` dont la cible renvoie a la page elle-meme enferme le joueur : le
moteur re-court-circuite indefiniment.

- **336 / 137** (bug **preexistant**, revele par le recensement). Le 336 porte
  `V 137`, et le 137 disait « Revenir en arriere pour trouver une solution »
  vers 336 : le joueur ne pouvait plus jamais lire les quatre options du
  bassin de Vase. Le livre (137) dit « Retournez au 336 pour examiner la
  meilleure facon de vous tirer d'affaire » ; le 137 propose maintenant ces
  quatre facons directement (`C 085`, `C 257`, `C 171`, `C 400`), en plus de
  `C 153`. Sa prose etait par ailleurs cassee (« Si vous l'avez deja tue : »
  suivi de rien) et a ete recousue sur le texte du livre.
- **209 / 168** (boucle que la ligne `V 168` aurait creee). Le 168 renvoyait a
  209 ; il renvoie desormais aux deux pages d'action du 209 : `C 082`
  (reprendre le combat -- la memoire des monstres du moteur rend bien « le
  meme total d'ENDURANCE qu'au moment de votre fuite », promesse du livre) et
  `C 034` (magie), en plus de `C 330` (quitter).

### c) Trois liens faux et un choix perdu

| page | avant | apres | le livre |
| --- | --- | --- | --- |
| 147 | `CL 213 267` | `CL 213 106` | « Si vous etes Malchanceux, rendez-vous au **106** » (147). Le portage sautait la page 106 -- et avec elle les 2 points d'ENDURANCE perdus dans la bagarre et l'option de fuir au 179 |
| 400 | `CU FEU 336` | `CU FEU 188` | « Une Pierre de Feu ? Rendez-vous au **188** » (400) |
| 400 | `CU FLETRISSURE 336` | `CU FLETRISSURE 380` | « de Fletrissure ? Rendez-vous au **380** » (400) |
| 145 | trois Pierres | + `CU GLACE 126` | « de Glace ? Rendez-vous au **126** » (145). La prose du portage annoncait deja « quatre emplacements » pour trois choix |
| 330 | `C 268` seul | + `C 129` | « Si vous y avez vu une creature lors d'une precedente visite, rendez-vous au 129 » (330) : la phrase etait dans la prose, sans le choix qui va avec |

### d) Une page anglaise tronquee

`TEXTEN/N350/N382.TXT` s'arretait au milieu d'une phrase (« If you have one
or ») et ne portait **aucun choix** : c'etait la seule page sans issue de tout
le corpus anglais qui ne soit ni une mort ni une fin. Sa derniere phrase et
ses trois choix (`C 270`, `C 190`, `C 223`) sont retablis d'apres le francais
et le livre. Deux pages anglaises (190, 223) redeviennent joignables du meme
coup.

---

## Laisse a l'arbitrage du proprietaire

1. **La musique n'existe pas.** Ni `SCOSWAMP.MORE/MUSIC`, ni directive `MU`,
   ni fichier `.MB`, ni code. Si le lot musique doit exister, il faut d'abord
   une ligne `MU` dans `DIRECTIVE` (`reflow_txt.py`) et dans `classify_line`
   (`scoswamp.c`) -- c'est du code, hors de ce lot.
2. **Le moteur n'annonce pas la fin.** Sur une page sans issue, la ligne du
   bas reste `M_TOUCHES` (« ESPACE=VUE A-Z=CHOIX I=SAC Q=QUITTER »). Les
   touches `N` (nouvelle partie), `L` (charger) et `Q` existent bien dans
   `handle_key`, mais rien ne les nomme a ce moment-la. Un message dedie
   serait un changement de `build_messages.py` + `scoswamp.c`.
3. **« FIN DE L'AVENTURE » : jusqu'ou ?** Elle figure maintenant sur les sept
   fins vivantes, plus 175 et 260 qui l'avaient deja. Restent sans marqueur
   les deux autres victoires (**158**, **358**) et dix des onze morts. Faut-il
   generaliser ?
4. **Terminologie anglaise.** `TEXTEN` melange « Asphodel » (006, 164, 175,
   212) et « Antherique » (389, catalogue `OBJEN.TXT` : « Antherique Berry »).
   Les 036 et 076, refondus ici, ont ete alignes sur « Antherique » ; le reste
   attend une decision.
5. **Le sorcier servi n'est pas un drapeau.** Le 232 (« Si vous vous etes mis
   au service de Gayolard ») et le 330 (« si vous y avez vu une creature »)
   restent des choix libres, faute d'un bit `.G` et d'une memoire des
   creatures apercues. Deux drapeaux caches suffiraient ; c'est un changement
   de `build_objects.py` et de trois autres fichiers.
6. **Soixante fichiers ne sont pas sous forme canonique** (directives placees
   en tete plutot qu'en pied). `reflow_txt.py` rend « problemes : 0 » mais
   « a reecrire : 60 ». Les deux pages que ce lot touchait (049 FR/EN) ont ete
   normalisees ; les soixante autres attendent un `--apply` decide par le
   proprietaire, qui produirait un diff large et purement cosmetique.

---

## Verifications

    python3 SCOSWAMP.MORE/TOOLS/reflow_txt.py SCOSWAMP             -> problemes : 0
    python3 SCOSWAMP.MORE/TOOLS/reflow_txt.py SCOSWAMP --derive    -> problemes : 0
    make -C SCOSWAMP/SRC          -> OK : tient en memoire, marge de 184 octets.
    make -C SCOSWAMP/SRC hdv      -> SCOSWAMP: 1284 files, 7331 blocks
    cmake --build ... --target test_rules && .../test_rules  -> regles : tout passe
    python3 SCOSWAMP.MORE/TOOLS/build_objects.py --root .   -> catalogue inchange

Et, pour la couverture du corpus : aucune page orpheline, aucune cible
inexistante, aucune boucle `V`, dans les deux langues.
