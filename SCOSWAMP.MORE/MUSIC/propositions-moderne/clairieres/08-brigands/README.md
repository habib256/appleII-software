# Clairière 8 — Clairière aux brigands (`hub` 019, case 0,2)

**`BRIGANDS.MB.BIN` — 2 258 octets, 37,3 s, boucle.**

## Les pages

| Page | Titre | Ce qui s'y passe |
| ---: | --- | --- |
| 065 | Clairière aux brigands | le grand champignon, les voix, cinq hommes épiés derrière un arbre |
| 343 | Retour aux Brigands | amis, ou fuis, trompés, tués |
| 019 | Deux sentiers | le large chemin du nord, l'étroit sentier de l'est |

## La pièce

| | |
| --- | --- |
| Titre | **Cinq Voix derrière l'Arbre** |
| Source | composition originale, `brigands.py` (ce dossier) |
| Licence | GPL v3, comme le reste du dépôt |
| Caractère | effronté, pas méchant : « l'Anneau de Cuivre reste froid, ils ne paraissent pas malfaisants. Il serait cependant stupide de prendre des risques inutiles » |
| Mode | **ré mineur éolien** (ré mi fa sol la si♭ do) — **majeur à la fin** |
| Tempo | **180** à la noire (auparavant 176) |
| Forme | intro (4) — A (8) — B (8) — A' (8) |
| Durée | 28 mesures à 4/4 = **37,3 s** — la plus courte des douze |
| Taille | **2 258 octets** (marge 46 sur le tampon de zone) |
| Notes | 420 de hauteur + **114 coups de batterie**, **0 abandonnée** |
| Voix | **cinq parties de hauteur** + la batterie sur la voix 5 |

## Ce que la révision a changé

- **un crochet** de deux mesures, `la ré' do' la fa / sol fa mi ré` : une
  descente effrontée, celle de gens qui ne sont pas méchants mais qui prennent
  la bourse. Énoncé trois fois ;
- **une réponse** aux mesures 8, 12 et 28 : le chant tient et les cinq voix —
  voix 3, à droite — répondent. On les entend de l'autre côté ;
- **la surprise, et c'est la meilleure des douze** : la pièce **finit en ré
  majeur**. Le fa dièse de la dernière mesure n'existe nulle part ailleurs dans
  le morceau ; il tombe après un accord de **la majeur** à la mesure 20, qui
  l'annonce. Les brigands vous saluent. Et comme la boucle repart sur le ré
  mineur de l'intro, la tierce se recouvre à chaque tour — le fondu de fin
  passe exactement dessus ;
- **un silence** : mesure 20, un temps et demi où plus personne ne parle, la
  caisse claire seule. C'est là qu'on décide de les saluer ou de les charger ;
- **le rythme harmonique varie** : grille à la demi-mesure ; la basse pose
  jusqu'au salut, puis balance croche pointée - croche pour le A' ;
- **le tempo monte de 176 à 180**.

## La batterie

**Un tambourin de foire**, et la plus fournie des douze : cent quatorze coups,
12 % d'occupation. Contretemps au charleston, caisse claire aux deuxième et
quatrième temps, grosse caisse au premier, un charleston ouvert par mesure au
A'. Rien derrière l'arbre : l'intro est muette, et c'est ce qui fait entrer le
A. Le bourdon de ré a cédé la place.

## Ce qui la relie à `nord`, et ce qui l'en sépare

L'ostinato de la zone a quatre notes ; celui-ci en a **cinq** — un homme par
note, ré - fa - la - sol - mi, quatre croches et une noire. Il fait donc trois
temps dans une mesure qui en compte quatre : la figure décale d'un temps à
chaque mesure et ne retombe à sa place que toutes les quatre mesures. Aux quatre
dernières mesures la noire finale s'allonge à la blanche, la cellule fait quatre
temps, et tout retombe ensemble. L'harmonie est le tétracorde descendant
ré - do - si♭ - la, la marche de tous les brigands de la musique modale.

## Les six voix, mesurées

`python3 ../../verifier.py brigands.mid --bpm 180`

| voix | côté | ce qui s'y trouve | registre | notes |
| ---: | :---: | --- | --- | ---: |
| 0 | **gauche** | la mélodie, seule | D5..A6 | 87 |
| 1 | gauche | le contre-chant, détaché | A3..A4 | 75 |
| 2 | **gauche** | la basse, sèche puis balancée | A2..G3 | 72 |
| 3 | **droite** | **les cinq voix**, et les réponses | D4..A♯4 | 132 |
| 4 | droite | les accords tenus | F3..A4 | 54 |
| 5 | **droite** | **LA BATTERIE** — charleston fermé 54, caisse claire 27, grosse caisse 24, charleston ouvert 8, cymbale 1 | bruit | 114 |

Stéréo mesurée **56/44**, aucune note abandonnée, `verifier.py` conclut `OK`.

⚠ **2 258 octets, marge 46.** Toute retouche de `brigands.py` doit être
reconvertie avant d'être crue.

## Régénérer

```sh
cd SCOSWAMP.MORE/MUSIC/propositions-moderne/clairieres/08-brigands
python3 brigands.py
python3 ../../../midi_to_mb.py brigands.mid BRIGANDS.MB.BIN \
    --bpm 180 --max 2304 --wav BRIGANDS.wav
```
