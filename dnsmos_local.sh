#!/bin/bash

data_dir='/dockerdata/thujunchen/enhance_data/dns4_testclips/dnsmos/fscanet/enhanced_0296'
output_dir='./df2_woenhance_woschdule_wreverb'

python dnsmos_local.py \
        --testset_dir $data_dir \
        --csv_path $output_dir