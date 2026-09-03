#!/usr/bin/env python3
"""Atelier de composition six voix pour la Mockingboard — style fantasy moderne.

Ce module ne joue rien et n'ecrit pas de flux MB1 : il ecrit un **MIDI** que
`../midi_to_mb.py` reduit ensuite a six voix carrees et rend en WAV stereo.
C'est une generalisation de `../accueil.py`, qui melait la composition, le MIDI,
le MB1 et le rendu dans un seul fichier pour trois voix.

    from compose import *
    p = Piece("D", "dorian", bpm=136, beats_per_bar=4)
    p.add("melodie", line("D5:1 F5:.5 G5:.5 A5:2"))
    ...
    p.write(Path(__file__).with_suffix(".mid"))

## Les six voix et la stereo

Deux AY-3-8910 : voix 0-2 a **gauche**, voix 3-5 a **droite**. Le lecteur ne
choisit pas la voix — `midi_to_mb.reduce_voices()` le fait, et il le fait par
**hauteur** : a chaque frontiere, les notes qui commencent sont triees du grave
a l'aigu (la plus haute servie d'abord) et prennent les voix libres dans
l'ordre `0, 3, 1, 4, 2, 5`, c'est-a-dire en alternant les deux puces. Quand les
six registres restent bien separes et qu'ils sonnent tous en meme temps, la
repartition est donc **entrelacee** :

    dessus -> 0 (G)   2e -> 3 (D)   3e -> 1 (G)   4e -> 4 (D)   5e -> 2 (G)   basse -> 5 (D)

Composer pour cette machine, c'est donc **ecrire six registres distincts et les
garder distincts** : melodie aigue, contre-chant, deux voix d'accords, basse,
pedale. Si deux voix se croisent, elles echangent leurs cotes en cours de route.
`stats()` mesure ce qui se passe reellement ; `verifier.py` le confirme apres
conversion.

## Le budget

Le tampon du lecteur fait 2 560 octets et la consigne est de rester sous 2 400.
Une note coute environ 3 a 4 octets (NOTE + OFF + les delais). Il faut donc de
l'ordre de **600 notes au total** pour une boucle de 60 s : une seule voix en
croches continues en mange la moitie. D'ou l'ecriture du style : bourdons tenus,
quintes ouvertes en rondes, une seule voix rapide a la fois.

## Ce qu'il faut eviter

- plus de six notes simultanees : la reduction abandonne l'interieur (`stats()`
  le signale) ;
- des hauteurs hors de C2..B6 (MIDI 36..95) : `fold()` les ramene a l'octave et
  la basse remonte au milieu de la texture ;
- deux notes de la meme voix qui se touchent : `Piece.write()` raccourcit tout
  d'un souffle (`GATE`) pour que l'onde carree articule.
"""
from pathlib import Path
import struct

TICKS = 480                       # ticks MIDI par noire
GATE = 0.06                       # souffle retire a chaque note, en temps
LO, HI = 36, 95                   # C2..B6, la table de `midi_to_mb.py`

NOTE_OF = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

MODES = {
    "ionien":     (0, 2, 4, 5, 7, 9, 11),
    "dorien":     (0, 2, 3, 5, 7, 9, 10),
    "phrygien":   (0, 1, 3, 5, 7, 8, 10),
    "lydien":     (0, 2, 4, 6, 7, 9, 11),
    "mixolydien": (0, 2, 4, 5, 7, 9, 10),
    "eolien":     (0, 2, 3, 5, 7, 8, 10),
    "mineur_h":   (0, 2, 3, 5, 7, 8, 11),   # mineur harmonique
}

QUALITIES = {
    "":     (0, 4, 7),         "m":    (0, 3, 7),
    "5":    (0, 7, 12),        "sus2": (0, 2, 7),      "sus4": (0, 5, 7),
    "dim":  (0, 3, 6),         "aug":  (0, 4, 8),
    "7":    (0, 4, 7, 10),     "m7":   (0, 3, 7, 10),  "maj7": (0, 4, 7, 11),
    "6":    (0, 4, 7, 9),      "m6":   (0, 3, 7, 9),
    "add9": (0, 4, 7, 14),     "madd9": (0, 3, 7, 14), "m9": (0, 3, 7, 10, 14),
    "7sus4": (0, 5, 7, 10),
}


