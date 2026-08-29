#include "rules.h"
#include "dice.h"
#include <string.h>

/* ── Les Pierres ─────────────────────────────────────────────────────────── */

static const char* const kStoneFr[STONE_COUNT] = {
    "HABILETE", "ENDURANCE", "CHANCE", "FEU", "GLACE", "ILLUSION",
    "AMITIE", "CROISSANCE", "BENEDICTION",
    "TERREUR", "FLETRISSURE", "MALEDICTION"
};

static const char* const kStoneEn[STONE_COUNT] = {
    "SKILL", "STAMINA", "LUCK", "FIRE", "ICE", "ILLUSION",
    "FRIENDSHIP", "GROWTH", "BLESSING",
    "FEAR", "WITHERING", "CURSE"
};

StoneKind stone_kind(Stone s)
{
    if (s >= STONE_TERREUR) return STONE_MALEFIQUE;
    if (s >= STONE_AMITIE)  return STONE_BENEFIQUE;
    return STONE_NEUTRE;
}

const char* stone_name(Stone s, int english)
{
    if (s < 0 || s >= STONE_COUNT) return "";
    return english ? kStoneEn[s] : kStoneFr[s];
}

static char upcase(char ch)
{
    return (ch >= 'a' && ch <= 'z') ? (char)(ch - 'a' + 'A') : ch;
}

static int same_name(const char* a, const char* b)
{
    while (*a && *b) {
        if (upcase(*a) != upcase(*b)) return 0;
        ++a; ++b;
    }
    return *a == *b;
}

Stone stone_from_name(const char* name)
{
    int i;
    for (i = 0; i < STONE_COUNT; ++i) {
        if (same_name(name, kStoneFr[i]) || same_name(name, kStoneEn[i])) {
            return (Stone)i;
        }
    }
    return STONE_COUNT;
}

/* ── La Feuille d'Aventure ───────────────────────────────────────────────── */

void character_roll(Character* c)
{
    int i;

    c->hab0 = c->hab = (unsigned char)(roll_d6()  + 6);
    c->end0 = c->end = (unsigned char)(roll_2d6() + 12);
    c->cha0 = c->cha = (unsigned char)(roll_d6()  + 6);

    /* "quelques Pieces d'Or qui vous permettront de subvenir a de menues
     * depenses" : le livre ne chiffre pas, le corpus parle en dizaines. */
    c->gold       = 20;
    c->provisions = 0;
    for (i = 0; i < STONE_COUNT; ++i) c->stones[i] = 0;
}

/* Plancher a zero, plafond au total de depart. */
static void adjust(unsigned char* cur, unsigned char start, int delta)
{
    int v = (int)*cur + delta;
    if (v < 0)             v = 0;
    if (v > (int)start)    v = (int)start;
    *cur = (unsigned char)v;
}

void character_adjust_hab(Character* c, int d) { adjust(&c->hab, c->hab0, d); }
void character_adjust_end(Character* c, int d) { adjust(&c->end, c->end0, d); }
void character_adjust_cha(Character* c, int d) { adjust(&c->cha, c->cha0, d); }

int character_is_dead(const Character* c) { return c->end == 0; }

/* ── Tentez votre Chance ─────────────────────────────────────────────────── */

int luck_test(Character* c)
{
    unsigned char roll = roll_2d6();
    int lucky = (roll <= c->cha);

    /* Le point se paie meme quand la CHANCE est deja a zero -- auquel cas le
     * jet est perdu d'avance, ce que le livre assume : "plus vous vous fierez
     * a votre chance, plus vous courrez de risques". */
    if (c->cha > 0) --c->cha;
    return lucky;
}

/* ── Batailles ───────────────────────────────────────────────────────────── */

void monster_init(Monster* m)
{
    m->hab = 0; m->end = 0; m->end0 = 0;
    m->damage = 2; m->stop_at = 0; m->name[0] = '\0';
}

void monster_seal(Monster* m) { m->end0 = m->end; }

int monster_is_beaten(const Monster* m) { return m->end <= m->stop_at; }

void combat_round(const Character* c, const Monster* m, Round* out)
{
    out->monster_force = (unsigned char)(roll_2d6() + m->hab);
    out->hero_force    = (unsigned char)(roll_2d6() + c->hab);
    if (out->hero_force > out->monster_force)      out->outcome = ROUND_HERO_HITS;
    else if (out->hero_force < out->monster_force) out->outcome = ROUND_MONSTER_HITS;
    else                                          out->outcome = ROUND_DODGE;
}

int combat_apply(Character* c, Monster* m, const Round* r, int use_luck)
{
    int lucky = 0;
    int dmg;

    if (r->outcome == ROUND_HERO_HITS) {
        dmg = 2;
        if (use_luck) {
            lucky = luck_test(c);
            /* "Chanceux : oter deux points de plus. Malchanceux : la blessure
             * n'etait qu'une simple ecorchure [...] vous n'aurez ote qu'un
             * seul point." */
            dmg = lucky ? 4 : 1;
        }
        m->end = (unsigned char)((m->end > dmg) ? (m->end - dmg) : 0);
    } else if (r->outcome == ROUND_MONSTER_HITS) {
        dmg = (int)m->damage;
        if (use_luck) {
            lucky = luck_test(c);
            /* "Chanceux : rajoutez un point d'ENDURANCE [...] Malchanceux :
             * enlevez encore un point." Le modificateur est de UN point, pas
             * une moitie : sur une blessure doublee il donne 3 ou 5. */
            dmg += lucky ? -1 : 1;
        }
        character_adjust_end(c, -dmg);
    }
    return lucky;
}

