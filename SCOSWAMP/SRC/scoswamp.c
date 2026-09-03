#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include <conio.h>
#include <stdarg.h>
#include <apple2enh.h>
#include <peekpoke.h>
#include "paths.h"
#include "memory_swap.h"
#include "hgr_rle.h"
#include "rules.h"
#include "dice.h"
#include "messages.h"
#include "sfx.h"
#include "music.h"

/* Bornes du segment LOWBSS, exportees par le lieur (define = yes) sous les
 * noms __LOWBSS_RUN__ et __LOWBSS_SIZE__. cc65 prefixe tout identifiant C
 * d'un '_', d'ou un souligne de moins ici. Leur "adresse" est la valeur :
 * c'est l'idiome cc65 pour les symboles de segment. */
extern char _LOWBSS_RUN__[];
extern char _LOWBSS_SIZE__[];

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
#define MAX_PATH  10

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
    unsigned char object; /* OBJ_COUNT si aucune condition d'objet */
    unsigned char obj_mode; /* 1=possede, 2=ne possede pas, 3=consomme */
    char* title;          /* pointe dans file_buffer, valide jusqu'a la scene suivante */
} Choice;

/* Structure pour l'état global de l'application */
typedef struct {
    int current_scene;
    unsigned char video_mode;  /* 0=texte 80col, 1=HGR plein, 2=mixte */
    Choice choices[MAX_CHOICES];
    unsigned char num_choices;
    char language[3];  /* FR ou EN */
    char imgPath[MAX_PATH];
    char txtPath[MAX_PATH];
    unsigned char has_image; /* image de la scene decodee en page HGR 1 ? */

    /* La Feuille d'Aventure et la rencontre en cours. */
    Character hero;
    unsigned char hero_ready; /* les des ont ete jetes */
    /* "Parfois, vous les affronterez comme si elles n'etaient qu'un seul
     * monstre ; parfois, vous les combattrez une par une." Les deux rencontres
     * a plusieurs du Marais sont du second type : une file, affrontee dans
     * l'ordre ou la page la donne. */
    Monster   foes[MAX_FOES];
    unsigned char foe_count; /* nombre de lignes M sur la page */
    unsigned char foe_cur;   /* adversaire en cours dans la file */
    int       flee_target;   /* scene ou mene la Fuite, -1 si la page n'en offre pas */
    int       pending_scene; /* scene a charger au prochain tour de boucle, -1 sinon */
    int       revisit;       /* ligne V : ou aller si la clairiere est deja vue, -1 sinon */
    unsigned char choose_n;  /* Pierres a choisir en entrant, 0 si aucune */
    char      choose_cats[3];/* categories permises : N, B, M */
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
 * remesure le 2026-09-03. fread en lit SIZE-1 et reserve le dernier octet au
 * '\0'. reflow_txt.py tient exactement la meme limite. */
#define FILE_BUFFER_SIZE 1253
/* En LOWBSS ($1000-$1FFF, voir scoswamp.cfg) : la RAM basse entre le tampon
 * ProDOS et HGR page 1, que le lieur ignorait. main() la met a zero. */
#pragma bss-name (push, "LOWBSS")
char file_buffer[FILE_BUFFER_SIZE];
#pragma bss-name (pop)

/* Sauvegarde binaire SCS2 : format explicite, independant du remplissage des
 * structures C. Dix emplacements numerotes de 0 a 9 sur le disque. */
#define SAVE_HEADER 8
/* Le titre de la page ou la partie s'est arretee, tel que la ligne T le
 * donne, sur 32 octets termines par zero : la page des sauvegardes l'affiche
 * pour que le joueur se situe dans le Marais avant de reprendre. */
#define SAVE_TITLE  32
#define SAVE_SIZE (SAVE_HEADER + SAVE_TITLE + sizeof(Character) + SCENE_MEMORY_SIZE + MONSTER_MEMORY_SIZE)
#define save_data ((unsigned char*)file_buffer)
static unsigned char restoring;
static char* scene_title;   /* la ligne T de la page, dans file_buffer */
static void render_scene(void);
void load_scene(int scene_id);
static unsigned char show_saves(unsigned char saving);

#pragma code-name (push, "LC")
#pragma rodata-name (push, "LC")
#pragma code-name (push, "CODE")
static unsigned char* save_u16(unsigned char* p, unsigned int v)
{ *p++ = (unsigned char)v; *p++ = (unsigned char)(v >> 8); return p; }
#pragma code-name (pop)
#pragma code-name (push, "CODE")
static unsigned int load_u16(const unsigned char* p)
{ return (unsigned int)p[0] | ((unsigned int)p[1] << 8); }
#pragma code-name (pop)

#pragma code-name (push, "CODE")
static unsigned char save_checksum(void)
{
    unsigned int i; unsigned char sum=0;
    for(i=5;i<SAVE_SIZE;i++) sum^=save_data[i];
    return sum;
}
#pragma code-name (pop)

/* pack_save repasse en CODE : avec le titre, la Language Card debordait
 * d'un octet, et la fenetre principale a 7 Ko de marge. */
#pragma code-name (push, "CODE")
static void pack_save(void)
{
    unsigned char* p = save_data + SAVE_HEADER;
    unsigned char n = scene_title ? (unsigned char)strlen(scene_title) : 0;
    if (n > SAVE_TITLE - 1) n = SAVE_TITLE - 1;
    /* Le titre vit dans file_buffer, que save_data recouvre : il part en
     * premier, et par memmove, car sa source peut chevaucher sa place. */
    if (n) memmove(p, scene_title, n);
    memset(p + n, 0, SAVE_TITLE - n);
    p += SAVE_TITLE;
    memcpy(save_data, "SCS3", 4);
    save_u16(save_data + 5, (unsigned int)app.current_scene);
    save_data[7] = app.language[0];
    memcpy(p,&app.hero,sizeof app.hero); p+=sizeof app.hero;
    scene_memory_export(p); p += SCENE_MEMORY_SIZE; monster_memory_export(p);
    save_data[4]=save_checksum();
}

#pragma code-name (pop)
static int unpack_save(void)
{
    const unsigned char* p; int scene;
    if (memcmp(save_data,"SCS3",4)!=0 || save_data[4]!=save_checksum()) return 0;
    p=save_data+5; scene=(int)load_u16(p); p+=2;
    app.language[0]=*p++; app.language[1]=(app.language[0]=='F')?'R':'N'; app.language[2]='\0';
    p += SAVE_TITLE;
    memcpy(&app.hero,p,sizeof app.hero); p+=sizeof app.hero;
    scene_memory_import(p); p+=SCENE_MEMORY_SIZE; monster_memory_import(p);
    app.hero_ready=1;
    restoring=1;
    app.pending_scene=scene;
    return 1;
}
#pragma rodata-name (pop)
#pragma code-name (pop)

/* Les appels ProDOS doivent vivre en memoire principale : ProDOS utilise la
 * Language Card et peut remplacer le code LC pendant un open/read/write. */
static int enter_save(unsigned char slot)
{
    memcpy(app.imgPath,"PARTIE0",8); app.imgPath[6]=(char)('0'+slot);
    return chdir("/SCOSWAMP")==0 && chdir("SAVE")==0;
}

static int save_game(unsigned char slot)
{
    int fd, ok; pack_save();
    if(!enter_save(slot)) return 0;
    fd=open(app.imgPath,O_WRONLY|O_TRUNC); if(fd<0) return 0;
    ok=(write(fd,save_data,SAVE_SIZE)==SAVE_SIZE); close(fd); return ok;
}

static int load_game(unsigned char slot)
{
    FILE* f; int ok;
    if(!enter_save(slot)) return 0;
    f=fopen(app.imgPath,"r"); if(!f) return 0;
    /* Une troncature est refusee ici ; toute alteration des octets lus est
     * ensuite detectee par la signature et le checksum de unpack_save. */
    ok=(fread(save_data,1,SAVE_SIZE,f)==SAVE_SIZE); fclose(f);
    return ok && unpack_save();
}

/* Le titre range dans un emplacement, ou une chaine vide si l'emplacement
 * est vierge (les PARTIEn du disque font deux octets) ou d'un autre format.
 * Ne lit que l'en-tete : dix emplacements a lister, pas dix parties. */
static void slot_title(unsigned char slot, char* out)
{
    FILE* f;
    unsigned char hdr[SAVE_HEADER + SAVE_TITLE];
    out[0] = '\0';
    if (!enter_save(slot)) return;
    f = fopen(app.imgPath, "r"); if (!f) return;
    if (fread(hdr, 1, sizeof hdr, f) == sizeof hdr && memcmp(hdr, "SCS3", 4) == 0) {
        memcpy(out, hdr + SAVE_HEADER, SAVE_TITLE);
        out[SAVE_TITLE - 1] = '\0';
    }
    fclose(f);
}

/* Decoupage de la scene courante. Titre et lignes de corps ne sont pas
 * recopies : ce sont des pointeurs DANS file_buffer, dont les fins de ligne
 * ont ete remplacees par des '\0'. Le buffer n'est reecrit qu'au chargement
 * de la scene suivante, donc ils restent valides tant qu'on affiche celle-ci
 * -- et ca evite un seul octet de copie. */
static char* body_lines[BODY_ROWS];
static unsigned char body_count;

static int enter_asset_dir(const char* kind, int scene_id)
{
    char bucket[5];
    unsigned int subdirectory = ((unsigned int)scene_id / 50u) * 50u;

    if (chdir("/SCOSWAMP") != 0) return 0;
    if (chdir(kind) != 0) return 0;
    *put_scene(bucket, subdirectory) = '\0';
    if (chdir(bucket) != 0) return 0;
    return 1;
}

static void report_open_error(const char* path)
{
    (void)path;
    cputs("Erreur\r");
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

/* Le formateur maison, a la place de la famille printf.
 *
 * Il connait %u, %s et %c, une largeur (%2u, %-12s) et une precision (%.75s)
 * -- tout ce que le code et le catalogue MSGFR/MSGEN emploient. Toute autre
 * lettre de conversion est lue comme %u. Rien de plus : _printf, vsnprintf,
 * vcprintf et ltoa coutaient 1,5 Ko de code pour ces trois conversions, et
 * sprintf les embarquait meme sans affichage formate.
 *
 * Les valeurs passent en `unsigned int` : cc65 promeut les caracteres et
 * octets a l'appel (pusha0), comme pour printf. Tout est en unsigned char
 * ici, et les locales sont statiques (-Cl) : chaque `int` ou variable de
 * pile coute une poignee d'octets par acces sur 6502. */
/* La sortie de cfmt : l'ecran, ou un tampon quand fmt_out est pose. La barre
 * de titre se compose ainsi en memoire pour etre peinte d'un bloc. */
static char* fmt_out;
static void emit(char c) { if (fmt_out) { *fmt_out = c; ++fmt_out; } else cputc(c); }
static void pad_spaces(unsigned char n) { while (n) { emit(' '); --n; } }

static void cfmt(const char* f, ...)
{
    va_list ap;
    char buf[6];
    /* Trois pointeurs en page zero (la banque de registres de cc65 en tient
     * exactement trois). `f` reste en pile : va_start prend son adresse. */
    register const char* p = f;
    register const char* s;
    register char* q;
    unsigned char c, left, width, prec, n;
    va_start(ap, f);
    for (;;) {
        c = (unsigned char)*p++;
        if (c == 0) break;
        if (c != '%') { emit((char)c); continue; }
        left = 0; width = 0; prec = 255;
        c = (unsigned char)*p++;
        if (c == '-') { left = 1; c = (unsigned char)*p++; }
        while (c >= '0' && c <= '9') { width = width * 10 + (c - '0'); c = (unsigned char)*p++; }
        if (c == '.') {
            prec = 0;
            while ((c = (unsigned char)*p++) >= '0' && c <= '9') prec = prec * 10 + (c - '0');
        }
        if (c == 'c') {
            buf[0] = (char)va_arg(ap, int); buf[1] = '\0'; s = buf;
        } else if (c == 's') {
            s = va_arg(ap, const char*);
        } else {
            unsigned int v = va_arg(ap, unsigned int);
            q = buf + sizeof(buf) - 1;
            *q = '\0';
            do { *--q = (char)('0' + v % 10u); v /= 10u; } while (v);
            s = q;
        }
        n = (unsigned char)strlen(s);
        if (n > prec) n = prec;
        width = (width > n) ? (unsigned char)(width - n) : 0;
        if (!left) { pad_spaces(width); width = 0; }
        while (n) { emit(*s++); --n; }
        pad_spaces(width);
    }
    va_end(ap);
}

/* Les deux lignes que toute erreur de disque affiche, une seule fois en
 * RODATA. errno est celui de cc65, l'autre le code ProDOS brut. */
static void wait_any(void)
{
    cputs("Appuyez sur une touche...\r\n");
    cgetc();
}

static void prodos_error(const char* source)
{
    cputs("Source: "); cputs(source);
    cfmt("\r\nerrno=%u ProDOS=%u\r\n", (unsigned)errno, (unsigned)_oserror);
}

static void render_title_bar(void)
{
    char sheet[40];
    unsigned char n;

    /* Une fois les des jetes, la barre porte la Feuille d'Aventure : les trois
     * caracteristiques sont ce qu'on consulte a chaque page, et le livre les
     * veut sous les yeux en permanence. Avant la creation du personnage, elle
     * sert encore au rappel des touches. */
    memset(title_bar, ' ', 80);
    title_bar[80] = '\0';

    if (scene_title != NULL) {
        n = (unsigned char)strlen(scene_title);
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
        /* Les etiquettes suivent la langue : en anglais ce sont SKILL,
         * STAMINA et LUCK, les trois mots de Fighting Fantasy. Le test en
         * clair plutot que is_fr() : cette fonction est definie plus bas.
         * cfmt ecrit dans `sheet` (fmt_out), et le bloc est cale a droite. */
        fmt_out = sheet;
        cfmt((app.language[0] == 'F') ? "HAB %u/%u  END %u/%u  CHA %u/%u"
                                      : "SKL %u/%u  STA %u/%u  LCK %u/%u",
             app.hero.hab, app.hero.hab0, app.hero.end, app.hero.end0,
             app.hero.cha, app.hero.cha0);
        n = (unsigned char)(fmt_out - sheet);
        fmt_out = NULL;
        memcpy(title_bar + 79 - n, sheet, n);
    } else {
        /* Avant la creation du personnage : le rappel des touches. Il vit au
         * catalogue -- la barre ne se peint jamais avant messages_load. */
        const char* hint = msg(M_TOUCHES);
        n = (unsigned char)strlen(hint);
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
static unsigned char choice_available(unsigned char i)
{
    Choice* c = &app.choices[i];
    unsigned char has;
    if (c->require < STONE_COUNT && !character_has_stone(&app.hero, (Stone)c->require)) return 0;
    if (c->object < OBJ_COUNT) {
        has = (unsigned char)character_has_object(&app.hero, (Object)c->object);
        return c->obj_mode == 2 ? !has : has;
    }
    if (c->object & 0x80) {
        has = (unsigned char)character_has_amulet(&app.hero, (Amulet)(c->object & 0x7f));
        return c->obj_mode == 2 ? !has : has;
    }
    if (c->object == 0x7f) {
        unsigned char n=character_amulet_count(&app.hero);
        return n >= (c->obj_mode >> 4) && n <= (c->obj_mode & 15);
    }
    return 1;
}

static char choice_tag(int i)
{
    return choice_available(i) ? (char)('A' + i) : '-';
}

/* Deux choix courts tiennent sur une ligne, en deux colonnes. */
static unsigned char pair_fits(unsigned char i)
{
    return i + 1 < app.num_choices &&
           strlen(app.choices[i].title)     <= CHOICE_WIDTH - 3 &&
           strlen(app.choices[i + 1].title) <= CHOICE_WIDTH - 3;
}

static void render_choices(void)
{
    unsigned char i, rows = 0, row;

    /* Les choix se calent en BAS des quatre lignes : la derniere ligne de
     * choix est toujours la ligne 24, et le vide reste au-dessus, contre le
     * texte. On compte d'abord les lignes, avec la meme regle de pairage. */
    for (i = 0; i < app.num_choices; i += pair_fits(i) ? 2 : 1) rows++;
    if (rows > CHOICE_ROWN - CHOICE_ROW0 + 1) rows = CHOICE_ROWN - CHOICE_ROW0 + 1;
    row = (unsigned char)(CHOICE_ROWN + 1 - rows);

    i = 0;
    while (i < app.num_choices && row <= CHOICE_ROWN) {
        gotoxy(0, row);
        if (pair_fits(i)) {
            cfmt("%c) %s", choice_tag(i), app.choices[i].title);
            gotoxy(CHOICE_COL2, row);
            cfmt("%c) %s", choice_tag(i + 1), app.choices[i + 1].title);
            i += 2;
        } else {
            cfmt("%c) %.75s", choice_tag(i), app.choices[i].title);
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
#pragma code-name (push, "LC")
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
#pragma code-name (push, "CODE")
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
    case 'B': return 4;
    case 'E': return 0;
    case 'H': return 1;
    case 'C': return 2;
    case 'O': return 3;
    }
    return 4;
}
#pragma code-name (pop)
#pragma code-name (pop)

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
    case 4:
        app.hero.weapon_bonus += (unsigned char)d;
        if (app.hero.weapon_bonus > 2) app.hero.weapon_bonus=2;
        break;
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
    c->object   = OBJ_COUNT;
    c->obj_mode = 0;
    c->title = (char*)title;
}

static void push_object_choice(int scene, Object o, unsigned char mode,
                               const char* title)
{
    Choice* c;
    push_choice(scene, STONE_COUNT, STONE_COUNT, title);
    if (app.num_choices == 0) return;
    c = &app.choices[app.num_choices - 1];
    c->object = (unsigned char)o; c->obj_mode = mode;
}

static void lose_items(unsigned char n)
{
    unsigned char i;
    unsigned int bits;
    while (n) {
        for (i = 0; i < STONE_COUNT && !app.hero.stones[i]; ++i) {}
        if (i < STONE_COUNT) { --app.hero.stones[i]; --n; continue; }
        /* Seuls les dix objets visibles peuvent etre voles. Les bits suivants
         * sont des faits narratifs caches, pas des biens poses dans le sac. */
        bits = app.hero.objects & 0x03FEu;
        if (bits) {
            bits &= bits - 1;
            app.hero.objects = (app.hero.objects & ~0x03FEu) | bits;
            --n; continue;
        }
        if (app.hero.amulets) {
            app.hero.amulets &= (unsigned char)(app.hero.amulets - 1);
            --n; continue;
        }
        break;
    }
}

/* Classe une ligne du fichier. Le format d'une page :
 *
 *   T  <id> <titre>             titre, en video inverse ligne 1
 *   V  <id> [<page> ...]        "si vous y etes deja venu, rendez-vous au
 *                               <id>" -- doit preceder tout le reste de la
 *                               page, qu'un detour annule. Les numeros qui
 *                               suivent sont les AUTRES pages de la meme
 *                               clairiere (page-hub, variantes de recit) :
 *                               le detour se declenche si l'une d'elles, ou
 *                               <id>, ou la page courante, a deja ete vue.
 *                               Sans elles, entrer par un autre sentier
 *                               rejouait la premiere visite
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
 *   E0 <CARAC> <delta>          variation du TOTAL DE DEPART, valeur courante
 *                               comprise. En perte elle est definitive :
 *                               E0 HABILETE -2 (page 87). En gain elle releve
 *                               le plafond : E0 CHANCE +2, la benediction de
 *                               Grognard (page 155)
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
 *   PD / PO / PX                 retire deux objets, un objet, ou tout le sac
 *   TR                           echange jusqu'a trois objets/amulettes contre
 *                               autant de Pierres neutres a choisir
 *   CL <ok> <ko> [<dok> <dko>]  "Tentez votre Chance" : la page envoie en
 *                               <ok> si Chanceux, en <ko> sinon, avec un
 *                               effet d'ENDURANCE optionnel sur chaque
 *                               branche -- le livre en pose deux ("si vous
 *                               etes Chanceux, vous perdez 2 points
 *                               d'ENDURANCE et vous vous rendez au 270")
 *   CP <PIERRE> <id> <titre>    choix qui remet une Pierre Magique
 *   CU <PIERRE> <id> <titre>    choix qui EXIGE et consomme une Pierre
 *   G/GX/GA <OBJET>              donne/retire un objet, ou remet les amulettes
 *   CI/CN/GU <OBJET> <id> ...   possede/ne possede pas/possede et consomme
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
    /* Les trois premieres lettres, lues une fois. Chaque `l[1] == 'X'` sur le
     * pointeur coutait un rechargement indirect (ldy/lda (ptr),y) ; sur trois
     * octets statiques c'est un `lda` absolu. Une centaine de comparaisons
     * dans cette fonction : 4,6 Ko avant, sans changer une seule regle. */
    unsigned char c0 = (unsigned char)l[0];
    unsigned char c1 = (unsigned char)l[1];
    unsigned char c2 = (unsigned char)l[2];

    if (app.revisit >= 0) return;   /* la page est court-circuitee (ligne V) */

    /* L'instantane contient deja les effets d'entree de la scene reprise. */
    if (restoring && ((c0 == 'E' && (c1 == ' ' || c1 == '0' || c1 == 'D')) ||
                      (c0 == 'P' && (c1 == ' ' || c1 == 'C' ||
                                                   c1 == 'D' || c1 == 'O' ||
                                                   c1 == 'X')) ||
                      (c0 == 'G' && (c1 == ' ' || c1 == 'X' || c1 == 'A')) ||
                      (c0 == 'C' && c1 == 'E') ||
                      (c0 == 'T' && c1 == 'R') ||
                      (c0 == 'V' && c1 == ' '))) return;

    if (c0 == 'G' && c1 == 'X' && c2 == ' ') {
        t = take_word(l + 3, &word);
        (void)t; character_take_object(&app.hero, object_from_name(word));
        return;
    }
    if (c0 == 'G' && c1 == 'A' && c2 == ' ') {
        take_uint(l+3,&a);
        character_trade_amulets(&app.hero,a);
        return;
    }
    if (c0 == 'G' && c1 == ' ') {
        Amulet am;
        t = take_word(l + 2, &word);
        (void)t; am=amulet_from_name(word);
        if (am != AMULET_COUNT) character_give_amulet(&app.hero, am);
        else character_give_object(&app.hero,object_from_name(word));
        return;
    }
    if (c0 == 'C' && (c1 == 'I' || c1 == 'N') && c2 == ' ') {
        Object o;
        Amulet am;
        unsigned char mode = (c1 == 'I') ? 1 : 2;
        t = take_word(l + 3, &word); o = object_from_name(word);
        t = take_uint(t, &a);
        am=amulet_from_name(word);
        if (am != AMULET_COUNT) push_object_choice((int)a, (Object)(0x80|am), mode, t);
        else if (o != OBJ_COUNT) push_object_choice((int)a, o, mode, t);
        return;
    }
    if (c0 == 'C' && c1 == 'A' && c2 == ' ') {
        unsigned int lo, hi;
        t=take_uint(l+3,&lo); t=take_uint(t,&hi); t=take_uint(t,&a);
        push_object_choice((int)a,(Object)0x7f,
                           (unsigned char)((lo<<4)|hi),t);
        return;
    }
    if (c0 == 'G' && c1 == 'U' && c2 == ' ') {
        Object o;
        t = take_word(l + 3, &word); o = object_from_name(word);
        t = take_uint(t, &a);
        if (o != OBJ_COUNT) push_object_choice((int)a, o, 3, t);
        return;
    }
    if (c0 == 'P' && (c1 == 'D' || c1 == 'O') && c2 == '\0') {
        lose_items((unsigned char)(c1 == 'D' ? 2 : 1));
        return;
    }
    if (c0 == 'P' && c1 == 'X' && c2 == '\0') {
        memset(app.hero.stones, 0, sizeof app.hero - 9);
        return;
    }
    if (c0 == 'T' && c1 == 'R' && c2 == '\0') {
        unsigned int bits = app.hero.objects & 0x018Cu;
        a = 0;
        while (bits && a < 3) { bits &= bits - 1; ++a; }
        app.hero.objects = (app.hero.objects & ~0x018Cu) | bits;
        while (app.hero.amulets && a < 3) {
            app.hero.amulets &= (unsigned char)(app.hero.amulets - 1); ++a;
        }
        app.choose_n = (unsigned char)a;
        app.choose_cats[0] = 'N'; app.choose_cats[1] = '\0';
        return;
    }

    /* MD et MS qualifient le dernier adversaire declare. */
    if (c0 == 'M' && c1 == 'D' && c2 == ' ' && app.foe_count > 0) {
        take_uint(l + 3, &a);
        app.foes[app.foe_count - 1].damage = (unsigned char)a;
        return;
    }
    if (c0 == 'M' && c1 == 'S' && c2 == ' ' && app.foe_count > 0) {
        take_uint(l + 3, &a);
        app.foes[app.foe_count - 1].stop_at = (unsigned char)a;
        return;
    }
    /* MV se lit avec MD et MS -- donc avant le test `M ` d'une seule lettre,
     * qui l'avalerait -- mais sans leur garde `foe_count > 0` : MV ne qualifie
     * pas le dernier adversaire declare, et peut preceder les lignes M. */
    if (c0 == 'M' && c1 == 'V' && c2 == ' ') {
        take_uint(l + 3, &a);
        app.win_scene = (int)a;
        return;
    }
    if (c0 == 'M' && c1 == 'B' && c2 == ' ') {
        /* MB <si-vous-touchez> <si-touche> : duel au premier sang. */
        t = take_uint(l + 3, &a);
        app.mb_ok = (int)a;
        take_uint(t, &b);
        app.mb_ko = (int)b;
        return;
    }
    if (c0 == 'M' && c1 == ' ') {
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
    if (c0 == 'E' && c1 == '0' && c2 == ' ') {
        /* Variation du total de depart : perte definitive (page 87) ou
         * benediction qui releve le plafond (page 155). */
        /* Ce n'est pas carac_apply -- celle-ci deplace le PLAFOND -- mais
         * la meme numerotation, que rules.c connait. */
        t = take_word(l + 3, &word);
        character_shift0(&app.hero, carac_of(word), atoi(t));
        return;
    }
    if (c0 == 'C' && c1 == 'E' && c2 == ' ') {
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
    if (c0 == 'E' && c1 == 'D' && c2 == ' ') {
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
    if (c0 == 'E' && c1 == ' ') {
        t = take_word(l + 2, &word);
        /* L'or passe par character_adjust_gold comme le reste : un
         * `gold += delta` sur un champ non signe donnait 65535 Pieces d'Or au
         * heros sans le sou qui en depense une. */
        carac_apply(carac_of(word), atoi(t));
        return;
    }
    if (c0 == 'P' && c1 == 'C' && c2 == ' ') {
        t = take_uint(l + 3, &a);
        app.choose_n = (unsigned char)a;
        strncpy(app.choose_cats, t, sizeof(app.choose_cats) - 1);
        app.choose_cats[sizeof(app.choose_cats) - 1] = '\0';
        return;
    }
    if (c0 == 'P' && c1 == ' ') {
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
    if (c0 == 'C' && c1 == 'L' && c2 == ' ') {
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
    if (c0 == 'C' && c1 == 'U' && c2 == ' ') {
        Stone st;
        t = take_word(l + 3, &word);
        st = stone_from_name(word);
        t = take_uint(t, &a);
        if (st != STONE_COUNT)
            push_choice((int)a, (unsigned char)STONE_COUNT, (unsigned char)st, t);
        return;
    }
    if (c0 == 'C' && c1 == 'P' && c2 == ' ') {
        Stone st;
        t = take_word(l + 3, &word);
        st = stone_from_name(word);
        t = take_uint(t, &a);
        if (st != STONE_COUNT)
            push_choice((int)a, st, (unsigned char)STONE_COUNT, t);
        return;
    }
    if (c0 == 'V' && c1 == ' ') {
        /* "Si vous y etes deja venu, rendez-vous au 142. Sinon, lisez ce qui
         * suit." Le detour decide, plus rien de la page ne doit jouer : ni
         * son texte, ni ses choix, ni surtout ses lignes E et P, qui
         * donneraient une seconde fois ce qu'on a deja pris. D'ou le garde
         * en tete de fonction -- et l'invariant, verifie par reflow_txt.py,
         * que la ligne V precede tout le reste.
         *
         * Le livre dit "si vous Y etes deja venu" -- dans la CLAIRIERE, pas
         * sur cette page. Or une clairiere en occupe plusieurs : la page
         * d'arrivee, la page-hub qui porte les sentiers, la page de revisite
         * ou l'on entre parfois directement depuis le voisin. Le bitmap est
         * indexe sur la page, donc revenir par une autre porte rejouait la
         * premiere visite -- creature ressuscitee, objets redonnes. D'ou la
         * liste : on teste la page courante, la cible, puis chaque page
         * citee, et le premier drapeau leve suffit. */
        t = take_uint(l + 2, &a);
        b = (unsigned int)app.current_scene;
        while (!scene_visited(b)) {
            if (*t) { t = take_uint(t, &b); continue; }
            if (b == a) return;   /* la cible a ete testee : la liste est finie */
            b = a;                /* passer par la revisite compte aussi */
        }
        app.revisit = (int)a;
        return;
    }
    if (c0 == 'C' && c1 == 'S' && c2 == ' ') {
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
    if (c0 == 'D' && c1 == 'V' && c2 == ' ') {
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
    if (c0 == 'C' && c1 == 'F' && c2 == ' ') {
        t = take_uint(l + 3, &a);
        app.flee_target = (int)a;
        return;
    }

    if (c0 == 'T' && c1 == ' ') {
        t = l + 2;
        while (*t >= '0' && *t <= '9') t++;
        while (*t == ' ') t++;
        scene_title = t;
    } else if (c0 == 'C' && c1 == ' ') {
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
        if (body_count > 0 || c0 != '\0') {
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
    unsigned char crlf;

    /* Build paths */
    if (build_paths(scene_id, app.language, app.imgPath, app.txtPath) != 0) {
        if (display_mode) {
            cfmt("Erreur: scene %u hors plage (0-999).\r\n", scene_id);
            wait_any();
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
            prodos_error("chdir composant texte");
            wait_any();
        }
        return 0;
    }

    /* Open text file */
    f = fopen(app.txtPath, "r");
    if (!f) {
        if (display_mode) {
            report_open_error(app.txtPath);
            wait_any();
        }
        return 0;
    }
    
    /* Read file into buffer */
    bytes_read = fread(file_buffer, 1, sizeof(file_buffer) - 1, f);
    fclose(f);
    
    if (bytes_read == 0) {
        if (display_mode) {
            cputs("Erreur: fichier vide.\r\n");
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
static void put_gauge(unsigned char v, unsigned char v0)
{
    unsigned char i, n;
    n = (v0 == 0 || v == 0)
        ? 0
        : (unsigned char)(((unsigned int)v * 10u + v0 - 1u) / v0);
    if (n > 10) n = 10;
    cputc('[');
    for (i = 0; i < 10; i++) cputc((i < n) ? '#' : '-');
    cputc(']');
}

/* Une touche et son verbe : la touche en video inverse, comme la barre de
 * titre. Entre crochets, l'oeil devait chercher ; en inverse il accroche. */
static void put_key(const char* key, const char* label)
{
    revers(1); cfmt(" %s ", key); revers(0);
    cfmt(" %s   ", label);
}

/* Un demi-bandeau de combattant : nom en inverse, HABILETE, jauge, points. */
static void put_fighter(const char* name, unsigned char nmax,
                        unsigned char hab,
                        unsigned char end, unsigned char end0)
{
    unsigned char n = 0;

    revers(1);
    while (name[n] && n < nmax) { cputc(name[n]); n++; }
    revers(0);

    cfmt(is_fr() ? " HAB %u " : " SKL %u ", hab);
    put_gauge(end, end0);
    cfmt(" %u/%u", end, end0);
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
    cputs(text);
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
    unsigned char n, i, row, back;
    char key;
    Stone s;

    /* Le sac s'ecrit dans la page texte, et il faut donc l'ALLUMER : sans ca,
     * ouvert depuis le mode image, il se dessinait derriere l'illustration et
     * sa boucle avalait ESPACE, RETURN et les lettres sans que rien ne bouge a
     * l'ecran -- seul ESC en sortait, et il en fallait un second pour que la
     * bascule video reprenne. Vu de l'exterieur, la machine etait bloquee en
     * HGR. Les autres ecrans modaux (l'aide, le choix des Pierres) forcaient
     * deja le texte ; celui-ci etait le seul a ne pas le faire.
     * On rend au joueur, en sortant, le mode qu'il avait choisi : le sac
     * ouvert en plein combat rend son illustration au combat. */
    back = app.video_mode;
    set_video_mode(0);

    for (;;) {
        clrscr();
        render_title_bar();
        gotoxy(0, 2);
        cfmt(msg(M_SAC_A_DOS), app.hero.gold);

        n = 0; row = 4;
        for (s = 0; s < STONE_COUNT; s++) {
            if (app.hero.stones[s] == 0) continue;
            gotoxy(0, row++);
            cfmt("%c) %2u  %-12s  %c%s",
                    'A' + n, app.hero.stones[s],
                    stone_name(s, !is_fr()), kKind[stone_kind(s)],
                    stone_usable(s, in_combat)
                        ? "" : (msg(M_INTERDITE_EN_PLEIN)));
            shown[n++] = s;
        }
        /* Objets visibles, suivis des six amulettes ; les drapeaux narratifs
         * (indices 9 et suivants) ne figurent jamais dans le sac. */
        for (i = 0; i < 10; ++i) {
            if (!character_has_object(&app.hero, (Object)i)) continue;
            gotoxy(40, 4 + i);
            cfmt("- %s", object_name((Object)i, !is_fr()));
        }
        for (i = 0; i < AMULET_COUNT; ++i) {
            if (!character_has_amulet(&app.hero, (Amulet)i)) continue;
            gotoxy(40, 13 + i);
            cfmt("- %s", amulet_name((Amulet)i, !is_fr()));
        }
        if (n == 0 && app.hero.objects == 0) {
            gotoxy(0, 4);
            cputs(msg(M_AUCUNE_PIERRE_MAGIQUE));
        }

        print_at(22, msg(M_UNE_PIERRE_SE));
        key = cgetc();
        /* [I] est une bascule : elle ouvre le sac et le referme. */
        if (key == 27 || key == 'I' || key == 'i') break;
        /* Une lettre hors de A..Z passe en negatif, donc au-dela de n
         * une fois dans l'octet : un seul test suffit. */
        i = (unsigned char)((key >= 'a') ? (key - 'a') : (key - 'A'));
        if (i >= n) continue;

        s = shown[i];
        clear_bottom();
        gotoxy(0, 22);
        switch (stone_use(&app.hero, s, in_combat)) {
        case STONE_USE_FORBIDDEN:
            cputs(msg(M_LE_PREMIER_COUP));
            break;
        case STONE_USE_NONE:
            cputs(msg(M_PIERRE_ABSENTE));
            break;
        default:
            cfmt(msg(M_LA_PIERRE_DE), stone_name(s, !is_fr()));
            break;
        }
        wait_key_at(23, msg_continue());
    }

    set_video_mode(back);
}

/* "A plusieurs reprises au cours de votre aventure [...] vous aurez la
 * possibilite de faire appel a votre chance" -- mais sur ces pages-la le livre
 * ne laisse pas le choix : il ORDONNE le jet et annonce les deux issues. Le
 * moteur le joue donc lui-meme, une fois la page lue. Rend la scene ou aller. */
#pragma code-name (push, "LC")
static int run_luck_test(void)
{
    unsigned char roll;
    int lucky;

    gotoxy(0, CHOICE_ROW0);
    cfmt(msg(M_TENTEZ_VOTRE_CHANCE), app.hero.cha);
    pad_to(79);
    cgetc();

    /* Le jet est releve avant d'etre applique, pour pouvoir le montrer : la
     * regle veut qu'un point de CHANCE parte a chaque tentative, gagnee ou
     * perdue. */
    roll = roll_2d6();
    lucky = (roll <= app.hero.cha);
    gotoxy(0, CHOICE_ROW0);
    cfmt(msg(M_JET_DE_CHANCE), (unsigned)roll, (unsigned)app.hero.cha);
    pad_to(79);
    row_blank(CHOICE_ROW0 + 2);
    if (app.hero.cha > 0) app.hero.cha--;

    print_at(CHOICE_ROW0 + 1, lucky ? msg(M_CHANCEUX) : msg(M_MALCHANCEUX));
    character_adjust_end(&app.hero, lucky ? app.luck_dok : app.luck_dko);
    render_title_bar();
    wait_key_at(CHOICE_ROWN, msg_continue());
    return lucky ? app.luck_ok : app.luck_ko;
}
#pragma code-name (pop)

/* "Lancez un de et retranchez le chiffre obtenu de votre total d'ENDURANCE."
 * Le livre ordonne le jet, il ne le propose pas : le moteur le joue, mais il
 * le MONTRE -- un de qui tombe en coulisse ne se distingue pas d'une perte
 * seche, et le joueur ne saurait pas ce qu'il vient de payer.
 *
 * Meme cadre que run_luck_test, et deux messages seulement : la prose de la
 * page est encore a l'ecran au-dessus, elle dit deja ce que le de coute et
 * sur quoi ; la Feuille d'Aventure de la ligne 1 dit ce qu'il a coute. */
#pragma code-name (push, "LC")
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
    cfmt(msg(M_VOUS_JETEZ), (unsigned)roll);
    pad_to(79);
    carac_apply(app.dice_carac, (n < 0) ? -(int)roll : (int)roll);
    render_title_bar();
    wait_key_at(CHOICE_ROWN, msg_continue());
}
#pragma code-name (pop)

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
#pragma code-name (push, "LC")
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
    cfmt(msg(M_JET_CONTRE), (unsigned)roll, (unsigned)against);
    pad_to(79);
    wait_key_at(CHOICE_ROWN, msg_continue());
    return (roll <= against) ? app.cs_ok : app.cs_ko;
}
#pragma code-name (pop)

/* "Vous choisirez ces six Pierres dans la liste qui figure au debut de ce
 * livre, mais vous ne pourrez les prendre que..." -- un bon sorcier ne donne
 * pas de Pierre malefique, un mauvais pas de Pierre benefique, et l'on a le
 * droit de prendre plusieurs fois la meme ("par exemple 4 Pierres de Feu"). */
#pragma code-name (push, "LC")
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
        cfmt("%c) %-12s %c", 'A' + count, stone_name(s, !is_fr()), k);
        allowed[count++] = s;
    }
    if (count == 0) { app.choose_n = 0; return; }
    print_at(20, msg(M_PRENDRE_UNE_PIERRE));

    while (app.choose_n > 0) {
        gotoxy(0, 2);
        cfmt(msg(M_CHOISISSEZ_PIERRES), (unsigned)app.choose_n);
        key = cgetc();
        i = (key >= 'a') ? (key - 'a') : (key - 'A');
        if (i >= 0 && i < count) {
            character_give_stone(&app.hero, allowed[i], 1);
            app.choose_n--;
        }
    }
}
#pragma code-name (pop)

/* Un combat. Rend 0 si le heros meurt, 1 si la creature tombe, 2 s'il fuit. */
static int run_combat(void)
{
    unsigned char assaut = 0;
    unsigned char use_luck, lucky;
    unsigned char pending = 0;  /* une blessure annoncee attend d'etre encaissee */
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
            cputs(msg(M_VOUS_FUYEZ_ELLE));
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
                cfmt(msg(M_S_EFFONDRE), app.foes[app.foe_cur].name);
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
        cfmt(msg(M_ASSAUT_FORCE_D), assaut, r.hero_force,
                r.hero_force > r.monster_force ? ">"
                : (r.hero_force < r.monster_force ? "<" : "="),
                r.monster_force);
        if (app.foe_count > 1) cfmt("   %u/%u",
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
        cputs(r.outcome == ROUND_HERO_HITS ? msg(M_VOUS_L_AVEZ)
                                           : msg(M_ELLE_VOUS_A));
        cfmt(msg(M_DEGATS), (unsigned)hurt);
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
#pragma code-name (push, "LC")
/* Rend 1 si le joueur a repris une sauvegarde : unpack_save a alors deja
 * pose le heros, les memoires et la scene en attente, rien a remettre a
 * zero. L'ecran se repeint apres une page des sauvegardes refermee sans
 * charger. */
static unsigned char game_over(void)
{
    char key;

    for (;;) {
        set_video_mode(0);
        clrscr();
        gotoxy(0, 6);
        cputs(msg(M_VOTRE_ENDURANCE_EST));
        print_at(8, msg(M_MORT_RECOMMENCER));
        key = cgetc();
        if (key == 'R' || key == 'r') return 0;
        if ((key == 'L' || key == 'l') && show_saves(0)) return 1;
        if (key == 'Q' || key == 'q') {
            videomode(VIDEOMODE_40COL);
            clrscr();
            exit(0);
        }
    }
}
#pragma code-name (pop)

/* La creation du personnage, telle que le livre l'ouvre. */
#pragma code-name (push, "LC")
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
    cputs(msg(M_FEUILLE_D_AVENTURE));
    gotoxy(0, 5);
    cfmt(msg(M_HABILETE_DE),   app.hero.hab);
    gotoxy(0, 6);
    cfmt(msg(M_ENDURANCE_DES), app.hero.end);
    gotoxy(0, 7);
    cfmt(msg(M_CHANCE_DE),   app.hero.cha);
    gotoxy(0, 9);
    cfmt(msg(M_UNE_EPEE_UNE), app.hero.gold);
    gotoxy(0, 10);
    cputs(msg(M_AUCUN_DE_CES));
    wait_key_at(13, msg(M_ESPACE_ENTRER_DANS));
}
#pragma code-name (pop)

/* La mort et ce qui la suit, en un seul endroit. Le combat n'en a plus le
 * monopole : "si vous survivez" (pages 252, 261, 274) dit que le de de la
 * ligne ED peut tuer lui aussi, et dupliquer les cinq lignes couterait plus
 * cher que la fonction. */
static void die_and_restart(void)
{
    if (game_over()) return;
    monster_memory_reset();
    scene_memory_reset();
    app.hero_ready = 0;
    app.pending_scene = 0;
}

/* Charger une nouvelle scene - version optimisée */
void load_scene(int scene_id) {
    int issue;

    /* La musique ne joue que sur l'accueil : coupee avant toute lecture
     * disque (ProDOS masque les IRQ pendant les E/S, et l'AY tiendrait la
     * derniere note), relancee plus bas une fois la page 000 chargee. */
    music_stop();

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
    /* Une ligne E peut tuer a l'entree -- "vous perdez 5 points d'ENDURANCE",
     * page 357 -- et seuls le de et le combat etaient testes. La page se lit
     * d'abord, puis c'est la mort. La garde hero_ready ecarte l'accueil, ou
     * le heros n'existe pas encore et son ENDURANCE vaut zero. */
    if (app.hero_ready && character_is_dead(&app.hero)) {
        wait_key_at(CHOICE_ROWN, msg_continue());
        die_and_restart();
        return;
    }

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
    if (scene_id == 0) music_play();   /* apres les lectures disque de la page */

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
/* L'ecran-titre vit sur le disque (TITLE.TXT), comme tout le contenu : 26
 * cprintf et ~850 octets de chaines pour un ecran montre une fois etaient le
 * plus gros gisement d'octets du binaire. S'il manque, la ligne de secours
 * suffit a choisir la langue. */
void display_language_selection(void) {
    static char line[81];
    FILE* f;

    videomode(VIDEOMODE_80COL);
    clrscr();
    /* Sur le volume, l'empaqueteur retire l'extension .TXT -- meme
     * convention que MSGFR/MSGEN. */
    f = fopen("TITLE", "r");
    if (f) {
        while (fgets(line, sizeof(line), f)) { cputs(line); cputc('\r'); }
        fclose(f);
    } else {
        cputs("[F] Francais   [E] English\r\n");
    }
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

/* Fonction pour gérer les choix de l'utilisateur */
/* La page des sauvegardes. Dix emplacements, chacun sous le titre de la
 * page ou la partie s'est arretee. `saving` dit si [0-9] ecrit ou reprend.
 * La touche qui l'a ouverte la referme, ESC aussi. Rend 1 si une partie a
 * ete chargee (pending_scene est alors pose par unpack_save). */
static unsigned char show_saves(unsigned char saving)
{
    char title[SAVE_TITLE];
    unsigned char slot;
    char key;

    set_video_mode(0);
    for (;;) {
        clrscr();
        render_title_bar();
        print_at(2, msg(saving ? M_SAUVEGARDES : M_CHARGEMENTS));
        for (slot = 0; slot < 10; slot++) {
            slot_title(slot, title);
            gotoxy(2, 4 + slot);
            cfmt("%c) %s", '0' + slot, title[0] ? title : msg(M_VIDE));
        }
        key = cgetc();
        if (key == 27) return 0;
        if (saving  && (key == 'S' || key == 's')) return 0;
        if (!saving && (key == 'L' || key == 'l')) return 0;
        if (key < '0' || key > '9') continue;
        slot = (unsigned char)(key - '0');
        if (saving) {
            print_at(CHOICE_ROW0, msg(save_game(slot) ? M_SAUVE_OK : M_SAUVE_ERREUR));
            wait_key_at(CHOICE_ROWN, msg_continue());
            return 0;
        }
        if (load_game(slot)) return 1;
        print_at(CHOICE_ROW0, msg(M_CHARGE_ERREUR));
        wait_key_at(CHOICE_ROWN, msg_continue());
    }
}

void handle_user_input(char key) {
    unsigned char choice_num;
    Choice* c;
    
    if (key == ' ' || key == '\r' || key == 27) {
        /* Barre d'espace, RETURN ou ESC : cycler les modes */
        cycle_video_mode();
        
    } else if (key == 'I' || key == 'i') {
        /* Hors combat, toutes les Pierres sont utilisables. */
        show_inventory(0);
        render_scene();

    } else if (key == 'H' || key == 'h') {
        show_help();

    } else if (key == 'S' || key == 's' || key == 'L' || key == 'l') {
        /* pack_save et load_game partagent file_buffer avec le texte de la
         * scene. Sans partie chargee, on relit la page au prochain tour pour
         * restaurer ses pointeurs ; restoring interdit de rejouer les gains,
         * pertes, jets et autres effets d'entree. */
        if (!show_saves(key == 'S' || key == 's')) {
            restoring = 1;
            app.pending_scene = app.current_scene;
        }

    } else if ((key == 'R' || key == 'r') && app.num_choices == 0) {
        /* Recommencer depuis une page sans issue : la meme remise a zero que
         * die_and_restart, sans l'ecran de mort -- la page vient de la dire. */
        monster_memory_reset();
        scene_memory_reset();
        app.hero_ready = 0;
        app.pending_scene = 0;

    } else if (key == 'Q' || key == 'q') {
        /* Quitter */
        set_video_mode(0);
        videomode(VIDEOMODE_40COL);
        clrscr();
        if (strcmp(app.language, "FR") == 0) {
            cputs("Au revoir!\r\n");
        } else {
            cputs("Goodbye!\r\n");
        }
        exit(0);
        
    } else if ((key >= 'A' && key <= 'Z') || (key >= 'a' && key <= 'z')) {
        /* Choix par lettre */
        choice_num = (unsigned char)((key >= 'a') ? (key - 'a') : (key - 'A'));
        if (choice_num < app.num_choices) {
            c = &app.choices[choice_num];
            if (!choice_available(choice_num)) {
                /* On ne lance pas un sort qu'on n'a pas. */
                clear_bottom();
                print_at(CHOICE_ROW0, msg(M_PIERRE_ABSENTE));
                wait_key_at(CHOICE_ROWN, msg_continue());
                render_scene();
                return;
            }
            /* La Pierre exigee se desintegre en servant. */
            if (c->require < STONE_COUNT) stone_use(&app.hero, (Stone)c->require, 0);
            /* Une Pierre offerte par le choix change de main avant le saut. */
            if (c->grant < STONE_COUNT) character_give_stone(&app.hero, (Stone)c->grant, 1);
            if (c->obj_mode == 3) character_take_object(&app.hero, (Object)c->object);
            /* Le premier choix de l'introduction lance la creation : le
             * joueur comprend d'abord qui il va incarner, puis les des
             * produisent sa Feuille d'Aventure avant l'entree au Marais. */
            if (!app.hero_ready) roll_character();
            load_scene(c->scene_id);
        }
    }
}

void main(void) {
    char key;

    /* LOWBSS n'est pas dans la BSS que crt0 met a zero : on le fait ici,
     * avant tout, avec les bornes que le lieur exporte (scoswamp.cfg). */
    memset(_LOWBSS_RUN__, 0, (size_t)_LOWBSS_SIZE__);

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
        clrscr();
        prodos_error("chdir(/SCOSWAMP)");
        cputs("Cause: entree volume/repertoire HDV invalide\r\n");
        wait_any();
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
    music_detect();   /* Mockingboard : slots 7..1 ; sans carte, tout reste muet */

    /* L'introduction vient avant les des : son choix A initie explicitement
     * la creation du personnage. [L] peut aussi reprendre une partie ici. */
    load_scene(0);
    
    /* Boucle principale. La scène en attente évite que load_scene s'appelle
     * lui-même sur une Fuite ou une mort : la pile cc65 fait 2 Ko et une
     * poursuite de clairière en clairière la mangerait. */
    while (1) {
        if (app.pending_scene >= 0) {
            int next = app.pending_scene;
            app.pending_scene = -1;
            load_scene(next);
            restoring = 0;
            continue;
        }
        /* Une page restee sans aucun choix est une fin -- mort par la prose,
         * victoire, ou combat gagne sans suite. Le moteur offre alors de
         * recommencer, de reprendre une sauvegarde ou de quitter, plutot que
         * de laisser le joueur devant un ecran muet. Ici, au point ou la
         * page est vraiment inactive : apres les des, les jets et le combat. */
        if (app.num_choices == 0) print_at(CHOICE_ROWN, msg(M_MORT_RECOMMENCER));
        key = cgetc();
        handle_user_input(key);
    }
}
