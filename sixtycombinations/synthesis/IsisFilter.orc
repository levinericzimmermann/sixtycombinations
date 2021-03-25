; filter singing synthesis files by sine tone data

; setting general details
sr     = 96000
ksmps  = 1
0dbfs  = 1
nchnls = 1 

; init of global values
gaSample = 0


; sample player
instr 1
    gaSample diskin2 p4, 1, 0
endin

; filter instrument
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

    ; aSigToAdjust poscil3 iamp, kfreq
    ; aSigToAdjust poscil3 0.2, kfreq
    aSigFiltered resonx gaSample, kfreq, ibandwidth, 2
    ; aSigBalanced balance aSigFiltered, aSigToAdjust
    aSigBalanced balance aSigFiltered, gaSample

    kenv linseg 0, iattack, 1, idur - (iattack + irelease), 1, irelease, 0

    out aSigBalanced * kenv
endin
