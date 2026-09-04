#ifndef HGR_RLE_H
#define HGR_RLE_H

#include <stdio.h>

#define HGR_RLE_DECODED_SIZE 16384u

/* `__fastcall__` est une extension cc65 : le decodeur est aussi compile sur la
 * machine hote par TOOLS/test_hgr_rle.c, ou le mot-cle n'existe pas. */
#ifndef __CC65__
#define __fastcall__
#endif

/* Bulk-load and decode one DHRR v1 stream to DHGR page 1 (aux then main). */
int __fastcall__ hgr_rle_load(const char* path);

/* Decode un flux HGRR v1 vers `dst`. Rend 1 si le flux est valide et complet.
 * C'est le point d'entree testable : `hgr_rle_load` y ajoute ProDOS et
 * l'ecriture directe en memoire video. */
int hgr_rle_decode_file(FILE* input, unsigned char* dst, unsigned int dst_size);

#endif
