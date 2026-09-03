#!/usr/bin/env python3
"""Génère la carte complète du Marais aux Scorpions depuis carte.json.

Usage : python3 gen_carte.py /chemin/vers/carte.json
Les fichiers carte_marais.svg et carte_marais.txt sont écrits dans le dossier
courant. Aucune dépendance autre que la bibliothèque standard n'est requise.
"""

import argparse
import html
import json
import textwrap
from collections import Counter, defaultdict
from pathlib import Path

W, H = 1400, 1800
LEFT, TOP = 90, 205
CW, CH = 205, 142
BW, BH = 174, 104
OPP = {"N": "S", "S": "N", "E": "O", "O": "E"}
MISSION = {
    "Gayolard": {232},                         # baie d'Anthérique, clr 11
    "Pompatarte": {78},                        # carte jusqu'à Courbensaule
    "Stratagus": {314, 84, 165, 230, 304},     # cinq amulettes
}
MCOLOR = {"Gayolard": "#2e8b57", "Pompatarte": "#b7791f", "Stratagus": "#7b4ab5"}


def esc(value):
    return html.escape(str(value), quote=True)


def short_title(title, width=23):
    return textwrap.shorten(title.replace("Clairiere", "Clr."), width=width,
                            placeholder="…")


def center(c):
    return LEFT + c["x"] * CW + CW / 2, TOP + c["y"] * CH + CH / 2


def anchor(c, direction):
    x, y = center(c)
    return {"N": (x, y-BH/2), "S": (x, y+BH/2),
            "E": (x+BW/2, y), "O": (x-BW/2, y)}[direction]


