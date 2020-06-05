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
NPULSES=$1
AMP=$2
DUR=$3
MTTXS=$4
MN1P8=$5
MN1P9=$6
TMP=$7
#create appropriate tmp python file

[ -z "$7" ] && $TMP='temp'
echo $TMP

#echo "generating template file: $7"
#sed "
#s/CFGNPULSES/$NPULSES/
#s/CFGAMP/$AMP/
#s/CFGDUR/$DUR/
#s/CFGMTTXS/$MTTXS/
#s/CFGMN1P8/$MN1P8/
#s/CFGMN1P9/$MN1P9/
#" template.py > $7