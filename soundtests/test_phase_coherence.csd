<CsoundSynthesizer>

<CsInstruments>
sr     = 48000
ksmps  = 1
nchnls = 2
0dbfs  = 1

          instr 1
iamp      =         p4
icps      =         p5

asig      poscil3    iamp, icps
          outs      asig, asig
          endin
</CsInstruments>

<CsScore>
i 1 0 0.1 0.5 200
i 1 1 0.02 0.5 200
i 1 3 0.1 0.5 200
</CsScore>
</CsoundSynthesizer>

