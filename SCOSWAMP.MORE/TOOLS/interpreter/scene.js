/* scene.js -- lire une page et en tirer ce qu'elle contient.
 *
 * Portage de classify_line() (SCOSWAMP/SRC/scoswamp.c). La TABLE des
 * directives ne vit plus dans le code : elle est dans le descripteur du jeu,
 * et c'est elle qui dit quels jetons existent, comment ils s'ecrivent et
 * lesquels sont des effets d'entree. Le code, lui, porte le SENS de chaque
 * jeton -- une trentaine de gestes que tout jeu a choix multiples partage.
 *
 * Une ligne qui ne correspond a aucune directive du descripteur est du texte.
 * C'est ce qui laisse SPACETRIP, qui n'emploie que `C`, se decrire par le
 * meme lecteur sans qu'une seule ligne change ici.
 */

import * as R from './rules.js';

/* ── Lecture d'arguments : take_uint / take_int / take_word ───────────── */

class Cur {
  constructor(s, i) { this.s = s; this.i = i || 0; }
  get rest() { return this.s.slice(this.i); }
  get atEnd() { return this.i >= this.s.length; }
  skipSpaces() { while (this.s[this.i] === ' ') this.i++; }
  /* Avance sur les chiffres puis sur les espaces, et rend la valeur lue. */
  uint() {
    let v = 0;
    while (this.s[this.i] >= '0' && this.s[this.i] <= '9') v = v * 10 + (this.s.charCodeAt(this.i++) - 48);
    this.skipSpaces();
    return v;
  }
  /* La meme chose, signe compris : les effets d'une ligne CE sont negatifs. */
  int() {
    let neg = false;
    if (this.s[this.i] === '-') { neg = true; this.i++; }
    else if (this.s[this.i] === '+') this.i++;
    const v = this.uint();
    return neg ? -v : v;
  }
  /* Avance sur un mot et rend le mot ; le curseur se pose sur le suivant. */
  word() {
    const start = this.i;
    while (this.i < this.s.length && this.s[this.i] !== ' ') this.i++;
    const w = this.s.slice(start, this.i);
    this.skipSpaces();
    return w;
  }
}

/* Les quatre mots que E, E0, CE et ED acceptent. L'INITIALE suffit : c'est le
 * choix de carac_of(), faute de frappe comprise -- reflow_txt.py la refuse du
 * cote ou l'on peut se payer une verification. 4 = le bonus d'arme. */
export function caracOf(w) {
  switch ((w || ' ')[0]) {
    case 'B': return 4;
    case 'E': return 0;
    case 'H': return 1;
    case 'C': return 2;
    case 'O': return 3;
    default:  return 4;
  }
}
export const CARAC_NOMS = ['ENDURANCE', 'HABILETE', 'CHANCE', 'OR', 'BONUS D\'ARME'];

/* L'effet, par la seule porte qui connaisse les bornes : plafond au total de
 * depart pour les trois caracteristiques, plancher zero pour les quatre. */
export function caracApply(hero, c, d) {
  switch (c) {
    case 0: R.adjustEnd(hero, d); break;
    case 1: R.adjustHab(hero, d); break;
    case 2: R.adjustCha(hero, d); break;
    case 3: R.adjustGold(hero, d); break;
    case 4: hero.weaponBonus = Math.min(2, hero.weaponBonus + d); break;
  }
}

/* ── Les choix de la page ─────────────────────────────────────────────── */

const NO_STONE = () => R.STONE_COUNT();
const NO_OBJ = () => R.OBJ_COUNT();

function pushChoice(app, scene, grant, require, title) {
  if (app.choices.length >= app.proj.moteur.maxChoix) return;
  app.choices.push({ scene, grant, require, object: NO_OBJ(), objMode: 0, title });
}

function pushObjectChoice(app, scene, o, mode, title) {
  pushChoice(app, scene, NO_STONE(), NO_STONE(), title);
  const c = app.choices[app.choices.length - 1];
  if (!c) return;
  c.object = o; c.objMode = mode;
}

/* Un choix qui exige une Pierre absente du sac se VOIT mais ne se prend pas :
 * savoir ce qu'une Pierre aurait permis fait partie de la lecture. */
