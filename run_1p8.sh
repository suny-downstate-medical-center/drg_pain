#!bin/bash

#create appropriate tmp python file
echo "generating freqtmp.py file"
for CNDCT in 1.0 1.2 1.4 1.6 1.8 2.0
do
    bash gen_tmp.sh 30 0.3 5 1.0 ${CNDCT} 1.0 > mn1p8tmp
    for FREQ in 25 23 21 19 17 15 13 11 9 7 5
    do
        echo "TESTING: cndct: ${CNDCT}, freq: ${FREQ} Hz"
        sed "s/CFGFREQ/${FREQ}/; s/CFGSIMLABEL/mn1p9${CNDCT}freq${FREQ}" mn1p8tmp > cfg.py
        python init.py
    done
done

#iterate and run processes
#clean up
rm freqtmp.py
