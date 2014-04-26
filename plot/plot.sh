#!/bin/bash
#set -o nounset # way to shit the bed, virtualenv...
set -o errexit

cd ${0%/*} # god this bash stuff is so stupid. cd to script's directory

rm -f tosplit.dat
touch tosplit.dat

source ../venv/bin/activate

for cutoff in {1,2,3,50,100}
do
    echo $cutoff
    ../venv/bin/python ../classify.py --posts t --cutoff $cutoff --dat >> tosplit.dat
done

./split_dat.sh

gnuplot cutoff.plot