def load_and_analyse(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    clearings = data["clairieres"]
    by_hub = {c["hub"]: c for c in clearings}
    anomalies = []

    cells = defaultdict(list)
    for c in clearings:
        cells[(c["x"], c["y"])].append(c["hub"])
    for pos, hubs in sorted(cells.items()):
        if len(hubs) > 1:
            anomalies.append(f"collision en {pos}: hubs {hubs}")

    owners = defaultdict(list)
    for c in clearings:
        for page in c["pages"]:
            owners[page].append(c["hub"])
    for page, hubs in sorted(owners.items()):
        if len(hubs) > 1:
            anomalies.append(f"page {page:03d} rattachée à plusieurs lieux: hubs {hubs}")

    ids = defaultdict(list)
    for c in clearings:
        if c["id"] is not None:
            ids[c["id"]].append(c["hub"])
    for number, hubs in sorted(ids.items()):
        if len(hubs) > 1:
            anomalies.append(f"numéro de clairière {number} en double: hubs {hubs}")

    directed = {}
    external = []
    for c in clearings:
        for direction, page in c.get("sorties", {}).items():
            target_hub = c.get("voisins", {}).get(direction)
            # Arbitrage documenté : le libellé de 230 dit est, la prose dit nord.
            actual_dir = "N" if c["hub"] == 230 and direction == "E" else direction
            if target_hub is None:
                external.append((c, actual_dir, page))
                anomalies.append(f"sortie hub {c['hub']:03d} {actual_dir} vers page {page:03d} sans clairière")
            elif target_hub not in by_hub:
                anomalies.append(f"voisin hub {target_hub} inconnu depuis hub {c['hub']}")
            else:
                directed[(c["hub"], target_hub)] = (actual_dir, page)

    edges = []
    seen = set()
    for (a, b), (direction, page) in directed.items():
        key = frozenset((a, b))
        if key in seen:
            continue
        seen.add(key)
        rev = directed.get((b, a))
        reciprocal = bool(rev)
        ca, cb = by_hub[a], by_hub[b]
        teleport = (a == 218 and b == 58)
        length = abs(ca["x"]-cb["x"]) + abs(ca["y"]-cb["y"])
        edges.append({"a": ca, "b": cb, "dir": direction, "page": page,
                      "reciprocal": reciprocal, "teleport": teleport,
                      "long": length == 2})
    return data, clearings, edges, external, anomalies


def svg(data, clearings, edges, external):
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           '<defs>',
           '<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#8b3a3a"/></marker>',
           '<pattern id="water" width="24" height="12" patternUnits="userSpaceOnUse"><path d="M0 6 Q6 1 12 6 T24 6" fill="none" stroke="#69a9c9" stroke-width="2"/></pattern>',
           '<filter id="shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="3" stdDeviation="3" flood-opacity=".18"/></filter>',
           '</defs>', '<rect width="100%" height="100%" fill="#f7f3e8"/>',
           '<text x="700" y="62" text-anchor="middle" font-family="sans-serif" font-size="32" font-weight="700" fill="#243b2f">Le Marais aux Scorpions — carte des clairières</text>',
           '<text x="700" y="96" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#516056">Nord ↑ · x croît vers l’est · y croît vers le sud</text>']

    # Coordonnées et grille discrète.
    for x in range(6):
        cx = LEFT + x*CW + CW/2
        out.append(f'<text x="{cx}" y="160" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#66746b">x={x}</text>')
    for y in range(9):
        cy = TOP + y*CH + CH/2
        out.append(f'<text x="45" y="{cy+5}" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#66746b">y={y}</text>')
        for x in range(6):
            out.append(f'<rect x="{LEFT+x*CW+7}" y="{TOP+y*CH+7}" width="{CW-14}" height="{CH-14}" rx="9" fill="none" stroke="#d8d3c4" stroke-dasharray="3 7"/>')

    # Rivière sur toute la ligne y=3, derrière les nœuds.
    ry = TOP + 3*CH + CH/2
    out += [f'<rect x="60" y="{ry-30}" width="1280" height="60" rx="25" fill="#d7edf3" opacity=".92"/>',
            f'<rect x="60" y="{ry-23}" width="1280" height="46" fill="url(#water)"/>',
            f'<text x="1285" y="{ry-36}" text-anchor="end" font-family="sans-serif" font-size="15" font-weight="700" fill="#347996">RIVIÈRE CROUPIE → OUEST</text>']

    # Liens derrière les cases.
    for e in edges:
        a, b, d = e["a"], e["b"], e["dir"]
        p1, p2 = anchor(a, d), anchor(b, OPP[d])
        if e["teleport"]:
            # Courbe hors grille pour ne pas la confondre avec un sentier.
            x1, y1 = p1; x2, y2 = p2
            path = f'M {x1} {y1} C 25 {y1}, 25 {y2}, {x2} {y2}'
            out.append(f'<path d="{path}" fill="none" stroke="#8b3a3a" stroke-width="4" stroke-dasharray="10 8" marker-end="url(#arrow)"/>')
            out.append(f'<text x="27" y="{(y1+y2)/2}" transform="rotate(-90 27 {(y1+y2)/2})" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#8b3a3a">PIÈGE DU FEU FOLLET</text>')
        else:
            marker = '' if e["reciprocal"] else ' marker-end="url(#arrow)"'
            dash = ' stroke-dasharray="12 7"' if not e["reciprocal"] else ''
            out.append(f'<line x1="{p1[0]}" y1="{p1[1]}" x2="{p2[0]}" y2="{p2[1]}" stroke="#596b55" stroke-width="5" stroke-linecap="round"{dash}{marker}/>')
            if e["long"]:
                mx, my = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
                out.append(f'<circle cx="{mx}" cy="{my}" r="13" fill="#f7f3e8" stroke="#596b55"/><text x="{mx}" y="{my+5}" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="700">2</text>')

    # Sorties hors grille : vraie sortie au sud et deux dangers de la falaise.
    for c, d, page in external:
        x1, y1 = anchor(c, d)
        dx, dy = {"N": (0,-52), "S": (0,52), "E": (52,0), "O": (-52,0)}[d]
        danger = page in (30, 321)
        color = "#a23a35" if danger else "#2f6f49"
        out.append(f'<line x1="{x1}" y1="{y1}" x2="{x1+dx}" y2="{y1+dy}" stroke="{color}" stroke-width="4" stroke-dasharray="8 6" marker-end="url(#arrow)"/>')
        label = f"DANGER p.{page:03d}" if danger else f"SORTIE SUD p.{page:03d}"
        out.append(f'<text x="{x1+dx}" y="{y1+dy+20}" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="700" fill="{color}">{label}</text>')

    # Clairières.
    for c in clearings:
        cx, cy = center(c); x, y = cx-BW/2, cy-BH/2
        special = c["hub"] in (58, 78)
        fill = "#fff4c7" if c["hub"] == 58 else ("#e1f1d7" if c["hub"] == 78 else "#fffdf7")
        stroke = "#b66b22" if c["hub"] == 58 else ("#356f47" if c["hub"] == 78 else "#526454")
        out.append(f'<g filter="url(#shadow)"><rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="{5 if special else 2}"/></g>')
        marks = [name for name, hubs in MISSION.items() if c["hub"] in hubs]
        for i, name in enumerate(marks):
            out.append(f'<rect x="{x+5+i*15}" y="{y+5}" width="11" height="11" rx="3" fill="{MCOLOR[name]}"/>')
        number = "—" if c["id"] is None else str(c["id"])
        if c["hub"] == 179: number = "9 bis"
        out.append(f'<text x="{cx}" y="{y+27}" text-anchor="middle" font-family="sans-serif" font-size="21" font-weight="700" fill="#243b2f">{esc(number)}</text>')
        title = short_title(c["titre"])
        out.append(f'<text x="{cx}" y="{y+51}" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="600" fill="#31453a">{esc(title)}</text>')
        pages = "Pages " + ", ".join(f"{p:03d}" for p in c["pages"])
        for i, line in enumerate(textwrap.wrap(pages, width=27)[:2]):
            out.append(f'<text x="{cx}" y="{y+74+i*17}" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#58655d">{esc(line)}</text>')
        if c["hub"] == 45:
            out.append(f'<path d="M {cx-33} {cy+36} L {cx-33} {cy+60} M {cx+33} {cy+36} L {cx+33} {cy+60} M {cx-42} {cy+47} L {cx+42} {cy+47}" stroke="#7b4e2e" stroke-width="7"/>')
            out.append(f'<text x="{cx}" y="{cy+77}" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="700" fill="#7b4e2e">PONT UNIQUE</text>')

    ly = 1535
    out += [f'<rect x="72" y="{ly}" width="1256" height="215" rx="18" fill="#fffdf7" stroke="#bcb7a9"/>',
            f'<text x="98" y="{ly+31}" font-family="sans-serif" font-size="20" font-weight="700" fill="#243b2f">Légende</text>',
            f'<line x1="100" y1="{ly+61}" x2="170" y2="{ly+61}" stroke="#596b55" stroke-width="5"/><text x="185" y="{ly+67}" font-family="sans-serif" font-size="15">sentier réciproque</text>',
            f'<line x1="390" y1="{ly+61}" x2="460" y2="{ly+61}" stroke="#596b55" stroke-width="4" stroke-dasharray="10 6" marker-end="url(#arrow)"/><text x="475" y="{ly+67}" font-family="sans-serif" font-size="15">sens unique</text>',
            f'<circle cx="713" cy="{ly+61}" r="13" fill="#fff" stroke="#596b55"/><text x="713" y="{ly+66}" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="700">2</text><text x="735" y="{ly+67}" font-family="sans-serif" font-size="15">sentier long (2 cases)</text>',
            f'<line x1="1010" y1="{ly+61}" x2="1080" y2="{ly+61}" stroke="#8b3a3a" stroke-width="4" stroke-dasharray="10 7"/><text x="1092" y="{ly+67}" font-family="sans-serif" font-size="15">téléportation / piège</text>']
    for i, name in enumerate(("Gayolard", "Pompatarte", "Stratagus")):
        xx = 104 + i*385
        desc = {"Gayolard":"Baie d’Anthérique", "Pompatarte":"route de Courbensaule", "Stratagus":"cinq Amulettes"}[name]
        out.append(f'<rect x="{xx}" y="{ly+92}" width="16" height="16" rx="3" fill="{MCOLOR[name]}"/><text x="{xx+26}" y="{ly+106}" font-family="sans-serif" font-size="15"><tspan font-weight="700">{name}</tspan> — {desc}</text>')
    out += [f'<text x="100" y="{ly+148}" font-family="sans-serif" font-size="15" fill="#39483f">Cases encadrées : départ p.195 (clairière 1) et Courbensaule. Tiret : lieu sans numéro dans le livre.</text>',
            f'<text x="100" y="{ly+178}" font-family="sans-serif" font-size="15" fill="#39483f">La rivière traverse y=3 d’est en ouest ; la clairière 35 porte l’unique pont nord–sud.</text>',
            f'<text x="100" y="{ly+204}" font-family="sans-serif" font-size="14" fill="#6a716c">35 clairières · 39 liens internes (38 sentiers + 1 piège) · 3 sentiers longs</text>', '</svg>']
    return "\n".join(out) + "\n"


