#!/bin/bash

pref='https://c.stat100.ameba.jp/vcard/ratio20/images/card/ssr_sample/'
suff='.mp4'

cat UR.txt | while read id 
do
    cd ~/Downloads/mp4
    curl -O -f ${pref}${id}${suff}
done
