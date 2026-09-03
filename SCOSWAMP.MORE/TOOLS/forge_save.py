#!/usr/bin/env python3
"""forge_save.py - fabrique une sauvegarde SCS3 de SCOSWAMP et l'injecte dans
un volume ProDOS (.hdv) sans reconstruire l'image.

Prototype ecrit pour le rapport d'automatisation. Ne modifie rien de suivi.
"""
import argparse, struct, sys

SAVE_HEADER, SAVE_TITLE = 8, 32
CHAR_SIZE, SCENE_MEM, MON_MEM = 24, 52, 160
SAVE_SIZE = SAVE_HEADER + SAVE_TITLE + CHAR_SIZE + SCENE_MEM + MON_MEM  # 276

STONES = ["HABILETE","ENDURANCE","CHANCE","FEU","GLACE","ILLUSION",
          "AMITIE","CROISSANCE","BENEDICTION","TERREUR","FLETRISSURE","MALEDICTION"]
OBJECTS = ["ANNEAU","CAPE","CHAINE","AIMANT","FIOLE","BAIE","EPEMAGIQUE",
           "BIJOU","CORNE","PLUMES","ANTHERIQUE"]
AMULETS = ["LOUP","FLEUR","OISEAU","ARAIGNEE","GRENOUILLE","FAUSSE_OISEAU"]


def build(scene, lang="F", title="", hab=(12,12), end=(20,20), cha=(11,11),
          gold=20, weapon_bonus=0, stones=None, objects=(), amulets=(),
          visited=(), monsters=()):
    b = bytearray(SAVE_SIZE)
    b[0:4] = b"SCS3"
    struct.pack_into("<H", b, 5, scene)
    b[7] = ord(lang)
    t = title.encode("ascii", "replace")[:SAVE_TITLE - 1]
    b[8:8 + len(t)] = t
    p = SAVE_HEADER + SAVE_TITLE                      # 40 : Character
    b[p+0], b[p+1] = hab
    b[p+2], b[p+3] = end
    b[p+4], b[p+5] = cha
    struct.pack_into("<H", b, p + 6, gold)             # 46
    b[p+8] = weapon_bonus                              # 48
    for name, n in (stones or {}).items():             # 49..60
        b[p + 9 + STONES.index(name)] = n
    mask = 0
    for o in objects:
        mask |= 1 << OBJECTS.index(o)
    struct.pack_into("<H", b, p + 21, mask)            # 61
    am = 0
    for a in amulets:
        am |= 1 << AMULETS.index(a)
    b[p + 23] = am                                     # 63
    p += CHAR_SIZE                                      # 64 : memoire des scenes
    for s in visited:
        b[p + (s >> 3)] |= 1 << (s & 7)
    p += SCENE_MEM                                      # 116 : memoire des monstres
    for i, (sc, idx, endv) in enumerate(monsters[:40]):
        struct.pack_into("<HBB", b, p + i * 4, sc, idx, endv)
    b[4] = 0
    x = 0
    for v in b[5:]:
        x ^= v
    b[4] = x
    return bytes(b)


def patch_hdv(hdv, blob, entry_blk=5878, entry_off=394, key_blk=5888):
    """Ecrit `blob` dans le bloc-cle de PARTIE9 et met l'EOF a jour."""
    with open(hdv, "r+b") as f:
        f.seek(key_blk * 512)
        f.write(blob.ljust(512, b"\0"))
        base = entry_blk * 512 + entry_off
        f.seek(base + 0x15)                            # EOF 3 octets LE
        f.write(bytes((len(blob) & 0xFF, (len(blob) >> 8) & 0xFF, 0)))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", type=int, required=True)
    ap.add_argument("--out")
    ap.add_argument("--hdv")
    a = ap.parse_args()
    blob = build(a.scene, title="FORGE %d" % a.scene,
                 hab=(12, 12), end=(24, 24), cha=(12, 12), gold=99,
                 stones={"FEU": 3, "CHANCE": 2},
                 objects=("BAIE", "CAPE"), amulets=("LOUP", "OISEAU"),
                 visited=(1, 155), monsters=((12, 0, 6),))
    assert len(blob) == SAVE_SIZE
    if a.out:
        open(a.out, "wb").write(blob)
    if a.hdv:
        patch_hdv(a.hdv, blob)
    print("SCS3 %d octets, checksum $%02X" % (len(blob), blob[4]))
