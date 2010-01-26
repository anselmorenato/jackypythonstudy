#!/bin/bash

MDEXEC1=$AMBERHOME/exe/sander.MPI
MDEXEC2=$AMBERHOME/exe/pmemd
MPIEXEC="mpijob mpirun"

cp ../2pre/system.prmtop ./
cp ../4equ/equ.rst ./

# sampling MD : 1ns - 21ns
cp equ.rst  sam00.rst
for i in `seq 1 20`
do
    NUM_NEW=`printf "%02d" $i`
    NUM_OLD=`expr $i - 1`
    NUM_OLD=`printf "%02d" $NUM_OLD`
    $MPIEXEC \
    $MDEXEC2 -O -i sam.inp \
                -p system.prmtop \
                -c sam$NUM_OLD.rst \
                -o sam$NUM_NEW.out \
                -r sam$NUM_NEW.rst \
                -x sam$NUM_NEW.mdcrd \
                -e sam$NUM_NEW.ene

    gzip sam$NUM_NEW.mdcrd
done
cp sam$NUM_NEW.rst sam.rst

