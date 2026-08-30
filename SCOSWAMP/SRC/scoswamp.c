#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <errno.h>
#include <unistd.h>
#include <conio.h>
#include <apple2enh.h>
#include <peekpoke.h>
#include "paths.h"
#include "memory_swap.h"
#include "hgr_rle.h"
#include "rules.h"
#include "dice.h"
#include "messages.h"
#include "sfx.h"

/* Adresse de la page HGR 1 */
#define HGR_PAGE1 ((unsigned char*)0x2000)
#define HGR_SIZE  8192
/* Le corpus ne depasse jamais 5 choix sur une page, et la ligne MV en retire
 * un a trente pages de plus : le sixieme emplacement etait une marge qu'on ne
 * pouvait plus se payer. Chaque emplacement coute 77 octets -- deux vides,
 * c'est un ecran de texte gaspille. reflow_txt.py refuse une page qui en
 * aurait plus, et c'est lui qui garde l'invariant. */
#define MAX_CHOICES 5
/* Pas FILENAME_MAX : build_paths n'ecrit jamais que "N999.RLE" (9 octets) et
 * "N999" (5). Deux champs de 64 octets pour ca, c'etaient 96 octets de BSS
 * dormants -- et c'est le seul levier memoire du programme qui ne depende
 * d'aucune mesure du corpus. */
#define MAX_PATH  16

/* Mise en page d'une scene, en dur sur les 24 lignes de l'ecran 80 colonnes :
 *
 *   ligne  1      barre en video inverse : titre de la scene + rappel touches
 *   lignes 2-20   le texte, deja replie a 78 colonnes dans le fichier
 *   lignes 21-24  les choix
 *
 * Les 4 lignes du bas ne sont pas un choix esthetique : ce sont EXACTEMENT
 * celles que le mode mixte laisse voir sous l'image HGR. Les choix y etant
 * toujours, on peut choisir sans quitter l'illustration.
 *
 * Le corps et les choix tiennent dans ce budget pour les 804 pages du corpus,
 * et SCOSWAMP.MORE/TOOLS/reflow_txt.py le verifie fichier par fichier. */
#define BODY_ROW0    1    /* premiere ligne de texte (0 = barre de titre) */
#define BODY_ROWS    19   /* lignes 2 a 20 */
#define CHOICE_ROW0  20   /* lignes 21 a 24 */
#define CHOICE_ROWN  23
#define CHOICE_COL2  40   /* colonne du 2e choix quand deux tiennent sur 1 ligne */
#define CHOICE_WIDTH 39   /* largeur utile d'une colonne de choix */

/* Le livre ne met jamais plus de trois adversaires sur une page : les deux
 * LOUPS du 224, les trois BRIGANDS du 235. */
#define MAX_FOES 3

/* Le titre de choix le plus long du corpus fait 72 caracteres, remesure le
 * 2026-08-30 sur les deux langues. 76 laisse trois caracteres de battement --
 * a cinq emplacements, chaque caractere de rab se paie cinq fois, donc
 * descendre a 73 rend 15 octets. Levier tenu en reserve, PAS pris : le corpus
 * est en cours d'edition ailleurs, et un titre de 73 caracteres serait
 * tronque a l'ecran sans que rien ne le dise. reflow_txt.py le refuse
 * desormais, ce qui rendra le levier prenable. */
#define CHOICE_TITLE 76

typedef struct {
    int scene_id;
    /* Pierre remise en choisissant cette option, STONE_COUNT si aucune. Le
     * livre pose le cas au paragraphe 283 : "Il vous donne alors une Pierre de
     * Magie benefique (choisissez vous-meme laquelle)". */
    unsigned char grant;
    /* Pierre exigee par ce choix, STONE_COUNT si aucune. Elle est consommee
     * en le prenant : "les Pierres de Magie se desintegrent des qu'on les a
     * utilisees". Sans ce champ, les 37 choix du corpus qui depensent une
     * Pierre ne touchaient pas au sac -- et rien n'empechait d'en lancer une
     * qu'on n'avait pas. */
    unsigned char require;
    char title[CHOICE_TITLE];
} Choice;

/* Structure pour l'état global de l'application */
typedef struct {
    int current_scene;
    int video_mode;  /* 0=texte 80col, 1=HGR plein (2=mixte pour combat futur) */
    Choice choices[MAX_CHOICES];
    int num_choices;
    char language[3];  /* FR ou EN */
    char imgPath[MAX_PATH];
    char txtPath[MAX_PATH];
    int has_image;    /* image de la scene decodee en page HGR 1 ? */

    /* La Feuille d'Aventure et la rencontre en cours. */
    Character hero;
    int       hero_ready;    /* les des ont ete jetes */
    /* "Parfois, vous les affronterez comme si elles n'etaient qu'un seul
     * monstre ; parfois, vous les combattrez une par une." Les deux rencontres
     * a plusieurs du Marais sont du second type : une file, affrontee dans
     * l'ordre ou la page la donne. */
    Monster   foes[MAX_FOES];
    int       foe_count;     /* nombre de lignes M sur la page */
    int       foe_cur;       /* adversaire en cours dans la file */
    int       flee_target;   /* scene ou mene la Fuite, -1 si la page n'en offre pas */
    int       pending_scene; /* scene a charger au prochain tour de boucle, -1 sinon */
    int       revisit;       /* ligne V : ou aller si la clairiere est deja vue, -1 sinon */
    unsigned char choose_n;  /* Pierres a choisir en entrant, 0 si aucune */
    char      choose_cats[4];/* categories permises : N, B, M */
    int       luck_ok;       /* scene si Chanceux, -1 si la page ne teste rien */
    int       luck_ko;       /* scene si Malchanceux */
    int       luck_dok;      /* ENDURANCE gagnee ou perdue sur la branche Chanceux */
    int       luck_dko;
    /* Ligne MV : ou aller quand le dernier adversaire de la file est tombe,
     * -1 si la page rend la main aux choix comme avant. */
    int       win_scene;
    /* Ligne ED : le jet de des visible. `dice_n` porte le SIGNE (gain ou
     * perte) et le NOMBRE de des dans sa valeur absolue ; 0 = pas de jet. */
    signed char   dice_n;
    unsigned char dice_carac;  /* 0 END, 1 HAB, 2 CHA, 3 OR */
    /* Ligne CS : 2d6 contre une caracteristique NOMMEE, sans depenser de
     * point de CHANCE -- le "Lancez deux des. Si le total est inferieur ou
     * egal a vos points d'ENDURANCE..." du livre. -1 = pas de test. */
    int       cs_ok, cs_ko;
    unsigned char cs_carac;
    /* Ligne MB : duel au premier sang. La premiere blessure arrete le combat
     * et decide de la suite -- qui a touche, pas qui est mort. -1 = non. */
    int       mb_ok, mb_ko;
    /* Ligne DV : l'ENDURANCE perdue au dernier combat GAGNE, pour que la
     * page d'apres n'ait pas a demander au joueur d'evaluer ses blessures.
     * dv_done bloque la cascade a la premiere ligne DV qui correspond. */
    unsigned char last_loss;
    unsigned char dv_done;
} AppState;

/* Variables globales optimisées */
AppState app;
/* La page la plus longue du corpus fait 1252 octets (TEXTFR/N350/N361.TXT),
 * remesure le 2026-08-30. Le tampon est la plus grosse variable du programme,
 * et 1344 lui laisse 7 % de marge. Descendre a 1280 rendrait 64 octets et
 * laisserait encore 27 octets au-dessus de la plus grosse page (fread en lit
 * SIZE-1) : levier tenu en reserve, PAS pris, parce qu'une page qui deborde
 * est tronquee en silence et que le corpus est en cours d'edition ailleurs.
 * Le prendre veut dire descendre le garde de reflow_txt.py a 1279 du meme
 * geste. reflow_txt.py refuse une page qui depasserait. */
#define FILE_BUFFER_SIZE 1344
char file_buffer[FILE_BUFFER_SIZE];

/* Decoupage de la scene courante. Titre et lignes de corps ne sont pas
 * recopies : ce sont des pointeurs DANS file_buffer, dont les fins de ligne
 * ont ete remplacees par des '\0'. Le buffer n'est reecrit qu'au chargement
 * de la scene suivante, donc ils restent valides tant qu'on affiche celle-ci
 * -- et ca evite un seul octet de copie. */
static char* scene_title;
static char* body_lines[BODY_ROWS];
static int   body_count;

static int enter_asset_dir(const char* kind, int scene_id)
{
    char bucket[5];
    unsigned int subdirectory = ((unsigned int)scene_id / 50u) * 50u;

    if (chdir("/SCOSWAMP") != 0) return 0;
    if (chdir(kind) != 0) return 0;
    sprintf(bucket, "N%03u", subdirectory);
    if (chdir(bucket) != 0) return 0;
    return 1;
}

static void report_open_error(const char* path)
{
    unsigned char prodos_error = (unsigned char)_oserror;
    int c_error = errno;

    cprintf("Erreur ouverture %s\r\n", path);
    cprintf("Source: fopen(path, r)\r\n");
    cprintf("errno=%d ProDOS=$%02X\r\n", c_error, prodos_error);
}

/* Fonction pour charger une image HGR */
/* Charge IMG/<bucket>/<prefixe><id>.RLE en page HGR 1.
 *
 *   'N' : l'illustration de la clairiere ;
 *   'B' : l'image de bataille, les deux adversaires face a face. Elle est
 *         optionnelle -- quand elle manque, on retombe sur l'illustration de
 *         la clairiere, qui montre deja la creature.
 *
 * build_paths ecrit "N012.RLE" ; changer le premier caractere suffit, et evite
 * un second sprintf dans un binaire ou chaque octet compte. */
