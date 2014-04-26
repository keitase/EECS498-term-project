set style data histogram
set style histogram rowstacked
set style fill solid
set boxwidth 0.5
set key invert samplen 0.2
set key samplen 0.2
set bmargin 3
set offset 0,2,0,0

set datafile separator "\t"

set title "Actual vs Predicted Success of Reddit Posts"

set term pngcairo
set output "time.png"

plot newhistogram "Actual" lt 9, \
     'time.dat' index 0 u 2:xtic(1) title "T. Neg", \
     '' index 0 u 3 title "F. Neg", \
     '' index 0 u 4 title "F. Pos", \
     '' index 0 u 5 title "T. Pos", \
     newhistogram "Predicted" lt 9, \
     'time.dat' index 1 u 2:xtic(1) notitle, \
     '' index 1 u 3 notitle, \
     '' index 1 u 4 notitle, \
     '' index 1 u 5 notitle

