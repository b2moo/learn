#!/bin/bash

# This file generates the data for the plots of figure 7 of the article

# Official parameters (K for K-parameterized experiments, D for dimension parameterized
# experiments
KPARAMS="50 100 150 200 250 300 350 400 450 500"
DPARAMS="3 4 5 10 50 100 200"

# dia-r (This is K Diagonal Restricted in the paper)
# dia-u (This is K Diagonal Unrestricted in the paper)
# big-c (This is K Big Overlapping Cube in the paper)
# k-cubes (This is K cubes in Z^d in the paper)
# k-dia (This is K Diagonal in the paper)
# mondec (This is Example 2 in the paper)
BENCHMARKS="dia-r dia-u big-c k-cubes k-dia mondec"

parseout() {
    sed "s/Total time needed: *\(.*\)/\1/; t; d"
}

# Clean the generated data
clean() {
  echo "Cleaning generated data";
  for bench in $BENCHMARKS
  do
    echo "clean $bench"
    cat reference_data/$bench.dat | head -n 1 > generated/$bench.dat
  done
}

if [ -z "$1" ]; then
    echo "USAGE: $0 [clean|all|$BENCHMARKS] [PARAM]"
    exit 1
elif [ "$1" = "clean" ]; then
   clean
fi
