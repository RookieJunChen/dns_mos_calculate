#!/bin/bash

source_dir='/dockerdata/thujunchen/dataset/ft_local/noisy_testclips'
dest_dir='/dockerdata/thujunchen/dataset/noisy'


neighbor_files=$(find $source_dir | grep "neighbor")
no_neighbor_files=$(find $source_dir | grep -v "neighbor")
neighbor_dir='/neighbor'
no_neighbor_dir='/no_neighbor'

neighbor=$dest_dir$neighbor_dir
mkdir $neighbor
for file in $neighbor_files
do
    cp $file $neighbor
    echo "cp $file $neighbor"
done

no_neighbor=$dest_dir$no_neighbor_dir
mkdir $no_neighbor
for file in $no_neighbor_files
do 
    cp $file $no_neighbor
    echo "cp $file $no_neighbor"
done


