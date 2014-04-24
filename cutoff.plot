set style data histograms
set style histogram rowstacked
set boxwidth 1 relative
set style fill solid 1.0 border -1
set yrange [0:4000]
set datafile separator "\t"
plot 'cutoff.dat' using 2 t "tru-neg", \
     'cutoff.dat' using 3:xticlabels(1) t "fls-neg", \
     'cutoff.dat' using 4:xticlabels(2) t "fls-pos", \
     'cutoff.dat' using 5:xticlabels(3) t "tru-pos"
