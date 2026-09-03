/*
 * Banc d'essai des regles de Defis Fantastiques, sur machine hote.
 *
 * Les regles sont de l'arithmetique pure : les verifier ici coute une seconde,
 * alors que les verifier dans l'emulateur demande de rejouer une partie et ne
 * couvre qu'un chemin. Chaque test porte la phrase du livre qu'il defend.
 */
#include "../../SCOSWAMP/SRC/rules.h"
#include "../../SCOSWAMP/SRC/dice.h"
#include <stdio.h>
#include <string.h>

static int failures = 0;

#define CHECK(cond, ...)                                                      \
    do {                                                                      \
        if (!(cond)) {                                                        \
            printf("ECHEC %s:%d: ", __FILE__, __LINE__);                      \
            printf(__VA_ARGS__); printf("\n"); ++failures;                    \
        }                                                                     \
    } while (0)

/* Un heros dont la CHANCE rend "Tentez votre Chance" deterministe :
 * cha=12 -> 2d6 <= 12 toujours vrai ; cha=1 -> 2d6 >= 2 toujours faux. */
static Character hero(unsigned char hab, unsigned char end, unsigned char cha)
{
    Character c;
    memset(&c, 0, sizeof c);
    c.hab = c.hab0 = hab;
    c.end = c.end0 = end;
    c.cha = c.cha0 = cha;
    return c;
}

static void test_dice(void)
{
    int i, seen[7] = {0};
    dice_seed(12345);
    for (i = 0; i < 6000; ++i) {
        unsigned char d = roll_d6();
        CHECK(d >= 1 && d <= 6, "de hors bornes: %u", d);
        ++seen[d];
    }
    for (i = 1; i <= 6; ++i) {
        /* 1000 attendus par face ; large fourchette, on cherche une face
         * morte ou un modulo biaise, pas la qualite statistique fine. */
        CHECK(seen[i] > 800 && seen[i] < 1200, "face %d sortie %d fois", i, seen[i]);
    }
    for (i = 0; i < 2000; ++i) {
        unsigned char d = roll_2d6();
        CHECK(d >= 2 && d <= 12, "2d6 hors bornes: %u", d);
    }
    /* Deterministe a semence egale : c'est ce qui rend ce fichier possible. */
    dice_seed(7); i = roll_d6() * 10 + roll_d6();
    dice_seed(7); CHECK(i == roll_d6() * 10 + roll_d6(), "semence non reproductible");
}

static void test_creation(void)
{
    int i;
    dice_seed(99);
    for (i = 0; i < 500; ++i) {
        Character c;
        character_roll(&c);
        /* "Lancez un de. Ajoutez 6 [...] HABILETE" */
        CHECK(c.hab >= 7  && c.hab <= 12, "HABILETE %u hors 7..12", c.hab);
        /* "Lancez ensuite les deux des. Ajoutez 12 [...] ENDURANCE" */
        CHECK(c.end >= 14 && c.end <= 24, "ENDURANCE %u hors 14..24", c.end);
        /* "Lancez a nouveau un de, ajoutez 6 [...] CHANCE" */
        CHECK(c.cha >= 7  && c.cha <= 12, "CHANCE %u hors 7..12", c.cha);
        CHECK(c.hab == c.hab0 && c.end == c.end0 && c.cha == c.cha0,
              "les valeurs de depart doivent egaler les courantes");
    }
}

static void test_plafond(void)
{
    /* "ce total ne doit en aucun cas exceder vos points de depart" */
    Character c = hero(9, 20, 8);
    character_adjust_end(&c, -6);   CHECK(c.end == 14, "END %u", c.end);
    character_adjust_end(&c, +99);  CHECK(c.end == 20, "END plafonnee a 20, vu %u", c.end);
    character_adjust_end(&c, -99);  CHECK(c.end == 0,  "END plancher 0, vu %u", c.end);
    CHECK(character_is_dead(&c), "ENDURANCE a zero = mort");
    character_adjust_hab(&c, +5);   CHECK(c.hab == 9,  "HAB plafonnee, vu %u", c.hab);
    character_adjust_cha(&c, +5);   CHECK(c.cha == 8,  "CHA plafonnee, vu %u", c.cha);
}

