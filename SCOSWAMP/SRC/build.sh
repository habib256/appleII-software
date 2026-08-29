#!/bin/bash
# Script de compilation rapide pour Le Marais aux Scorpions
# Usage: ./build.sh [clean|rebuild|info]

set -e  # Arrêter en cas d'erreur

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

case "${1:-build}" in
    clean)
        echo "==> Nettoyage des fichiers intermédiaires..."
        rm -f *.o *.s
        echo "==> Terminé"
        ;;
    
    distclean)
        echo "==> Nettoyage complet..."
        rm -f *.o *.s ../SCOSWAMP.BIN
        echo "==> Terminé"
        ;;
    
    rebuild)
        echo "==> Reconstruction complète..."
        rm -f *.o *.s ../SCOSWAMP.BIN
        make
        ;;
    
    info)
        echo "Configuration du projet :"
        echo "  Cible         : apple2enh (Apple IIe Enhanced)"
        echo "  Programme     : SCOSWAMP.BIN + SCOSWAMP.SYSTEM (lanceur ProDOS)"
        echo "  Sources       : scoswamp.c paths.c memory_swap.c rules.c dice.c"
        echo "  Sortie        : ../"
        echo "  Adresse start : \$4000 (HGR Page 1 à \$2000-\$3FFF préservé)"
        ;;
    
    build|*)
        echo "==> Compilation de Le Marais aux Scorpions..."
        
        # Vérifier que cc65 est installé
        if ! command -v cl65 &> /dev/null; then
            echo "ERREUR: cc65 n'est pas installé ou pas dans le PATH"
            echo "Installation: https://cc65.github.io/"
            exit 1
        fi
        
        # On delegue au Makefile. Cette ligne de lien etait autrefois recopiee
        # ici : elle avait deja divergé (ni rules.c, ni dice.c, ni
        # __HIMEM__=$BF00, ni le lanceur ProDOS), et un binaire lie sans
        # __HIMEM__ deborde son BSS SANS que ld65 le signale. Une seule
        # definition du lien, dans le Makefile.
        make

        echo ""
        echo "Pour tester :  make hdv    puis"
        echo "  ../../../pom2/build/POM2 --preset iie ../../dist/SCOSWAMP.HDV"
        ;;
esac
