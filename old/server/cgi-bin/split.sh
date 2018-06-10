#!/bin/sh

cd /home/oeplse/html/data/
head -n -1 LOG.CSV > TEMP.CSV
cp TEMP.CSV LOG.CSV
awk '/^millis/{close("file"f);f++}{print $0 > "file"f}' LOG.CSV
rm TEMP.CSV LOG.CSV
cd /home/oeplse/cgi-bin