# ── Hauteurs ──────────────────────────────────────────────────────────────
def midi(name):
    """\"D4\", \"F#3\", \"Bb5\" -> numero MIDI. C4 = 60."""
    letter, rest = name[0].upper(), name[1:]
    acc = 0
    while rest and rest[0] in "#b":
        acc += 1 if rest[0] == "#" else -1
        rest = rest[1:]
    return 12 * (int(rest) + 1) + NOTE_OF[letter] + acc


def pc(name):
    """Classe de hauteur d'un nom sans octave : \"Bb\" -> 10."""
    acc = sum(1 if c == "#" else -1 for c in name[1:] if c in "#b")
    return (NOTE_OF[name[0].upper()] + acc) % 12


def degree(root, mode, d, octave=4):
    """Degre `d` (1 = tonique) du mode, dans l'octave donnee ; d peut deborder.

    degree("D", "dorien", 1, 5) == midi("D5") ; degree(..., 8, 5) est l'octave.
    """
    steps = MODES[mode]
    i, up = (d - 1) % 7, (d - 1) // 7
    return 12 * (octave + 1) + pc(root) + steps[i] + 12 * up


def chord(name, octave=3):
    """\"Dm\", \"Bb\", \"A7sus4\", \"E5\" -> liste de hauteurs MIDI, fondamentale
    dans l'octave donnee. Un chiffre colle au nom fixe l'octave : \"Dm4\"."""
    i = 1
    while i < len(name) and name[i] in "#b":
        i += 1
    root, qual = name[:i], name[i:]
    if qual and qual[-1].isdigit() and (qual[:-1] in QUALITIES):
        octave, qual = int(qual[-1]), qual[:-1]
    if qual not in QUALITIES:
        raise ValueError(f"accord inconnu : {name!r} (qualite {qual!r})")
    r = 12 * (octave + 1) + pc(root)
    return [r + s for s in QUALITIES[qual]]


def fit(pitch, lo, hi):
    """Replie une hauteur par octaves dans la fenetre [lo, hi]."""
    while pitch < lo:
        pitch += 12
    while pitch > hi:
        pitch -= 12
    return pitch


def voicing(name, lo):
    """L'accord en position de fondamentale, la fondamentale posee dans [lo, lo+11].

    Rend `[fondamentale, tierce, quinte, ...]` en ordre croissant serre. C'est
    la cle de la stereo : chaque partie recoit **sa** fenetre de registre et n'en
    sort pas, donc l'ordre des six parties par hauteur ne change pas, donc
    `midi_to_mb.reduce_voices()` leur rend toujours la meme voix — le meme cote.
    """
    tones = chord(name, 3)
    root = fit(tones[0], lo, lo + 11)
    out = [root]
    for t in tones[1:]:
        n = root + (t - tones[0]) % 12
        while n <= out[-1]:
            n += 12
        out.append(n)
    return out


