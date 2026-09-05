/* ui.js -- l'ecran 80 colonnes, les images, et le banc d'essai autour.
 *
 * La moitie gauche reproduit la mise en page de la machine : barre de titre
 * en video inverse, 18 lignes de recit, la ligne de lieu, et les 4 lignes que
 * le mode mixte laisse voir sous l'illustration. Les memes bornes que
 * scoswamp.c, parce qu'un texte qui deborde ICI debordera LA-BAS -- c'est la
 * premiere chose qu'un atelier doit montrer.
 *
 * La moitie droite est ce que la machine ne peut pas montrer : le master
 * avant conversion, le flux DHGR decode a cote pour comparaison, la Feuille
 * d'Aventure, le journal des directives de la page et sa source.
 */

import * as D from './data.js';
import * as R from './rules.js';
import { matchDirective } from './scene.js';
import { decodeToImageData, decodeRawHgr, paletteUsage } from './dhgr.js';

const COLS = 80;
const pad = (s, n) => (s + ' '.repeat(n)).slice(0, n);

export class UI {
  constructor(root, proj) {
    this.proj = proj;
    this.root = root;
    this.el = {};
    this.resolveKey = null;
    this.variante = proj.images[0].id;
    this.onglet = 'journal';
    this.build();
    window.addEventListener('keydown', (e) => this.onKeyDown(e));
  }

  attach(engine) { this.engine = engine; this.app = engine.app; }

  /* ── Les touches ────────────────────────────────────────────────────── */

  /* Le moteur appelle `await ui.key()` la ou le C appelle cgetc(). Une seule
   * attente a la fois : c'est exactement la boucle de la machine. */
  key() { return new Promise((res) => { this.resolveKey = res; }); }

  press(k) {
    const r = this.resolveKey;
    if (!r) return;
    this.resolveKey = null;
    r(k);
  }

  /* Le banc d'essai reprend la main : '\0' est la touche qui ne fait rien,
   * et que chaque boucle du moteur sait reconnaitre pour abandonner. */
  resume() { this.press('\x00'); }

  onKeyDown(e) {
    if (e.target && /^(INPUT|SELECT|TEXTAREA)$/.test(e.target.tagName)) return;
    let k = null;
    if (e.key === 'Escape') k = '\x1b';
    else if (e.key === 'Enter') k = '\r';
    else if (e.key === ' ') k = ' ';
    else if (e.key.length === 1) k = e.key.toUpperCase();
    if (k === null) return;
    e.preventDefault();
    this.press(k);
  }

  /* ── Construction du cadre ──────────────────────────────────────────── */

