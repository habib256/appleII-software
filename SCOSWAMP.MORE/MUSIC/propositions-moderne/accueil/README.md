# Zone `accueil` — l'écran de titre

**`ACCUEIL.MB.BIN` — 2 070 octets, 49,9 s, boucle.**

## Ce que la zone couvre

| Page | Titre | Rôle |
| --- | --- | --- |
| 000 | écran d'accueil | la seule page où le moteur entre sans qu'un choix y mène |

Aucune clairière. La page 000 est le portage, pas le livre
(`SCOSWAMP/DOCS/CARTOGRAPHIE.md` § 6.2). Elle remplace `COMEAGAIN.MB`,
aujourd'hui sur le disque.

## La pièce

| | |
| --- | --- |
| Titre | **L'Appel du Marais** |
| Source | composition originale, `accueil.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt — aucune œuvre tierce |
| Caractère | ouverture de film : un coup de gong à six voix, un bourdon qui s'installe, un appel de cor qui monte à la quinte et revient une octave plus haut |
| Mode | **ré dorien** (ré mi fa sol la **si** do) — le si bécarre est la lueur qui manque à tout le reste du jeu |
| Tempo | **136** à la noire |
| Forme | intro (4) — A « le seuil » (8) — B « l'appel » (8) — A' à l'octave (8) |
| Durée | 28 mesures à 4/4 = **49,9 s** |
| Taille | **2 070 octets** |
| Notes | 539 écrites, 0 abandonnée par la réduction |

Harmonie : Dm-C-Dm-Am puis F-C-G-Dm en A ; B ouvre sur F-G-C-Am avant de
retomber. Le sol majeur du mode dorien (mesures 19 et 26) est la cadence
caractéristique, celle qui empêche la pièce de sonner mineur d'école.

## Les six voix

Mesuré par `../verifier.py accueil.mid --bpm 136` — c'est l'attribution réelle
de `midi_to_mb.py`, pas une intention.

| voix | côté | rôle | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | mélodie | D5..A6 | 90 |
| 1 | **gauche** | médiane (contre-chant / accords) | A3..A4 | 70 |
| 2 | **gauche** | basse, fondamentale et quinte grave | E2..G3 | 134 |
| 3 | **droite** | médiane (arpège) | A3..D5 | 111 |
| 4 | **droite** | médiane (contre-chant / accords) | A3..A4 | 120 |
| 5 | **droite** | bourdon de ré, refrappé toutes les deux mesures | D2 | 14 |

Image stéréo : **la mélodie et la basse à gauche, l'arpège et le bourdon à
droite**, les voix d'accompagnement médianes réparties des deux côtés. Voir
`../INDEX.md` § 3 pour pourquoi l'attribution se fait ainsi et pourquoi elle
tient.

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/accueil
python3 accueil.py
python3 ../../midi_to_mb.py accueil.mid ACCUEIL.MB.BIN \
    --bpm 136 --max 2304 --wav ACCUEIL.wav
python3 ../verifier.py accueil.mid --bpm 136
```

Le `.wav` n'est pas suivi par git (`.gitignore:76`) : c'est un rendu, et il est
*exactement* ce que la carte jouera — six ondes carrées, deux puces, rien d'autre.
