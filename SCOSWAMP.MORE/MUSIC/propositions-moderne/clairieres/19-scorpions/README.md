# Clairière 19 — La clairière des scorpions

**`SCORPIONS.MB.BIN` — 2 018 octets, 31,6 s, boucle.**

## La clairière

| | |
| --- | --- |
| `hub` | **319** |
| Pages | 118 (l'embuscade), 303 (le retour), 319 (choisir une direction) |
| Case | (3,4) |
| Zone de référence | `danger` (`DANGER.MB`) |
| Sorties | N → 138 (le pont), E → 047, O → 066 |
| Contenu | nuée de petits SCORPIONS ; `CL 070 182` — jamais de choix à prendre |

« Votre Anneau de Cuivre vous picote au doigt. En baissant les yeux, vous voyez
des dizaines de petits scorpions accourir vers vous. Tentez votre Chance. » La
page 319 s'appelle « Vous vous hâtez de choisir une direction ».

## La pièce

| | |
| --- | --- |
| Titre | **La Nuée** |
| Source | composition originale, `scorpions.py` |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | ça grouille et ça court — la plus rapide et la plus courte des douze |
| Mode | **ré phrygien** (ré **mi♭** fa sol la si♭ do) |
| Tempo | **184** à la noire (180 auparavant) — **le plus rapide des trente-cinq** |
| Forme | intro (4) — A (8) — B (8) l'assaut — A' (4) |
| Durée | 24 mesures à 4/4 = **31,6 s** |
| Taille | **2 018 octets** (tampon de zone : 2 304) |
| Notes | 404 de hauteur + **108 coups de batterie**, **0 abandonnée** |

**Ce qu'elle garde de la zone `danger` :** le mode **phrygien**, donc le
demi-ton posé juste au-dessus de la tonique — mi♭ contre ré — et le **bourdon
de tonique** immobile. Le frottement est le procédé de la zone, et il est ici la
piqûre de l'Anneau.

**Ce qui lui appartient :** la vitesse, et le **grouillement** — les doubles
croches de la mélodie, les seules du dossier, et la basse en noires dès la
première mesure.

## Ce que la révision a changé

- **un crochet**, et c'est le grouillement lui-même : quatre doubles croches qui
  montent l'accord d'un trait, une noire au sommet, une blanche qui retombe —
  puis la même chose **un demi-ton plus haut**, sur le mi♭ phrygien. Mesure 5,
  redit mesure 9, repris mesures 21-22. La paire ré / mi♭ est ce qu'on emporte
  de cette clairière ;
- **une réponse** : mesures 8, 11 et 17, le chant tient et l'arpège — la voix 3,
  à **droite** — répond la même montée, plus bas. Une bête appelle à gauche, une
  autre répond à droite : c'est une nuée, pas un solo ;
- **un rythme harmonique varié** : neuf mesures changent d'accord au milieu, ce
  qui donne deux pas de basse au lieu de quatre, et les mesures 17-18 n'en
  changent plus du tout ;
- **la surprise, et c'est *le silence*** : mesure 17, tout s'arrête. La batterie
  se tait, la basse tient une **ronde**, le contre-chant une ronde, le chant un
  mi♭ tenu, et l'arpège seul fait battre mi♭ contre ré. C'est « Tentez votre
  Chance » : une seconde où rien ne bouge avant que tout reparte. Roulement de
  toms mesure 18, et la nuée est de nouveau sur vous ;
- **une cadence affirmée** : mesure 20, un **la majeur** avec son do♯ — la
  sensible, interdite au phrygien, et donc la seule chose qui puisse conclure
  ici ;
- **un arc de densité** : intro à deux sons par demi-mesure, la grosse caisse
  seule mesure 3, le galop en A, doublé en B, le silence, puis A' plein ;
- **une fin qui prépare la boucle** : la dernière mesure lâche la nuée, ne garde
  que le frottement mi♭ - ré, et retombe sur le **la** par lequel la pièce
  recommence.

Le tempo passe de 180 à **184** : on n'a pas le choix, la page ne le laisse pas.

## La batterie

Un **galop**, pas une marche : grosse caisse sur le temps **et sur la croche qui
suit** (`K.HKS.H.`), caisse claire au troisième, charleston entre les deux ; en
B la caisse claire revient aussi sur la dernière croche (`K.HKS.HS`). Puis
**rien** sur la mesure du gel, un roulement de quatre toms, et le galop plein.

108 coups, 324 octets — 14 % du temps sonnant, la batterie la plus présente des
douze après le pique-nique. Elle prend la **voix 5, à droite** : cinq parties de
hauteur, et c'est la voix d'accords tenus qui a cédé la place — le bourdon de
tonique fait le caractère de la zone `danger`.

## Les six voix, mesurées

`python3 ../../verifier.py clairieres/19-scorpions/scorpions.mid --bpm 184`

| voix | côté | rôle | registre | notes | occupation |
| ---: | :---: | --- | --- | ---: | ---: |
| 0 | **gauche** | mélodie, les doubles croches du grouillement | F4..G6 | 95 | 94 % |
| 1 | gauche | médiane : le contre-chant, et l'arpège quand il passe sous lui | D3..A4 | 97 | 94 % |
| 2 | **gauche** | bourdon de ré (la tonique) | D2 | 6 | 100 % |
| 3 | **droite** | arpège de la nuée, et les trois réponses | G3..D♯5 | 114 | 93 % |
| 4 | droite | basse, quatre noires | G2..A♯3 | 92 | 94 % |
| 5 | **droite** | **batterie** — 41 grosse caisse, 36 charleston, 26 caisse claire, 4 toms, 1 cymbale | bruit | 108 | 14 % |

`OK — 6 voix employées, stéréo 59/41, aucune note abandonnée.`

## Refabriquer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/19-scorpions
python3 scorpions.py
python3 ../../../midi_to_mb.py scorpions.mid SCORPIONS.MB.BIN \
    --bpm 184 --max 2304 --wav SCORPIONS.wav
```
