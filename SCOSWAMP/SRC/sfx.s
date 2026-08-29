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

SPEAKER = $C030

        .bss
period: .res 1
count:  .res 1

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
; sweep : balaye la periode de A vers X, quelques demi-ondes a chaque palier.
; A < X monte vers les graves (chute), A > X descend vers les aigus.
; ---------------------------------------------------------------------------
.proc sweep
        sta     period
        stx     count           ; periode d'arrivee
step:   ldy     #12             ; demi-ondes par palier
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

; --- Le heros touche : un claquement bref et haut, sec comme une lame. ------
.proc _sfx_hit
        lda     #40
        ldx     #90
        jmp     tone
.endproc

; --- Le heros encaisse : plus grave et plus long, un coup sourd. ------------
.proc _sfx_hurt
        lda     #170
        ldx     #70
        jmp     tone
.endproc

; --- Esquive : deux clics tres courts, rien de plus. ------------------------
.proc _sfx_dodge
        lda     #70
        ldx     #6
        jsr     tone
        ldy     #100            ; un silence entre les deux
:       dey
        bne     :-
        lda     #70
        ldx     #6
        jmp     tone
.endproc

; --- Une creature s'effondre : une chute vers les graves. -------------------
; La plage est courte a dessein : chaque palier coute period*5*12 cycles, et
; balayer 60->200 mettait plus d'une seconde -- une eternite quand la page
; aligne trois BRIGANDS.
.proc _sfx_fall
        lda     #60
        ldx     #140
        jmp     sweep
.endproc

; --- Mort du heros : la meme chute, plus lente et plus basse. ---------------
; La mort du heros a droit a sa longueur : c'est la fin de la partie.
.proc _sfx_death
        lda     #90
        ldx     #220
        jsr     sweep
        lda     #255
        ldx     #120
        jmp     tone
.endproc
