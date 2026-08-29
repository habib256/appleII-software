#include "dice.h"

/* Congruentiel lineaire 32 bits, constantes de Numerical Recipes. On ne prend
 * que les bits de poids fort : les bits bas d'un LCG ont une periode courte
 * (le bit 0 alterne), et un modulo 6 dessus donnerait des des biaises. */
static unsigned long state = 1UL;

void dice_seed(unsigned int seed)
{
    state = (unsigned long)seed;
    if (state == 0UL) state = 1UL;   /* 0 est un point fixe : le fuir */
}

static unsigned int next16(void)
{
    state = state * 1664525UL + 1013904223UL;
    return (unsigned int)((state >> 16) & 0xFFFFUL);
}

unsigned char roll_d6(void)
{
    return (unsigned char)(next16() % 6u + 1u);
}

unsigned char roll_2d6(void)
{
    return (unsigned char)(roll_d6() + roll_d6());
}

#ifdef __CC65__

#include <conio.h>

char dice_seed_from_keypress(void)
{
    unsigned int spin = 0;
    char key;

    /* Passer par kbhit/cgetc, PAS par une lecture directe de $C000. Le
     * firmware 80 colonnes du //e tient sa propre file d'entree : lire le
     * verrou materiel dans son dos lui laissait la touche, et cgetc la rendait
     * une seconde fois -- au demarrage, le 'F' du choix de langue etait relu
     * par l'ecran suivant, qui passait tout seul. */
    while (!kbhit()) {
        ++spin;
    }
    key = cgetc();

    /* Melanger le compte d'attente avec la touche : deux joueurs qui appuient
     * au meme instant sur des touches differentes ne partent pas sur la meme
     * partie. Sans ca, l'Apple II n'a aucune source de hasard au demarrage. */
    dice_seed(spin ^ ((unsigned int)key << 8) ^ 0xA53Cu);
    return key;
}

#endif
