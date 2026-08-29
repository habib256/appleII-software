#!/bin/sh
# Convertit les PNG de SCOSWAMP.MORE/GENERATED en flux HGR RLE pour le disque.
#
#   N<id>.png -> SCOSWAMP/IMG/N<bucket>/N<id>.RLE.BIN   l'illustration de la clairiere
#   B<id>.png -> SCOSWAMP/IMG/N<bucket>/B<id>.RLE.BIN   l'illustration de bataille
#
# Le bucket est celui du moteur : (id / 50) * 50. Un PNG plus recent que son
# RLE est reconverti, les autres sont laisses tranquilles -- la conversion des
# 400 scenes prend plusieurs minutes.
set -e
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
HGR="$(dirname "$0")/build/scoswamp_hgr"

[ -x "$HGR" ] || {
    echo "Absent : $HGR"
    echo "  cmake -S $(dirname "$0") -B $(dirname "$0")/build"
    echo "  cmake --build $(dirname "$0")/build --target scoswamp_hgr"
    exit 1
}

converted=0
skipped=0
for png in "$ROOT"/SCOSWAMP.MORE/GENERATED/[NB][0-9][0-9][0-9].png; do
    [ -e "$png" ] || continue
    name=$(basename "$png" .png)
    id=$(echo "$name" | cut -c2-4)
    # 10#$id force la base 10 : sans lui "008" est lu comme de l'octal et
    # l'arithmetique du shell s'arrete sur "value too great for base".
    bucket=$(printf 'N%03d' $(( 10#$id / 50 * 50 )))
    out="$ROOT/SCOSWAMP/IMG/$bucket/$name.RLE.BIN"
    if [ -e "$out" ] && [ ! "$png" -nt "$out" ]; then
        skipped=$((skipped + 1))
        continue
    fi
    mkdir -p "$(dirname "$out")" "$ROOT/SCOSWAMP.MORE/HGR-PREVIEW"
    "$HGR" convert "$png" "$out" "$ROOT/SCOSWAMP.MORE/HGR-PREVIEW/$name.png" >/dev/null
    echo "  $name -> $bucket/$name.RLE.BIN"
    converted=$((converted + 1))
done
echo "==> $converted converti(s), $skipped a jour"
