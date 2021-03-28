; orchestra file containing all different instruments that are used

; setting general details
sr     = 48000
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
    ifreqStart = p8
    ifreqStop = p9
    iglissandoDuration0 = p10
    iglissandoDuration1 = p11
    kenv linseg 0, iattack, 1, idur - (iattack + irelease), 1, irelease, 0
    kfreq linseg ifreqStart, iglissandoDuration0, ifreq, idur - (iglissandoDuration0 + iglissandoDuration1), ifreq, iglissandoDuration1, ifreqStop
    asig poscil3 iamp * kenv, kfreq
    out asig
endin

; filtered white noise
instr 2
    idur = p3
    ifreq = p4
    iamp = p5
    iattack = p6
    irelease = p7
    ifreqStart = p8
    ifreqStop = p9
    iglissandoDuration0 = p10
    iglissandoDuration1 = p11
    ibandwidth = p12

    kfreq linseg ifreqStart, iglissandoDuration0, ifreq, idur - (iglissandoDuration0 + iglissandoDuration1), ifreq, iglissandoDuration1, ifreqStop

    aSigToAdjust poscil3 iamp, kfreq
    aSig noise 1, 0
    ; aSigFiltered reson aSig, kfreq, ibandwidth, 1
    ; aSigFiltered butterbp aSig, kfreq, ibandwidth, 1
    aSigFiltered resonx aSig, kfreq, ibandwidth, 4
    aSigBalanced balance aSigFiltered, aSigToAdjust

    kenv linseg 0, iattack, 1, idur - (iattack + irelease), 1, irelease, 0

    out aSigBalanced * kenv
endin