  build() {
    this.root.innerHTML = `
      <header class="barre">
        <strong>${this.proj.titre}</strong>
        <span class="sep"></span>
        <label>Langue <select id="langue"></select></label>
        <label>Page <input id="goto" type="number" min="0" max="${this.proj.moteur.pageMax}" step="1" size="4"></label>
        <button id="allerA">Aller a</button>
        <label>Graine <input id="graine" type="number" value="1" size="6"></label>
        <button id="semer">Semer</button>
        <span class="sep"></span>
        <span id="etat" class="etat"></span>
      </header>
      <main>
        <section class="gauche">
          <div id="ecran" class="ecran"></div>
          <div id="zoneBasse" class="zoneBasse"></div>
          <div id="touches" class="touches"></div>
        </section>
        <section class="droite">
          <div class="cartouche">
            <div class="entete">
              <select id="variante"></select>
              <span id="imageEtat" class="etat"></span>
            </div>
            <div class="imageBoite">
              <canvas id="toile" width="280" height="192"></canvas>
              <img id="photo" alt="">
              <div id="imageVide" class="vide"></div>
            </div>
          </div>
          <div id="feuille" class="cartouche"></div>
          <div class="cartouche">
            <div class="onglets">
              <button data-onglet="journal">Journal</button>
              <button data-onglet="source">Source</button>
              <button data-onglet="sac">Sac</button>
              <button data-onglet="directives">Directives</button>
            </div>
            <div id="panneau" class="panneau"></div>
          </div>
        </section>
      </main>
      <div id="modale" class="modale" hidden></div>`;

    const $ = (id) => this.root.querySelector('#' + id);
    this.el = {
      ecran: $('ecran'), zoneBasse: $('zoneBasse'), touches: $('touches'),
      toile: $('toile'), photo: $('photo'), imageVide: $('imageVide'),
      imageEtat: $('imageEtat'), variante: $('variante'), feuille: $('feuille'),
      panneau: $('panneau'), modale: $('modale'), etat: $('etat'),
      goto: $('goto'), graine: $('graine'), langue: $('langue'),
    };

    for (const v of this.proj.images) {
      const o = document.createElement('option');
      o.value = v.id; o.textContent = v.nom;
      this.el.variante.append(o);
    }
    for (const l of this.proj.langues) {
      const o = document.createElement('option');
      o.value = l.code; o.textContent = l.nom;
      this.el.langue.append(o);
    }
    this.el.variante.onchange = () => { this.variante = this.el.variante.value; this.showImage(); };
    this.el.langue.onchange = async () => {
      await this.engine.setLangue(this.el.langue.value);
      this.engine.app.pending = this.engine.app.currentScene;
      this.resume();
    };
    $('allerA').onclick = () => {
      const n = parseInt(this.el.goto.value, 10);
      if (Number.isFinite(n)) this.engine.gotoPage(n);
    };
    $('semer').onclick = () => {
      R.diceSeed(parseInt(this.el.graine.value, 10) || 1);
      this.majEtat('graine posee');
    };
    this.root.querySelectorAll('[data-onglet]').forEach((b) => {
      b.onclick = () => { this.onglet = b.dataset.onglet; this.render(); };
    });
  }

  majEtat(t) { this.el.etat.textContent = t; }

  /* ── L'ecran de la machine ──────────────────────────────────────────── */

  /* Barre de titre : le titre de la page a gauche, le rappel des touches
   * derriere, la Feuille d'Aventure calee a droite -- render_title_bar(). */
  barreTitre() {
    const app = this.app;
    let l = ' '.repeat(COLS).split('');
    const mets = (i, s) => { for (let k = 0; k < s.length && i + k < COLS; k++) l[i + k] = s[k]; };
    if (app.title) {
      const t = app.title.slice(0, 40);
      mets(1, t);
      if (app.heroReady) mets(t.length + 3, app.lang === 'FR' ? 'I:SAC M:CARTE H:AIDE' : 'I:BAG M:MAP   H:HELP');
    }
    if (app.heroReady) {
      const h = app.hero;
      const f = app.lang === 'FR'
        ? `HAB ${h.hab}/${h.hab0}  END ${h.end}/${h.end0}  CHA ${h.cha}/${h.cha0}`
        : `SKL ${h.hab}/${h.hab0}  STA ${h.end}/${h.end0}  LCK ${h.cha}/${h.cha0}`;
      mets(COLS - 1 - f.length, f);
    } else {
      const hint = app.msg('M_TOUCHES');
      mets(COLS - 1 - hint.length, hint);
    }
    return l.join('');
  }

  /* La ligne de lieu -- render_place(). Quand la page n'est d'aucun lieu, la
   * clairiere collante s'affiche entre parentheses : c'est un souvenir, pas
   * une position. */
  barreLieu() {
    const app = this.app;
    if (!app.carte || app.mapHere < 0) return null;
    const bloc = app.carte.langue[app.lang] || app.carte.langue.FR;
    const nom = bloc.noms[app.mapHere];
    if (D.clairiereDePage(app.carte, app.currentScene) !== app.mapHere) return ` (${nom})`;
    const dirs = bloc.chaines[D.MS.DIRS] || 'NSEO';
    const m = app.carte.clr[app.mapHere].out;
    let s = ` ${nom}   ${bloc.chaines[D.MS.LIEU]} `;
    for (let d = 0; d < 4; d++) if (m & (1 << d)) s += dirs[d] + ' ';
    if (R.sceneVisited(app.mem, app.currentScene) && this.clairiereVue(app.mapHere)) s += `  ${bloc.chaines[D.MS.DEJA]}`;
    return s;
  }

