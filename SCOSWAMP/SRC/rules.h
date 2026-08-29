/*
 * RULES - Les regles de Defis Fantastiques, telles que le livre les enonce.
 *
 * Source : "Le Marais aux Scorpions" (Defis Fantastiques 08, Gallimard 1985),
 * sections "Habilete, Endurance et Chance", "Batailles", "Fuite", "Chance",
 * "Comment retablir...", "Equipement" et "La Magie" des pages liminaires.
 * Chaque regle non evidente porte ci-dessous la phrase du livre qui la fonde :
 * c'est la seule facon de trancher plus tard un desaccord entre le code et une
 * page du corpus.
 *
 * Ce fichier ne connait ni l'ecran ni ProDOS : il compile aussi bien avec cc65
 * que sur la machine hote, ou tests/test_rules.c le passe au banc.
 */

#ifndef RULES_H
#define RULES_H

/* ── Les douze Pierres Magiques ───────────────────────────────────────────
 * "Il existe en tout douze sortes de Pierres Magiques." Elles se rangent en
 * trois categories, et cette appartenance a une consequence de jeu : "il vous
 * sera impossible d'obtenir des Pierres Magiques benefiques aupres d'un
 * sorcier malefique, ou des pierres malefiques aupres d'un bon sorcier". */
typedef enum {
    /* Neutres */
    STONE_HABILETE = 0,
    STONE_ENDURANCE,
    STONE_CHANCE,
    STONE_FEU,
    STONE_GLACE,
    STONE_ILLUSION,
    /* Benefiques */
    STONE_AMITIE,
    STONE_CROISSANCE,
    STONE_BENEDICTION,
    /* Malefiques */
    STONE_TERREUR,
    STONE_FLETRISSURE,
    STONE_MALEDICTION,
    STONE_COUNT
} Stone;

typedef enum {
    STONE_NEUTRE = 0,
    STONE_BENEFIQUE,
    STONE_MALEFIQUE
} StoneKind;

StoneKind   stone_kind(Stone s);
const char* stone_name(Stone s, int english);
/* Rend STONE_COUNT si le nom n'est pas reconnu. Comparaison insensible a la
 * casse et aux accents : les pages du corpus ecrivent "Fletrissure" sans
 * accent, le livre "FLETRISSURE". */
Stone       stone_from_name(const char* name);

/* ── La Feuille d'Aventure ────────────────────────────────────────────────
 * "Bien que vous puissiez obtenir des points supplementaires d'HABILETE,
 * d'ENDURANCE et de CHANCE, ce total ne doit en aucun cas exceder vos points
 * de depart." D'ou le couple (courant, depart) pour chacune des trois. */
typedef struct {
    unsigned char hab,  hab0;
    unsigned char end,  end0;
    unsigned char cha,  cha0;
    unsigned int  gold;
    unsigned char provisions;
    unsigned char stones[STONE_COUNT];
} Character;

/* "Lancez un de. Ajoutez 6 [...] HABILETE. Lancez ensuite les deux des.
 * Ajoutez 12 [...] ENDURANCE. [...] Lancez a nouveau un de, ajoutez 6 [...]
 * CHANCE." L'equipement de depart : une epee, une cotte de mailles, un sac a
 * dos et "quelques Pieces d'Or". */
void character_roll(Character* c);

/* Ajoute (ou retire, si delta < 0) des points en respectant le plafond de
 * depart et le plancher zero. Passer par ici pour TOUTE variation : c'est le
 * seul endroit qui connait la regle du plafond. */
void character_adjust_hab(Character* c, int delta);
void character_adjust_end(Character* c, int delta);
void character_adjust_cha(Character* c, int delta);

int  character_is_dead(const Character* c);   /* ENDURANCE tombee a zero */

/* ── Tentez votre Chance ──────────────────────────────────────────────────
 * "jetez deux des. Si le chiffre obtenu est egal ou inferieur a vos points de
 * CHANCE, vous etes Chanceux [...] Chaque fois que vous Tenterez votre
 * Chance, il vous faudra oter un point a votre total de CHANCE."
 * Rend 1 si Chanceux. Le point de CHANCE est consomme dans tous les cas. */
int luck_test(Character* c);

/* ── Batailles ────────────────────────────────────────────────────────────
 * L'adversaire n'a que deux nombres : "vous inscrirez les points d'HABILETE
 * et d'ENDURANCE de la creature". */
typedef struct {
    unsigned char hab;
    unsigned char end;
    unsigned char end0;      /* l'ENDURANCE que le livre lui donne, pour la jauge */
    /* Deux exceptions que le livre pose page par page, et qu'il faut donc
     * pouvoir ecrire dans la page plutot que dans le code. Au paragraphe 12 :
     * "vous perdez 4 points d'ENDURANCE au lieu de 2 en raison de la puissance
     * du coup" (damage=4) et "si vous parvenez a reduire a 6 les points
     * d'ENDURANCE du Geant, rendez-vous au 61" (stop_at=6). */
    unsigned char damage;    /* ENDURANCE perdue par coup recu -- 2 par defaut */
    unsigned char stop_at;   /* le combat cesse a cette ENDURANCE -- 0 par defaut */
    char          name[24];
} Monster;