/* La bourse. Elle n'a pas de plafond dans le livre -- "quelques Pieces d'Or
 * qui vous permettront de subvenir a de menues depenses", jamais de maximum --
 * mais elle a un plancher, et c'est lui qui compte : le champ est non signe,
 * et un heros sans le sou qui paie une piece a l'aubergiste (page 078)
 * repassait a 65535 Pieces d'Or. */
static void test_or(void)
{
    Character c = hero(9, 20, 8);

    c.gold = 0;
    character_adjust_gold(&c, -1);
    CHECK(c.gold == 0, "une bourse vide reste vide, vu %u", c.gold);

    c.gold = 3;
    character_adjust_gold(&c, -5);
    CHECK(c.gold == 0, "on ne paie pas ce qu'on n'a pas, vu %u", c.gold);

    c.gold = 3;
    character_adjust_gold(&c, +100);
    CHECK(c.gold == 103, "aucun plafond sur l'or, vu %u", c.gold);

    /* Le contrat va jusqu'a 32 767, la borne de l'int 16 bits de cc65 par
     * lequel le calcul passe. Le corpus distribue 370 Pieces d'Or en tout :
     * la borne est hors d'atteinte de deux ordres de grandeur, mais elle est
     * le contrat, et un test la tient. */
    c.gold = 20000u;
    character_adjust_gold(&c, +12000);
    CHECK(c.gold == 32000u, "la bourse porte quatre chiffres et plus, vu %u", c.gold);

    /* Le jet `ED OR +1` de la page 135 passe par la meme porte : un gain
     * ordinaire s'ajoute, sans plafond de depart contrairement aux trois
     * caracteristiques. */
    c.gold = 20;
    character_adjust_gold(&c, +6);
    CHECK(c.gold == 26, "un de d'or s'ajoute, vu %u", c.gold);
}

static void test_chance(void)
{
    Character c;
    int i;

    /* "Si le chiffre obtenu est egal ou inferieur a vos points de CHANCE,
     * vous etes Chanceux" : a 12, tout 2d6 passe. */
    dice_seed(4);
    c = hero(9, 20, 12);
    CHECK(luck_test(&c) == 1, "CHANCE 12 doit toujours etre Chanceux");
    /* "il vous faudra oter un point a votre total de CHANCE" */
    CHECK(c.cha == 11, "un point de CHANCE consomme, vu %u", c.cha);

    c = hero(9, 20, 1);
    CHECK(luck_test(&c) == 0, "CHANCE 1 ne peut jamais etre Chanceux");
    CHECK(c.cha == 0, "CHANCE consommee, vu %u", c.cha);
    /* A zero, le jet est perdu d'avance et ne descend pas sous zero. */
    for (i = 0; i < 5; ++i) CHECK(luck_test(&c) == 0, "CHANCE 0 -> Malchanceux");
    CHECK(c.cha == 0, "CHANCE ne passe pas sous zero, vu %u", c.cha);
}

static void test_assaut(void)
{
    Character c = hero(10, 20, 12);
    Monster m; Round r; int i;
    dice_seed(31);
    monster_init(&m); m.hab = 8; m.end = 12; strcpy(m.name, "GEANT");

    for (i = 0; i < 500; ++i) {
        combat_round(&c, &m, &r);
        /* "Jetez les deux des [...] Ajoutez ses points d'HABILETE" */
        CHECK(r.hero_force    >= 12 && r.hero_force    <= 22, "FA heros %u", r.hero_force);
        CHECK(r.monster_force >= 10 && r.monster_force <= 20, "FA monstre %u", r.monster_force);
        CHECK((r.outcome == ROUND_HERO_HITS)    == (r.hero_force >  r.monster_force), "issue");
        CHECK((r.outcome == ROUND_MONSTER_HITS) == (r.hero_force <  r.monster_force), "issue");
        CHECK((r.outcome == ROUND_DODGE)        == (r.hero_force == r.monster_force), "issue");
    }

    /* Les deux epees magiques du livre n'ont pas la meme puissance : celle
     * offerte par Stratagus vaut +1, celle prise sur lui vaut +2. */
    c = hero(10, 20, 12); c.objects = (1u << OBJ_EPEMAGIQUE); c.weapon_bonus=2;
    dice_seed(77); combat_round(&c, &m, &r); i = r.hero_force;
    c.weapon_bonus=1;
    dice_seed(77); combat_round(&c, &m, &r);
    CHECK(i == r.hero_force + 1, "epee prise +2 contre epee offerte +1");
}

