/* paths.c - noms de fichiers des scenes */
#include <string.h>
#include "paths.h"

/* "N" puis l'id sur trois chiffres, sans terminateur ; rend la suite.
 * Un sprintf("N%03u") faisait entrer tout le formateur de chaines (1,5 Ko
 * de _printf, vsnprintf, ltoa) pour ecrire quatre caracteres. */
char* put_scene(char* p, unsigned int id)
{
    unsigned char v = 0, d;
    /* id <= 999 : les centaines tiennent dans un octet, le reste aussi.
     * Par soustractions -- une division 16 bits appelle la bibliotheque. */
    while (id >= 100) { id -= 100; ++v; }
    *p++ = 'N';
    *p++ = (char)('0' + v);
    d = (unsigned char)id; v = 0;
    while (d >= 10) { d -= 10; ++v; }
    *p++ = (char)('0' + v);
    *p++ = (char)('0' + d);
    return p;
}

/* Image "Nddd.RLE" et texte "Nddd". Le volume aplatit chaque classe d'asset
 * dans un seul repertoire ProDOS ; le sous-repertoire N000/N050/... est
 * choisi par enter_asset_dir, pas ici. `lang` n'entre pas dans les noms. */
int build_paths(unsigned int scene_id, const char* lang,
                char* imgPath, char* txtPath)
{
    (void)lang;
    if (scene_id > 999) return -1;
    memcpy(put_scene(imgPath, scene_id), ".RLE", 5);
    *put_scene(txtPath, scene_id) = '\0';
    return 0;
}
