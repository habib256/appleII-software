; Fast streaming HGRR loader for Apple IIe Enhanced / cc65.
; int __fastcall__ hgr_rle_load(const char* path);
; Reads 1 KiB chunks and decodes natively to HGR page 1 ($2000-$3FFF).
        .setcpu "65C02"
        .import _fopen, _fread, _fclose, pushax
        .importzp ptr1, ptr2
        .export _hgr_rle_load

HGR_END_HI = $40
CHUNK_SIZE = $0080

        .segment "BSS"
file_ptr:       .res 2
rep_byte:       .res 1
saved_80store:  .res 1
remaining:      .res 2
saved_dst:      .res 2

; Le tampon de lecture vit en RAM basse ($1000-$1FFF, segment LOWBSS de
; scoswamp.cfg) : autant de moins dans la fenetre $4000-$BF00.
;
; 128 octets et non 1 Ko depuis le menu MAP (2026-09-04). ProDOS lit par blocs
; de 512 octets et les met en cache dans SON tampon ($0800) : reduire le notre
; ne change pas le nombre de BLOCS lus, seulement le nombre d'appels a fread --
; 64 au lieu de 8 pour une image de 8 Ko, dont trois sur quatre ne sont qu'une
; recopie depuis le cache. Les 896 octets rendus ont fait place en RAM basse a
; l'etat de l'application, a la memoire des monstres, a la table de rabattement
; page -> clairiere, a la barre de titre et aux lignes de corps, qui ont quitte
; la fenetre principale d'autant.
        .segment "LOWBSS"
packed_data:    .res CHUNK_SIZE

        .segment "RODATA"
read_mode:      .asciiz "rb"
magic:          .byte 'H','G','R','R',1,0,0,$20

        .segment "CODE"

.proc refill
        lda ptr2
        sta saved_dst
        lda ptr2+1
        sta saved_dst+1
        lda #<packed_data
        ldx #>packed_data
        jsr pushax
        lda #1
        ldx #0
        jsr pushax
        lda #<CHUNK_SIZE
        ldx #>CHUNK_SIZE
        jsr pushax
        lda file_ptr
        ldx file_ptr+1
        jsr _fread
        sta remaining
        stx remaining+1
        lda saved_dst
        sta ptr2
        lda saved_dst+1
        sta ptr2+1
        lda #<packed_data
        sta ptr1
        lda #>packed_data
        sta ptr1+1
        lda remaining
        ora remaining+1
        beq empty
        sec
        rts
empty:  clc
        rts
.endproc

.proc get_byte
        phx
        lda remaining
        ora remaining+1
        bne available
        jsr refill
        bcc eof
available:
        lda remaining
        bne dec_low
        dec remaining+1
dec_low:
        dec remaining
        lda (ptr1)
        inc ptr1
        bne got
        inc ptr1+1
got:    plx                    ; PLX écrase N/Z avec le signe de X ;
        pha                    ; on les recharge depuis l'octet lu, sinon le
        pla                    ; `bmi repeat_token` de l'appelant teste X.
        sec                    ; (PLA laisse C intact)
        rts
eof:    plx
        clc
        rts
.endproc

.proc advance_dst
        inc ptr2
        bne ok
        inc ptr2+1
ok:     lda ptr2+1
        cmp #HGR_END_HI
        rts
.endproc

.proc restore_80store
        bit saved_80store      ; bit 7 = 80STORE était actif avant l'image
        bpl :+
        sta $C001              ; le rétablir, sinon le texte 80 col est amputé
:       rts
.endproc

.proc close_fail
        jsr restore_80store
        lda file_ptr
        ldx file_ptr+1
        jsr _fclose
        lda #0
        tax
        rts
.endproc

.proc _hgr_rle_load
        jsr pushax             ; fopen(path, "rb")
        lda #<read_mode
        ldx #>read_mode
        jsr _fopen
        sta file_ptr
        stx file_ptr+1
        ora file_ptr+1
        bne opened
        lda #0
        tax
        rts
opened:
        stz remaining
        stz remaining+1
        ldx #0
header_loop:
        jsr get_byte
        bcc header_fail
        cmp magic,x
        bne header_fail
        inx
        cpx #8
        bne header_loop

        stz ptr2
        lda #$20
        sta ptr2+1
        lda $C018              ; RD80STORE : mémoriser l'état avant de couper
        sta saved_80store
        lda #$20
        sta $C000              ; 80STORE/RAMRD/RAMWRT off
        sta $C002
        sta $C004
next_token:
        lda ptr2+1
        cmp #HGR_END_HI
        beq success
        jsr get_byte
        bcc decode_fail
        bmi repeat_token
        tax
        inx
literal_loop:
        jsr get_byte
        bcc decode_fail
        sta (ptr2)
        jsr advance_dst
        beq literal_advanced
        bcs decode_fail
literal_advanced:
        dex
        bne literal_loop
        bra next_token

repeat_token:
        and #$7F
        clc
        adc #3
        tax
        jsr get_byte
        bcc decode_fail
        sta rep_byte           ; en RAM plutôt que sur la pile : le PLA
repeat_loop:                   ; écrasait le Z posé par advance_dst
        lda rep_byte
        sta (ptr2)
        jsr advance_dst
        beq repeat_advanced
        bcs decode_fail
repeat_advanced:
        dex
        bne repeat_loop
        bra next_token

success:
        jsr restore_80store
        lda file_ptr
        ldx file_ptr+1
        jsr _fclose
        lda #1
        ldx #0
        rts
header_fail:
decode_fail:
        jmp close_fail
.endproc