/* Met les valeurs par defaut du livre : 2 points par blessure, combat jusqu'a
 * zero. A appeler avant de lire les champs d'une page. */
void monster_init(Monster* m);
/* Fige l'ENDURANCE de depart. A appeler quand la page a fini d'etre lue et
 * AVANT monster_enter, qui peut rendre une valeur deja entamee. */
void monster_seal(Monster* m);
int  monster_is_beaten(const Monster* m);

typedef enum {
    ROUND_DODGE = 0,      /* Forces d'Attaque egales : "vous avez chacun esquive" */
    ROUND_HERO_HITS,
    ROUND_MONSTER_HITS
} RoundOutcome;

typedef struct {
    unsigned char hero_force;      /* 2d6 + HABILETE du heros */
    unsigned char monster_force;   /* 2d6 + HABILETE de la creature */
    RoundOutcome  outcome;
} Round;

/* Un assaut : etapes 1 a 3 du livre. Ne modifie rien, se contente de jeter les
 * des et de remplir `out` -- c'est l'appelant qui decide ENSUITE s'il Tente sa
 * Chance, parce que le livre place ce choix apres la blessure.
 *
 * Le resultat passe par un pointeur et non par la valeur de retour : cc65 rend
 * les structures par valeur de travers, et ca s'etait vu a l'ecran sous la
 * forme d'assauts a Forces d'Attaque egales qui blessaient au lieu d'esquiver.
 * Le banc d'essai sur machine hote ne pouvait pas l'attraper -- il compile
 * avec un vrai compilateur C. */
void combat_round(const Character* c, const Monster* m, Round* out);

/* Etapes 4 a 6. `use_luck` = le joueur Tente sa Chance sur cette blessure.
 *   il blesse   : -2 ENDURANCE ; Chanceux -4, Malchanceux -1
 *   il est blesse : -damage ; Chanceux -(damage-1), Malchanceux -(damage+1)
 * Rend 1 si la Chance a ete tentee ET etait bonne (pour l'affichage). */
int combat_apply(Character* c, Monster* m, const Round* r, int use_luck);

/* "Si vous prenez la Fuite, cependant, la creature vous aura automatiquement
 * inflige une blessure [...] Vous oterez alors deux points a votre ENDURANCE.
 * Pour cette blessure, vous pourrez toutefois vous servir de votre CHANCE." */
int combat_flee(Character* c, const Monster* m, int use_luck);

/* ── Memoire des clairieres ───────────────────────────────────────────────
 * "notez les modifications intervenues dans son total d'ENDURANCE et conservez
 * ces indications car il est possible que vous reveniez plus tard dans cette
 * clairiere [...] il vous faudrait peut-etre reprendre le combat la ou vous
 * l'aviez laisse." Le Marais est le seul Defis Fantastiques ou l'on revient
 * sur ses pas : sans cette memoire, fuir puis revenir soignerait le monstre. */
/* Une entree par creature laissee blessee derriere soi. Le livre ne place un
 * adversaire que dans 29 clairieres : 40 emplacements couvrent le pire cas
 * avec de la marge, pour 120 octets, la ou un octet par paragraphe en aurait
 * coute 402 -- et sur cette machine 282 octets, c'est un ecran de texte. */
#define MONSTER_SLOTS 40

void monster_memory_reset(void);

/* Reprend la file d'adversaires d'une clairiere la ou on l'avait laissee.
 *
 * "Parfois, vous les affronterez comme si elles n'etaient qu'un seul monstre ;
 * parfois, vous les combattrez une par une" : les deux rencontres a plusieurs
 * du Marais sont du second type, d'ou une file. Il faut donc se souvenir non
 * seulement de l'ENDURANCE entamee mais de QUEL adversaire etait en cours.
 *
 * Rend l'indice ou reprendre, et ajuste l'ENDURANCE de cet adversaire-la.
 * Rend `count` si toute la file est tombee lors d'une visite precedente. */
int  monster_enter(unsigned int scene, Monster* foes, int count);
void monster_remember(unsigned int scene, int index, const Monster* m);

/* ── La Magie ─────────────────────────────────────────────────────────────
 * "chacune d'elle vous permettra de jeter un sort, mais un seul, car les
 * Pierres de Magie se desintegrent des qu'on les a utilisees." */
typedef enum {
    STONE_USE_OK = 0,        /* consommee, effet narratif a la page */
    STONE_USE_NONE,          /* le heros n'en a pas */
    STONE_USE_FORBIDDEN      /* interdite a ce moment (voir stone_usable) */
} StoneUse;

void character_give_stone(Character* c, Stone s, unsigned char n);
int  character_has_stone(const Character* c, Stone s);

/* "Vous avez le droit d'utiliser les pierres d'ENDURANCE, d'HABILETE et de
 * CHANCE a tout moment, sauf au cours d'un combat. Si vous souhaitez en faire
 * usage au debut de l'affrontement, rien ne s'y oppose, mais il vous est
 * interdit de vous en servir sitot que le premier coup a ete donne."
 * `in_combat` = un assaut a deja eu lieu. */
int      stone_usable(Stone s, int in_combat);
StoneUse stone_use(Character* c, Stone s, int in_combat);

#endif /* RULES_H */