static int load_hgr_image_as(int scene_id, char prefix) {
    if (build_paths(scene_id, app.language, app.imgPath, app.txtPath) != 0) {
        return 0;  /* Scene ID hors plage */
    }
    app.imgPath[0] = prefix;

    if (!enter_asset_dir("IMG", scene_id)) {
        return 0;
    }
    return hgr_rle_load(app.imgPath);
}

int load_hgr_image(int scene_id) { return load_hgr_image_as(scene_id, 'N'); }

/* Soft switches pour les modes video - version optimisée avec memory swap */
void set_video_mode(int mode) {
    if (mode == 0) {
        /* Mode texte 80 colonnes - restaurer le texte sauvegardé */
        switch_to_text();
        app.video_mode = 0;
    } else if (mode == 1) {
        /* Mode HGR plein écran - sauvegarder le texte actuel */
        switch_to_hgr();
        app.video_mode = 1;
    } else if (mode == 2) {
        /* Mode mixte HGR + 4 lignes texte */
        switch_to_mixed();
        app.video_mode = 2;
    }
}

/* ── Mise en page ─────────────────────────────────────────────────────── */

/* Barre de titre, ligne 1, en video inverse sur les 80 colonnes.
 *
 * Le rappel des touches vit ici plutot qu'en bas : les 4 lignes du bas sont
 * reservees aux choix, et un rappel fixe en tete est de toute facon plus
 * lisible qu'une ligne qui se deplace avec la longueur du texte. */
static char title_bar[81];

static char* put_str(char* p, const char* t) { while (*t) *p++ = *t++; return p; }

static char* put_u8(char* p, unsigned char v)
{
    if (v >= 100) *p++ = (char)('0' + v / 100u);
    if (v >= 10)  *p++ = (char)('0' + (v / 10u) % 10u);
    *p++ = (char)('0' + v % 10u);
    return p;
}

static void render_title_bar(void)
{
    char sheet[40];
    int i, n;

    /* Une fois les des jetes, la barre porte la Feuille d'Aventure : les trois
     * caracteristiques sont ce qu'on consulte a chaque page, et le livre les
     * veut sous les yeux en permanence. Avant la creation du personnage, elle
     * sert encore au rappel des touches. */
    for (i = 0; i < 80; i++) title_bar[i] = ' ';
    title_bar[80] = '\0';

    if (scene_title != NULL) {
        n = (int)strlen(scene_title);
        if (n > 40) n = 40;
        memcpy(title_bar + 1, scene_title, n);
        /* Le rappel se glisse apres le titre : c'est le seul endroit visible
         * en permanence, et [H] mene au detail. Il suit la langue, comme les
         * etiquettes de caracteristiques. */
        if (app.hero_ready) {
            memcpy(title_bar + n + 3,
                   (app.language[0] == 'F') ? "I:SAC   H:AIDE"
                                            : "I:BAG   H:HELP", 14);
        }
    }
    if (app.hero_ready) {
        /* Formatage a la main : `sprintf` ferait entrer tout le formateur de
         * chaines dans le binaire pour ces six nombres, et la fenetre
         * $4000-$9600 est pleine. */
        /* Les etiquettes suivent la langue : en anglais ce sont SKILL,
         * STAMINA et LUCK, les trois mots de Fighting Fantasy. Elles restaient
         * en francais quelle que soit la partie. */
        /* Le test en clair plutot que is_fr() : cette fonction est definie
         * plus bas, avec le reste de l'ecran de combat. */
        char* q = sheet;
        const int fr = (app.language[0] == 'F');
        q = put_str(q, fr ? "HAB " : "SKL ");
        q = put_u8(q, app.hero.hab); *q++ = '/';
        q = put_u8(q, app.hero.hab0);
        q = put_str(q, fr ? "  END " : "  STA ");
        q = put_u8(q, app.hero.end); *q++ = '/';
        q = put_u8(q, app.hero.end0);
        q = put_str(q, fr ? "  CHA " : "  LCK ");
        q = put_u8(q, app.hero.cha); *q++ = '/';
        q = put_u8(q, app.hero.cha0);
        n = (int)(q - sheet);
        memcpy(title_bar + 79 - n, sheet, n);
    } else {
        /* Avant la creation du personnage : le rappel des touches. Il vit au
         * catalogue -- la barre ne se peint jamais avant messages_load. */
        const char* hint = msg(M_TOUCHES);
        n = (int)strlen(hint);
        memcpy(title_bar + 79 - n, hint, n);
    }

    revers(1);
    cputsxy(0, 0, title_bar);
    revers(0);
}

/* Les choix, dans les 4 lignes du bas.
 *
 * Deux par ligne quand les deux tiennent dans une demi-largeur, sinon un seul
 * sur toute la ligne : c'est ce qui fait entrer jusqu'a 5 choix dans 4 lignes
 * (6 scenes du livre en ont 5). Rien n'est jamais ecrit dans la derniere
 * cellule de l'ecran : le firmware ferait scroller et toute la mise en page
 * remonterait d'une ligne. */
/* Un choix qui exige une Pierre absente du sac ne porte pas de lettre : on
 * le voit -- le livre l'ecrit, et savoir ce qu'une Pierre aurait permis fait
 * partie de la lecture -- mais on ne peut pas le prendre. */
static int choice_available(int i)
{
    unsigned char req = app.choices[i].require;
    return req >= STONE_COUNT || character_has_stone(&app.hero, (Stone)req);
}

static char choice_tag(int i)
{
    return choice_available(i) ? (char)('A' + i) : '-';
}

static void render_choices(void)
{
    int i = 0;
    int row = CHOICE_ROW0;

    while (i < app.num_choices && row <= CHOICE_ROWN) {
        if (i + 1 < app.num_choices &&
            (int)strlen(app.choices[i].title)     <= CHOICE_WIDTH - 3 &&
            (int)strlen(app.choices[i + 1].title) <= CHOICE_WIDTH - 3) {
            gotoxy(0, row);
            cprintf("%c) %s", choice_tag(i), app.choices[i].title);
            gotoxy(CHOICE_COL2, row);
            cprintf("%c) %s", choice_tag(i + 1), app.choices[i + 1].title);
            i += 2;
        } else {
            gotoxy(0, row);
            cprintf("%c) %.75s", choice_tag(i), app.choices[i].title);
            i += 1;
        }
        row++;
    }
}

static void render_scene(void)
{
    int i;

    clrscr();
    render_title_bar();
    for (i = 0; i < body_count; i++) {
        cputsxy(0, BODY_ROW0 + i, body_lines[i]);
    }
    render_choices();
}

/* ── Lecture d'une page de scene ──────────────────────────────────────── */

/* Avance sur les chiffres puis sur les espaces, et rend la valeur lue. */
static char* take_uint(char* t, unsigned int* out)
{
    unsigned int v = 0;
    while (*t >= '0' && *t <= '9') { v = v * 10u + (unsigned int)(*t - '0'); t++; }
    while (*t == ' ') t++;
    *out = v;
    return t;
}

/* La meme chose, signe compris : les effets d'une ligne CE sont negatifs. */
static char* take_int(char* t, int* out)
{
    unsigned int v;
    int neg = 0;
    if (*t == '-') { neg = 1; t++; } else if (*t == '+') t++;
    t = take_uint(t, &v);
    *out = neg ? -(int)v : (int)v;
    return t;
}

/* Avance sur un mot, le termine par '\0', et rend le debut du suivant. */
static char* take_word(char* t, char** word)
{
    *word = t;
    while (*t && *t != ' ') t++;
    if (*t == ' ') { *t = '\0'; t++; while (*t == ' ') t++; }
    return t;
}

/* Les quatre mots que E, E0, CE et ED acceptent, lus une seule fois.
 * Quatre branches repetaient la meme table de strcmp ; ED en aurait fait une
 * cinquieme, et sur cette machine neuf comparaisons de chaines valent un
 * ecran de texte. Rend 4 si le mot n'est pas reconnu.
 * Les mots restent en francais dans les deux corpus, comme les lignes E/E0/CE
 * existantes : c'est de la mecanique, pas du texte affiche. */
static unsigned char carac_of(const char* w)
{
    /* L'INITIALE suffit : ENDURANCE, HABILETE, CHANCE et OR sont les quatre
     * seuls mots que le format admet, et leurs premieres lettres different
     * deux a deux. Quatre strcmp coutaient les quatre chaines en RODATA plus
     * leur boucle, pour distinguer ce qu'un octet distingue. La contrepartie
     * est qu'une faute de frappe passe -- "EDURANCE" serait lue comme
     * ENDURANCE -- et c'est reflow_txt.py qui la refuse, du cote ou l'on peut
     * se payer une verification. */
    switch (*w) {
    case 'E': return 0;
    case 'H': return 1;
    case 'C': return 2;
    case 'O': return 3;
    }
    return 4;
}

/* L'effet, applique par la seule porte qui connaisse les regles de bornes :
 * plafond au total de depart pour les trois caracteristiques, plancher zero
 * pour les quatre. */
static void carac_apply(unsigned char c, int d)
{
    switch (c) {
    case 0: character_adjust_end(&app.hero, d);  break;
    case 1: character_adjust_hab(&app.hero, d);  break;
    case 2: character_adjust_cha(&app.hero, d);  break;
    case 3: character_adjust_gold(&app.hero, d); break;
    }
}

