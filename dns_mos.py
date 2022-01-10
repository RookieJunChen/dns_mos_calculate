import argparse
import glob
import json
import os

import numpy as np
import pandas as pd
import requests
import soundfile as sf
import librosa

from urllib.parse import urlparse, urljoin

# URL for the web service
SCORING_URI_DNSMOS = 'https://dnsmos.azurewebsites.net/score'
SCORING_URI_DNSMOS_P835 = 'https://dnsmos.azurewebsites.net/v1/dnsmosp835/score'
# If the service is authenticated, set the key or token
AUTH_KEY = 'd3VoYW4tdW5pdjpkbnNtb3M='

# Set the content type
headers = {'Content-Type': 'application/json'}
# If authentication is enabled, set the authorization header
headers['Authorization'] = f'Basic {AUTH_KEY}'


def main(args):
    # args.testset_dir = [r'C:\Users\cyrillv\Desktop\谱修复样例及DNSMOS指标\test_data\online_samples\gate_unet_skipcnn_sisnr_epoch16']
    # args.score_file = [r'./online_samples/gate_unet_skipcnn_sisnr_epoch16/score.csv']

    # args.testset_dir = [
    #     r'C:\Users\cyrillv\Desktop\谱修复样例及DNSMOS指标\test_data\online_samples\gate_unet_mini_rt_stcm_SeparableConv2d_mini_speccompress_sisnr_compressmse_batchnorm_epoch23', \
    #     r'C:\Users\cyrillv\Desktop\谱修复样例及DNSMOS指标\test_data\online_samples\gate_unet_mini_rt_stcm_SeparableConv2d_mini_speccompress_sisnr_compressmse_track_true_epoch19', \
    #     r'C:\Users\cyrillv\Desktop\谱修复样例及DNSMOS指标\test_data\online_samples\gate_unet_mini_rt_stcm_Separableonv2d_mini_speccompress_sisnr_compressmse_mini_v2_epoch28', \
    #     r'C:\Users\cyrillv\Desktop\谱修复样例及DNSMOS指标\test_data\online_samples\gate_unet_mini_rt_stcm_Separableonv2d_mini_speccompress_sisnr_compressmse_mini_epoch27']
    #
    # args.score_file = [
    #     r'./online_samples/gate_unet_mini_rt_stcm_SeparableConv2d_mini_speccompress_sisnr_compressmse_batchnorm_epoch23/score.csv', \
    #     r'./online_samples/gate_unet_mini_rt_stcm_SeparableConv2d_mini_speccompress_sisnr_compressmse_track_true_epoch19/score.csv', \
    #     r'./online_samples/gate_unet_mini_rt_stcm_Separableonv2d_mini_speccompress_sisnr_compressmse_mini_v2_epoch28/score.csv', \
    #     r'./online_samples/gate_unet_mini_rt_stcm_Separableonv2d_mini_speccompress_sisnr_compressmse_mini_epoch27/score.csv']

    args.testset_dir = [
        r'D:\数据集\noisy\neighbor',
        r'D:\数据集\noisy\no_neighbor']

    args.score_file = [
        r'./noisy_neighbor/score.csv',
        r'./noisy_no_neighbor/score.csv']

    for idx in range(len(args.testset_dir)):
        print(args.testset_dir[idx])
        audio_clips_list = glob.glob(os.path.join(args.testset_dir[idx], "*.wav"))  # glob：搜索列表中符合的文件，返回列表
        print(audio_clips_list)
        scores = []
        dir_path = args.score_file[idx].split('score.csv')[0]
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        if not os.path.exists(os.path.join(dir_path, 'file_mos.txt')):
            f = open(os.path.join(dir_path, 'file_mos.txt'), 'w')
            dict = {}
        else:
            f = open(os.path.join(dir_path, 'file_mos.txt'), 'r')
            dict = {}
            lines = f.readlines()
            for line in lines:
                utt_id = line.split('.wav')[0]
                # print('utt_id store', utt_id)
                dict[utt_id] = 1
        flag = 0
        for fpath in audio_clips_list:

            utt_id = fpath.split('\\')[-1].split('.wav')[0]
            # print('utt_id', utt_id)
            if utt_id in dict:
                # print('find uttid', utt_id)
                continue
            flag = 1
            f = open(os.path.join(dir_path, 'file_mos.txt'), 'a+')
            audio, fs = sf.read(fpath)
            if fs != 16000:
                audio = librosa.resample(audio, fs, target_sr=16000)
                print('Only sampling rate of 16000 is supported as of now')
            data = {"data": audio.tolist(), "filename": os.path.basename(fpath)}
            input_data = json.dumps(data)
            # Make the request and display the response
            if args.method == 'p808':
                u = SCORING_URI_DNSMOS
            else:
                u = SCORING_URI_DNSMOS_P835
            try_flag = 1
            while try_flag:
                try:
                    resp = requests.post(u, data=input_data, headers=headers, timeout=50)
                    try_flag = 0
                    score_dict = resp.json()
                except:
                    try_flag = 1
                    print('retry')
            score_dict['file_name'] = os.path.basename(fpath)
            if args.method == 'p808':
                f.write(score_dict['file_name'] + ' ' + str(score_dict['mos']) + '\n')
                print(score_dict['mos'], ' ', score_dict['file_name'])
            else:
                f.write(score_dict['file_name'] + ' SIG[{}], BAK[{}], OVR[{}]'.format(score_dict['mos_sig'],
                                                                                      score_dict['mos_bak'],
                                                                                      score_dict['mos_ovr']) + '\n')
                print(score_dict['file_name'] + ' SIG[{}], BAK[{}], OVR[{}]'.format(score_dict['mos_sig'],
                                                                                      score_dict['mos_bak'],
                                                                                      score_dict['mos_ovr']))
            f.close()

            scores.append(score_dict)
        if flag:
            df = pd.DataFrame(scores)
            if args.method == 'p808':
                print('Mean MOS Score for the files is ', np.mean(df['mos']))
            else:
                print('Mean scores for the files: SIG[{}], BAK[{}], OVR[{}]'.format(np.mean(df['mos_sig']),
                                                                                    np.mean(df['mos_bak']),
                                                                                    np.mean(df['mos_ovr'])))

            if args.score_file[idx]:
                df.to_csv(args.score_file[idx])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--testset_dir",
                        default=r'C:\Users\cyrillv\Desktop\谱修复样例及DNSMOS指标\test_data\谱修复测试集_yuanjun\noisy',
                        help='Path to the dir containing audio clips to be evaluated')
    parser.add_argument('--score_file', default=r'./谱修复测试集_yuanjun/noisy/score.csv',
                        help='If you want the scores in a CSV file provide the full path')
    parser.add_argument('--method', default='p808', const='p808', nargs='?', choices=['p808', 'p835'],
                        help='Choose which method to compute P.808 or P.835. Default is P.808')
    args = parser.parse_args()
    main(args)
