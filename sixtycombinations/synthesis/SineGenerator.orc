; super simple csound sine generator instrument

sr     = 96000
ksmps  = 1
0dbfs  = 1
nchnls = 1

instr 1
    asig poscil3 p5, p4
    out asig
endin