static void test_blessures(void)
{
    Character c;
    Monster m;
    Round r;
    dice_seed(5);
    monster_init(&m); m.hab = 8; m.end = 20; strcpy(m.name, "X");

    /* "vous diminuez donc de deux points son ENDURANCE" */
    c = hero(10, 20, 9); r.outcome = ROUND_HERO_HITS;
    combat_apply(&c, &m, &r, 0);
    CHECK(m.end == 18, "blessure simple = -2, vu %u", m.end);

    /* Chanceux : "vous pouvez oter deux points de plus" -> -4 en tout */
    c = hero(10, 20, 12); m.end = 20;
    CHECK(combat_apply(&c, &m, &r, 1) == 1, "CHANCE 12 = Chanceux");
    CHECK(m.end == 16, "blessure grave = -4, vu %u", m.end);
    CHECK(c.cha == 11, "le jet coute un point de CHANCE");

    /* Malchanceux : "au lieu d'enlever les deux points [...] un seul" */
    c = hero(10, 20, 1); m.end = 20;
    CHECK(combat_apply(&c, &m, &r, 1) == 0, "CHANCE 1 = Malchanceux");
    CHECK(m.end == 19, "ecorchure = -1, vu %u", m.end);

    /* Le heros encaisse */
    r.outcome = ROUND_MONSTER_HITS;
    c = hero(10, 20, 9);  combat_apply(&c, &m, &r, 0);
    CHECK(c.end == 18, "blessure recue = -2, vu %u", c.end);
    c = hero(10, 20, 12); combat_apply(&c, &m, &r, 1);
    CHECK(c.end == 19, "coup attenue = -1, vu %u", c.end);
    c = hero(10, 20, 1);  combat_apply(&c, &m, &r, 1);
    CHECK(c.end == 17, "coup aggrave = -3, vu %u", c.end);

    /* Paragraphe 12 : la massue coute 4 points au lieu de 2, et le
     * modificateur de CHANCE reste de UN point -- donc 3 ou 5. */
    m.damage = 4;
    c = hero(10, 20, 9);  combat_apply(&c, &m, &r, 0);
    CHECK(c.end == 16, "massue = -4, vu %u", c.end);
    c = hero(10, 20, 12); combat_apply(&c, &m, &r, 1);
    CHECK(c.end == 17, "massue attenuee = -3, vu %u", c.end);
    c = hero(10, 20, 1);  combat_apply(&c, &m, &r, 1);
    CHECK(c.end == 15, "massue aggravee = -5, vu %u", c.end);
    m.damage = 2;

    /* Esquive : personne ne perd rien */
    r.outcome = ROUND_DODGE;
    c = hero(10, 20, 9); m.end = 20;
    combat_apply(&c, &m, &r, 0);
    CHECK(c.end == 20 && m.end == 20, "l'esquive ne coute rien");

    /* L'ENDURANCE d'une creature ne passe pas sous zero */
    r.outcome = ROUND_HERO_HITS; m.end = 1;
    c = hero(10, 20, 9); combat_apply(&c, &m, &r, 0);
    CHECK(m.end == 0, "ENDURANCE creature plancher 0, vu %u", m.end);
}

