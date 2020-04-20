#!/bin/bash

# Set the number of threads to 1
export OMP_NUM_THREADS=1
export PROC_COUNT=1
export PWSCF_SCRATCH=/opt/scratch
export PWSCF_PP=/opt/pp
export PWSCF_CACHE=/opt/pwscf_cache
export PWSCF_BIN=/opt/qe/bin/pw.x


thisdir=$(pwd)
echo $thisdir
cd ../../
topdir=$(pwd)
echo $topdir
./package.sh
cd $thisdir
python3 $topdir/qeforfit.py input.in

