set title "Recall+Precision vs Number of Posts Collected"

set term pngcairo
set output "rps.png"

plot "rps.dat" using 1:2 title 'Recall' with lines, \
     "rps.dat" using 1:3 title 'Precision' with lines
