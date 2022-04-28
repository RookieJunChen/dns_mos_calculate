# README

Code to calculate DNS_MOS score by calling the dns_mos interface provided by Microsoft.


## Usage

### Online
Modify the `testset_dir` and `score_file` in the code.

Then:

```shell
python dns_mos.py
```

### Offline
```shell
python dnsmos_local.py \
  --sig_model_path $Path_of_sig.onnx \
  --bak_ovr_model_path $Path_of_bak_ovr.onnx \
  --testset_dir $Testset_dir \
  --csv_path $Result_path \
  --run_name $NAME
```
