from constant.os import *
from utils.os import *
from utils.sound import *

import os
from typing import Optional
import sox
import wave
import numpy as np


def get_sample_rate(file_path: str):
    """
    wav 파일의 sample rate를 추출

    Parameters:
        file_path: sample rate를 확인 할 파일의 경로

    Returns:
        파일의 sample rate를 반환한다.
        PCM과 같은 이유로 분석할 수 없는 파일은 na를 반환한다.
    """
    try:
        with wave.open(file_path, 'rb') as wav_in:
            sample_rate = wav_in.getframerate()
            return sample_rate
    except:
        return np.nan


def resampling(file_path_list: list[str], output_path: Optional[str] = None, target_sample_rate: int = 16000):
    """
    Change sample rate

    Before start:

        sox를 설치하여야 아래 함수를 수행할 수 있다.

        OS X: brew install sox

        linux: apt-get install sox

        windows: exe 파일을 다운받아 실행: https://sourceforge.net/projects/sox/files/sox/14.4.1/

    Parameters:
        file_path_list: 변환하고자 하는 wav 파일 리스트

        output_path: 변환된 결과물을 저장하고자 하는 폴더 경로. 없을 경우 변환된 파일로 기존 파일을 대치한다.

        target_sample_rate: 변환하고자 하는 sample rate

    Returns: None
    """

    __output_path = output_path
    if __output_path == None:
        __output_path = os.path.join(
            main_path, 'baby-cry-classification-resampling-temp-folder')
        if os.path.exists(__output_path):
            remove_path_with_files(__output_path)
        os.mkdir(__output_path)
    else:
        if not os.path.exists(__output_path):
            raise OSError(f'Output path {__output_path} not exist')

    tfm = sox.Transformer()
    tfm.convert(samplerate=target_sample_rate)

    for file_path in file_path_list:
        if not os.path.exists(file_path):
            raise OSError(f'File {file_path} not exist')

        file = file_path.rsplit('/', 1)[1]
        output_file_path = os.path.join(__output_path, file)

        tfm.build(file_path, output_file_path)

        if output_path == None:
            remove_file(file_path)
            move_file(output_file_path, file_path)

    if output_path == None:
        remove_path_with_files(__output_path)


def is_same_sample_rate(file_path_list: list[str], target_sample_rate: int):
    """
    파일 리스트의 sample rate가 target_sample_rate와 동일한지 확인한다.

    Parameters:
        file_path_list: 확인하고자 하는 파일의 경로가 담긴 리스트
        target_sample_rate: 확인하고자 하는 sample rate 값.

    Returns:
        모든 파일의 sample rate가 target_sample_rate와 일치할 경우 True를
        그렇지 않을 경우 False를 반환한다.
    """
    sample_rate_set = list(set([get_sample_rate(file_path)
                           for file_path in file_path_list]))

    if len(sample_rate_set) == 1 and sample_rate_set[0] == target_sample_rate:
        return True
    return False


if __name__ == '__main__':
    import sys
    sys.path.append(
        '/Users/jaewone/developer/tensorflow/baby-cry-classification')

    file_list = []
    filee_folder = ''

    resampling(
        file_path_list=[os.path.join(filee_folder, file)
                        for file in file_list],
        # output_path = os.path.join(main_path, 'test2'),
        target_sample_rate=16000
    )

    if is_same_sample_rate([os.path.join(filee_folder, file) for file in file_list], 16000):
        print(f'존재하는 sample rate는 16000 뿐이다.')
