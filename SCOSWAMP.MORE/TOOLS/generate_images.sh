#!/usr/bin/env bash
# Genere les images d'un manifeste en appelant codex exec, une image par ligne.
#
#   generate_images.sh <manifest.jsonl> [limite]
#
# Chaque ligne porte son prompt, sa destination, et — quand la scene cite un
# sujet des bibles — les planches de reference qui fixent son visage. Les
# planches sont attachees avec `-i` : le texte decrit, la planche montre.
# C'est la difference entre "un maitre des loups" et *ce* maitre des loups ;
# sans elle le meme personnage change de tete d'une image a l'autre, ce qui
# est precisement le defaut que ce script existe pour corriger.
#
# Le script saute une ligne dont l'image existe deja : il est relancable,
# et une generation interrompue reprend ou elle s'est arretee.
set -euo pipefail

manifest="${1:?usage: generate_images.sh <manifest.jsonl> [limite]}"
limit="${2:-0}"
root="$(cd "$(dirname "$0")/../.." && pwd)"

done_count=0
# Le champ des references porte "-" quand il n'y en a pas : un champ vide au
# milieu d'une ligne se fait avaler par read, et le prompt glissait d'une place.
while IFS=$'\t' read -r dest refs prompt; do
    [ -n "$dest" ] || continue
    if [ -f "$root/$dest" ]; then continue; fi
    if [ "$limit" -gt 0 ] && [ "$done_count" -ge "$limit" ]; then break; fi

    mkdir -p "$root/$(dirname "$dest")"
    # Le tableau porte deja le mode de bac a sable : sous bash 3.2 (celui de
    # macOS) l'expansion d'un tableau vide sous `set -u` avorte le script.
    args=(--sandbox workspace-write)
    nrefs=0
    if [ "$refs" != "-" ]; then
        # Les references passent en piece jointe, pas en texte.
        IFS='|' read -r -a paths <<< "$refs"
        for p in "${paths[@]}"; do
            args+=(-i "$root/$p")
            nrefs=$(( nrefs + 1 ))
        done
    fi

    printf '%s' "$dest"
    if [ "$nrefs" -gt 0 ]; then printf ' (%d ref)' "$nrefs"; fi
    printf '\n'

    # Le prompt arrive par stdin : il contient des retours a la ligne et des
    # guillemets, et passer par argv les ferait manger par le shell.
    printf '%b\n\nGenerate this image and save it to %s as a PNG. Resolution: HIGH -- the short side must be at least 1000 pixels (e.g. 1400x960 landscape, 1024x1536 portrait). Never output the bare 280x192 display size: this file is a master reference and needs the detail.\n' \
        "$prompt" "$root/$dest" \
        | codex exec "${args[@]}" - >/dev/null 2>&1
    done_count=$(( done_count + 1 ))
done < <(python3 -c '
import json, signal, sys
# Le lecteur s en va quand la limite est atteinte : mourir du SIGPIPE plutot
# que de vomir une trace.
signal.signal(signal.SIGPIPE, signal.SIG_DFL)
for line in open(sys.argv[1], encoding="utf-8"):
    r = json.loads(line)
    print("\t".join((r["source_png"],
                     "|".join(r.get("refs", [])) or "-",
                     r["prompt"].replace("\\", "\\\\").replace("\n", "\\n").replace("\t", " "))))
' "$manifest")

echo "$done_count image(s) generee(s)"
