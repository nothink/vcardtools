#!/bin/bash

pref='https://c.stat100.ameba.jp/vcard/ratio20/images/card/gif/frame/'
suff='.png'

cat UR.txt | while read id 
do
    cd ~/Downloads/gif/frame
    curl -O -f ${pref}${id}${suff}
done