static void test_fuite(void)
{
    /* "Vous oterez alors deux points a votre ENDURANCE. [...] vous pourrez
     * toutefois vous servir de votre CHANCE" */
    Character c;
    Monster m;
    dice_seed(17);
    monster_init(&m); m.hab = 8; m.end = 10;
    c = hero(9, 20, 9);  combat_flee(&c, &m, 0); CHECK(c.end == 18, "fuite = -2, vu %u", c.end);
    c = hero(9, 20, 12); combat_flee(&c, &m, 1); CHECK(c.end == 19, "fuite chanceuse = -1, vu %u", c.end);
    c = hero(9, 20, 1);  combat_flee(&c, &m, 1); CHECK(c.end == 17, "fuite malchanceuse = -3, vu %u", c.end);

    /* Paragraphe 12 : "les coups de votre adversaire vous infligent une double
     * blessure. Vous perdrez donc 4 points d'ENDURANCE en vous echappant." */
    m.damage = 4;
    c = hero(9, 20, 9);  combat_flee(&c, &m, 0); CHECK(c.end == 16, "fuite du GEANT = -4, vu %u", c.end);
    c = hero(9, 20, 12); combat_flee(&c, &m, 1); CHECK(c.end == 17, "fuite chanceuse = -3, vu %u", c.end);
    c = hero(9, 20, 1);  combat_flee(&c, &m, 1); CHECK(c.end == 15, "fuite malchanceuse = -5, vu %u", c.end);
}

static void test_memoire_clairieres(void)
{
    /* "conservez ces indications car il est possible que vous reveniez plus
     * tard dans cette clairiere [...] reprendre le combat la ou vous l'aviez
     * laisse." */
    Monster m[3];
    unsigned char snapshot[MONSTER_MEMORY_SIZE];
    monster_memory_reset();

    monster_init(&m[0]); m[0].hab = 9; m[0].end = 12; strcpy(m[0].name, "GEANT");
    monster_seal(&m[0]);
    CHECK(m[0].end0 == 12, "l'ENDURANCE de depart est figee, vu %u", m[0].end0);
    CHECK(monster_enter(12, m, 1) == 0, "premiere visite : on commence au premier");
    CHECK(m[0].end == 12, "premiere visite : l'ENDURANCE du livre, vu %u", m[0].end);

    m[0].end = 4;
    monster_remember(12, 0, &m[0]);
    CHECK(m[0].end0 == 12, "la jauge garde le maximum du livre, vu %u", m[0].end0);

    monster_init(&m[0]); m[0].hab = 9; m[0].end = 12;   /* la page redonne le livre */
    CHECK(monster_enter(12, m, 1) == 0, "retour : le combat reprend");
    CHECK(m[0].end == 4, "retour : ENDURANCE entamee, vu %u", m[0].end);

    m[0].end = 0; monster_remember(12, 0, &m[0]);
    m[0].end = 12;
    CHECK(monster_enter(12, m, 1) == 1, "creature morte : la file est finie");

    monster_init(&m[0]); m[0].end = 9;
    CHECK(monster_enter(300, m, 1) == 0 && m[0].end == 9, "clairiere jamais visitee");

    /* Le seuil du paragraphe 12 : "si vous parvenez a reduire a 6 les points
     * d'ENDURANCE du Geant, rendez-vous au 61". Le combat cesse a 6, pas a 0. */
    monster_init(&m[0]); m[0].end = 12; m[0].stop_at = 6;
    CHECK(monster_is_beaten(&m[0]) == 0, "12 > 6 : le combat continue");
    m[0].end = 6;
    CHECK(monster_is_beaten(&m[0]) == 1, "a 6, le Geant flechit");
    monster_remember(200, 0, &m[0]);
    m[0].end = 12;
    CHECK(monster_enter(200, m, 1) == 1, "retour : le seuil est deja atteint");

    /* Une file : "vous devrez les combattre tous deux a tour de role"
     * (paragraphe 224, les deux LOUPS). Fuir devant le second puis revenir
     * doit reprendre AU SECOND, pas au premier. */
    monster_memory_reset();
    monster_init(&m[0]); m[0].hab = 7; m[0].end = 5;
    monster_init(&m[1]); m[1].hab = 6; m[1].end = 6;
    CHECK(monster_enter(224, m, 2) == 0, "premiere visite : le premier LOUP");

    m[0].end = 0;                       /* le premier tombe */
    m[1].end = 3;                       /* le second est entame, on fuit */
    monster_remember(224, 1, &m[1]);

    monster_init(&m[0]); m[0].hab = 7; m[0].end = 5;
    monster_init(&m[1]); m[1].hab = 6; m[1].end = 6;
    CHECK(monster_enter(224, m, 2) == 1, "retour : on reprend au second LOUP");
    CHECK(m[1].end == 3, "et il est toujours entame, vu %u", m[1].end);
    CHECK(m[0].end == 5, "le premier n'est pas ressuscite pour autant, vu %u", m[0].end);

    /* C'est ce bloc exact que PARTIE0..PARTIE9 ecrivent sur disque. Une
     * extinction/reprise doit donc conserver l'adversaire courant et sa
     * blessure, pas seulement un retour dans la meme session. */
    monster_memory_export(snapshot);
    monster_memory_reset();
    monster_memory_import(snapshot);
    monster_init(&m[0]); m[0].hab = 7; m[0].end = 5;
    monster_init(&m[1]); m[1].hab = 6; m[1].end = 6;
    CHECK(monster_enter(224, m, 2) == 1,
          "sauvegarde combat : reprise au second LOUP");
    CHECK(m[1].end == 3,
          "sauvegarde combat : blessure conservee, vu %u", m[1].end);

    m[1].end = 0; monster_remember(224, 1, &m[1]);
    monster_init(&m[1]); m[1].hab = 6; m[1].end = 6;
    CHECK(monster_enter(224, m, 2) == 2, "les deux tombes : plus de combat");
}

