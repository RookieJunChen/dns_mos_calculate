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


def get_the_same(str_list1, str_list2):
    depart1 = []
    depart2 = []
    same_str_1 = []
    same_str_2 = []
    for str in str_list1:
        filename = str.split(' ')[0]
        depart1.append((filename, str))
    for str in str_list2:
        filename = str.split(' ')[0]
        depart2.append((filename, str))
    for filename, totalstr in depart1:
        for filename2, totalstr2 in depart2:
            if filename == filename2:
                same_str_1.append(totalstr)
                same_str_2.append(totalstr2)
    return same_str_1, same_str_2


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


file_name1 = "C:/Users/thujunchen/Desktop/SE工作/DNSMOS/noisy_no_neighbor/file_mos.txt"
file_name2 = "C:/Users/thujunchen/Desktop/SE工作/DNSMOS/yukai_11_no_neighbor/file_mos.txt"
counter = 1500
list1 = read_from_txt(file_name1, counter)
list2 = read_from_txt(file_name2, counter)

same_str_1, same_str_2 = get_the_same(list1, list2)

SIG, BAK, OVR = get_score(same_str_1)
print(file_name1 + " " + "SIG={}, BAK={}, OVR={}".format(SIG, BAK, OVR))
SIG, BAK, OVR = get_score(same_str_2)
print(file_name2 + " " + "SIG={}, BAK={}, OVR={}".format(SIG, BAK, OVR))
# SIG, BAK, OVR = get_score(read_from_txt(file_name, counter))
# print("SIG={}, BAK={}, OVR={}".format(SIG, BAK, OVR))
