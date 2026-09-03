# Clairières 25 à 35 — une musique par clairière

Onze pièces originales, **une par clairière**, écrites avec `../compose.py` et
converties par `../../midi_to_mb.py`. Chacune est une **variation dans la
couleur de sa zone** — même famille de mode, même procédé identifiable que le
thème de zone — avec son propre thème et son propre caractère, tirés des pages
de la clairière.

Tout tient dans le **tampon de zone : 2 304 octets**. La plus grosse est
`RONDPOINT.MB.BIN` (2 153 o, 151 octets de marge) ; la plus légère est
`BETE.MB.BIN` (1 176 o).

**Aucune des onze n'abandonne une seule note à la réduction six voix** (`0
abandonnées` à la conversion, polyphonie maximale = 6 exactement).

## Le tableau

| # | Clairière (`hub`) | Fichier disque | Pièce | Mode | bpm | Durée | Octets |
| ---: | --- | --- | --- | --- | ---: | ---: | ---: |
| 25 | Herbe à Pinces (187) | `PINCES.MB` | **L'Herbe qui Serre** | mi phrygien | **176** | 44,1 s | 2 038 |
| 26 | Orques des Marais (309) | `ORQUES.MB` | **Trois Arcs dans la Brume** | ré phrygien | 158 | 43,0 s | 2 017 |
| 27 | Cul-de-sac de la Bête (125) | `BETE.MB` | **Le Rocher qui Respire** | sol phrygien | 143 | 45,8 s | 1 176 |
| 28 | Arbres-Épées (022) | `ARBRESEPEES.MB` | **Les Bras qui Repoussent** | fa phrygien | 166 | 40,9 s | 1 987 |
| 29 | Tente aux araignées (165) | `ARAIGNEES.MB` | **Le Fil d'Argent** | do♯ phrygien | 150 | 45,3 s | 1 885 |
| 30 | Clairière des grenouilles (230) | `GRENOUILLES.MB` | **Le Bal des Mares** | sol éolien | 166 | 40,9 s | 2 029 |
| 31 | La rivière profonde (044) | `PROFONDE.MB` | **L'Eau Noire** | sol dorien | 136 | 49,9 s | 1 873 |
| 32 | Maître des Loups (314) | `MAITRELOUPS.MB` | **Le Cor du Maître** | mi éolien | 143 | 47,4 s | 1 978 |
| **33** | **Le large rond-point, départ (058)** | `RONDPOINT.MB` | **Le Cœur du Marais** | ré éolien | 158 | 49,1 s | **2 153** |
| 34 | Pierres et tronc creux (390) | `TRONC.MB` | **Pierres Plates** | do éolien | 150 | 45,3 s | 1 888 |
| 35 | Bête du bassin (082) | `BASSIN.MB` | **Ce qui Monte du Bassin** | fa éolien | 143 | 47,4 s | 1 969 |

**Total : 20 993 octets** pour les onze, sur ~28 Mo libres. Ce qui compte n'est
pas la somme mais la plus grosse : 2 153 o < 2 304 o.

## Zone de référence, procédé gardé, procédé propre

| # | Zone | Ce qui vient de la zone | Ce qui n'est qu'à cette clairière |
| ---: | --- | --- | --- |
| 25 | `danger` | demi-ton phrygien fa–mi, bourdon fixe | l'arpège troué : trois croches, un silence — la pince qui claque |
| 26 | `danger` | demi-ton phrygien mi♭–ré, bourdon fixe | rythme pointé partout, bourdon-tambour toutes les 2 mesures, fanfare énoncée deux fois un demi-ton plus haut |
| 27 | `danger` | demi-ton phrygien la♭–sol, bourdon fixe | **6/4** (la seule des 35), arpège boiteux 1+½+½+1+1½+1½, bourdon refrappé à chaque mesure |
| 28 | `danger` | demi-ton phrygien sol♭–fa, bourdon fixe | **canon** : la cellule fa–sol♭–fa repousse au contre-chant (mes. 6, 18, 22) |
| 29 | `danger` | demi-ton phrygien ré–do♯, crescendo par la densité | arpège de **3** sons dans **4** temps (la toile), l'incendie à la mesure 17 |
| 30 | `sud` | marche i-VI-III-VII sur bourdon immobile | la mélodie **saute** l'octave en croches, la basse alterne fondamentale et quinte grave |
| 31 | `riviere` | croches ininterrompues, bourdon sur la **quinte** | le **remous** : l'arpège revient sur lui-même (0-2-1-2-0-1-2-1) |
| 32 | `sud` | marche i-VI-III-VII sur bourdon immobile | le **cor** : appels en quintes et quartes à vide, arpège sans aucune tierce |
| 33 | `sud` | marche i-VI-III-VII, **même tonique que la zone** | le thème du Marais : montée ré-mi-fa énoncée trois fois (les trois sentiers), plus une coda |
| 34 | `sud` | marche i-VI-III-VII sur bourdon immobile | arpège de **quintes à vide** (liste `CREUX`), le coup de poing sur le tronc en notes répétées |
| 35 | `sud` | marche i-VI-III-VII sur bourdon immobile | la **basse ascendante** (elle ne redescend qu'à la barre de mesure), le Bijou Violet sur le VI majeur |

Les cinq clairières `danger` sont toutes phrygiennes, sur cinq toniques
distinctes (mi, ré, sol, fa, do♯) ; les cinq clairières `sud` sont toutes
éoliennes (sol, mi, ré, do, fa) ; la clairière `riviere` est dorienne, comme le
pont. Aucune ne reprend la tonique de son thème de zone, **sauf le rond-point**,
qui prend exactement celle de `sud` parce qu'il est le cœur du lieu.

## La stéréo

Les six voix sortent partout dans la même disposition que les dix thèmes de
zone (`../INDEX.md` § 3), vérifiée pièce par pièce avec `../verifier.py` :

| voix | côté | rôle |
| ---: | :---: | --- |
| 0 | **gauche** | la mélodie, seule |
| 1 | gauche | une médiane (contre-chant) |
| 2 | **gauche** | la basse, seule |
| 3 | **droite** | l'arpège ou l'ostinato, l'essentiel du mouvement |
| 4 | droite | une médiane (accords tenus) |
| 5 | **droite** | le bourdon, seul, immobile |

Vérification d'une pièce :

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres
python3 ../verifier.py 33-rondpoint/rondpoint.mid --bpm 158
```