/* Ajoute un choix a la page. Quatre directives fabriquaient chacune le leur
 * a la main : le meme bloc de 120 octets, quatre fois. */
static void push_choice(int scene, unsigned char grant, unsigned char require,
                        const char* title)
{
    Choice* c;
    if (app.num_choices >= MAX_CHOICES) return;
    c = &app.choices[app.num_choices++];
    c->scene_id = scene;
    c->grant    = grant;
    c->require  = require;
    strncpy(c->title, title, CHOICE_TITLE - 1);
    c->title[CHOICE_TITLE - 1] = '\0';
}

/* Classe une ligne du fichier. Le format d'une page :
 *
 *   T  <id> <titre>             titre, en video inverse ligne 1
 *   V  <id>                     "si vous y etes deja venu, rendez-vous au
 *                               <id>" -- doit preceder tout le reste de la
 *                               page, qu'un detour annule
 *   M  <hab> <end> <nom>        la creature de la clairiere (Batailles)
 *   MD <n>                      ses coups coutent n ENDURANCE (defaut 2)
 *   MS <n>                      le combat cesse a n ENDURANCE (defaut 0)
 *   MB <ok> <ko>                duel au premier sang : la premiere blessure
 *                               arrete le combat, <ok> si vous touchez,
 *                               <ko> si c'est vous qui etes touche
 *   CS <STAT> <ok> <ko>         "Lancez deux des" contre la caracteristique
 *                               nommee, gratuit (pas de point de CHANCE)
 *   DV <max> <id>               en cascade : premiere ligne dont la perte du
 *                               dernier combat est <= max fabrique l'unique
 *                               choix "continuer" vers <id>
 *   MV <id>                     apres le dernier adversaire tombe, la page
 *                               envoie en <id> sans repasser par les choix.
 *                               Le jumeau de CF cote victoire : elle remplace
 *                               le choix de garde que le joueur devait
 *                               prendre lui-meme, et rend la ligne d'ecran
 *                               qu'il mangeait sur les 4 disponibles
 *   E  <CARAC> <delta>          effet a l'entree : E ENDURANCE -2
 *   E0 <CARAC> <delta>          perte qui entame le TOTAL DE DEPART, donc
 *                               definitive : E0 HABILETE -2
 *   ED <CARAC> <+-ndes>         jet de des VISIBLE : `ED ENDURANCE -1` =
 *                               "lancez un de et perdez autant de points
 *                               d'ENDURANCE" ; `ED OR +1` = un de de Pieces
 *                               d'Or. Le signe dit gain ou perte, la valeur
 *                               absolue le nombre de des (1 ou 2). Le jet est
 *                               DIFFERE, contrairement a CE : la ligne remplit
 *                               seulement dice_n / dice_carac, et load_scene
 *                               le joue une fois la page AFFICHEE -- sinon le
 *                               joueur ne verrait rien. Donc la position de la
 *                               ligne dans le fichier n'ordonne rien : le jet
 *                               tombe toujours avant le combat de la page
 *   CE <CARAC> <dok> <dko>      "Tentez votre Chance" sans branchement : il
 *                               decide d'un effet, la page continue
 *   P  <PIERRE> <n>             le sorcier vous donne n Pierres Magiques
 *   PC <n> <cats>               il vous en laisse choisir n parmi les
 *                               categories citees (N neutre, B benefique,
 *                               M malefique)
 *   CL <ok> <ko> [<dok> <dko>]  "Tentez votre Chance" : la page envoie en
 *                               <ok> si Chanceux, en <ko> sinon, avec un
 *                               effet d'ENDURANCE optionnel sur chaque
 *                               branche -- le livre en pose deux ("si vous
 *                               etes Chanceux, vous perdez 2 points
 *                               d'ENDURANCE et vous vous rendez au 270")
 *   CP <PIERRE> <id> <titre>    choix qui remet une Pierre Magique
 *   CU <PIERRE> <id> <titre>    choix qui EXIGE et consomme une Pierre
 *   C  <id> <titre>             choix
 *   CF <id> <titre>             Fuite -- "n'est possible que si elle est
 *                               specifiee a la page ou vous vous trouverez"
 *   <reste>                     le texte de la scene
 */
static void classify_line(char* l)
{
    char* t;
    char* word;
    unsigned int a, b;

    if (app.revisit >= 0) return;   /* la page est court-circuitee (ligne V) */

    /* MD et MS qualifient le dernier adversaire declare. */
    if (l[0] == 'M' && l[1] == 'D' && l[2] == ' ' && app.foe_count > 0) {
        take_uint(l + 3, &a);
        app.foes[app.foe_count - 1].damage = (unsigned char)a;
        return;
    }
    if (l[0] == 'M' && l[1] == 'S' && l[2] == ' ' && app.foe_count > 0) {
        take_uint(l + 3, &a);
        app.foes[app.foe_count - 1].stop_at = (unsigned char)a;
        return;
    }
    /* MV se lit avec MD et MS -- donc avant le test `M ` d'une seule lettre,
     * qui l'avalerait -- mais sans leur garde `foe_count > 0` : MV ne qualifie
     * pas le dernier adversaire declare, et peut preceder les lignes M. */
    if (l[0] == 'M' && l[1] == 'V' && l[2] == ' ') {
        take_uint(l + 3, &a);
        app.win_scene = (int)a;
        return;
    }
    if (l[0] == 'M' && l[1] == 'B' && l[2] == ' ') {
        /* MB <si-vous-touchez> <si-touche> : duel au premier sang. */
        t = take_uint(l + 3, &a);
        app.mb_ok = (int)a;
        take_uint(t, &b);
        app.mb_ko = (int)b;
        return;
    }
    if (l[0] == 'M' && l[1] == ' ') {
        /* Chaque ligne M ajoute un adversaire a la file, dans l'ordre de la
         * page -- c'est l'ordre dans lequel le livre les fait venir. */
        if (app.foe_count < MAX_FOES) {
            Monster* f = &app.foes[app.foe_count];
            monster_init(f);
            t = take_uint(l + 2, &a);
            t = take_uint(t, &b);
            f->hab = (unsigned char)a;
            f->end = (unsigned char)b;
            strncpy(f->name, t, sizeof(f->name) - 1);
            f->name[sizeof(f->name) - 1] = '\0';
            app.foe_count++;
        }
        return;
    }
    if (l[0] == 'E' && l[1] == '0' && l[2] == ' ') {
        /* Perte qui entame le total de depart : elle ne se rattrape jamais. */
        int delta;
        unsigned char k;
        t = take_word(l + 3, &word);
        delta = atoi(t);
        /* Deux appels propres -- ce n'est pas la primitive de carac_apply,
         * celle-ci abaisse le PLAFOND -- mais le meme aiguillage. */
        k = carac_of(word);
        if      (k == 0) character_lower_end0(&app.hero, delta);
        else if (k == 1) character_lower_hab0(&app.hero, delta);
        return;
    }
    if (l[0] == 'C' && l[1] == 'E' && l[2] == ' ') {
        /* "Tentez votre Chance" qui ne branche pas : il decide seulement d'un
         * effet, et la page continue de se lire. Le livre le fait souvent --
         * "si vous etes Malchanceux, vous tombez et perdez 2 points
         * d'ENDURANCE, mais vous parvenez tout de meme a grimper". */
        int dok, dko;
        t = take_word(l + 3, &word);
        t = take_int(t, &dok);
        take_int(t, &dko);
        carac_apply(carac_of(word), luck_test(&app.hero) ? dok : dko);
        return;
    }
    /* ED avant E, meme raison que MV avant M. */
    if (l[0] == 'E' && l[1] == 'D' && l[2] == ' ') {
        t = take_word(l + 3, &word);
        app.dice_carac = carac_of(word);
        /* atoi et pas take_uint : ici le signe porte le sens de la ligne.
         * Aucun bornage ici -- deux comparaisons 16 bits signees coutaient 55
         * octets pour un cas qui ne se presente pas. C'est run_dice_roll qui
         * tient la regle "deux des au plus", et il la tient quoi qu'ecrive la
         * page. */
        if (app.dice_carac < 4) app.dice_n = (signed char)atoi(t);
        return;
    }
    if (l[0] == 'E' && l[1] == ' ') {
        t = take_word(l + 2, &word);
        /* L'or passe par character_adjust_gold comme le reste : un
         * `gold += delta` sur un champ non signe donnait 65535 Pieces d'Or au
         * heros sans le sou qui en depense une. */
        carac_apply(carac_of(word), atoi(t));
        return;
    }
    if (l[0] == 'P' && l[1] == 'C' && l[2] == ' ') {
        t = take_uint(l + 3, &a);
        app.choose_n = (unsigned char)a;
        strncpy(app.choose_cats, t, sizeof(app.choose_cats) - 1);
        app.choose_cats[sizeof(app.choose_cats) - 1] = '\0';
        return;
    }
    if (l[0] == 'P' && l[1] == ' ') {
        Stone s;
        t = take_word(l + 2, &word);
        s = stone_from_name(word);
        if (s != STONE_COUNT) {
            unsigned int n = 1;
            if (*t) take_uint(t, &n);
            character_give_stone(&app.hero, s, (unsigned char)n);
        }
        return;
    }
    if (l[0] == 'C' && l[1] == 'L' && l[2] == ' ') {
        t = take_uint(l + 3, &a);
        app.luck_ok = (int)a;
        t = take_uint(t, &a);
        app.luck_ko = (int)a;
        /* Les deux deltas sont optionnels et peuvent etre negatifs : atoi
         * plutot que take_uint, qui ne lit pas le signe. */
        if (*t) {
            app.luck_dok = atoi(t);
            while (*t && *t != ' ') t++;
            while (*t == ' ') t++;
            app.luck_dko = atoi(t);
        }
        return;
    }
    if (l[0] == 'C' && l[1] == 'U' && l[2] == ' ') {
        Stone st;
        t = take_word(l + 3, &word);
        st = stone_from_name(word);
        t = take_uint(t, &a);
        if (st != STONE_COUNT)
            push_choice((int)a, (unsigned char)STONE_COUNT, (unsigned char)st, t);
        return;
    }
    if (l[0] == 'C' && l[1] == 'P' && l[2] == ' ') {
        Stone st;
        t = take_word(l + 3, &word);
        st = stone_from_name(word);
        t = take_uint(t, &a);
        if (st != STONE_COUNT)
            push_choice((int)a, st, (unsigned char)STONE_COUNT, t);
        return;
    }
    if (l[0] == 'V' && l[1] == ' ') {
        /* "Si vous y etes deja venu, rendez-vous au 142. Sinon, lisez ce qui
         * suit." Le detour decide, plus rien de la page ne doit jouer : ni
         * son texte, ni ses choix, ni surtout ses lignes E et P, qui
         * donneraient une seconde fois ce qu'on a deja pris. D'ou le garde
         * en tete de fonction -- et l'invariant, verifie par reflow_txt.py,
         * que la ligne V precede tout le reste. */
        take_uint(l + 2, &a);
        if (scene_visited((unsigned int)app.current_scene)) app.revisit = (int)a;
        return;
    }
    if (l[0] == 'C' && l[1] == 'S' && l[2] == ' ') {
        /* CS <STAT> <ok> <ko> : le jet est joue par load_scene, comme un jet
         * de Chance, mais contre la caracteristique nommee et gratuit. */
        t = take_word(l + 3, &word);
        app.cs_carac = carac_of(word);
        t = take_uint(t, &a);
        app.cs_ok = (int)a;
        take_uint(t, &b);
        app.cs_ko = (int)b;
        return;
    }
    if (l[0] == 'D' && l[1] == 'V' && l[2] == ' ') {
        /* DV <max> <id>, en cascade : la premiere ligne dont la perte du
         * dernier combat ne depasse pas <max> fabrique l'unique choix de la
         * page -- "continuer" -- vers sa cible. Le moteur repond ainsi a
         * "Evaluez vos blessures" a la place du joueur. */
        t = take_uint(l + 3, &a);
        t = take_uint(t, &b);
        if (!app.dv_done && app.last_loss <= (unsigned char)a) {
            app.dv_done = 1;
            push_choice((int)b, (unsigned char)STONE_COUNT,
                        (unsigned char)STONE_COUNT, msg(M_K_CONTINUER));
        }
        return;
    }
    if (l[0] == 'C' && l[1] == 'F' && l[2] == ' ') {
        t = take_uint(l + 3, &a);
        app.flee_target = (int)a;
        return;
    }

    if (l[0] == 'T' && l[1] == ' ') {
        t = l + 2;
        while (*t >= '0' && *t <= '9') t++;
        while (*t == ' ') t++;
        scene_title = t;
    } else if (l[0] == 'C' && l[1] == ' ') {
        /* take_uint plutot que sscanf : sur cc65 le premier appel a scanf
         * fait entrer plusieurs kilo-octets d'analyseur de format dans le
         * binaire, pour lire trois chiffres. */
        t = take_uint(l + 2, &a);
        if (t != l + 2 && *t != '\0')
            push_choice((int)a, (unsigned char)STONE_COUNT,
                        (unsigned char)STONE_COUNT, t);
    } else if (body_count < BODY_ROWS) {
        /* Pas de ligne vide en tete : le fichier en a une sous le titre, et
         * elle couterait la ligne de marge du budget de 19. */
        if (body_count > 0 || l[0] != '\0') {
            body_lines[body_count++] = l;
        }
    }
}