  clairiereVue(i) {
    const app = this.app;
    return app.carte.pages.some((p) => p.clr === i && R.sceneVisited(app.mem, p.page));
  }

  render() {
    const app = this.app;
    if (!app) return;
    const m = this.proj.moteur;
    const lignes = [];
    lignes.push({ t: this.barreTitre(), inv: true });
    for (let i = 0; i < m.lignesTexte; i++) lignes.push({ t: app.body[i] || '' });
    const lieu = this.barreLieu();
    lignes.push(lieu === null ? { t: '' } : { t: pad(lieu, COLS - 1), inv: true });

    this.el.ecran.innerHTML = lignes
      .map((l) => `<div class="ligne${l.inv ? ' inv' : ''}">${esc(pad(l.t, COLS))}</div>`)
      .join('');

    this.renderZoneBasse();
    this.renderFeuille();
    this.renderPanneau();
    this.renderModale();
    this.showImage();
    this.el.goto.value = app.currentScene;
  }

  /* Les 4 lignes du bas : le combat, un message du moteur, ou les choix. */
  renderZoneBasse() {
    const app = this.app;
    const z = this.el.zoneBasse;
    z.innerHTML = '';
    const touches = [];

    if (app.combat) {
      const c = app.combat, f = c.foe;
      z.append(el('div', 'ligne combat', [
        el('span', 'moi', [txt(`${app.msg('M_VOUS')}  END ${app.hero.end}/${app.hero.end0} `), jauge(app.hero.end, app.hero.end0)]),
        el('span', 'lui', [txt(`${f.name}  HAB ${f.hab}  END ${f.end}/${f.end0} `), jauge(f.end, f.end0)]),
      ]));
      for (const l of c.lignes || []) z.append(el('div', 'ligne', [txt(l)]));
      if (c.verdict) z.append(el('div', 'ligne verdict', [txt(c.verdict)]));
      if (c.premier) touches.push(['ESPACE', app.msg('M_K_ENGAGER'), ' '], ['I', app.msg('M_K_SAC'), 'I']);
      else touches.push(['ESPACE', c.pending ? app.msg(c.hits ? 'M_K_FRAPPER' : 'M_K_ENCAISSER') : app.msg('M_K_SUIVANT'), ' ']);
      if (c.fuite) touches.push(['F', app.msg('M_K_FUIR'), 'F']);
      if (c.enjeu) touches.push(['C', app.msg('M_K_ENJEU', c.enjeu.cha, c.enjeu.bon, c.enjeu.mauvais), 'C']);
    } else if (app.bottom.some((l) => l)) {
      for (const l of app.bottom) z.append(el('div', 'ligne', [txt(l)]));
      touches.push(['ESPACE', app.hint || app.msg('M_K_CONTINUER'), ' ']);
    } else {
      /* Les choix, avec la regle de pairage de render_choices : deux par
       * ligne quand les deux tiennent dans une demi-largeur. */
      const cs = app.choices;
      const tient = (i) => i + 1 < cs.length && cs[i].title.length <= 36 && cs[i + 1].title.length <= 36;
      for (let i = 0; i < cs.length;) {
        const ligne = el('div', 'ligne choix', []);
        ligne.append(this.boutonChoix(i));
        if (tient(i)) { ligne.append(this.boutonChoix(i + 1)); i += 2; } else i += 1;
        z.append(ligne);
      }
      if (!cs.length && app.hint) z.append(el('div', 'ligne', [txt(app.hint)]));
      if (app.heroReady) touches.push(['I', app.msg('M_K_SAC'), 'I'], ['M', 'carte', 'M'], ['H', 'aide', 'H'],
                                      ['S', 'sauver', 'S'], ['L', 'charger', 'L']);
      if (!cs.length) touches.push(['R', 'recommencer', 'R']);
    }

    this.el.touches.innerHTML = '';
    for (const [k, label, key] of touches) {
      const b = el('button', 'touche', [el('kbd', '', [txt(k)]), txt(' ' + label)]);
      b.onclick = () => this.press(key);
      this.el.touches.append(b);
    }
  }

