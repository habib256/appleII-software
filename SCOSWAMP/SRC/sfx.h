/*
 * SFX - les bruitages du combat, sur le haut-parleur de la machine.
 *
 * Un seul bit de sortie en $C030 : chaque lecture fait claquer la membrane.
 * Une hauteur s'obtient en le claquant a intervalle regulier, un bruit en
 * variant l'intervalle. Tout est en assembleur (sfx.s) : une boucle C sur
 * cc65 met plusieurs dizaines de cycles par tour, ce qui plafonnerait les
 * sons dans les graves et les rendrait tributaires de l'optimiseur.
 *
 * Le Mockingboard viendra plus tard ; ces routines ne servent que le
 * haut-parleur interne, present sur toutes les machines.
 */

#ifndef SFX_H
#define SFX_H

void __fastcall__ sfx_hit(void);     /* le heros touche */
void __fastcall__ sfx_hurt(void);    /* le heros encaisse */
void __fastcall__ sfx_dodge(void);   /* les deux esquivent */
void __fastcall__ sfx_fall(void);    /* une creature s'effondre */
void __fastcall__ sfx_death(void);   /* l'ENDURANCE du heros tombe a zero */

/* Un cinquieme de seconde de silence. Il vit ici et non dans le C parce que
 * c'est la meme affaire que les sons : un compte de cycles, que l'optimiseur
 * de cc65 ferait varier d'une version a l'autre -- et qu'il supprimerait tout
 * simplement si la boucle etait ecrite en C sans effet de bord. */
void __fastcall__ sfx_beat(void);    /* le temps que le coup tombe */

#endif /* SFX_H */
