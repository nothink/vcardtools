#!/bin/bash

pref='https://c.stat100.ameba.jp/vcard/ratio20/images/card/gif/320/'
suff='.gif'

cat UR.txt | while read id 
do
    cd ~/Downloads/gif/320
    curl -O -f ${pref}${id}${suff}
done
