import re
import numpy as np


def read_from_txt(filename, counter):
    str_list = []
    with open(filename, "r") as f:
        for line in f.readlines():
            if counter == 0:
                break
            # line = line.split('\n')
            str_list.append(line)
            counter = counter - 1
        f.close()
    return str_list


def get_score(str_list):
    sig_list = []
    bak_list = []
    ovr_list = []
    number_format = re.compile(r"(\d)+.(\d)*")
    sig_format = re.compile(r"SIG\[(\d)+.(\d)*\]")
    bak_format = re.compile(r"BAK\[(\d)+.(\d)*\]")
    ovr_format = re.compile(r"OVR\[(\d)+.(\d)*\]")
    for str in str_list:
        sig_result = (sig_format.search(str)).group(0)
        sig_number = float((number_format.search(sig_result)).group(0))
        sig_list.append(sig_number)
        bak_result = (bak_format.search(str)).group(0)
        bak_number = float((number_format.search(bak_result)).group(0))
        bak_list.append(bak_number)
        ovr_result = (ovr_format.search(str)).group(0)
        ovr_number = float((number_format.search(ovr_result)).group(0))
        ovr_list.append(ovr_number)
        # print(number.group(0))
    return np.mean(sig_list), np.mean(bak_list), np.mean(ovr_list)


file_name = "C:/Users/thujunchen/Desktop/SE工作/DNSMOS/weixin_neighbor/file_mos.txt"
counter = 58
SIG, BAK, OVR = get_score(read_from_txt(file_name, counter))
print("SIG={}, BAK={}, OVR={}".format(SIG, BAK, OVR))
