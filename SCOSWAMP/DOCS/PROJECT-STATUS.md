# Statut du projet SCOSWAMP

Adaptation bilingue de *Scorpion Swamp* pour Apple IIe Enhanced.

## État actuel

| Composant | État |
|---|---:|
| Scènes françaises | 402/402 |
| Scènes anglaises | 402/402 |
| Images disponibles | 402/402 |
| Images restant à créer | 0 |
| Moteur bilingue | Complet |
| Chargement HGR RLE | Complet |

Le comptage couvre `N000` à `N401`. Les 401 illustrations autres que `N000`
ont été entièrement régénérées. La page de titre `N000` a volontairement été
conservée. La direction artistique validée est la
variante II : illustration pulp *sword and sorcery* de la fin des années 1970,
silhouettes franches, ombres à l'encre, aplats limités et excellente lisibilité
après réduction en HGR 280×192.

## Format graphique

- Affichage Apple II HGR : 280×192, page décompressée de 8 192 octets.
- Palette POM2/Le Chat Mauve : noir, blanc, violet, vert, bleu, orange.
- Fichier hôte : `IMG/Nxxx/Nyyy.RLE.BIN`.
- Nom vu par ProDOS : `IMG/Nxxx/Nyyy.RLE`.
- Compression `HGRR` version 1 : blocs littéraux et répétitions RLE.
- Chargeur 65C02 `SRC/hgr_loader.s` : lectures groupées de 1 Kio et décodage
  assembleur direct vers `$2000-$3FFF`.

Les pages HGR brutes sont archivées hors du volume exécutable dans
`SCOSWAMP.MORE/RAW-HGR/`. Les nouvelles sources et leurs aperçus HGR sont dans
`SCOSWAMP.MORE/GENERATED/` et `SCOSWAMP.MORE/HGR-PREVIEW/`.

### Prompt maître retenu

- Une scène décisive fidèle au texte français, jamais un collage des choix.
- Style pulp *sword and sorcery* de la fin des années 1970.
- Formes HGR nettes, silhouettes lisibles et contours essentiels épais.
- Palette : noir, blanc, violet, vert, bleu et orange.
- Grands espaces noirs ; aucun texte, cadre, logo, filigrane, dégradé,
  anticrénelage ou détail minuscule.
- Éviter le concept art moderne brillant, l'aérographe lisse, les bulles de BD
  et le tramage aléatoire.

## Compilation et exécution

```sh
cd SCOSWAMP/SRC
make
```

Les 401 sources régénérées sont converties par `scoswamp_hgr` en fichiers
`RLE.BIN` et en aperçus HGR. Les 402 fichiers RLE, page de titre comprise, ont
été validés avec succès.

Le volume final est `dist/SCOSWAMP.HDV` (volume ProDOS `/SCOSWAMP`, 7 641
blocs, 1 231 fichiers). Point important : le constructeur HDV doit recevoir deux
blocs d'amorçage provenant d'un disque bloc ProDOS, tels que les 1 024 octets
situés après l'en-tête de 64 octets de `ScoSwamp-0.5alpha.2mg`. Il ne faut pas
utiliser directement les premiers blocs de `cc65-Chess/apple2/template.dsk` :
leur chargeur Disk II provoque une boucle de redémarrage à froid dans POM2.

Lancement validé :

```sh
/Users/gistair/src/pom2/build/POM2 --preset iie --display chatmauve \
  dist/SCOSWAMP.HDV
```

Le démarrage corrigé quitte bien la ROM et entre dans le programme SCOSWAMP.
Les scènes sans image restent jouables en mode texte.

## Travail restant

- Contrôler le rendu sur matériel composite réel en complément du rendu
  déterministe Le Chat Mauve.
