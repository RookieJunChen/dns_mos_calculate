#!/bin/bash

sig_model_path=''
bak_ovr_model_path=''
data_dir=''
output_dir=''

python dnsmos_local.py \
        --testset_dir $data_dir \
        --csv_path $output_dir \
        --run_name luoxiang_denoise \
        --sig_model_path $sig_model_path \
        --bak_ovr_model_path $bak_ovr_model_path

