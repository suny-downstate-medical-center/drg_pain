#!bin/bash

bash gen_tmp.sh 30 0.3 5 1.0 1.0 1.0 freqtmp

#iterate and run processes
for freq in 25 23 21 19 17 15 13 11 9 7 5
do
    echo "freq: $freq Hz"
    sed "s/CFGFREQ/$freq/" freqtmp | sed "s/CFGSIMLABEL/freq$freq" > cfg.py
    python init.py
done
#clean up
