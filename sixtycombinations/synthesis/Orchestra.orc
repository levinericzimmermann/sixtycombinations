; orchestra file containing all different instruments that get used

sr     = 96000
ksmps  = 1
0dbfs  = 1
nchnls = 1

instr 1
    ; kenv expseg 0.0000001, p6, 1, p3 - (p6 + p7), 1, p7, 0.0000001
    ; linseg works better than expseg (empirical statement)
    kenv linseg 0, p6, 1, p3 - (p6 + p7), 1, p7, 0
    asig poscil3 p5 * kenv, p4
    out asig
endin


instr 2
    kenv linseg 0, p6, 1, p3 - (p6 + p7), 1, p7, 0
    asig noise kenv, p4
    out asig
endin
