# Zone `danger` — les dix clairières où le Marais mord

**Fichier proposé : `DANGER.MB` (`DANGER.MB.BIN`, 960 octets, 55,6 s de boucle)**

Cette zone n'est pas géographique : elle **traverse** le nord et le sud. Dix
clairières y sont rangées parce que la page d'arrivée y menace directement le
joueur, et non parce qu'elles se touchent sur la grille. C'est le seul endroit
du plan où l'ambiance l'emporte sur la carte.

## Clairières couvertes (10)

| `hub` | `id` | Titre | Case | Moitié | Pages |
| --- | --- | --- | --- | --- | --- |
| **153** | 28 | Le bassin de Vase | (1,2) | nord | 336, 137, 153 |
| **088** | 32 | Scorpion et nain | (2,2) | nord | 14, 338, 088 |
| **270** | 30 | Sables mouvants | (4,2) | nord | 41, 382, 270 |
| **319** | 13 | La clairière des scorpions | (3,4) | sud | 118, 303, 319 |
| **367** | 23 | Les Fleurs d'Angoisse | (0,5) | sud | 204, 250, 367 |
| **187** | 24 | Herbe à Pinces | (3,5) | sud | 388, 263, 33, 187 |
| **309** | 26 | Orques des Marais | (4,5) | sud | 290, 323, 352, 309 |
| **125** | — | Cul-de-sac de la Bête | (0,6) | sud | 11, 210, 299, 125, 228, 243 |
| **022** | 18 | La clairière des Arbres-Épées | (1,6) | sud | 157, 279, 022 |
| **165** | 17 | Tente aux araignées | (3,6) | sud | 144, 345, 354, 165 |

Ambiances qui justifient le regroupement :

- *« le rocher bouge […] deux yeux rouges vous fixent, furieux »*
  (`TEXTFR/N000/N011.TXT:9-10`) ;
- *« Leur pollen inspire la terreur et vous sentez vos mains trembler »*
  (`TEXTFR/N200/N204.TXT:9-10`) ;
- *« une clairière constellée de toiles »*, *« L'Anneau de Cuivre se réchauffe »*
  (`TEXTFR/N100/N144.TXT:5,12`) ;
- *« chacun de vos pas produit sur le sol un bruit de succion »*, *« une odeur
  répugnante »* (`TEXTFR/N300/N336.TXT:4-5,14`) ;
- *« un SCORPION GÉANT tient un NAIN […] le scorpion semble le dévorer »*
  (`TEXTFR/N000/N014.TXT:7-9`) ;
- *« des pinces apparaissent aux extrémités de ses tiges »*
  (`TEXTFR/N350/N388.TXT:10`).

## La pièce

| | |
| --- | --- |
| Œuvre | **Unquiet Thoughts** |
| Auteur | **John Dowland** (1563-1626), *The First Booke of Songes*, **1597** |
| Source | Mutopia Project, [piece-info.cgi?id=21](https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=21) |
| Fichiers | `https://www.mutopiaproject.org/ftp/DowlandJ/ALS1/UnquietThoughts/UnquietThoughts.{ly,mid}` |
| Licence | **domaine public** (Creative Commons No Rights Reserved) |
| Effectif d'origine | quatre voix (SATB) |
| Tempo retenu | **140** à la noire |
| Durée de boucle | 55,6 s |
| Taille | 960 octets |

## Pourquoi elle convient

C'est **la pièce jumelle de l'accueil** : `COMEAGAIN.MB` et celle-ci ouvrent le
même recueil de Dowland, 1597. Le jeu commence sur *Come Again* ; quand le
Marais montre les dents, c'est le même compositeur qui parle, mais son autre
face — d'où le titre : *pensées inquiètes*. Cette parenté d'écriture fait que la
zone `danger` ne sonne pas comme une pièce rapportée, elle sonne comme une
menace qui était là depuis le début.

Musicalement, elle vaut par son harmonie : Dowland module vite, place des
fausses relations et des notes étrangères que l'onde carrée rend **franchement
acides** — l'AY ne pardonne aucune dissonance, ce qui est ici l'effet recherché.
Aucune autre pièce du lot ne grince.

**Tempo.** 140 la noire : un ayre de Dowland se chante autour de 100, mais à 100
la carte le rend lugubre et immobile. À 140 la basse marche, l'inquiétude
devient nerveuse au lieu d'être triste — et la zone `mort` garde le monopole du
lent.

## Régénérer

```sh
python3 SCOSWAMP.MORE/MUSIC/midi_to_mb.py \
    SCOSWAMP.MORE/MUSIC/propositions/danger/UnquietThoughts.mid \
    SCOSWAMP.MORE/MUSIC/propositions/danger/DANGER.MB.BIN \
    --bpm 140 --vol 13,9,11 \
    --wav SCOSWAMP.MORE/MUSIC/propositions/danger/DANGER.wav
```