  boutonChoix(i) {
    const app = this.app, c = app.choices[i];
    const libre = choixDispo(app, c);
    const b = el('button', 'choixBouton' + (libre ? '' : ' bloque'), [
      el('span', 'tag', [txt((libre ? String.fromCharCode(65 + i) : '-') + ')')]),
      txt(' ' + c.title),
      el('span', 'cible', [txt(String(c.scene).padStart(3, '0'))]),
    ]);
    b.onclick = () => this.press(String.fromCharCode(65 + i));
    b.title = detailChoix(app, c);
    return b;
  }

  /* ── Les panneaux de droite ─────────────────────────────────────────── */

  renderFeuille() {
    const app = this.app;
    if (!app.heroReady) { this.el.feuille.innerHTML = '<div class="titre">Feuille d\'Aventure</div><div class="vide">les des ne sont pas encore jetes</div>'; return; }
    const h = app.hero;
    const l = (nom, v, v0) => `<div class="carac"><span>${nom}</span><b>${v}</b><i>/${v0}</i><span class="barre2"><span style="width:${v0 ? (100 * v) / v0 : 0}%"></span></span></div>`;
    this.el.feuille.innerHTML = `<div class="titre">Feuille d'Aventure</div>
      ${l('HABILETE', h.hab, h.hab0)}${l('ENDURANCE', h.end, h.end0)}${l('CHANCE', h.cha, h.cha0)}
      <div class="menus">${h.gold} Pieces d'Or${h.weaponBonus ? ` &middot; Epee Magique +${h.weaponBonus}` : ''}</div>`;
  }

  renderPanneau() {
    const app = this.app, p = this.el.panneau;
    this.root.querySelectorAll('[data-onglet]').forEach((b) =>
      b.classList.toggle('actif', b.dataset.onglet === this.onglet));

    if (this.onglet === 'journal') {
      p.innerHTML = app.trace.length
        ? app.trace.map((t) => `<div class="trace"><code>${esc(t.jeton)}</code><span class="ligne2">${esc(t.ligne)}</span><em>${esc(t.note || '')}</em></div>`).join('')
        : '<div class="vide">aucune directive sur cette page</div>';
    } else if (this.onglet === 'source') {
      p.innerHTML = `<pre class="source">${(app.source || '').split('\n').map((l) => {
        const d = matchDirective(this.proj, l);
        return d ? `<span class="dir" title="${esc(d.aide || '')}">${esc(l)}</span>` : esc(l);
      }).join('\n')}</pre>`;
    } else if (this.onglet === 'sac') {
      p.innerHTML = this.htmlSac();
    } else {
      p.innerHTML = `<table class="dirs"><tr><th>jeton<th>3e<th>entree<th>role</tr>${
        this.proj.directives.map((d) => `<tr><td><code>${d.jeton}</code><td>${d.troisieme === ' ' ? '␣' : d.troisieme}<td>${d.effetEntree ? 'oui' : ''}<td>${esc(d.aide || '')}</tr>`).join('')}</table>`;
    }
  }

  htmlSac() {
    const app = this.app;
    if (!app.heroReady) return '<div class="vide">pas de heros</div>';
    const h = app.hero;
    const pierres = h.stones.map((n, s) => (n ? `<li>${n} &times; ${R.stoneName(s, app.english)} <em>${R.stoneKind(s)}</em></li>` : '')).join('');
    const objets = R.cat.objets.map((o, i) => (i < R.cat.hidden0 && R.hasObject(h, i) ? `<li>${esc(o.libelle)}</li>` : '')).join('');
    const drapeaux = R.cat.objets.map((o, i) => (i >= R.cat.hidden0 && R.hasObject(h, i) ? `<li><code>${esc(o.cle)}</code></li>` : '')).join('');
    const amulettes = this.proj.amulettes.map((a, i) => (R.hasAmulet(h, i) ? `<li>${esc(app.english ? a.en : a.fr)}</li>` : '')).join('');
    return `<div class="colonnes">
      <div><h4>Pierres</h4><ul>${pierres || '<li class="vide">aucune</li>'}</ul></div>
      <div><h4>Objets</h4><ul>${objets || '<li class="vide">aucun</li>'}</ul>
           <h4>Amulettes</h4><ul>${amulettes || '<li class="vide">aucune</li>'}</ul>
           <h4>Drapeaux</h4><ul>${drapeaux || '<li class="vide">aucun</li>'}</ul></div></div>`;
  }

