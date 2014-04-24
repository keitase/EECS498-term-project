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

set term postscript color
set output "plot2.ps"

plot newhistogram "Actual" lt 9, \
     'cutoff3.dat' index 0 u 2:xtic(1) title "True Neg", \
     '' index 0 u 3 title "False Neg", \
     '' index 0 u 4 title "False Pos", \
     '' index 0 u 5 title "True Pos", \
     newhistogram "Predicted" lt 9, \
     'cutoff3.dat' index 1 u 2:xtic(1) notitle, \
     '' index 1 u 3 notitle, \
     '' index 1 u 4 notitle, \
     '' index 1 u 5 notitle