/* Fonction commune pour parser un fichier texte */
int parse_text_file(int scene_id, int display_mode) {
    FILE* f;
    size_t bytes_read;
    char* p;
    char* q;
    char* end;
    int crlf;

    /* Build paths */
    if (build_paths(scene_id, app.language, app.imgPath, app.txtPath) != 0) {
        if (display_mode) {
            cprintf("Erreur: scene %d hors plage (0-999).\r\n", scene_id);
            cprintf("Appuyez sur une touche...\r\n");
            cgetc();
        }
        return 0;
    }

    /* Réinitialiser la scène */
    app.num_choices = 0;
    body_count = 0;
    scene_title = NULL;

    /* Mode texte si on doit afficher */
    if (display_mode) {
        set_video_mode(0);
        videomode(VIDEOMODE_80COL);
        clrscr();
    }
    
    /* cc65/ProDOS rejects multi-component names in fopen on this runtime.
     * Navigate one component at a time, then open only the short basename. */
    if (!enter_asset_dir(strcmp(app.language, "FR") == 0 ? "TEXTFR" : "TEXTEN",
                         scene_id)) {
        if (display_mode) {
            cprintf("Source: chdir composant texte\r\n");
            cprintf("errno=%d ProDOS=$%02X\r\n", errno,
                    (unsigned char)_oserror);
            cprintf("Appuyez sur une touche...\r\n");
            cgetc();
        }
        return 0;
    }

    /* Open text file */
    f = fopen(app.txtPath, "r");
    if (!f) {
        if (display_mode) {
            report_open_error(app.txtPath);
            cprintf("Appuyez sur une touche...\r\n");
            cgetc();
        }
        return 0;
    }
    
    /* Read file into buffer */
    bytes_read = fread(file_buffer, 1, sizeof(file_buffer) - 1, f);
    fclose(f);
    
    if (bytes_read == 0) {
        if (display_mode) {
            cprintf("Erreur: fichier vide.\r\n");
        }
        return 0;
    }
    file_buffer[bytes_read] = '\0';

    /* Découper le buffer EN PLACE : chaque fin de ligne devient un '\0' et on
     * ne garde que des pointeurs. Plus de recopie ligne par ligne, donc plus
     * de tampon de 120 octets sur la pile ni de limite de longueur. */
    p = file_buffer;
    end = file_buffer + bytes_read;
    while (p < end) {
        q = p;
        while (q < end && *q != '\r' && *q != '\n') q++;
        crlf = (q + 1 < end && *q == '\r' && *(q + 1) == '\n');
        *q = '\0';
        classify_line(p);
        p = q + 1;
        if (crlf) p++;
    }

    if (display_mode && app.revisit < 0) {
        render_scene();
    }

    return 1;
}

/* Parser et afficher le fichier texte */
void display_scene_text(int scene_id) {
    parse_text_file(scene_id, 1);  /* Mode display */
}

/* Cycle des modes video : texte 80 col -> HGR plein -> HGR mixte -> texte.
 *
 * Que des soft-switches. Le texte reste en $400-$7FF et l'image en
 * $2000-$3FFF pendant tout le cycle, donc aucune bascule ne relit le disque ni
 * ne repeint quoi que ce soit -- et aucune ne passe par un mode intermediaire.
 * L'ancienne version redessinait l'ecran depuis le fichier de scene a chaque
 * retour au texte : c'etait l'acces disque et le clignotement. */
void cycle_video_mode(void) {
    if (!app.has_image) {
        return;  /* Pas d'image pour cette scene : le texte reste. */
    }
    app.video_mode = (app.video_mode + 1) % 3;
    set_video_mode(app.video_mode);
}

/* ── Combat et sac a dos ──────────────────────────────────────────────────
 *
 * Tout se joue dans les 4 lignes du bas : en mode mixte, l'illustration de la
 * creature reste a l'ecran pendant l'echange d'assauts. Les regles elles-memes
 * sont dans rules.c, qui ne connait pas l'ecran ; ici il n'y a que de
 * l'affichage et le dialogue avec le joueur.
 */

static int is_fr(void) { return app.language[0] == 'F'; }

/* Les invites qui reviennent, nommees une fois : cc65 ne fusionne pas les
 * litteraux identiques, chaque repetition coutait sa place en RODATA. */
static const char* msg_continue(void)
{ return msg(M_ESPACE_CONTINUER); }

/* Le nom de la barre d'espace, seul mot de l'invite qui ne vient pas du
 * catalogue : il est le meme dans les deux langues a une lettre pres. */
static const char* msg_space(void)
{ return is_fr() ? "ESPACE" : "SPACE"; }


/* Le bandeau de bataille : les deux adversaires face a face, chacun dans sa
 * moitie d'ecran, sous l'illustration. C'est la ligne qu'on lit entre deux
 * assauts, elle doit tenir en un coup d'oeil. */
/* Comble d'espaces jusqu'a la colonne demandee.
 *
 * C'est la moitie de la recette contre le clignotement : au lieu d'effacer une
 * ligne puis d'y ecrire -- deux passages, donc chaque cellule vue blanche
 * avant d'etre remplie -- on ecrit le texte puis on pousse des espaces jusqu'au
 * bord. Un seul passage, aucune cellule ne passe par le blanc. En 80 colonnes,
 * ou chaque caractere traverse la firmware, la difference se voit a l'oeil :
 * les 4 lignes du bas clignotaient a chaque coup porte. */
static void pad_to(unsigned char col)
{
    unsigned char x = wherex();
    while (x < col) { cputc(' '); x++; }
}