static void test_pierres(void)
{
    Character c = hero(11, 20, 9);
    Stone s;

    /* Les trois categories */
    CHECK(stone_kind(STONE_HABILETE)    == STONE_NEUTRE,    "HABILETE neutre");
    CHECK(stone_kind(STONE_ILLUSION)    == STONE_NEUTRE,    "ILLUSION neutre");
    CHECK(stone_kind(STONE_AMITIE)      == STONE_BENEFIQUE, "AMITIE benefique");
    CHECK(stone_kind(STONE_BENEDICTION) == STONE_BENEFIQUE, "BENEDICTION benefique");
    CHECK(stone_kind(STONE_TERREUR)     == STONE_MALEFIQUE, "TERREUR malefique");
    CHECK(stone_kind(STONE_MALEDICTION) == STONE_MALEFIQUE, "MALEDICTION malefique");

    /* Reconnaissance des noms, telle que les pages les ecrivent */
    CHECK(stone_from_name("Feu")         == STONE_FEU,         "Feu");
    CHECK(stone_from_name("fletrissure") == STONE_FLETRISSURE, "casse ignoree");
    CHECK(stone_from_name("FIRE")        == STONE_FEU,         "nom anglais");
    CHECK(stone_from_name("Pouet")       == STONE_COUNT,       "nom inconnu");
    for (s = 0; s < STONE_COUNT; ++s) {
        CHECK(stone_from_name(stone_name(s, 0)) == s, "aller-retour FR %d", (int)s);
        CHECK(stone_from_name(stone_name(s, 1)) == s, "aller-retour EN %d", (int)s);
    }

    /* "vous aurez le droit de prendre plusieurs pierres semblables" */
    character_give_stone(&c, STONE_FEU, 4);
    CHECK(character_has_stone(&c, STONE_FEU) == 4, "4 Pierres de Feu");

    /* "les Pierres de Magie se desintegrent des qu'on les a utilisees" */
    CHECK(stone_use(&c, STONE_FEU, 0) == STONE_USE_OK, "usage");
    CHECK(character_has_stone(&c, STONE_FEU) == 3, "une pierre consommee");
    CHECK(stone_use(&c, STONE_GLACE, 0) == STONE_USE_NONE, "pierre absente");

    /* "un nombre de points egal a la moitie de votre total de depart (si ce
     * total est impair, arrondissez au chiffre superieur)" : 11 -> 6 */
    c = hero(11, 20, 9);
    c.hab = 2;
    character_give_stone(&c, STONE_HABILETE, 1);
    CHECK(stone_use(&c, STONE_HABILETE, 0) == STONE_USE_OK, "pierre d'HABILETE");
    CHECK(c.hab == 8, "2 + 6 = 8, vu %u", c.hab);

    /* et jamais au-dela du total de depart */
    c = hero(11, 20, 9);
    c.hab = 10;
    character_give_stone(&c, STONE_HABILETE, 1);
    stone_use(&c, STONE_HABILETE, 0);
    CHECK(c.hab == 11, "plafonnee au depart, vu %u", c.hab);

    /* "il vous est interdit de vous en servir sitot que le premier coup a ete
     * donne" -- et la pierre ne doit pas etre consommee pour autant. */
    c = hero(11, 20, 9);
    c.end = 5;
    character_give_stone(&c, STONE_ENDURANCE, 1);
    CHECK(stone_use(&c, STONE_ENDURANCE, 1) == STONE_USE_FORBIDDEN, "interdite en combat");
    CHECK(character_has_stone(&c, STONE_ENDURANCE) == 1, "pierre non consommee");
    CHECK(c.end == 5, "aucun effet");
    CHECK(stone_use(&c, STONE_ENDURANCE, 0) == STONE_USE_OK, "autorisee hors combat");
    CHECK(c.end == 15, "5 + 10, vu %u", c.end);

    /* Les autres pierres restent utilisables pendant un combat. */
    c = hero(11, 20, 9);
    character_give_stone(&c, STONE_TERREUR, 1);
    CHECK(stone_use(&c, STONE_TERREUR, 1) == STONE_USE_OK, "TERREUR en combat");

    /* "vous devrez lancer un de et reduire votre total d'ENDURANCE d'un
     * nombre de points equivalant au chiffre obtenu." */
    {
        int i;
        dice_seed(3);
        for (i = 0; i < 200; ++i) {
            Character d = hero(11, 20, 9);
            character_give_stone(&d, STONE_MALEDICTION, 1);
            stone_use(&d, STONE_MALEDICTION, 0);
            CHECK(d.end >= 14 && d.end <= 19,
                  "MALEDICTION coute 1d6 ENDURANCE, vu %u", d.end);
        }
    }
}