  /* ── Les ecrans modaux ──────────────────────────────────────────────── */

  renderModale() {
    const app = this.app, m = app.modal, d = this.el.modale;
    if (!m) { d.hidden = true; d.innerHTML = ''; return; }
    d.hidden = false;
    let h = '';
    if (m.type === 'pierres') {
      h = `<h3>${app.msg('M_CHOISISSEZ_PIERRES', m.reste)}</h3><ul class="liste">` +
        m.allowed.map((s, i) => `<li data-k="${String.fromCharCode(65 + i)}"><kbd>${String.fromCharCode(65 + i)}</kbd> ${R.stoneName(s, app.english)} <em>${R.stoneKind(s)}</em></li>`).join('') + '</ul>';
    } else if (m.type === 'sac') {
      h = `<h3>${app.msg('M_SAC_A_DOS', app.hero.gold)}</h3><ul class="liste">` +
        m.shown.map((s, i) => `<li data-k="${String.fromCharCode(65 + i)}"><kbd>${String.fromCharCode(65 + i)}</kbd> ${app.hero.stones[s]} &times; ${R.stoneName(s, app.english)}` +
          `${R.stoneUsable(s, m.inCombat) ? '' : ' <em>' + app.msg('M_INTERDITE_EN_PLEIN') + '</em>'}</li>`).join('') +
        '</ul>' + this.htmlSac() + `<p class="note">${esc(m.note || app.msg('M_UNE_PIERRE_SE'))}</p>`;
    } else if (m.type === 'carte') {
      h = `<pre class="carte">${esc(this.dessinCarte())}</pre>`;
    } else if (m.type === 'aide') {
      h = `<pre>${esc(app.aide || '')}</pre>`;
    } else if (m.type === 'feuille') {
      const c = app.hero;
      h = `<h3>${app.msg('M_FEUILLE_D_AVENTURE')}</h3><pre>${esc([
        app.msg('M_HABILETE_DE', c.hab), app.msg('M_ENDURANCE_DES', c.end),
        app.msg('M_CHANCE_DE', c.cha), '', app.msg('M_UNE_EPEE_UNE', c.gold),
        app.msg('M_AUCUN_DE_CES'),
      ].join('\n'))}</pre><p class="note">${esc(app.msg('M_ESPACE_ENTRER_DANS'))}</p>`;
    } else if (m.type === 'mort') {
      h = `<h3>${esc(app.msg('M_VOTRE_ENDURANCE_EST'))}</h3><p class="note">${esc(app.msg('M_MORT_RECOMMENCER'))}</p>`;
    } else if (m.type === 'sauvegardes') {
      h = `<h3>${app.msg(m.saving ? 'M_SAUVEGARDES' : 'M_CHARGEMENTS')}</h3><ul class="liste">` +
        m.slots.map((s, i) => `<li data-k="${i}"><kbd>${i}</kbd> ${s ? esc(`${s.date} -- p.${s.scene} ${s.titre}`) : app.msg('M_VIDE')}</li>`).join('') + '</ul>';
    }
    d.innerHTML = `<div class="boite">${h}</div>`;
    d.querySelectorAll('[data-k]').forEach((li) => { li.onclick = () => this.press(String(li.dataset.k)); });
  }

