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
sed "s/CFGNPULSES/$NPULSES/" template.py | sed "s/CFGAMP/$AMP/" | sed "s/CFGDUR/$DUR/" | sed "s/CFGMTTXS/$MTTXS/" | sed "s/CFGMN1P8/$MN1P8/" | sed "s/CFGMN1P9/$MN1P9/" > freqtmp.py
#iterate and run processes
for freq in 25, 23, 21, 19, 17, 15, 13, 11, 9, 7, 5
do
    echo "freq: $freq Hz"
    sed "s/CFGFREQ/$freq/" freqtmp.py > cfg.py
    sed "s/CFGSIMLABEL/freq$freq"
    python init.py
done
#clean up
rm freqtmp.py