static void test_objets(void)
{
    Character c = hero(9, 20, 8);
    c.objects = 0;
    CHECK(object_from_name("inconnu") == OBJ_COUNT, "objet inconnu");
    CHECK(object_from_name("BJ") == OBJ_BIJOU, "bijou violet reconnu");
    CHECK(object_from_name("CO") == OBJ_CORNE, "corne de licorne reconnue");
    CHECK(object_from_name("PL") == OBJ_PLUMES, "plumes reconnues");
    character_give_object(&c, OBJ_BIJOU);
    character_give_object(&c, OBJ_CORNE);
    character_give_object(&c, OBJ_PLUMES);
    CHECK(character_has_object(&c, OBJ_BIJOU), "bijou entre dans le sac");
    CHECK(character_has_object(&c, OBJ_CORNE), "corne entre dans le sac");
    CHECK(character_has_object(&c, OBJ_PLUMES), "plumes entrent dans le sac");
    character_take_object(&c, OBJ_BIJOU);
    CHECK(!character_has_object(&c, OBJ_BIJOU), "bijou remis quitte le sac");
    c.amulets = 0;
    CHECK(amulet_from_name("ARAIGNEE") == AMULET_ARAIGNEE, "amulette araignee");
    CHECK(amulet_from_name("FAUX") == AMULET_FAUSSE_OISEAU,
          "fausse amulette distincte");
    CHECK(character_amulet_count(&c) == 0, "aucune amulette au depart");
    character_give_amulet(&c, AMULET_LOUP);
    CHECK(character_amulet_count(&c) == 1, "palier Stratagus : une amulette");
    character_give_amulet(&c, AMULET_FLEUR);
    CHECK(character_amulet_count(&c) == 2, "palier Stratagus : deux amulettes");
    character_give_amulet(&c, AMULET_OISEAU);
    character_give_amulet(&c, AMULET_ARAIGNEE);
    character_give_amulet(&c, AMULET_GRENOUILLE);
    CHECK(character_amulet_count(&c) == 5, "les cinq vraies amulettes sont distinctes");
    character_give_amulet(&c, AMULET_FAUSSE_OISEAU);
    CHECK(character_has_amulet(&c, AMULET_OISEAU), "l'amulette Oiseau authentique reste presente");
    CHECK(character_has_amulet(&c, AMULET_FAUSSE_OISEAU), "la fausse Oiseau a son propre bit");
    CHECK(character_amulet_count(&c) == 6,
          "la fausse trompe Stratagus sans remplacer l'authentique");
    c.gold=20;
    CHECK(character_trade_amulets(&c,500)==6, "six amulettes remises");
    CHECK(c.gold==3020, "500 pieces par amulette, vu %u",c.gold);
    CHECK(character_amulet_count(&c)==0, "les amulettes remises quittent le sac");
}