def pick(v, i):
    """`v[i]` avec debordement par octaves : -1 = le dernier son une octave plus bas."""
    return v[i % len(v)] + 12 * (i // len(v))


def guard(part, name="?"):
    """Verifie que tout tient dans C2..B6, sinon lever plutot que replier."""
    for n, t, d in part:
        if n is not None and not (LO <= n <= HI):
            raise ValueError(f"voix {name} : hauteur {n} hors de C2..B6 a t={t}")
    return part


# ── Ecriture en notation texte ────────────────────────────────────────────
def line(spec, t0=0.0, transpose=0):
    """\"D5:1 F5:.5 -:.5 A5:2\" -> [(hauteur, debut, duree)], silences ignores.

    Les durees sont en temps (1 = une noire). `-` est un silence : il avance le
    temps sans rien produire. C'est la notation de `../accueil.py`.
    """
    out, t = [], float(t0)
    for tok in spec.split():
        n, _, d = tok.partition(":")
        d = float(d)
        if n != "-":
            out.append((midi(n) + transpose, t, d))
        t += d
    return out


def lines(specs, t0=0.0, transpose=0, bar=4.0):
    """Une liste de mesures, chacune posee sur `bar` temps quoi qu'elle contienne."""
    out = []
    for i, s in enumerate(specs):
        out += line(s, t0 + i * bar, transpose)
    return out


def seq(items, t0=0.0):
    """[(hauteur|None, duree), ...] -> [(hauteur, debut, duree)]."""
    out, t = [], float(t0)
    for n, d in items:
        if n is not None:
            out.append((n, t, float(d)))
        t += float(d)
    return out


# ── Les figures du style ──────────────────────────────────────────────────
def ostinato(pitches, durs, t0, length, gap=0.0):
    """Un motif tourne en boucle du temps `t0` jusqu'a `t0 + length`.

    `pitches` est la cellule (hauteurs MIDI, `None` pour un trou), `durs` la
    duree de chaque note — un nombre unique s'applique a toutes. `gap` raccourcit
    chaque note sans decaler la grille (staccato).
    """
    if not isinstance(durs, (list, tuple)):
        durs = [durs] * len(pitches)
    out, t, i = [], float(t0), 0
    end = t0 + length
    while t < end - 1e-6:
        n, d = pitches[i % len(pitches)], durs[i % len(durs)]
        if n is not None:
            out.append((n, t, min(d - gap, end - t)))
        t += d
        i += 1
    return [(n, s, d) for n, s, d in out if d > 0.05]


def pedal(pitch, t0, length, retrig=None):
    """Un bourdon. Sans `retrig`, une seule note tenue — une note, trois octets.

    Avec `retrig`, la note est refrappee tous les `retrig` temps : le bourdon
    respire au lieu de se figer, au prix d'une note par frappe.
    """
    if retrig is None:
        return [(pitch, float(t0), float(length))]
    return ostinato([pitch], retrig, t0, length)


def bed(chords, t0, per_chord, lo, which=1):
    """Le lit d'accords : **une** note tenue par accord — trois octets la mesure.

    `which` choisit le son (0 = fondamentale, 1 = tierce, 2 = quinte, -1 = la
    quinte une octave plus bas). Deux appels avec deux `lo` differents donnent
    les deux voix d'accords du plan a six voix, sans jamais se croiser.
    """
    return [(pick(voicing(c, lo), which), t0 + i * per_chord, per_chord)
            for i, c in enumerate(chords)]


def progression(chords, t0, per_chord, pattern, lo):
    """Marche harmonique : `pattern` est joue sur chaque accord de la suite.

    Chaque element de `pattern` est `(indice, duree)` ; l'indice designe un son
    de l'accord pose a partir de `lo` (0 = fondamentale), et deborde par octaves.
    `None` a la place de l'indice fait un silence.
    """
    out = []
    for i, c in enumerate(chords):
        v = voicing(c, lo)
        t = t0 + i * per_chord
        for k, d in pattern:
            if k is not None:
                out.append((pick(v, k), t, d))
            t += d
    return out


def arpeggio(chords, t0, per_chord, step, shape, lo):
    """Arpege continu : `shape` parcourt l'accord pose a partir de `lo`."""
    out = []
    for i, c in enumerate(chords):
        v = voicing(c, lo)
        for k in range(int(round(per_chord / step))):
            j = shape[k % len(shape)]
            if j is not None:
                out.append((pick(v, j), t0 + i * per_chord + k * step, step))
    return out


def double(part, semitones=-12, keep=None):
    """Doublure : la meme partie transposee. `keep` filtre (ex. `lambda n,t,d: d>=1`)."""
    return [(n + semitones, t, d) for n, t, d in part
            if keep is None or keep(n, t, d)]


def swell(part, t0, length, low, high, step=1.0):
    """Crescendo par la densite : inutile ici (pas de volume par note), garde
    la trace de l'intention en ecrivant la partie plus serree vers la fin."""
    raise NotImplementedError("le lecteur n'a pas de volume par note ; "
                              "faire le crescendo par le registre et la densite")


def shift(part, dt):
    return [(n, t + dt, d) for n, t, d in part]


def repeat(part, times, length):
    out = []
    for k in range(times):
        out += shift(part, k * length)
    return out


# ── La piece ──────────────────────────────────────────────────────────────
class Piece:
    """Six parties nommees, ecrites dans un MIDI a six pistes."""

    def __init__(self, root, mode, bpm, beats_per_bar=4, title=""):
        self.root, self.mode, self.bpm = root, mode, beats_per_bar and bpm
        self.bar = beats_per_bar
        self.title = title
        self.parts = []           # [(nom, [(hauteur, debut, duree)])]

    def deg(self, d, octave=4):
        return degree(self.root, self.mode, d, octave)

    def add(self, name, part):
        self.parts.append((name, guard(sorted(part, key=lambda e: e[1]), name)))
        return self

    @property
    def length(self):
        return max((t + d for _, p in self.parts for _, t, d in p), default=0.0)

    # -- diagnostic ------------------------------------------------------
    def holes(self):
        """Les temps forts ou une partie ne sonne pas — la faute qui melange la stereo.

        `reduce_voices()` remet tout d'aplomb chaque fois que les six parties
        attaquent ou tiennent ensemble : les notes tenues gardent leur voix, les
        notes neuves remplissent les voix libres de l'aigu au grave dans l'ordre
        `0, 3, 1, 4, 2, 5`. Si une partie se tait sur un temps fort, les cinq
        autres se decalent d'un cran et changent de cote. On ecrit donc des
        parties qui **sonnent sur chaque premier temps**, quitte a tenir.
        """
        bad = []
        for name, part in self.parts:
            miss = []
            b = 0.0
            while b < self.length - 1e-6:
                if not any(t <= b + 1e-6 < t + d for _, t, d in part):
                    miss.append(int(b // self.bar) + 1)
                b += self.bar
            if miss:
                bad.append((name, miss))
        return bad

    def stats(self):
        events = []
        for i, (_, p) in enumerate(self.parts):
            for n, t, d in p:
                events.append((t, 1, i, n)); events.append((t + d - 1e-9, -1, i, n))
        events.sort()
        cur, peak, over = 0, 0, 0.0
        last, prev = None, 0
        for t, k, _, _ in events:
            if last is not None and cur > 6:
                over += t - last
            cur += k; peak = max(peak, cur); last = t
        notes = sum(len(p) for _, p in self.parts)
        return {"notes": notes, "peak": peak, "over6_beats": round(over, 2),
                "beats": round(self.length, 2),
                "seconds": round(self.length * 60.0 / self.bpm, 1),
                "ranges": [(n, min((x for x, _, _ in p), default=0),
                            max((x for x, _, _ in p), default=0))
                           for n, p in self.parts]}

    # -- MIDI ------------------------------------------------------------
    @staticmethod
    def _vlq(n):
        out = [n & 0x7F]; n >>= 7
        while n:
            out.append(0x80 | (n & 0x7F)); n >>= 7
        return bytes(reversed(out))

    @classmethod
    def _track(cls, events, extra=b""):
        events.sort(key=lambda e: (e[0], e[1]))
        data = bytearray(extra); last = 0
        for tick, _, msg in events:
            data += cls._vlq(tick - last) + msg; last = tick
        data += cls._vlq(0) + b"\xFF\x2F\x00"
        return b"MTrk" + struct.pack(">I", len(data)) + bytes(data)

    def write(self, path, gate=GATE):
        tempo = b"\x00\xFF\x51\x03" + struct.pack(">I", 60_000_000 // int(self.bpm))[1:]
        num = self.bar
        chunks = [self._track([], tempo + bytes([0, 0xFF, 0x58, 0x04, num, 2, 0x18, 8]))]
        for ch, (_, part) in enumerate(self.parts[:16]):
            ev = [(0, 0, bytes([0xC0 | (ch & 15), 80]))]
            for n, t, d in part:
                d = max(d - gate, min(d * 0.6, 0.12))
                a, b = int(round(t * TICKS)), int(round((t + d) * TICKS))
                if b <= a:
                    b = a + 1
                ev.append((a, 1, bytes([0x90 | (ch & 15), n, 100])))
                ev.append((b, 0, bytes([0x80 | (ch & 15), n, 0])))
            chunks.append(self._track(ev))
        Path(path).write_bytes(b"MThd" + struct.pack(">IHHH", 6, 1, len(chunks), TICKS)
                               + b"".join(chunks))
        s = self.stats()
        print(f"{Path(path).name}: {s['notes']} notes, {s['beats']:g} temps "
              f"= {s['seconds']}s a {self.bpm:g} bpm, "
              f"polyphonie max {s['peak']}"
              + (f" (!! {s['over6_beats']} temps au-dessus de 6)" if s['peak'] > 6 else ""))
        for name, miss in self.holes():
            print(f"   !! {name} se tait au temps fort des mesures "
                  f"{', '.join(map(str, miss[:12]))}"
                  + (" ..." if len(miss) > 12 else ""))
        return s


__all__ = [n for n in dir() if not n.startswith("_")]
