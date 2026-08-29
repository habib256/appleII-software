/* paths.c - Path management implementation */
#include <stdio.h>
#include "paths.h"

int build_paths(unsigned int scene_id, const char* lang,
                char* imgPath, char* txtPath) {
    unsigned int subdirectory;
    
    /* Validate scene_id range */
    if (scene_id > 999) {
        return -1;
    }
    
    /* Kept for source-layout documentation; the distribution HDV flattens
     * each asset class to one ProDOS directory for reliable traversal. */
    subdirectory = (scene_id / 50) * 50;
    
    /* Short ProDOS image name: N<id>.RLE (8 characters).
     * Example: scene_id=1 -> "/SCOSWAMP/IMG/N000/N001.RLE"
     * Component lengths stay within ProDOS's 15-character limit.
     */
    sprintf(imgPath, "N%03u.RLE", scene_id);
    
    /* Build text path: TEXT<lang>/N<subdir>/N<id> (relative path for ProDOS)
     * Example: scene_id=1, lang="FR" -> "TEXTFR/N000/N001"
     * Path length: max 24 chars for scene 999 -> "TEXTFR/N950/N999"
     * Component lengths: "TEXTFR"=6, "N950"=4, "N999"=8 (all <= 15 chars, ProDOS compliant)
     */
    sprintf(txtPath, "N%03u", scene_id);
    
    return 0;
}