static void test_perte_definitive(void)
{
    /* "vous perdez 2 points d'HABILETE et devez reduire aussi de 2 points
     * votre total initial d'HABILETE. Vous ne pourrez plus jamais retrouver
     * tous vos points de depart" (paragraphe 87). */
    Character c = hero(11, 20, 8);
    character_shift0(&c, 1, -2);
    CHECK(c.hab0 == 9, "le plafond descend a 9, vu %u", c.hab0);
    CHECK(c.hab  == 9, "la valeur courante suit, vu %u", c.hab);

    /* Et rien ne la rend : le soin plafonne au nouveau total. */
    character_adjust_hab(&c, +5);
    CHECK(c.hab == 9, "le soin s'arrete au nouveau plafond, vu %u", c.hab);

    /* "vous perdez 2 points [...] et devez reduire aussi de 2 points votre
     * total initial" : une HABILETE deja entamee perd ses 2 points elle aussi. */
    c = hero(11, 20, 8); c.hab = 4;
    character_shift0(&c, 1, -2);
    CHECK(c.hab == 2 && c.hab0 == 9, "4-2 sous un plafond de 9, vu %u/%u", c.hab, c.hab0);

    /* Le plafond ne tombe jamais a zero : ce serait une mort que le livre ne
     * prononce pas. La valeur courante, elle, a le plancher ordinaire. */
    c = hero(11, 20, 8);
    character_shift0(&c, 1, -50);
    CHECK(c.hab0 == 1 && c.hab == 0, "plafond a 1, valeur a 0, vu %u/%u", c.hab, c.hab0);
}

static void test_benediction(void)
{
    /* Grognard benit le paladin au village, avant le Marais, ou la CHANCE est
     * encore a son total de depart : les 2 points relevent le plafond, sinon
     * ils ne donneraient rien (paragraphe 155). */
    Character c = hero(11, 20, 8);
    character_shift0(&c, 2, +2);
    CHECK(c.cha0 == 10, "le plafond monte a 10, vu %u", c.cha0);
    CHECK(c.cha  == 10, "les points sont donnes tout de suite, vu %u", c.cha);

    /* Une CHANCE deja entamee (page 272, -2, puis retour vers Grognard)
     * recoit ses 2 points ET garde le nouveau plafond pour plus tard. */
    c = hero(11, 20, 8); c.cha = 6;
    character_shift0(&c, 2, +2);
    CHECK(c.cha == 8 && c.cha0 == 10, "6+2 sous un plafond de 10, vu %u/%u", c.cha, c.cha0);
    character_adjust_cha(&c, +5);
    CHECK(c.cha == 10, "le rattrapage s'arrete au plafond releve, vu %u", c.cha);
}

/* Le test de la ligne `V <cible> [<page> ...]`, tel que classify_line le joue :
 * la page courante, puis la cible, puis chaque page citee. Le moteur vit dans
 * scoswamp.c, qui n'est pas lie ici -- mais la REGLE, elle, ne tient qu'au
 * bitmap de rules.c, et c'est elle qu'on verifie. */
static int detour_clairiere(unsigned int courante, unsigned int cible,
                            const unsigned int* autres, unsigned int n)
{
    unsigned int i;
    if (scene_visited(courante) || scene_visited(cible)) return 1;
    for (i = 0; i < n; ++i)
        if (scene_visited(autres[i])) return 1;
    return 0;
}