export function choiceAvailable(app, c) {
  const hero = app.hero;
  if (c.require < R.STONE_COUNT() && !R.hasStone(hero, c.require)) return false;
  if (c.object < R.OBJ_COUNT()) {
    const has = R.hasObject(hero, c.object);
    return c.objMode === 2 ? !has : has;
  }
  if (c.object & 0x80) {
    const has = R.hasAmulet(hero, c.object & 0x7f);
    return c.objMode === 2 ? !has : has;
  }
  if (c.object === 0x7f) {                    /* ligne CA : un intervalle */
    const n = R.amuletCount(hero);
    return n >= (c.objMode >> 4) && n <= (c.objMode & 15);
  }
  return true;
}

/* ── Les directives, un geste par jeton ───────────────────────────────── */

/* Chaque implementation recoit (app, cur, ligne) et rend, si elle veut, une
 * phrase pour le journal du lecteur -- c'est ce journal qui fait de ce
 * programme un banc d'essai et pas seulement un jeu. */
const OPS = {
  GX(app, cur) {
    const w = cur.word();
    R.takeObject(app.hero, R.objectFromName(w));
    return `retire ${w}`;
  },

  GA(app, cur) {
    const each = cur.uint();
    const n = R.tradeAmulets(app.hero, each);
    return `${n} amulette(s) revendue(s) a ${each} Pieces d'Or`;
  },

  G(app, cur) {
    const w = cur.word();
    const am = R.amuletFromName(w);
    if (am !== R.AMULET_COUNT()) { R.giveAmulet(app.hero, am); return `donne ${R.amuletName(am, app.english)}`; }
    const o = R.objectFromName(w);
    R.giveObject(app.hero, o);
    return `donne ${R.objectName(o) || w}`;
  },

  CI(app, cur) { return objCond(app, cur, 1); },
  CN(app, cur) { return objCond(app, cur, 2); },

  CA(app, cur) {
    const lo = cur.uint(), hi = cur.uint(), id = cur.uint();
    pushObjectChoice(app, id, 0x7f, (lo << 4) | hi, cur.rest);
    return `choix ${id} si ${lo} a ${hi} amulettes`;
  },

  GU(app, cur) {
    const w = cur.word(), o = R.objectFromName(w), id = cur.uint();
    if (o !== R.OBJ_COUNT()) pushObjectChoice(app, id, o, 3, cur.rest);
    return `choix ${id} qui consomme ${w}`;
  },

  PD(app) { R.loseItems(app.hero, 2); return 'on vous prend deux biens'; },
  PO(app) { R.loseItems(app.hero, 1); return 'on vous prend un bien'; },
  PX(app) {
    app.hero.stones = app.hero.stones.map(() => 0);
    app.hero.objects = 0; app.hero.amulets = 0;
    return 'le sac est vide';
  },

  /* Jusqu'a trois biens troques contre autant de Pierres neutres a choisir.
   * Les quatre objets troquables sont ceux du masque 0x018C : Chaine d'Or,
   * Aimant d'Or, Bijou Violet, Corne de Licorne. */
  TR(app) {
    const MASK = 0x018c;
    let bits = app.hero.objects & MASK, n = 0;
    while (bits && n < 3) { bits &= bits - 1; n++; }
    app.hero.objects = (app.hero.objects & ~MASK) | bits;
    while (app.hero.amulets && n < 3) { app.hero.amulets &= app.hero.amulets - 1; n++; }
    app.chooseN = n;
    app.chooseCats = 'N';
    return `${n} bien(s) troque(s) contre autant de Pierres neutres`;
  },

  MD(app, cur) { const n = cur.uint(); lastFoe(app, (f) => { f.damage = n; }); return `degats ${n}`; },
  MS(app, cur) { const n = cur.uint(); lastFoe(app, (f) => { f.stopAt = n; }); return `combat jusqu'a ${n}`; },
  MI(app, cur) {
    const p = cur.uint();
    if (app.foes.length) app.foeImg[app.foes.length - 1] = p;
    return `image de bataille empruntee a la page ${p}`;
  },

  MU(app, cur, l) {
    let t = l.slice(3);
    if (t[0] === '+') { app.musicOver = true; t = t.slice(1); }
    app.musicName = t;
    return `musique ${t || '(silence)'}${app.musicOver ? ' (surcouche)' : ''}`;
  },

  MV(app, cur) { app.winScene = cur.uint(); return `victoire -> ${app.winScene}`; },
  MB(app, cur) { app.mbOk = cur.uint(); app.mbKo = cur.uint(); return `premier sang : ${app.mbOk} / ${app.mbKo}`; },

  /* Chaque ligne M ajoute un adversaire a la file, dans l'ordre de la page --
   * c'est l'ordre dans lequel le livre les fait venir. */
  M(app, cur) {
    if (app.foes.length >= app.proj.moteur.maxAdversaires) return 'file pleine : adversaire ignore';
    const f = R.newMonster();
    f.hab = cur.uint(); f.end = cur.uint(); f.name = cur.rest;
    app.foeImg[app.foes.length] = 0;
    app.foes.push(f);
    return `adversaire ${f.name} HAB ${f.hab} END ${f.end}`;
  },

  E0(app, cur) {
    const k = caracOf(cur.word()), d = cur.int();
    R.shift0(app.hero, k, d);
    return `TOTAL DE DEPART ${CARAC_NOMS[k]} ${d >= 0 ? '+' : ''}${d}`;
  },

  /* "Tentez votre Chance" qui ne branche pas : il decide d'un effet, la page
   * continue de se lire. Le jet tombe ICI, a la lecture de la ligne. */
  CE(app, cur) {
    const k = caracOf(cur.word()), dok = cur.int(), dko = cur.int();
    const { lucky, roll } = R.luckTest(app.hero);
    caracApply(app.hero, k, lucky ? dok : dko);
    return `Chance ${roll} : ${lucky ? 'Chanceux' : 'Malchanceux'}, ${CARAC_NOMS[k]} ${lucky ? dok : dko}`;
  },

  /* Le jet est DIFFERE : la ligne ne fait que remplir dice_n / dice_carac, et
   * le moteur le joue une fois la page AFFICHEE -- sinon le joueur ne verrait
   * rien. La position de la ligne dans le fichier n'ordonne donc rien. */
  ED(app, cur) {
    const k = caracOf(cur.word()), n = cur.int();
    app.diceCarac = k;
    if (k < 4) app.diceN = n;
    return `jet de ${Math.abs(n)} de(s) sur ${CARAC_NOMS[k]} (differe)`;
  },

  E(app, cur) {
    const k = caracOf(cur.word()), d = cur.int();
    caracApply(app.hero, k, d);
    return `${CARAC_NOMS[k]} ${d >= 0 ? '+' : ''}${d}`;
  },

  PC(app, cur) {
    app.chooseN = cur.uint();
    app.chooseCats = cur.rest;
    return `${app.chooseN} Pierre(s) a choisir parmi ${app.chooseCats}`;
  },

  P(app, cur) {
    const w = cur.word(), s = R.stoneFromName(w);
    if (s === R.STONE_COUNT()) return `Pierre inconnue : ${w}`;
    const n = cur.atEnd ? 1 : cur.uint();
    R.giveStone(app.hero, s, n);
    return `donne ${n} Pierre(s) de ${w}`;
  },

  CL(app, cur) {
    app.luckOk = cur.uint();
    app.luckKo = cur.uint();
    if (!cur.atEnd) { app.luckDok = cur.int(); app.luckDko = cur.int(); }
    return `Tentez votre Chance : ${app.luckOk} / ${app.luckKo}`;
  },

  CU(app, cur) { return stoneChoice(app, cur, true); },
  CP(app, cur) { return stoneChoice(app, cur, false); },

  /* "Si vous y etes deja venu, rendez-vous au 142. Sinon, lisez ce qui suit."
   * Le detour decide : plus rien de la page ne doit jouer, ni son texte, ni
   * ses choix, ni surtout ses lignes E et P qui donneraient une seconde fois
   * ce qu'on a deja pris. Les numeros qui suivent sont les AUTRES pages du
   * meme lieu : entrer par une autre porte compte aussi. */
  V(app, cur) {
    const cible = cur.uint();
    let b = app.currentScene;
    for (;;) {
      if (R.sceneVisited(app.mem, b)) break;
      if (!cur.atEnd) { b = cur.uint(); continue; }
      if (b === cible) return `jamais venu : la page se lit en entier`;
      b = cible;
    }
    app.revisit = cible;
    return `deja venu (page ${b}) : detour vers ${cible}`;
  },

  CS(app, cur) {
    app.csCarac = caracOf(cur.word());
    app.csOk = cur.uint();
    app.csKo = cur.uint();
    return `jet contre ${CARAC_NOMS[app.csCarac]} : ${app.csOk} / ${app.csKo}`;
  },

  /* En cascade : la premiere ligne dont la perte du dernier combat ne depasse
   * pas <max> fabrique l'unique choix de la page. */
  DV(app, cur) {
    const max = cur.uint(), id = cur.uint();
    if (!app.dvDone && app.lastLoss <= max) {
      app.dvDone = true;
      pushChoice(app, id, NO_STONE(), NO_STONE(), app.msg('M_K_CONTINUER'));
      return `blessures ${app.lastLoss} <= ${max} : continuer vers ${id}`;
    }
    return `blessures ${app.lastLoss} > ${max} : ligne sautee`;
  },

  CF(app, cur) { app.fleeTarget = cur.uint(); return `la Fuite mene en ${app.fleeTarget}`; },

  T(app, cur, l) {
    let i = 2;
    while (l[i] >= '0' && l[i] <= '9') i++;
    while (l[i] === ' ') i++;
    app.title = l.slice(i);
    return null;
  },

  C(app, cur) {
    const start = cur.i;
    const id = cur.uint();
    if (cur.i === start || cur.atEnd) return 'ligne C sans cible ni libelle : ignoree';
    pushChoice(app, id, NO_STONE(), NO_STONE(), cur.rest);
    return `choix -> ${id}`;
  },
};

