#!/bin/bash
awk 'NR % 2 == 1' tosplit.dat > actual.dat
awk 'NR % 2 == 0' tosplit.dat > predict.dat

echo "" >> actual.dat
echo "" >> actual.dat
cat actual.dat predict.dat > cutoff3.dat
