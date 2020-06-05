#!bin/bash

#cfg.freq = CFGFREQ
#cfg.npulses = CFGNPULSES
#cfg.amp = CFGAMP
#cfg.dur = CFGDUR
#cfg.mttxs = CFGMTTXS
#cfg.mn1p8 = CFGMN1P8
#cfg.mn1p9 = CFGMN1P9
#cfg.simLabel = 'CFGSIMLABEL'


#CFGFREQ='5'
NPULSES='30'
AMP='0.3'
DUR='5'
MTTXS='1.0'
MN1P8='1.0'
MN1P9='1.0'
#create appropriate tmp python file
echo "generating freqtmp.py file"
for CNDCT in 1.0 1.2 1.4 1.6 1.8 2.0
do
    bash gen_tmp 30 0.3 5 1.0 1.0 ${CNDCT} > mn1p9tmp
    for FREQ in 25 23 21 19 17 15 13 11 9 7 5
    do
        echo "TESTING: cndct: ${CNDCT}, freq: ${FREQ} Hz"
        sed "s/CFGFREQ/${FREQ}/; s/CFGSIMLABEL/mn1p9${CNDCT}freq${FREQ}" mn1p9tmp > cfg.py
        python init.py
    done
done

#iterate and run processes
#clean up
rm freqtmp.py
