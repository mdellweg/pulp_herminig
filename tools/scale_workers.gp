clear

set term post color size 8.0, 6.0
set out "scale_workers.eps"

set xlabel "# Workers"

set log
set xtics nomirror scale 1, 0 2
unset x2tics
set ytics nomirror
unset y2tics
set style data points

set pointsize 3

f1(x) = a1 + b1 * x
g1(x) = c1 + d1 * x
f2(x) = a2 + b2 * x
g2(x) = c2 + d2 * x

fit f1(x) 'old_workers.dat' u (log($7)):(log($2*1e-9/$1)) via a1, b1
fit g1(x) 'old_workers.dat' u (log($7)):(log($5)) via c1, d1
fit f2(x) 'new_workers.dat' u (log($7)):(log($2*1e-9/$1)) via a2, b2
fit g2(x) 'new_workers.dat' u (log($7)):(log($5)) via c2, d2

set multiplot layout 2, 1 title "Tasking system benchmark (Burst 256 tasks)"

set key left top
set ylabel "avg dispatch time (s)"
set yrange [0.01 : 0.1]
plot \
  'old_workers.dat' u 7:($2*1e-9/$1) axes x1y1 title "old tasking system", \
  'new_workers.dat' u 7:($2*1e-9/$1) axes x1y1 title "new tasking system", \
  exp(f1(log(x))) axes x1y1 notitle ls 1 lw 4, \
  exp(f2(log(x))) axes x1y1 notitle ls 2 lw 4

set key left bottom
set ylabel "avg service time (s)"
set yrange [0.01 : 100]
plot \
  'old_workers.dat' u 7:5 axes x1y2 title "old tasking system", \
  'new_workers.dat' u 7:5 axes x1y2 title "new tasking system", \
  exp(g1(log(x))) axes x1y1 notitle ls 1 lw 4, \
  exp(g2(log(x))) axes x1y1 notitle ls 2 lw 4

unset multiplot