## Refabriquer les onze

```sh
cd /Users/gistair/src/pom2adventure/SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres
M=../../../midi_to_mb.py
(cd 25-pinces       && python3 pinces.py       && python3 $M pinces.mid       PINCES.MB.BIN       --bpm 176 --max 2304 --wav PINCES.wav)
(cd 26-orques       && python3 orques.py       && python3 $M orques.mid       ORQUES.MB.BIN       --bpm 158 --max 2304 --wav ORQUES.wav)
(cd 27-bete         && python3 bete.py         && python3 $M bete.mid         BETE.MB.BIN         --bpm 143 --max 2304 --wav BETE.wav)
(cd 28-arbresepees  && python3 arbresepees.py  && python3 $M arbresepees.mid  ARBRESEPEES.MB.BIN  --bpm 166 --max 2304 --wav ARBRESEPEES.wav)
(cd 29-araignees    && python3 araignees.py    && python3 $M araignees.mid    ARAIGNEES.MB.BIN    --bpm 150 --max 2304 --wav ARAIGNEES.wav)
(cd 30-grenouilles  && python3 grenouilles.py  && python3 $M grenouilles.mid  GRENOUILLES.MB.BIN  --bpm 166 --max 2304 --wav GRENOUILLES.wav)
(cd 31-profonde     && python3 profonde.py     && python3 $M profonde.mid     PROFONDE.MB.BIN     --bpm 136 --max 2304 --wav PROFONDE.wav)
(cd 32-maitreloups  && python3 maitreloups.py  && python3 $M maitreloups.mid  MAITRELOUPS.MB.BIN  --bpm 143 --max 2304 --wav MAITRELOUPS.wav)
(cd 33-rondpoint    && python3 rondpoint.py    && python3 $M rondpoint.mid    RONDPOINT.MB.BIN    --bpm 158 --max 2304 --wav RONDPOINT.wav)
(cd 34-tronc        && python3 tronc.py        && python3 $M tronc.mid        TRONC.MB.BIN        --bpm 150 --max 2304 --wav TRONC.wav)
(cd 35-bassin       && python3 bassin.py       && python3 $M bassin.mid       BASSIN.MB.BIN       --bpm 143 --max 2304 --wav BASSIN.wav)
```

Le bloc se recolle tel quel dans un shell. `--vol` reste au défaut
`13,11,11,12,11,11` partout. Le `.wav` de chaque dossier **est** ce que la
Mockingboard jouera — six ondes carrées, deux puces, la même réduction, le même
tempo, la même stéréo. Il n'est pas suivi par git (`.gitignore:76`).

Rien n'est copié dans `SCOSWAMP/MUSIC/` : ce dossier reste un atelier tant que
le propriétaire n'a pas écouté et tranché.