/* Efface une ligne du bandeau sans la faire clignoter. */
static void row_blank(unsigned char row)
{
    gotoxy(0, row);
    pad_to(79);
}

/* Une jauge de dix cases : "[####------]".
 *
 * Les chiffres restent -- le livre compte en points -- mais c'est la barre qui
 * dit d'un coup d'oeil qui est en train de mourir. Arrondi vers le HAUT : tant
 * qu'il reste un point d'ENDURANCE, il reste une case, sinon la creature
 * paraitrait morte un assaut trop tot. */
static char* put_gauge(char* p, unsigned char v, unsigned char v0)
{
    unsigned char i, n;
    n = (v0 == 0 || v == 0)
        ? 0
        : (unsigned char)(((unsigned int)v * 10u + v0 - 1u) / v0);
    if (n > 10) n = 10;
    *p++ = '[';
    for (i = 0; i < 10; i++) *p++ = (i < n) ? '#' : '-';
    *p++ = ']';
    return p;
}

/* Une touche et son verbe : la touche en video inverse, comme la barre de
 * titre. Entre crochets, l'oeil devait chercher ; en inverse il accroche. */
static void put_key(const char* key, const char* label)
{
    revers(1); cprintf(" %s ", key); revers(0);
    cprintf(" %s   ", label);
}

/* Un demi-bandeau de combattant : nom en inverse, HABILETE, jauge, points. */
static void put_fighter(const char* name, unsigned char nmax,
                        unsigned char hab,
                        unsigned char end, unsigned char end0)
{
    char buf[40];
    char* q = buf;
    unsigned char n = 0;

    revers(1);
    while (name[n] && n < nmax) { cputc(name[n]); n++; }
    revers(0);

    q = put_str(q, is_fr() ? " HAB " : " SKL ");
    q = put_u8(q, hab);
    *q++ = ' ';
    q = put_gauge(q, end, end0);
    *q++ = ' ';
    q = put_u8(q, end); *q++ = '/'; q = put_u8(q, end0);
    *q = '\0';
    cprintf("%s", buf);
}

static void prompt_luck(void)
{
    gotoxy(0, CHOICE_ROWN);
    put_key(msg_space(), msg(M_K_ENCAISSER));
    put_key("C", msg(M_K_CHANCE));
    pad_to(79);
}

static void show_fighters(void)
{
    const Monster* m = &app.foes[app.foe_cur];

    gotoxy(0, CHOICE_ROW0);
    /* "VOUS" tient en quatre lettres, l'adversaire pas : la colonne de droite
     * commence a 33 plutot qu'a la moitie de l'ecran, ce qui laisse 19
     * caracteres a "MAITRE DES ARAIGNEES" au lieu de 12. Le demi-bandeau de
     * droite doit finir avant la colonne 79, ou l'ecran scrollerait. */
    put_fighter(msg(M_VOUS), 12, app.hero.hab, app.hero.end, app.hero.end0);
    pad_to(33);
    put_fighter(m->name, 19, m->hab, m->end, m->end0);
    pad_to(79);
}

static void clear_bottom(void)
{
    unsigned char r;
    /* 79 et pas 80 : ecrire la derniere cellule de l'ecran ferait scroller. */
    for (r = CHOICE_ROW0; r <= CHOICE_ROWN; r++) cclearxy(0, r, 79);
}


static void print_at(unsigned char row, const char* text)
{
    /* Le texte PUIS des espaces jusqu'au bord, en un seul passage : une
     * invite courte ecrite par-dessus une longue ne laisse pas depasser sa
     * fin -- "[ESPACE] continuer" suivi du reste de "[C] Tentez votre
     * Chance" -- et la ligne ne clignote pas. 79 et pas 80, la derniere
     * cellule de l'ecran ferait scroller. */
    gotoxy(0, row);
    cprintf("%s", text);
    pad_to(79);
}

static void wait_key_at(unsigned char row, const char* prompt)
{
    print_at(row, prompt);
    cgetc();
}

/* La meme attente, mais avec la touche en video inverse comme le reste du
 * combat : "[ESPACE] continuer" jurait a cote de " ESPACE  encaisser ". */
static void wait_space_at(unsigned char row, const char* label)
{
    gotoxy(0, row);
    put_key(msg_space(), label);
    pad_to(79);
    cgetc();
}

/* Le sac a dos. Affiche par-dessus le texte, refermé par ESC.
 * `in_combat` = un assaut a deja eu lieu : les pierres d'HABILETE, d'ENDURANCE
 * et de CHANCE deviennent alors interdites (regle "Quand peut-on se servir des
 * Pierres de Magie ?"). */
static void show_inventory(int in_combat)
{
    /* N)eutre, B)enefique, M)alefique : la categorie compte (un bon sorcier ne
     * donne pas de pierre malefique), mais elle tient en une lettre. */
    static const char kKind[3] = { 'N', 'B', 'M' };
    Stone shown[STONE_COUNT];
    int n, i, row;
    char key;
    Stone s;

    for (;;) {
        clrscr();
        render_title_bar();
        gotoxy(0, 2);
        cprintf(msg(M_SAC_A_DOS), app.hero.gold);

        n = 0; row = 4;
        for (s = 0; s < STONE_COUNT; s++) {
            if (app.hero.stones[s] == 0) continue;
            gotoxy(0, row++);
            cprintf("%c) %2u  %-12s  %c%s",
                    'A' + n, app.hero.stones[s],
                    stone_name(s, !is_fr()), kKind[stone_kind(s)],
                    stone_usable(s, in_combat)
                        ? "" : (msg(M_INTERDITE_EN_PLEIN)));
            shown[n++] = s;
        }
        if (n == 0) {
            gotoxy(0, 4);
            cprintf(msg(M_AUCUNE_PIERRE_MAGIQUE));
        }

        print_at(22, msg(M_UNE_PIERRE_SE));
        key = cgetc();
        if (key == 27) return;
        i = (key >= 'a') ? (key - 'a') : (key - 'A');
        if (i < 0 || i >= n) continue;

        s = shown[i];
        clear_bottom();
        gotoxy(0, 22);
        switch (stone_use(&app.hero, s, in_combat)) {
        case STONE_USE_FORBIDDEN:
            cprintf(msg(M_LE_PREMIER_COUP));
            break;
        case STONE_USE_NONE:
            cprintf(msg(M_PIERRE_ABSENTE));
            break;
        default:
            cprintf(msg(M_LA_PIERRE_DE), stone_name(s, !is_fr()));
            break;
        }
        wait_key_at(23, msg_continue());
    }
}

/* "A plusieurs reprises au cours de votre aventure [...] vous aurez la
 * possibilite de faire appel a votre chance" -- mais sur ces pages-la le livre
 * ne laisse pas le choix : il ORDONNE le jet et annonce les deux issues. Le
 * moteur le joue donc lui-meme, une fois la page lue. Rend la scene ou aller. */
static int run_luck_test(void)
{
    unsigned char roll;
    int lucky;

    gotoxy(0, CHOICE_ROW0);
    cprintf(msg(M_TENTEZ_VOTRE_CHANCE), app.hero.cha);
    pad_to(79);
    cgetc();

    /* Le jet est releve avant d'etre applique, pour pouvoir le montrer : la
     * regle veut qu'un point de CHANCE parte a chaque tentative, gagnee ou
     * perdue. */
    roll = roll_2d6();
    lucky = (roll <= app.hero.cha);
    gotoxy(0, CHOICE_ROW0);
    cprintf(msg(M_JET_DE_CHANCE), (unsigned)roll, (unsigned)app.hero.cha);
    pad_to(79);
    row_blank(CHOICE_ROW0 + 2);
    if (app.hero.cha > 0) app.hero.cha--;

    print_at(CHOICE_ROW0 + 1, lucky ? msg(M_CHANCEUX) : msg(M_MALCHANCEUX));
    character_adjust_end(&app.hero, lucky ? app.luck_dok : app.luck_dko);
    render_title_bar();
    wait_key_at(CHOICE_ROWN, msg_continue());
    return lucky ? app.luck_ok : app.luck_ko;
}

/* "Lancez un de et retranchez le chiffre obtenu de votre total d'ENDURANCE."
 * Le livre ordonne le jet, il ne le propose pas : le moteur le joue, mais il
 * le MONTRE -- un de qui tombe en coulisse ne se distingue pas d'une perte
 * seche, et le joueur ne saurait pas ce qu'il vient de payer.
 *
 * Meme cadre que run_luck_test, et deux messages seulement : la prose de la
 * page est encore a l'ecran au-dessus, elle dit deja ce que le de coute et
 * sur quoi ; la Feuille d'Aventure de la ligne 1 dit ce qu'il a coute. */
static void run_dice_roll(void)
{
    signed char   n = app.dice_n;
    unsigned char roll;

    print_at(CHOICE_ROW0, msg(M_LANCEZ_LES_DES));
    /* Les choix de la page sont peints en dessous : les effacer, sinon on
     * lirait "lancer les des" au-dessus de lettres qu'on ne peut pas taper. */
    row_blank(CHOICE_ROW0 + 1);
    row_blank(CHOICE_ROW0 + 2);
    cgetc();

    /* Un de, deux au plus : le livre n'en jette jamais davantage sur ces
     * pages, et un compteur en bonne et due forme demandait une valeur
     * absolue de char signe -- 40 octets pour choisir entre un et deux. */
    roll = roll_d6();
    if (n > 1 || n < -1) roll = (unsigned char)(roll + roll_d6());

    gotoxy(0, CHOICE_ROW0);
    cprintf(msg(M_VOUS_JETEZ), (unsigned)roll);
    pad_to(79);
    carac_apply(app.dice_carac, (n < 0) ? -(int)roll : (int)roll);
    render_title_bar();
    wait_key_at(CHOICE_ROWN, msg_continue());
}

