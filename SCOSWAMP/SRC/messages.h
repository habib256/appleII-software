/* Genere par SCOSWAMP.MORE/TOOLS/build_messages.py -- ne pas editer.
 * L'ordre suit MSGFR / MSGEN sur le disque. */

#ifndef MESSAGES_H
#define MESSAGES_H

enum {
    M_ESPACE_CONTINUER,
    M_ESPACE_ENCAISSER_C,
    M_VOUS_HAB_END,
    M_SAC_A_DOS,
    M_INTERDITE_EN_PLEIN,
    M_AUCUNE_PIERRE_MAGIQUE,
    M_UNE_PIERRE_SE,
    M_LE_PREMIER_COUP,
    M_PIERRE_ABSENTE,
    M_LA_PIERRE_DE,
    M_ESPACE_ENGAGER_I,
    M_F_FUITE,
    M_ESPACE_ASSAUT_SUIVANT,
    M_F_FUITE2,
    M_VOUS_FUYEZ_ELLE,
    M_CHANCEUX,
    M_MALCHANCEUX,
    M_ASSAUT_FORCE_D,
    M_VOUS_AVEZ_CHACUN,
    M_VOUS_L_AVEZ,
    M_ELLE_VOUS_A,
    M_CHANCEUX2,
    M_MALCHANCEUX2,
    M_S_EFFONDRE,
    M_HELPFR,
    M_FICHIER_D_AIDE,
    M_VOTRE_ENDURANCE_EST,
    M_ESPACE_RECOMMENCER,
    M_FEUILLE_D_AVENTURE,
    M_HABILETE_DE,
    M_ENDURANCE_DES,
    M_CHANCE_DE,
    M_UNE_EPEE_UNE,
    M_AUCUN_DE_CES,
    M_ESPACE_ENTRER_DANS,
    M_CHOISISSEZ_PIERRES,
    M_PRENDRE_UNE_PIERRE,
    M_TENTEZ_VOTRE_CHANCE,
    M_JET_DE_CHANCE,
    MSG_COUNT
};

/* Charge le catalogue de la langue voulue. Rend 0 si le fichier manque
 * ou ne contient pas MSG_COUNT lignes -- mieux vaut un ecran vide
 * qu'un catalogue decale d'une ligne. */
int  messages_load(int english);
char* msg(int id);

#endif /* MESSAGES_H */
