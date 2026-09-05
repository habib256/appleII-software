#!/usr/bin/env bash
# Genere les images d'un manifeste en appelant codex exec, une image par ligne.
#
#   generate_images.sh <manifest.jsonl> [limite] [paralleles]
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
#
# Une image coute ~2 minutes de mur, presque entierement passees a attendre
# le service : les 439 pages du jeu font 14 h en file simple. Le troisieme
# argument lance N generations de front (defaut 1). Chaque tache ecrit son
# propre fichier, donc rien a synchroniser ; ce qui echoue ne laisse pas de
# PNG et sera repris au prochain passage. Le journal de chaque tache est
# garde et cite quand elle echoue -- `codex exec` muet sur un quota depasse
# ressemblait sinon a une generation reussie.
set -euo pipefail

manifest="${1:?usage: generate_images.sh <manifest.jsonl> [limite] [paralleles]}"
limit="${2:-0}"
jobs="${3:-1}"
root="$(cd "$(dirname "$0")/../.." && pwd)"

work="$(mktemp -d "${TMPDIR:-/tmp}/scoswamp-gen.XXXXXX")"
trap 'rm -rf "$work"' EXIT

# ── Decoupage du manifeste en taches ────────────────────────────────────────
# Un fichier par image : le prompt contient des retours a la ligne et des
# guillemets, et le faire transiter par une ligne de xargs le mutilerait.
python3 -c '
import json, os, sys
manifest, work, root, limit = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
n = 0
for line in open(manifest, encoding="utf-8"):
    r = json.loads(line)
    dest = r["source_png"]
    if os.path.exists(os.path.join(root, dest)) and os.environ.get("FORCE", "0") != "1":
        continue
    if limit and n >= limit:
        break
    d = os.path.join(work, "%04d" % n)
    os.makedirs(d)
    with open(d + "/dest", "w", encoding="utf-8") as f:
        f.write(dest + "\n")
    with open(d + "/refs", "w", encoding="utf-8") as f:
        f.write("\n".join(r.get("refs", [])) + ("\n" if r.get("refs") else ""))
    with open(d + "/prompt", "w", encoding="utf-8") as f:
        f.write(r["prompt"] + "\n")
    n += 1
print(n)
' "$manifest" "$work" "$root" "$limit" > "$work/count"
total="$(cat "$work/count")"
echo "$total image(s) a generer, $jobs de front"
[ "$total" -gt 0 ] || { echo "0 image(s) generee(s)"; exit 0; }

# ── Une tache ───────────────────────────────────────────────────────────────
# Rappelee par xargs, donc exportee. `--sandbox workspace-write` est ce que
# codex exige pour ecrire le PNG.
run_one() {
    d="$1"
    dest="$(cat "$d/dest")"
    args=(--sandbox workspace-write)
    nrefs=0
    while IFS= read -r p; do
        [ -n "$p" ] || continue
        args+=(-i "$GEN_ROOT/$p")
        nrefs=$(( nrefs + 1 ))
    done < "$d/refs"

    mkdir -p "$GEN_ROOT/$(dirname "$dest")"
    printf '%s\n\nGenerate this image and save it to %s as a PNG. Resolution: HIGH -- the short side must be at least 1000 pixels (e.g. 1400x960 landscape, 1024x1536 portrait). Never output the bare 140x192 DHGR colour display size: this file is a master reference and needs the detail.\n' \
        "$(cat "$d/prompt")" "$GEN_ROOT/$dest" \
        | codex exec "${args[@]}" - > "$d/log" 2>&1 || true

    # Certains agents ont historiquement confondu le numero de texte T029
    # avec le nom d'image N029 et depose le rendu a la racine de MORE. Ne pas
    # jeter une generation valable pour cette seule erreur de chemin. On ne
    # recupere toutefois qu'un fichier cree pendant cette tache (`-nt`), afin
    # de ne jamais recycler un ancien brouillon comme nouvelle image.
    base="$(basename "$dest" .png)"
    if [ ! -f "$GEN_ROOT/$dest" ] && [[ "$base" == N[0-9][0-9][0-9] ]]; then
        misplaced="$GEN_ROOT/SCOSWAMP.MORE/T${base#N}.png"
        if [ -f "$misplaced" ] && [ "$misplaced" -nt "$d/prompt" ]; then
            mv "$misplaced" "$GEN_ROOT/$dest"
        fi
    fi

    # L'agent d'image laisse parfois derriere lui ses essais -- des pastilles
    # de palette de quelques centaines d'octets nommees B284-0.png, B284-1.png
    # a cote de B284.png. Elles echappent au motif du convertisseur, mais un
    # dossier ou l'on ne distingue plus un rendu d'un brouillon ne se relit pas.
    # Le nom exact du brouillon varie -- B284-0.png, N025.raw.png,
    # N098.source.png -- mais il commence toujours par le nom de la cible.
    # On efface donc tout ce qui partage sa racine sans etre elle.
    # Ne jamais utiliser `${base}?*.png` ici : pour `CLAIRIERE.png`, ce motif
    # englobe les vraies references `CLAIRIERE_01.png`, etc. Les brouillons
    # connus portent soit un tiret numerote, soit le suffixe `.raw`.
    for stray in "$GEN_ROOT/${dest%.png}"-[0-9]*.png "$GEN_ROOT/${dest%.png}.raw.png"; do
        [ -e "$stray" ] && rm -f "$stray"
    done

    if [ -f "$GEN_ROOT/$dest" ]; then
        printf 'ok   %s (%d ref)\n' "$dest" "$nrefs"
    else
        cp "$d/log" "$GEN_FAILDIR/$(basename "$dest" .png).log" 2>/dev/null || true
        printf 'ECHEC %s -- journal %s/%s.log\n' \
            "$dest" "$GEN_FAILDIR" "$(basename "$dest" .png)"
    fi
}
export -f run_one
export GEN_ROOT="$root"
# Vide a chaque passage : le decompte final se lit dedans, et un journal
# laisse par un lot precedent ferait denoncer un echec deja repris.
GEN_FAILDIR="$root/SCOSWAMP.MORE/GENERATED/.failed"
rm -rf "$GEN_FAILDIR"
mkdir -p "$GEN_FAILDIR"
export GEN_FAILDIR

find "$work" -mindepth 1 -maxdepth 1 -type d | sort \
    | xargs -P "$jobs" -I{} bash -c 'run_one "$@"' _ {}

made=$(find "$work" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
failed=$(find "$GEN_FAILDIR" -name '*.log' | wc -l | tr -d ' ')
echo "$(( made - failed )) image(s) generee(s), $failed echec(s)"