/* La valeur courante d'une caracteristique, pour le test CS. L'or n'est pas
 * testable : le livre ne compare jamais 2d6 a une bourse. */
static unsigned char carac_value(unsigned char c)
{
    if (c == 0) return app.hero.end;
    if (c == 1) return app.hero.hab;
    return app.hero.cha;
}

/* Ligne CS : "Lancez deux des. Si le total est inferieur ou egal a vos points
 * d'ENDURANCE..." -- le meme geste que le jet de Chance, mais contre la
 * caracteristique nommee et sans depenser de point de CHANCE. Rend la scene
 * ou aller. */
static int run_stat_test(void)
{
    unsigned char roll, against;

    print_at(CHOICE_ROW0, msg(M_LANCEZ_LES_DES));
    row_blank(CHOICE_ROW0 + 1);
    row_blank(CHOICE_ROW0 + 2);
    cgetc();

    roll = roll_2d6();
    against = carac_value(app.cs_carac);
    gotoxy(0, CHOICE_ROW0);
    cprintf(msg(M_JET_CONTRE), (unsigned)roll, (unsigned)against);
    pad_to(79);
    wait_key_at(CHOICE_ROWN, msg_continue());
    return (roll <= against) ? app.cs_ok : app.cs_ko;
}

/* "Vous choisirez ces six Pierres dans la liste qui figure au debut de ce
 * livre, mais vous ne pourrez les prendre que..." -- un bon sorcier ne donne
 * pas de Pierre malefique, un mauvais pas de Pierre benefique, et l'on a le
 * droit de prendre plusieurs fois la meme ("par exemple 4 Pierres de Feu"). */
static void choose_stones(void)
{
    static const char kKindLetter[3] = { 'N', 'B', 'M' };
    Stone allowed[STONE_COUNT];
    int count, i;
    char key;
    Stone s;

    /* La liste des Pierres permises ne bouge pas d'un choix a l'autre : on la
     * dessine UNE fois. Seul le compteur change, et il tient sur une ligne.
     * Tout repeindre a chaque prise faisait clignoter l'ecran neuf fois de
     * suite pour six Pierres. */
    set_video_mode(0);
    clrscr();
    render_title_bar();

    count = 0;
    for (s = 0; s < STONE_COUNT; s++) {
        const char k = kKindLetter[stone_kind(s)];
        if (strchr(app.choose_cats, k) == NULL) continue;
        gotoxy(0, 4 + count);
        cprintf("%c) %-12s %c", 'A' + count, stone_name(s, !is_fr()), k);
        allowed[count++] = s;
    }
    if (count == 0) { app.choose_n = 0; return; }
    print_at(20, msg(M_PRENDRE_UNE_PIERRE));

    while (app.choose_n > 0) {
        gotoxy(0, 2);
        cprintf(msg(M_CHOISISSEZ_PIERRES), (unsigned)app.choose_n);
        key = cgetc();
        i = (key >= 'a') ? (key - 'a') : (key - 'A');
        if (i >= 0 && i < count) {
            character_give_stone(&app.hero, allowed[i], 1);
            app.choose_n--;
        }
    }
}

/* Un combat. Rend 0 si le heros meurt, 1 si la creature tombe, 2 s'il fuit. */
static int run_combat(void)
{
    unsigned int assaut = 0;
    int use_luck, lucky;
    int pending = 0;            /* une blessure annoncee attend d'etre encaissee */
    unsigned char hurt;
    unsigned char end_in = app.hero.end;   /* pour last_loss (lignes DV) */
    Round r;
    char key;

    /* Le combat s'affiche en mode mixte : l'illustration des adversaires
     * au-dessus, l'echange d'assauts dans les 4 lignes du bas. C'est pour ca
     * que le bandeau porte les caracteristiques des DEUX combattants -- la
     * barre de titre, elle, disparait sous l'image. */
    if (app.has_image) set_video_mode(2);

    for (;;) {
        /* Chaque ligne est reecrite en un passage, aucune n'est effacee
         * d'abord : c'est ce qui faisait clignoter le bandeau a chaque coup. */
        render_title_bar();
        show_fighters();
        if (assaut == 0) {
            row_blank(CHOICE_ROW0 + 1);
            row_blank(CHOICE_ROW0 + 2);
        }

        /* L'invite : une touche par assaut. Avant le premier coup, les Pierres
         * de caracteristique sont encore permises, donc le sac reste ouvrable ;
         * ensuite la meme frappe encaisse la blessure annoncee et enchaine sur
         * l'assaut suivant. Seule la Chance demande une frappe de plus, et
         * c'est voulu : le livre la fait choisir APRES avoir vu qui a touche. */
        gotoxy(0, CHOICE_ROWN);
        put_key(msg_space(),
                msg(assaut == 0 ? M_K_ENGAGER
                    : (!pending ? M_K_SUIVANT
                       : (r.outcome == ROUND_HERO_HITS ? M_K_FRAPPER
                                                       : M_K_ENCAISSER))));
        if (pending) put_key("C", msg(M_K_CHANCE));
        if (assaut == 0) put_key("I", msg(M_K_SAC));
        if (app.flee_target >= 0) put_key("F", msg(M_K_FUIR));
        put_key("ESC", msg(M_K_IMAGE));
        pad_to(79);

        key = cgetc();
        /* ESC fait tourner les modes video sans quitter le combat : le mode
         * mixte met l'illustration de la creature au-dessus des 4 lignes ou
         * s'echangent les assauts. */
        if (key == 27) { cycle_video_mode(); continue; }
        if ((key == 'I' || key == 'i') && assaut == 0) { show_inventory(0); continue; }
        if ((key == 'F' || key == 'f') && app.flee_target >= 0) {
            gotoxy(0, CHOICE_ROW0);
            cprintf(msg(M_VOUS_FUYEZ_ELLE));
            pad_to(79);
            row_blank(CHOICE_ROW0 + 1);
            row_blank(CHOICE_ROW0 + 2);
            prompt_luck();
            key = cgetc();
            use_luck = (key == 'C' || key == 'c');
            lucky = combat_flee(&app.hero, &app.foes[app.foe_cur], use_luck);
            render_title_bar();
            if (use_luck) print_at(CHOICE_ROW0 + 2, lucky ? (msg(M_CHANCEUX))
                                                          : (msg(M_MALCHANCEUX)));
            /* La creature blessee garde son ENDURANCE entamee : on peut
             * revenir dans la clairiere et reprendre le combat. */
            monster_remember((unsigned int)app.current_scene, app.foe_cur, &app.foes[app.foe_cur]);
            wait_space_at(CHOICE_ROWN, msg(M_K_CONTINUER));
            set_video_mode(0);
            return character_is_dead(&app.hero) ? 0 : 2;
        }
        use_luck = (pending && (key == 'C' || key == 'c'));
        if (!use_luck && key != ' ' && key != '\r') continue;

        /* Encaisser la blessure en attente, puis enchainer : c'est ce qui fait
         * tenir un assaut en une seule frappe. */
        if (pending) {
            pending = 0;
            lucky = combat_apply(&app.hero, &app.foes[app.foe_cur], &r, use_luck);
            render_title_bar();
            show_fighters();
            if (use_luck) {
                /* La Chance a change la blessure : le dire, et rendre la main
                 * plutot que d'enchainer -- on vient de payer un point. */
                print_at(CHOICE_ROW0 + 2, lucky ? (msg(M_CHANCEUX2))
                                                : (msg(M_MALCHANCEUX2)));
                wait_space_at(CHOICE_ROWN, msg(M_K_CONTINUER));
            }
            if (monster_is_beaten(&app.foes[app.foe_cur])) {
                sfx_fall();
                gotoxy(0, CHOICE_ROW0 + 2);
                cprintf(msg(M_S_EFFONDRE), app.foes[app.foe_cur].name);
                pad_to(79);
                /* "vous devrez les combattre tous deux a tour de role" : le
                 * suivant se presente, et le heros garde l'ENDURANCE qui lui
                 * reste -- aucun repit entre deux adversaires. */
                app.foe_cur++;
                monster_remember((unsigned int)app.current_scene, app.foe_cur,
                                 &app.foes[app.foe_cur < app.foe_count
                                           ? app.foe_cur : app.foe_count - 1]);
                wait_space_at(CHOICE_ROWN, msg(M_K_CONTINUER));
                if (app.foe_cur >= app.foe_count) {
                    /* "Evaluez vos blessures" : la page d'apres peut brancher
                     * sur ce que le combat a coute (lignes DV). */
                    app.last_loss = (end_in > app.hero.end)
                                  ? (unsigned char)(end_in - app.hero.end) : 0;
                    set_video_mode(0);
                    return 1;
                }
                assaut = 0;      /* le sac redevient ouvrable avant l'assaut */
                continue;
            }
            if (character_is_dead(&app.hero)) {
                sfx_death();
                monster_remember((unsigned int)app.current_scene, app.foe_cur, &app.foes[app.foe_cur]);
                set_video_mode(0);
                return 0;
            }
            /* Duel au premier sang : la blessure vient d'etre encaissee, le
             * combat s'arrete la et la suite dit QUI a touche. Le detour par
             * win_scene reutilise la sortie de MV telle quelle. */
            if (app.mb_ok >= 0) {
                app.win_scene = (r.outcome == ROUND_HERO_HITS) ? app.mb_ok
                                                               : app.mb_ko;
                wait_space_at(CHOICE_ROWN, msg(M_K_CONTINUER));
                set_video_mode(0);
                return 1;
            }
        }

        /* L'assaut suivant, jete et annonce dans la foulee. */
        assaut++;
        combat_round(&app.hero, &app.foes[app.foe_cur], &r);
        gotoxy(0, CHOICE_ROW0 + 1);
        cprintf(msg(M_ASSAUT_FORCE_D), assaut, r.hero_force,
                r.hero_force > r.monster_force ? ">"
                : (r.hero_force < r.monster_force ? "<" : "="),
                r.monster_force);
        if (app.foe_count > 1) cprintf("   %u/%u",
                                       (unsigned)(app.foe_cur + 1),
                                       (unsigned)app.foe_count);
        pad_to(79);

        /* Le bruitage suit QUI a touche : lame seche contre coup sourd. Il
         * part avant le texte, pour tomber en meme temps que l'annonce. */
        if (r.outcome == ROUND_DODGE) {
            sfx_dodge();
            print_at(CHOICE_ROW0 + 2, msg(M_VOUS_AVEZ_CHACUN));
            continue;   /* personne n'est blesse : rien a encaisser */
        }
        if (r.outcome == ROUND_HERO_HITS) sfx_hit(); else sfx_hurt();
        /* "chaque blessure coute 2 points d'ENDURANCE" -- sauf aux creatures
         * dont la page dit autrement (ligne MD). On annonce la perte seche ;
         * la Chance peut encore la changer, et la jauge dira le vrai. */
        hurt = (r.outcome == ROUND_HERO_HITS) ? 2 : app.foes[app.foe_cur].damage;
        gotoxy(0, CHOICE_ROW0 + 2);
        cprintf("%s", r.outcome == ROUND_HERO_HITS ? (msg(M_VOUS_L_AVEZ))
                                                   : (msg(M_ELLE_VOUS_A)));
        cprintf(msg(M_DEGATS), (unsigned)hurt);
        pad_to(79);
        pending = 1;
    }
}