def ascii_map(clearings, edges, external):
    # Grille compacte : 6 cellules de 8 colonnes et 5 intervalles de 3 = 63.
    cols, rows = 63, 17
    canvas = [[" "] * cols for _ in range(rows)]
    px = lambda x: 3 + x*11
    py = lambda y: y*2
    by_hub = {c["hub"]: c for c in clearings}
    for e in edges:
        if e["teleport"]:
            continue
        a, b = e["a"], e["b"]
        x1, y1, x2, y2 = px(a["x"]), py(a["y"]), px(b["x"]), py(b["y"])
        if y1 == y2:
            for x in range(min(x1,x2)+4, max(x1,x2)-3): canvas[y1][x] = "-"
            if not e["reciprocal"]: canvas[y1][x2-4 if x2>x1 else x2+4] = ">" if x2>x1 else "<"
        elif x1 == x2:
            for y in range(min(y1,y2)+1, max(y1,y2)): canvas[y][x1] = "|"
            if not e["reciprocal"]: canvas[y2-1 if y2>y1 else y2+1][x1] = "v" if y2>y1 else "^"
    for c in clearings:
        label = " - " if c["id"] is None else ("9b " if c["hub"] == 179 else f"{c['id']:>2} ")
        if c["hub"] == 58: label = "*1 "
        if c["hub"] == 78: label = " C "
        token = f"[{label}]"
        x, y = px(c["x"]), py(c["y"])
        canvas[y][x-2:x+3] = list(token)
    lines = ["LE MARAIS AUX SCORPIONS - CARTE DES CLAIRIERES"[:80],
             "NORD ^   C=COURBENSAULE  *1=DEPART p.195  -=SANS NUMERO", ""]
    lines += ["".join(r).rstrip() for r in canvas]
    lines += ["", "RIVIERE CROUPIE: LIGNE y=3; PONT UNIQUE EN CLAIRIERE 35.",
              "--/| RECIPROQUE   ->/^/v SENS UNIQUE   LONG TRAIT: 2 CASES",
              "PIEGE: 15 --(FEU FOLLET, SENS UNIQUE)--> 1",
              "MISSIONS: GAYOLARD=11; POMPATARTE=C; STRATAGUS=4,27,17,8,14.", ""]
    lines.append("LIEUX (numero: titre; pages)")
    for c in sorted(clearings, key=lambda z: (z["y"], z["x"])):
        num = "-" if c["id"] is None else ("9bis" if c["hub"] == 179 else str(c["id"]))
        prefix = f"{num:>4}: {c['titre']}; pages "
        pages = ",".join(f"{p:03d}" for p in c["pages"])
        lines.extend(textwrap.wrap(prefix + pages, width=80, subsequent_indent="      "))
    assert all(len(line) <= 80 for line in lines)
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("json", type=Path, help="chemin de carte.json")
    args = ap.parse_args()
    data, clearings, edges, external, anomalies = load_and_analyse(args.json)
    Path("carte_marais.svg").write_text(svg(data, clearings, edges, external), encoding="utf-8")
    Path("carte_marais.txt").write_text(ascii_map(clearings, edges, external), encoding="ascii", errors="replace")
    reciprocal = sum(e["reciprocal"] for e in edges)
    oneway = len(edges) - reciprocal
    print(f"Clairières placées : {len(clearings)}")
    print(f"Liens tracés : {len(edges)} ({reciprocal} réciproques, {oneway} à sens unique; "
          f"{sum(e['teleport'] for e in edges)} piège hors grille)")
    print(f"Sorties externes tracées : {len(external)}")
    print(f"Incohérences rencontrées : {len(anomalies)}")
    for item in anomalies:
        print(f"- {item}")


if __name__ == "__main__":
    main()
