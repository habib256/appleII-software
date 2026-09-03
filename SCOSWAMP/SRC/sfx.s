; ---------------------------------------------------------------------------
; SFX - bruitages du combat sur le haut-parleur interne
;
; $C030 : toute lecture inverse la position de la membrane. Une note est donc
; une suite de lectures espacees d'un delai constant ; sa hauteur est l'inverse
; de ce delai. Le delai est compte en boucle a vide, ce qui lie la hauteur a
; l'horloge : sur un Apple II a 1,023 MHz une periode de N donne environ
; 102300/N Hz. Le //c+ tourne quatre fois plus vite et montera d'autant --
; assume, ces bruits sont des ponctuations, pas de la musique.
; ---------------------------------------------------------------------------

        .export _sfx_hit, _sfx_hurt, _sfx_dodge, _sfx_fall, _sfx_death
        .export _sfx_beat

SPEAKER = $C030

        .bss
period: .res 1
count:  .res 1
steplen:.res 1                  ; demi-ondes par palier d'un balayage

        .code

; ---------------------------------------------------------------------------
; tone : A = periode (delai entre deux claquements), X = nombre de demi-ondes
; ---------------------------------------------------------------------------
.proc tone
        sta     period
        stx     count
loop:   lda     SPEAKER         ; claquement
        ldy     period
delay:  dey
        bne     delay
        dec     count
        bne     loop
        rts
.endproc

; ---------------------------------------------------------------------------
; sweep : balaye la periode de A vers X, `steplen` demi-ondes a chaque palier.
; A < X monte vers les graves (chute), A > X descend vers les aigus.
;
; steplen fait la difference entre un coup et une chute : peu de demi-ondes
; par palier donne un transitoire bref -- l'oreille entend un impact et non
; une note -- tandis qu'un palier long fait chanter le balayage.
; ---------------------------------------------------------------------------
.proc sweep
        sta     period
        stx     count           ; periode d'arrivee
        ; Tout appelant de sweep DOIT poser steplen avant : a zero, le
        ; `ldy` chargerait 0 et la boucle ferait 256 tours par palier.
step:   ldy     steplen
:       lda     SPEAKER
        ldx     period
:       dex
        bne     :-
        dey
        bne     :--
        lda     period
        cmp     count
        beq     done
        bcc     up
        dec     period          ; vers l'aigu
        jmp     step
up:     inc     period          ; vers le grave
        jmp     step
done:   rts
.endproc

; --- Un silence long, le temps d'un battement -----------------------------
; Le seul "bruitage" qui ne fait aucun bruit. Les des tombent, on les lit,
; PUIS le coup porte : sans cette respiration les deux annonces apparaissent
; du meme coup de touche et il ne se passe rien -- le joueur lit un resultat
; au lieu d'assister a un assaut.
;
; La machine n'a pas d'horloge et le portage n'a pas de Mockingboard : il ne
; reste que le compte de cycles, comme pour les hauteurs ci-dessus. La boucle
; interne fait 5 cycles (dey/bne) et 256 tours, soit 1 280 cycles ; 160 tours
; externes font environ 206 000 cycles, un cinquieme de seconde a 1,023 MHz.
; Sur //c+ a 4 MHz le battement sera quatre fois plus court -- comme les sons,
; et pour la meme raison.
.proc _sfx_beat
        ldx     #160
outer:  ldy     #0
:       dey
        bne     :-
        dex
        bne     outer
        rts
.endproc

; --- Un silence court, pour detacher deux coups. ---------------------------
.proc gap
        ldx     #40
outer:  ldy     #0
:       dey
        bne     :-
        dex
        bne     outer
        rts
.endproc

; --- Le heros touche ------------------------------------------------------
; Une note pure sonnait comme un bip de terminal. Un balayage tres court vers
; le grave donne un transitoire : l'oreille y entend un choc, pas une note.
.proc _sfx_hit
        php
        sei                     ; le tick de la Mockingboard fausserait la boucle calibree
        lda     #4
        sta     steplen
        lda     #22
        ldx     #60
        jsr     sweep
        plp
        rts
.endproc

; --- Le heros encaisse ----------------------------------------------------
; Deux coups sourds plutot qu'un bourdonnement : le premier est l'impact, le
; second, plus grave, le corps qui accuse.
.proc _sfx_hurt
        php
        sei                     ; le tick de la Mockingboard fausserait la boucle calibree
        lda     #150
        ldx     #26
        jsr     tone
        jsr     gap
        lda     #205
        ldx     #22
        jsr     tone
        plp
        rts
.endproc

; --- Esquive --------------------------------------------------------------
; Deux ticks de hauteurs differentes : deux lames qui se croisent, pas un
; double clic de souris.
.proc _sfx_dodge
        php
        sei                     ; le tick de la Mockingboard fausserait la boucle calibree
        lda     #48
        ldx     #7
        jsr     tone
        jsr     gap
        lda     #38
        ldx     #7
        jsr     tone
        plp
        rts
.endproc

; --- Une creature s'effondre : une chute vers les graves. -------------------
; La plage est courte a dessein : chaque palier coute period*5*12 cycles, et
; balayer 60->200 mettait plus d'une seconde -- une eternite quand la page
; aligne trois BRIGANDS.
.proc _sfx_fall
        php
        sei                     ; le tick de la Mockingboard fausserait la boucle calibree
        lda     #12
        sta     steplen
        lda     #60
        ldx     #140
        jsr     sweep
        jsr     gap
        lda     #235            ; le corps qui touche le sol
        ldx     #30
        jsr     tone
        plp
        rts
.endproc

; --- Mort du heros : la meme chute, plus lente et plus basse. ---------------
; La mort du heros a droit a sa longueur : c'est la fin de la partie.
.proc _sfx_death
        php
        sei                     ; le tick de la Mockingboard fausserait la boucle calibree
        lda     #16             ; paliers plus longs : la chute chante
        sta     steplen
        lda     #90
        ldx     #220
        jsr     sweep
        lda     #255
        ldx     #120
        jsr     tone
        plp
        rts
.endproc