  /* La carte, dessinee comme show_map() la dessine : une grille 6 x 9, les
   * sentiers d'abord, les cases par-dessus, et rien qui n'ait ete vu. */
  dessinCarte() {
    const app = this.app, carte = app.carte;
    const bloc = carte.langue[app.lang] || carte.langue.FR;
    const COL = [2, 8, 14, 20, 26, 32], ROW = [2, 4, 6, 8, 10, 12, 14, 16, 18];
    const DC = [0, 0, 1, -1], DR = [-1, 1, 0, 0], SC = [1, 1, 4, -1];
    const g = Array.from({ length: 20 }, () => new Array(COLS).fill(' '));
    const put = (c, r, s) => { for (let i = 0; i < s.length; i++) if (c + i < COLS && r >= 0 && r < 20) g[r][c + i] = s[i]; };
    const vu = carte.clr.map((_, i) => this.clairiereVue(i));
    const nVus = vu.filter(Boolean).length;

    put(1, 0, `${bloc.chaines[D.MS.TITRE]} -- ${nVus} ${bloc.chaines[D.MS.SUR35]}`);
    for (let i = 0; i < 6; i++) put(COL[i] + 1, 1, String(i));
    for (let i = 0; i < 9; i++) put(0, ROW[i], String(i));

    /* Un sentier n'est dessine que depuis une clairiere VUE, et il finit par
     * '?' quand l'autre bout est inconnu -- « un rayon termine par ? ». */
    carte.clr.forEach((cl, i) => {
      if (!vu[i]) return;
      const r = ROW[cl.y], c = COL[cl.x];
      if (cl.out & 0x10) put(c + 1, r + 1, 'v');
      for (let d = 0; d < 4; d++) {
        if (!(cl.out & (1 << d))) continue;
        const j = D.voisin(carte, i, d);
        if (j < 0) continue;
        let n = 2;
        if (vu[j]) {
          n = d < 2 ? Math.abs(ROW[carte.clr[j].y] - r) - 1 : Math.abs(COL[carte.clr[j].x] - c) - 4;
        }
        let cc = c + SC[d], rr = r + DR[d];
        const glyphe = DC[d] ? '-' : '|';
        for (let k = n; k > 0; k--) {
          put(cc, rr, k > 1 || vu[j] ? glyphe : '?');
          cc += DC[d]; rr += DR[d];
        }
      }
    });
    carte.clr.forEach((cl, i) => {
      if (!vu[i]) return;
      const ici = i === app.mapHere;
      put(COL[cl.x], ROW[cl.y], (ici ? '<' : '(') + (cl.num ? String(cl.num).padStart(2) : ' ?') + (ici ? '>' : ')'));
    });

    /* Le panneau de droite : ou l'on est, et ce qui en part. */
    const dirs = bloc.chaines[D.MS.DIRS] || 'NSEO';
    let r = 2;
    if (app.mapHere >= 0) {
      const cl = carte.clr[app.mapHere];
      put(38, r++, (cl.num ? `N ${cl.num}  ` : '') + bloc.noms[app.mapHere]);
      put(38, r++, bloc.chaines[D.MS.SORTIES]);
      for (let d = 0; d < 4; d++) {
        if (!(cl.out & (1 << d))) continue;
        const j = D.voisin(carte, app.mapHere, d);
        const connu = j >= 0 && vu[j];
        put(38, r++, `  ${dirs[d]}  ${pad(connu ? bloc.noms[j] : '?', 12)}  ${bloc.chaines[connu ? D.MS.VUE : D.MS.INCONNUE]}`);
      }
      if (cl.out & 0x10) put(38, r++, `  v  ${pad('', 12)}  ${bloc.chaines[D.MS.HORS]}`);
    }
    put(38, 11, bloc.chaines[D.MS.LEGENDE]);
    for (let i = 0; i < 5; i++) put(40, 12 + i, bloc.chaines[D.MS.LEG1 + i]);
    put(38, 18, `${nVus} ${bloc.chaines[D.MS.SUR35]}`);
    put(0, 19, bloc.chaines[D.MS.TOUCHES]);
    return g.map((l) => l.join('').replace(/\s+$/, '')).join('\n');
  }

