set style data histograms
set style histogram rowstacked
set boxwidth 1 relative
set style fill solid 1.0 border -1
set yrange [0:1.5]
set datafile separator " "
plot 'internet.dat' using 2 t "Var 1", '' using 3:xticlabels(1) t "Var 2"
