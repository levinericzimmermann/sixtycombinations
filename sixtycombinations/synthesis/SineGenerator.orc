; super simple csound sine generator instrument

sr     = 96000
ksmps  = 1
0dbfs  = 1
nchnls = 1

instr 1
    kenv expseg 0.0000001, p6, 1, p3 - (p6 + p7), 1, p7, 0.0000001
    asig poscil3 p5 * kenv, p4
    out asig
endin
