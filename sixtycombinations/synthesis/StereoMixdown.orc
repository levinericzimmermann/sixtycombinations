; simple csound sampler for stereo mixdown

sr     = 96000
ksmps  = 1
0dbfs  = 1
nchnls = 2

instr 1
    asig diskin2 p4, 1
    aSigL  =     asig * sin((p5 + 0.5) * $M_PI_2)
    aSigR  =     asig * cos((p5 + 0.5) * $M_PI_2)
    outs aSigL, aSigR
endin