int combat_flee(Character* c, const Monster* m, int use_luck)
{
    int lucky = 0;
    /* "rappelez-vous que les coups de votre adversaire vous infligent une
     * double blessure. Vous perdrez donc 4 points d'ENDURANCE en vous
     * echappant" : la blessure de fuite est celle de la creature. */
    int dmg = (int)m->damage;

    if (use_luck) {
        lucky = luck_test(c);
        dmg += lucky ? -1 : 1;
    }
    character_adjust_end(c, -dmg);
    return lucky;
}

/* ── Memoire des clairieres ──────────────────────────────────────────────── */

/* Table clairsemee : seules les clairieres ou l'on a effectivement combattu y
 * figurent. `scene == 0` marque un emplacement libre -- la clairiere 0 est
 * l'ecran de titre, elle n'a pas d'adversaire. `index` retient lequel de la
 * file etait en cours ; sans lui, fuir devant le deuxieme LOUP puis revenir
 * ferait recommencer au premier. */
static struct {
    unsigned int  scene;
    unsigned char index;
    unsigned char end;
} seen[MONSTER_SLOTS];

void monster_memory_reset(void)
{
    unsigned int i;
    for (i = 0; i < MONSTER_SLOTS; ++i) {
        seen[i].scene = 0; seen[i].index = 0; seen[i].end = 0;
    }
}

static int slot_of(unsigned int scene)
{
    int i;
    for (i = 0; i < MONSTER_SLOTS; ++i) if (seen[i].scene == scene) return i;
    return -1;
}

int monster_enter(unsigned int scene, Monster* foes, int count)
{
    int i = slot_of(scene);
    int idx;

    if (i < 0) return 0;                 /* jamais combattu ici */
    idx = (int)seen[i].index;
    if (idx >= count) return count;      /* toute la file est tombee */
    foes[idx].end = seen[i].end;
    /* L'adversaire en cours peut avoir ete acheve juste avant la fuite. */
    if (monster_is_beaten(&foes[idx])) return idx + 1;
    return idx;
}

void monster_remember(unsigned int scene, int index, const Monster* m)
{
    int i = slot_of(scene);
    if (i < 0) i = slot_of(0);      /* premier emplacement libre */
    /* Table pleine : on oublie cette clairiere, ses adversaires seront de
     * nouveau entiers au prochain passage. Impossible avec les 26 du livre. */
    if (i >= 0) {
        seen[i].scene = scene;
        seen[i].index = (unsigned char)index;
        seen[i].end   = m->end;
    }
}

/* ── Les clairieres deja parcourues ────────────────────────────────────── */

#define SCENE_BITS 52          /* 402 paragraphes arrondis a l'octet */

static unsigned char visited[SCENE_BITS];

void scene_memory_reset(void)
{
    unsigned int i;
    for (i = 0; i < SCENE_BITS; ++i) visited[i] = 0;
}

int scene_visited(unsigned int scene)
{
    if (scene >= SCENE_BITS * 8) return 0;
    return (visited[scene >> 3] & (1 << (scene & 7))) != 0;
}

void scene_mark_visited(unsigned int scene)
{
    if (scene < SCENE_BITS * 8) visited[scene >> 3] |= (1 << (scene & 7));
}

/* ── La Magie ────────────────────────────────────────────────────────────── */

void character_give_stone(Character* c, Stone s, unsigned char n)
{
    if (s >= 0 && s < STONE_COUNT) {
        /* "vous aurez le droit de prendre plusieurs pierres semblables, par
         * exemple 4 Pierres de Feu." */
        unsigned int total = (unsigned int)c->stones[s] + n;
        c->stones[s] = (unsigned char)(total > 255u ? 255u : total);
    }
}

int character_has_stone(const Character* c, Stone s)
{
    return (s >= 0 && s < STONE_COUNT) ? c->stones[s] : 0;
}

int stone_usable(Stone s, int in_combat)
{
    if (!in_combat) return 1;
    /* Seules les trois pierres de caracteristique sont bridees, et seulement
     * une fois le premier coup donne. */
    return !(s == STONE_HABILETE || s == STONE_ENDURANCE || s == STONE_CHANCE);
}

/* "vous recupererez un nombre de points egal a la moitie de votre total de
 * depart (si ce total est impair, arrondissez le resultat au chiffre
 * superieur)". */
static int half_round_up(unsigned char start) { return ((int)start + 1) / 2; }

StoneUse stone_use(Character* c, Stone s, int in_combat)
{
    if (s < 0 || s >= STONE_COUNT)  return STONE_USE_NONE;
    if (c->stones[s] == 0)          return STONE_USE_NONE;
    if (!stone_usable(s, in_combat)) return STONE_USE_FORBIDDEN;

    --c->stones[s];

    switch (s) {
    case STONE_HABILETE:
        character_adjust_hab(c, half_round_up(c->hab0));
        break;
    case STONE_ENDURANCE:
        character_adjust_end(c, half_round_up(c->end0));
        break;
    case STONE_CHANCE:
        character_adjust_cha(c, half_round_up(c->cha0));
        break;
    case STONE_MALEDICTION:
        /* "vous devrez lancer un de et reduire votre total d'ENDURANCE d'un
         * nombre de points equivalant au chiffre obtenu." Le sort qui frappe
         * l'adversaire est narratif : c'est la page qui l'ecrit. */
        character_adjust_end(c, -(int)roll_d6());
        break;
    default:
        /* FEU, GLACE, ILLUSION, AMITIE, CROISSANCE, BENEDICTION, TERREUR,
         * FLETRISSURE : aucun effet chiffre sur le heros. La pierre est
         * consommee, la page decide de la suite. BENEDICTION soigne une
         * creature (+3/+3/+3), mais le livre ne donne les totaux de depart
         * d'aucune creature : l'effet reste a la narration. */
        break;
    }
    return STONE_USE_OK;
}