function lastFoe(app, fn) { if (app.foes.length) fn(app.foes[app.foes.length - 1]); }

function objCond(app, cur, mode) {
  const w = cur.word(), o = R.objectFromName(w), id = cur.uint();
  const am = R.amuletFromName(w);
  if (am !== R.AMULET_COUNT()) pushObjectChoice(app, id, 0x80 | am, mode, cur.rest);
  else if (o !== R.OBJ_COUNT()) pushObjectChoice(app, id, o, mode, cur.rest);
  else return `jeton inconnu : ${w}`;
  return `choix ${id} si ${mode === 1 ? '' : 'PAS '}${w}`;
}

function stoneChoice(app, cur, exige) {
  const w = cur.word(), st = R.stoneFromName(w), id = cur.uint();
  if (st === R.STONE_COUNT()) return `Pierre inconnue : ${w}`;
  if (exige) pushChoice(app, id, NO_STONE(), st, cur.rest);
  else pushChoice(app, id, st, NO_STONE(), cur.rest);
  return `choix ${id} qui ${exige ? 'exige' : 'remet'} une Pierre de ${w}`;
}

/* ── Le classement d'une ligne ────────────────────────────────────────── */

/* La boucle de kOps : premier jeton dont les deux lettres correspondent et
 * dont le troisieme caractere satisfait la regle. L'ordre du descripteur fait
 * foi -- 'M ' avalerait 'MV' s'il passait devant. */
