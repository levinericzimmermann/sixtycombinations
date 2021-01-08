; super simple csound sampler

sr     = 96000
ksmps  = 1
0dbfs  = 1
nchnls = 1

instr 1
    asig diskin2 p5, 1, p4
    out asig
endin