/* ── L'aide ──────────────────────────────────────────────────────────────
 *
 * Le texte vit sur le disque, dans /SCOSWAMP/HELPFR et /SCOSWAMP/HELPEN, pas
 * dans le binaire : c'est du contenu, il se traduit et se corrige sans
 * recompiler -- et il tenait mal dans les 22 Ko de la fenetre programme.
 */
static void show_help(void)
{
    FILE* f;
    char line[81];
    unsigned char row = 2;
    int n;

    set_video_mode(0);
    clrscr();
    render_title_bar();

    if (chdir("/SCOSWAMP") != 0 ||
        (f = fopen(msg(M_HELPFR), "r")) == NULL) {
        print_at(4, msg(M_FICHIER_D_AIDE));
    } else {
        while (row < CHOICE_ROW0 && fgets(line, sizeof(line), f) != NULL) {
            n = (int)strlen(line);
            while (n > 0 && (line[n - 1] == '\n' || line[n - 1] == '\r')) line[--n] = '\0';
            if (n > 0) cputsxy(0, row, line);
            row++;
        }
        fclose(f);
    }
    wait_key_at(CHOICE_ROWN, msg_continue());
    render_scene();
}

/* Fin de partie : "jusqu'a ce que vos points d'ENDURANCE [...] aient ete
 * reduits a zero (mort)". */
/* "jusqu'a ce que vos points d'ENDURANCE [...] aient ete reduits a zero
 * (mort)". Le joueur repart de zero ou rend la main a ProDOS -- avec ProDOS
 * 2.4 c'est Bitsy Bye qui reprend, et l'on peut lancer autre chose sans
 * redemarrer la machine. Le stub de sortie cc65 fait le QUIT du MLI ; c'est
 * la seule sortie possible depuis que le jeu occupe la place de
 * BASIC.SYSTEM. */
static void game_over(void)
{
    char key;

    set_video_mode(0);
    clrscr();
    gotoxy(0, 6);
    cprintf(msg(M_VOTRE_ENDURANCE_EST));
    print_at(8, msg(M_MORT_RECOMMENCER));
    for (;;) {
        key = cgetc();
        if (key == 'R' || key == 'r') return;
        if (key == 'Q' || key == 'q') {
            videomode(VIDEOMODE_40COL);
            clrscr();
            exit(0);
        }
    }
}

/* La creation du personnage, telle que le livre l'ouvre. */
static void roll_character(void)
{
    character_roll(&app.hero);
    app.hero_ready = 1;
    scene_title = NULL;   /* sinon la barre garde le titre de la scene fatale */

    set_video_mode(0);
    videomode(VIDEOMODE_80COL);
    clrscr();
    render_title_bar();
    gotoxy(0, 3);
    cprintf(msg(M_FEUILLE_D_AVENTURE));
    gotoxy(0, 5);
    cprintf(msg(M_HABILETE_DE),   app.hero.hab);
    gotoxy(0, 6);
    cprintf(msg(M_ENDURANCE_DES), app.hero.end);
    gotoxy(0, 7);
    cprintf(msg(M_CHANCE_DE),   app.hero.cha);
    gotoxy(0, 9);
    cprintf(msg(M_UNE_EPEE_UNE), app.hero.gold);
    gotoxy(0, 10);
    cprintf(msg(M_AUCUN_DE_CES));
    wait_key_at(13, msg(M_ESPACE_ENTRER_DANS));
}

/* La mort et ce qui la suit, en un seul endroit. Le combat n'en a plus le
 * monopole : "si vous survivez" (pages 252, 261, 274) dit que le de de la
 * ligne ED peut tuer lui aussi, et dupliquer les cinq lignes couterait plus
 * cher que la fonction. */
static void die_and_restart(void)
{
    game_over();
    monster_memory_reset();
    scene_memory_reset();
    roll_character();
    app.pending_scene = 0;
}

/* Charger une nouvelle scene - version optimisée */
void load_scene(int scene_id) {
    int issue;

    app.current_scene = scene_id;
    app.num_choices = 0;  /* Réinitialiser les choix */
    app.has_image = 0;
    app.foe_count = 0;
    app.foe_cur = 0;
    app.flee_target = -1;
    app.revisit = -1;
    app.choose_n = 0;
    app.luck_ok = -1;
    app.luck_dok = 0;
    app.luck_dko = 0;
    /* Les deux premiers sont obligatoires : sans remise a zero ils fuiraient
     * d'une clairiere a la suivante -- une victoire d'hier renverrait ailleurs
     * la page d'aujourd'hui. Le troisieme est du zele, dice_carac n'etant lu
     * que si dice_n vaut autre chose que zero. */
    app.win_scene  = -1;
    app.dice_n     = 0;
    app.dice_carac = 0;
    app.cs_ok = -1; app.cs_ko = -1;
    app.mb_ok = -1; app.mb_ko = -1;
    /* last_loss ne se remet PAS a zero ici : c'est la page SUIVANT le combat
     * qui la lit (lignes DV). dv_done, si : la cascade repart a chaque page. */
    app.dv_done = 0;

    /* Charger d'abord le texte et les choix. Le chargeur HGR assembleur est
     * ensuite le dernier client ProDOS de la scène : son décodage direct en
     * mémoire vidéo ne peut donc perturber une ouverture de texte ultérieure.
     * C'est aussi la lecture du fichier qui applique les lignes E (effet) et
     * P (Pierres reçues) : elles jouent une fois par visite. */
    app.video_mode = 0;
    display_scene_text(scene_id);

    /* Deja venu : la page longue cede la place a sa version courte, sans rien
     * afficher entre les deux. Le passage n'est PAS marque -- c'est la page
     * courte qui l'est, et de toute facon celle-ci l'etait deja. */
    if (app.revisit >= 0) {
        app.pending_scene = app.revisit;
        return;
    }
    scene_mark_visited((unsigned int)scene_id);

    /* L'image est decodee en page HGR 1 mais PAS montree : on reste sur le
     * texte, c'est au joueur de basculer. Le decodage se fait donc sous un
     * ecran texte deja lisible, et non derriere une image qui s'affiche
     * toute seule. */
    /* Le de de la ligne ED tombe avant tout le reste : avant le jet de
     * Chance, avant le choix des Pierres, avant l'image, avant le combat.
     * C'est ce qui garantit l'ordre du 261 -- le de precede le combat de la
     * meme page quelle que soit la position de la ligne dans le fichier. */
    if (app.dice_n != 0) {
        run_dice_roll();
        /* "si vous survivez" : un ENDURANCE tombe a zero apres le jet part sur
         * game_over, exactement comme une mort au combat. */
        if (character_is_dead(&app.hero)) { die_and_restart(); return; }
        /* Le jet a ecrase les 4 lignes du bas : les repeindre. run_luck_test
         * n'en a jamais besoin, il rend toujours une scene ; ED laisse la
         * page en place et lui rend la main. */
        render_scene();
    }

    /* La page teste une caracteristique : 2d6 contre elle, et la suite
     * depend du jet -- rien a choisir. */
    if (app.cs_ok >= 0) {
        app.pending_scene = run_stat_test();
        return;
    }

    /* La page ordonne un jet de Chance : il decide de la suite, il n'y a donc
     * pas de choix a offrir au joueur. */
    if (app.luck_ok >= 0) {
        app.pending_scene = run_luck_test();
        return;
    }

    /* Le sorcier tend ses Pierres avant tout le reste : le joueur vient de
     * lire la page qui les lui offre. */
    if (app.choose_n > 0) {
        choose_stones();
        render_scene();
    }

    /* Une clairiere avec un adversaire prend son image de bataille si elle
     * existe, sinon son illustration ordinaire. */
    app.has_image = 0;
    if (app.foe_count > 0) app.has_image = load_hgr_image_as(scene_id, 'B');
    if (!app.has_image)  app.has_image = load_hgr_image_as(scene_id, 'N');

    if (app.foe_count == 0) return;

    for (issue = 0; issue < app.foe_count; issue++) monster_seal(&app.foes[issue]);

    /* "il est possible que vous reveniez plus tard dans cette clairiere et que
     * ce ou ces monstres s'y trouvent encore" : monster_enter rend l'ENDURANCE
     * laissee au dernier passage, et 0 si la creature est deja morte. */
    app.foe_cur = monster_enter((unsigned int)scene_id, app.foes, app.foe_count);
    /* La file peut avoir ete videe lors d'une visite precedente : c'est une
     * victoire acquise, pas un combat a rejouer. Elle sort donc par la meme
     * porte, et non plus par un `return` sec -- sans quoi une page passee a
     * MV, qui n'a plus AUCUNE ligne C, laisserait le joueur devant un ecran
     * sans issue. 3 = "gagne avant d'arriver" ; run_combat ne rend que 0
     * (mort), 1 (victoire) ou 2 (fuite). */
    issue = (app.foe_cur < app.foe_count) ? run_combat() : 3;

    if (issue == 0) {
        die_and_restart();
    } else if (issue == 2) {
        app.pending_scene = app.flee_target;
    } else if (app.win_scene >= 0) {
        /* La page dit ou mene la victoire : y aller, au lieu de repeindre une
         * page dont le seul choix etait "vous avez tue le Maitre". run_combat
         * a deja annonce l'effondrement et attendu ESPACE. */
        app.pending_scene = app.win_scene;
    } else if (issue == 1) {
        /* La creature vient de tomber : le combat a mange les 4 lignes du bas,
         * il faut y remettre les choix. Une file deja abattue (3) n'a rien
         * peint par-dessus : la page est restee telle que display_scene_text
         * l'a rendue. */
        render_scene();
    }
}

