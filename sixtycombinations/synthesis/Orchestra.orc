; orchestra file containing all different instruments that get used

sr     = 96000
ksmps  = 1
0dbfs  = 1
nchnls = 1

; simple sine oscillator
instr 1
    ; kenv expseg 0.0000001, p6, 1, p3 - (p6 + p7), 1, p7, 0.0000001
    ; linseg works better than expseg (empirical statement)
    idur = p3
    ifreq = p4
    iamp = p5
    iattack = p6
    irelease = p7
    kenv linseg 0, iattack, 1, idur - (iattack + irelease), 1, irelease, 0
    asig poscil3 iamp * kenv, ifreq
    out asig
endin

; filtered white noise
instr 2
    idur = p3
    ifreq = p4
    iamp = p5
    iattack = p6
    irelease = p7
    ibandwidth = p8

    aSigToAdjust poscil3 iamp, ifreq
    aSig noise 1, 0
    aSigFiltered reson aSig, ifreq, ibandwidth, 1
    ; aSigFiltered resonr aSig, ifreq, ibandwidth, 1
    aSigBalanced balance aSigFiltered, aSigToAdjust

    kenv linseg 0, iattack, 1, idur - (iattack + irelease), 1, irelease, 0

    out aSigBalanced * kenv
endin
