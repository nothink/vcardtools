#!/bin/bash

pref='https://c.stat100.ameba.jp/vcard/ratio20/images/card/ssr_sample/poster/'
suff='.png'

cat UR.txt | while read id 
do
    cd ~/Downloads/poster
    curl -O -f ${pref}${id}${suff}
done