/* Fonction pour afficher l'écran de sélection de langue */
void display_language_selection(void) {
    videomode(VIDEOMODE_80COL);
    clrscr();
    
    cprintf("\r\n");
    cprintf("          ====================================================\r\n");
    cprintf("                     SCORPIONS SWAMP\r\n");
    cprintf("                          LE MARAIS AUX SCORPIONS\r\n");
    cprintf("          ====================================================\r\n");
    cprintf("\r\n");
    cprintf("           Un livre dont vous etes le heros\r\n");
    cprintf("                               A Fighting Fantasy Gamebook\r\n");
    cprintf("\r\n");
    cprintf("               (1985) by Steve JACKSON & Ian LIVINGSTONE \r\n");
    cprintf("\r\n");
    cprintf("                    SELECT YOUR LANGUAGE / LANGUE\r\n");
    cprintf("\r\n");
    cprintf("                         [F] - Francais\r\n");
    cprintf("\r\n");
    cprintf("                         [E] - English\r\n");
    cprintf("\r\n");
    cprintf("\r\n");
    cprintf("               2025 Apple II Port by : Arnaud VERHILLE\r\n");
    cprintf("                                  (gist974@gmail.com)\r\n");
    cprintf("\r\n\r\n");
    cprintf("          ====================================================\r\n");
}

/* Fonction pour sélectionner la langue */
void select_language(void) {
    char key;
    
    display_language_selection();
    
    /* Attendre le choix de langue. C'est le premier appui de touche de la
     * partie : on en profite pour semer les des avec le temps d'attente --
     * l'Apple II n'a pas d'autre source de hasard au demarrage. */
    while (1) {
        key = dice_seed_from_keypress();
        if (key == 'F' || key == 'f') {
            strcpy(app.language, "FR");
            break;
        } else if (key == 'E' || key == 'e') {
            strcpy(app.language, "EN");
            break;
        }
    }
}

/* DEBUG: Afficher l'état actuel (peut être appelé avec touche spéciale) */
void show_debug_info(void) {
    int i;
    set_video_mode(0);
    videomode(VIDEOMODE_80COL);
    cprintf("\r\n=== DEBUG INFO ===\r\n");
    cprintf("Scene: %d\r\n", app.current_scene);
    cprintf("Video mode: %d\r\n", app.video_mode);
    cprintf("Num choices: %d\r\n", app.num_choices);
    cprintf("Has image: %d\r\n", app.has_image);
    if (app.num_choices > 0) {
        cprintf("\r\nChoix disponibles:\r\n");
        for (i = 0; i < app.num_choices; i++) {
            cprintf("%c) ID=%d %s\r\n", 'A'+i, app.choices[i].scene_id, app.choices[i].title);
        }
    }
    cprintf("\r\nAppuyez sur une touche...\r\n");
    cgetc();
    /* Retourner au mode vidéo précédent */
    display_scene_text(app.current_scene);
}

/* Fonction pour gérer les choix de l'utilisateur */
void handle_user_input(char key) {
    int choice_num;
    
    if (key == ' ' || key == '\r' || key == 27) {
        /* Barre d'espace, RETURN ou ESC : cycler les modes */
        cycle_video_mode();
        
    } else if (key == 'I' || key == 'i') {
        /* Hors combat, toutes les Pierres sont utilisables. */
        show_inventory(0);
        render_scene();

    } else if (key == 'H' || key == 'h') {
        show_help();

    } else if (key == 'Q' || key == 'q') {
        /* Quitter */
        set_video_mode(0);
        videomode(VIDEOMODE_40COL);
        clrscr();
        if (strcmp(app.language, "FR") == 0) {
            cprintf("Au revoir!\r\n");
        } else {
            cprintf("Goodbye!\r\n");
        }
        exit(0);
        
    } else if ((key >= 'A' && key <= 'Z') || (key >= 'a' && key <= 'z')) {
        /* Choix par lettre */
        choice_num = (key >= 'a') ? (key - 'a') : (key - 'A');
        if (choice_num < app.num_choices) {
            if (!choice_available(choice_num)) {
                /* On ne lance pas un sort qu'on n'a pas. */
                clear_bottom();
                print_at(CHOICE_ROW0, msg(M_PIERRE_ABSENTE));
                wait_key_at(CHOICE_ROWN, msg_continue());
                render_scene();
                return;
            }
            /* La Pierre exigee se desintegre en servant. */
            if (app.choices[choice_num].require < STONE_COUNT) {
                stone_use(&app.hero, (Stone)app.choices[choice_num].require, 0);
            }
            /* Une Pierre offerte par le choix change de main avant le saut. */
            if (app.choices[choice_num].grant < STONE_COUNT) {
                character_give_stone(&app.hero,
                                     (Stone)app.choices[choice_num].grant, 1);
            }
            load_scene(app.choices[choice_num].scene_id);
        }
    }
}

void main(void) {
    char key;
    unsigned char prefix_error;
    
    /* Initialiser l'état de l'application */
    app.current_scene = 0;
    app.video_mode = 0;  /* Démarrer en mode texte 80 colonnes */
    app.num_choices = 0;
    app.has_image = 0;
    app.foe_count = 0;
    app.foe_cur = 0;
    app.hero_ready = 0;
    app.flee_target = -1;
    app.revisit = -1;
    app.pending_scene = -1;
    monster_memory_reset();
    scene_memory_reset();
    strcpy(app.language, "FR");  /* Valeur par défaut */

    /* BASIC.SYSTEM ne garantit pas le préfixe cc65. Le fixer explicitement
     * valide aussi le nom de volume ProDOS avant toute ouverture de fichier. */
    if (chdir("/SCOSWAMP") != 0) {
        prefix_error = (unsigned char)_oserror;
        clrscr();
        cprintf("Source: chdir(/SCOSWAMP)\r\n");
        cprintf("Echec prefixe volume: errno=%d ProDOS=$%02X\r\n",
                errno, prefix_error);
        cprintf("Cause: entree volume/repertoire HDV invalide\r\n");
        cprintf("Appuyez sur une touche...\r\n");
        cgetc();
        return;
    }
    
    /* Note: Le prefix ProDOS est défini par l'environnement de lancement
     * (typiquement via BASIC.SYSTEM ou le répertoire du fichier .SYSTEM)
     * Les chemins relatifs dans ce programme sont résolus à partir de ce prefix
     * Voir PRODOS-MLI.md pour plus de détails sur chdir() et getcwd()
     */
    
    /* Sélection de langue */
    select_language();

    /* Le catalogue de l'interface suit la langue choisie. */
    messages_load(app.language[0] != 'F');

    /* "Avant de vous lancer dans cette aventure, il vous faut d'abord
     * determiner vos propres forces et faiblesses." */
    roll_character();
    
    /* Scene initiale (scene 0 = titre) : texte affiche, image prete en
     * coulisse, l'ecran de titre s'obtient d'un appui sur ESPACE. */
    load_scene(0);
    
    /* Boucle principale. La scène en attente évite que load_scene s'appelle
     * lui-même sur une Fuite ou une mort : la pile cc65 fait 2 Ko et une
     * poursuite de clairière en clairière la mangerait. */
    while (1) {
        if (app.pending_scene >= 0) {
            int next = app.pending_scene;
            app.pending_scene = -1;
            load_scene(next);
            continue;
        }
        key = cgetc();
        handle_user_input(key);
    }
}