static void test_clairieres_vues(void)
{
    /* "Si vous y etes deja venu, rendez-vous au 142. Sinon, lisez ce qui
     * suit." Vingt-six pages ouvrent la-dessus ; c'est ce drapeau qui les
     * departage, la ou le livre s'en remettait a la memoire du joueur. */
    unsigned int i;
    unsigned char snapshot[SCENE_MEMORY_SIZE];
    scene_memory_reset();

    CHECK(scene_visited(10) == 0, "au depart, aucune clairiere n'est vue");
    scene_mark_visited(10);
    CHECK(scene_visited(10) == 1, "la clairiere 10 est retenue");
    CHECK(scene_visited(11) == 0, "sa voisine ne l'est pas");
    CHECK(scene_visited(2)  == 0, "ni celle qui partage son octet");

    /* Export/import est le chemin utilise par les dix sauvegardes. */
    scene_memory_export(snapshot);
    scene_memory_reset();
    CHECK(scene_visited(10) == 0, "la RAM remise a zero oublie la clairiere");
    scene_memory_import(snapshot);
    CHECK(scene_visited(10) == 1,
          "sauvegarde : la scene deja visitee est restauree");

    /* La derniere scene mecanique est la 411 : elle doit tenir, et ce qui la
     * depasse doit repondre non plutot que d'ecrire hors du tableau. */
    scene_mark_visited(411);
    CHECK(scene_visited(411) == 1, "la derniere scene tient");
    scene_mark_visited(9999);
    CHECK(scene_visited(9999) == 0, "hors bornes : non, et rien d'ecrit");

    /* Une mort remet le marais a neuf : sans cela la partie suivante sauterait
     * les descriptions longues de clairieres ou elle n'est jamais allee. */
    scene_memory_reset();
    for (i = 0; i < 412; ++i)
        if (scene_visited(i)) { CHECK(0, "la remise a zero a laisse %u", i); break; }

    /* La clairiere 30, une seule porte : `V 382 270` sur la page 041.
     * Marquer 041 doit lever le detour, et NE PAS marquer 382 ni 270 --
     * c'est la page de revisite qui sera marquee a son tour, par load_scene. */
    {
        static const unsigned int clr30[] = { 270u };
        scene_memory_reset();
        CHECK(detour_clairiere(41, 382, clr30, 1) == 0,
              "premiere visite des Sables Mouvants : pas de detour");
        scene_mark_visited(41);
        CHECK(scene_visited(382) == 0, "041 vue ne marque pas 382");
        CHECK(scene_visited(270) == 0, "041 vue ne marque pas le hub 270");
        CHECK(detour_clairiere(41, 382, clr30, 1) == 1,
              "revenir en 041 renvoie bien au 382");
    }

    /* La clairiere 13, deux portes : `V 303 319` sur la page 118. Le pont
     * (045) depose au sud sur 303, la page de revisite ; le sentier de l'est
     * depose sur 118. Entrer par l'une puis par l'autre ne doit pas rejouer
     * la nuee de Scorpions -- c'etait le bug : le bitmap disait "page vue",
     * le livre dit "clairiere deja visitee". */
    {
        static const unsigned int clr13[] = { 319u };
        scene_memory_reset();
        CHECK(detour_clairiere(118, 303, clr13, 1) == 0,
              "jamais venu : la premiere visite se joue");
        scene_mark_visited(303);            /* entree par le pont */
        CHECK(scene_visited(118) == 0, "303 vue ne marque pas 118");
        CHECK(detour_clairiere(118, 303, clr13, 1) == 1,
              "deja passe par la revisite : arriver en 118 detourne");
        scene_memory_reset();
        scene_mark_visited(319);            /* seulement la page-hub */
        CHECK(detour_clairiere(118, 303, clr13, 1) == 1,
              "le hub 319 vu suffit a dire que la clairiere est connue");
        scene_memory_reset();
        scene_mark_visited(117);            /* une page d'une AUTRE clairiere */
        CHECK(detour_clairiere(118, 303, clr13, 1) == 0,
              "une page voisine non citee ne declenche rien");
    }
}

int main(void)
{
    test_dice();
    test_creation();
    test_plafond();
    test_or();
    test_chance();
    test_assaut();
    test_blessures();
    test_fuite();
    test_memoire_clairieres();
    test_clairieres_vues();
    test_perte_definitive();
    test_benediction();
    test_pierres();
    test_objets();
    if (failures == 0) printf("regles : tout passe\n");
    else               printf("regles : %d echec(s)\n", failures);
    return failures != 0;
}