export function matchDirective(proj, l) {
  const c0 = l[0] || '\0', c1 = l[1] || '\0', c2 = l[2] || '\0';
  for (const d of proj.directives) {
    const k0 = d.jeton[0], k1 = d.jeton.length > 1 ? d.jeton[1] : ' ';
    if (k0 !== c0 || k1 !== c1) continue;
    const t = d.troisieme;
    if (t === '*' || (t === '.' ? l.length <= 2 : c2 === ' ')) return d;
  }
  return null;
}

export function classifyLine(app, l) {
  if (app.revisit >= 0) return;    /* la page est court-circuitee (ligne V) */

  const d = matchDirective(app.proj, l);
  if (!d) {
    /* Pas de ligne vide en tete : le fichier en a une sous le titre, et elle
     * couterait la ligne de marge du budget de 18. */
    if (app.body.length < app.proj.moteur.lignesTexte && (app.body.length > 0 || l !== ''))
      app.body.push(l);
    return;
  }

  /* L'instantane d'une sauvegarde contient deja les effets d'entree de la
   * page reprise : les rejouer donnerait une seconde fois ce qu'on a pris.
   * C'est a cela que sert `effetEntree` dans le descripteur. */
  if (app.restoring && d.effetEntree) return;

  const impl = OPS[d.jeton];
  if (!impl) { app.trace.push({ jeton: d.jeton, ligne: l, note: 'directive declaree mais non implementee' }); return; }
  const cur = new Cur(l, d.jeton.length + 1);
  const note = impl(app, cur, l);
  if (note !== null) app.trace.push({ jeton: d.jeton, ligne: l, note });
}

/* Decoupe le fichier et classe chaque ligne, dans l'ordre : c'est la lecture
 * du fichier qui applique les effets d'entree (E, P, G, V...). */
export function parseScene(app, texte) {
  for (const l of texte.split(/\r\n|\r|\n/)) classifyLine(app, l);
}
