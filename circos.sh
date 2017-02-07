#!/bin/bash
blast=$1
for i in $(awk '{print $1}' $blast | sort | uniq); do
    grep -w "^$i" $blast >  aux
    python circos.py aux $i
    ~/circos/bin/circos -conf circos.conf
    mv circos.png "./images/"$i".png"
done