  /* ── L'image ────────────────────────────────────────────────────────── */

  async showImage() {
    const app = this.app;
    const cles = [app.imageKey, app.imageAlt].filter(Boolean);
    const v = this.proj.images.find((x) => x.id === this.variante) || this.proj.images[0];
    this.el.photo.hidden = true; this.el.toile.hidden = true;
    if (!cles.length) { this.el.imageVide.textContent = 'cette page n\'a pas d\'illustration'; this.el.imageEtat.textContent = ''; return; }

    for (const cle of cles) {
      const id = parseInt(cle.slice(1), 10);
      const chemin = D.fill(this.proj, v.chemin, { img: cle, id });
      const ok = await this.peindre(v, chemin, cle);
      if (ok) return;
    }
    this.el.imageVide.textContent = `${v.nom} : ${cles.join(' / ')} absent`;
    this.el.imageEtat.textContent = 'manquant';
  }

  async peindre(v, chemin, cle) {
    if (v.type === 'png') {
      const ok = await new Promise((res) => {
        const img = this.el.photo;
        img.onload = () => res(true);
        img.onerror = () => res(false);
        img.src = D.url(chemin);
      });
      if (!ok) return false;
      this.el.photo.hidden = false;
      this.el.imageVide.textContent = '';
      this.el.imageEtat.textContent = `${cle} -- ${this.el.photo.naturalWidth}x${this.el.photo.naturalHeight}`;
      return true;
    }
    let bytes;
    try { bytes = await D.getBytes(chemin); } catch { return false; }
    const ctx = this.el.toile.getContext('2d');
    const img = v.type === 'hgr-brut' ? decodeRawHgr(bytes, ctx)
                                      : decodeToImageData(bytes, v.palette, ctx);
    if (!img) { this.el.imageEtat.textContent = `${cle} : flux illisible`; return false; }
    ctx.putImageData(img, 0, 0);
    this.el.toile.hidden = false;
    this.el.imageVide.textContent = '';
    const u = v.type === 'hgr-brut' ? null : paletteUsage(bytes);
    this.el.imageEtat.textContent = `${cle} -- ${bytes.length} octets`
      + (u ? `, ${u.filter((n) => n).length} couleurs` : '');
    return true;
  }
}

/* ── Petits outils ──────────────────────────────────────────────────── */

function esc(s) {
  return String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}
function el(tag, cls, kids) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  (kids || []).forEach((k) => e.append(k));
  return e;
}
function txt(s) { return document.createTextNode(String(s ?? '')); }
function jauge(v, v0) {
  const n = v0 ? Math.round((10 * v) / v0) : 0;
  return txt('[' + '#'.repeat(n) + '.'.repeat(Math.max(0, 10 - n)) + ']');
}

/* Le meme test que choice_available, importe indirectement pour eviter une
 * dependance croisee entre l'ecran et l'analyseur. */
import { choiceAvailable as choixDispo } from './scene.js';

/* Ce que l'infobulle d'un choix dit : pourquoi il est ouvert ou ferme. */
function detailChoix(app, c) {
  const bouts = [`-> page ${c.scene}`];
  if (c.require < R.STONE_COUNT()) bouts.push(`exige une Pierre de ${R.stoneName(c.require, app.english)}`);
  if (c.grant < R.STONE_COUNT()) bouts.push(`remet une Pierre de ${R.stoneName(c.grant, app.english)}`);
  if (c.object < R.OBJ_COUNT()) bouts.push(`${c.objMode === 2 ? 'sans' : 'avec'} ${R.cat.objets[c.object].cle}${c.objMode === 3 ? ' (consomme)' : ''}`);
  else if (c.object & 0x80) bouts.push(`${c.objMode === 2 ? 'sans' : 'avec'} amulette ${app.proj.amulettes[c.object & 0x7f].cle}`);
  else if (c.object === 0x7f) bouts.push(`${c.objMode >> 4} a ${c.objMode & 15} amulettes`);
  return bouts.join(' | ');
}
