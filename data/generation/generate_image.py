from typing import List, Tuple

import cv2
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from .utils import *
from tqdm import tqdm
import random

# Fix Seed
seed_everything(42)

def getLabelFromCSV(filepath: str) -> List[str]:
    """
    Get word list from .csv file
    :param filepath: path to load label file
    :return: list of words
    """
    csv_ = pd.read_csv(filepath)
    return csv_['label'].to_list()


def load_normal_word(data_count, min_length, max_length, word_path: str = '../data/normal') -> List[str]:
    texts = None

    for i in range(min_length, max_length + 1):
        if not(os.path.isfile(os.path.join(word_path, f"word.{i}.txt"))):
            continue

        with open(os.path.join(word_path, f"word.{i}.txt"), 'r', encoding='utf-8') as f:
            data = f.read()
            if texts is None:
                texts = data.split('\n')
            else:
                texts += data.split('\n')
    random.shuffle(texts)
    return texts[:data_count]


def create_hash_text(texts: List[str], enc_type: str = None, max_length: int = -1):
    if len(texts) == 0:
        raise Exception('Origin words must more than 0')

    texts_ = []
    for text_ in texts:
        enc_text = get_enc(text_, enc_type)

        while enc_text[0] == '0':
            enc_text = get_enc(enc_text, enc_type)

        if max_length != -1:
            enc_text = enc_text[:max_length]

        texts_.append(enc_text)
    return texts_


def create_ip_text(data_count, ip_type: str = None, **kwargs) -> List[str]:
    ip_data = []

    print(f'[TEXT GENERATE] CREATE {data_count} {ip_type} texts.')

    for _ in range(data_count):
        ip_ = create_ip(ip_type, **kwargs)

        if ip_[0] == '0':
            continue

        ip_data.append(ip_)
        print(f'[IP GENERATE] : {len(ip_data)} / {data_count}', end='\r')

    ip_data = list(dict.fromkeys(ip_data))
    print(f'[IP GENERATED] : {len(ip_data)} / {data_count}', end='\r')

    while len(ip_data) < data_count:
        ip_ = create_ip(ip_type, **kwargs)

        if ip_[0] == '0':
            continue

        if ip_ not in ip_data:
            ip_data.append(ip_)
            print(f'[IP GENERATED] : {len(ip_data)} / {data_count}', end='\r')

    return ip_data


def create_mac_text(data_count) -> List[str]:
    mac_data = []

    for _ in range(data_count):
        mac_ = create_MAC()

        if mac_[0] == '0':
            continue

        mac_data.append(mac_)
        print(f'[MAC GENERATE] : {len(mac_data)} / {data_count}', end='\r')

    mac_data = list(dict.fromkeys(mac_data))
    print(f'[MAC GENERATED] : {len(mac_data)} / {data_count}', end='\r')

    while len(mac_data) < data_count:
        mac_ = create_MAC()

        if mac_[0] == '0':
            continue

        if mac_ not in mac_data:
            mac_data.append(mac_)
            print(f'[MAC GENERATED] : {len(mac_data)} / {data_count}', end='\r')

    return mac_data


def generate_image(text: str, text_index: int, save_path: str, font_style: dict, is_aa: bool = True, fill_background: Tuple[int, int, int] = (255,255,255), font_color: Tuple[int,int,int] = (0,0,0)):
    (text_width, text_height), _ = cv2.getTextSize(text, font_style['font'], font_style['font_scale'], font_style['thickness'])
    image = np.full(shape=(20, text_width + 1, 3), fill_value=fill_background, dtype=np.uint8)

    textX = (image.shape[1] - text_width) // 2
    textY = (image.shape[0] + text_height) // 2

    line_type = cv2.LINE_AA if is_aa else cv2.LINE_8
    cv2.putText(image, text, (textX, textY), font_style['font'], font_style['font_scale'], font_color, font_style['thickness'], lineType=line_type)

    cv2.imwrite(os.path.join(save_path, f'TEXT_{text_index}.png'), image)

    return None


def main(data_type: str, save_path: str, font_style: dict, data_count: int = 30000, load_from: str = None,
         min_length: int = 3, max_length: int = 10, is_aa: bool = True, fill_background: Tuple[int, int, int] = (255,255,255), font_color: Tuple[int,int,int] = (0,0,0), **kwargs):
    """
    :param data_type: Type of target domain that is in ['normal', 'hash', 'IPv4', 'IPv6', 'MAC'].
    :param data_count: count of generate text images
    :param font_color:
    :param fill_background:
    :param load_from:
    :param max_length:
    :param min_length:
    :param save_path:
    :param font_style:
    :param is_aa:
    :return:
    """

    min_length = max(1, min_length)
    max_length = min(31, max_length)
    texts = None

    # Loading labels from CSV files (for regenration)
    if load_from is not None:
        texts = getLabelFromCSV(load_from)
        data_count = len(texts) + 20
    else:
        data_count += 20

        # ==================== [Get texts] ====================
        if data_type.lower() == 'normal':  # ==================== [Normal Text] ====================
            texts = load_normal_word(data_count, min_length, max_length, '../normal')
        elif data_type.lower() == 'hash':  # ==================== [HASH Text] ====================
            if texts is not None:  # label이 이미 존재하는 경우
                texts = create_hash_text(texts=texts, enc_type=None, max_length=max_length)
            else:  # 텍스트 생성 후 hash 생성
                origin_words = load_normal_word(data_count=data_count, min_length=1, max_length=31, word_path='../normal')
                texts = create_hash_text(texts=origin_words, enc_type=None, max_length=max_length)
        elif data_type.lower() == 'ipv4':  # ==================== [IPv4 Text] ====================
            texts = create_ip_text(data_count, 'ipv4')
        elif data_type.lower() == 'ipv6':  # ==================== [IPv6 Text] ====================
            texts = create_ip_text(data_count, 'ipv6', **kwargs)
        elif data_type.lower() == 'ip':  # ==================== [IP(Mix IPv4, IPv6) Text] ====================
            texts = create_ip_text(data_count)
        elif data_type.lower() == 'mac':  # ==================== [MAC Address Text] ====================
            texts = create_mac_text(data_count)

    save_path_ = save_path
    save_path = os.path.join(save_path, data_type.upper())

    if not os.path.isdir(save_path):
        os.makedirs(save_path)

    print("===================== [GENERATE IMAGE] =====================")

    res_dict = {'filename': [], 'label': []}
    generated_images = 0
    current_index = 0

    with tqdm(total=(data_count-20)) as pbar:
        while generated_images < (data_count - 20):
            text = texts[current_index]
            current_index += 1

            # If upper is not acceptable
            try:
                text = text.upper()
            except:
                continue

            if text[0] == '0':
                continue

            generate_image(text=text, text_index=generated_images, save_path=save_path, font_style=font_style, is_aa=is_aa, fill_background=fill_background, font_color=font_color)

            res_dict['filename'].append(f'TEXT_{generated_images}.png')
            res_dict['label'].append(text)

            generated_images += 1
            pbar.update(1)

    pd.DataFrame(res_dict).to_csv(os.path.join(save_path_,f'{data_type.upper()}.csv'))


if __name__ == '__main__':
    FONT_STYLE = {
        'th': 5,
        'font': cv2.FONT_HERSHEY_SIMPLEX,
        'font_scale': 0.4,
        'thickness': 1
    }

    main(
        data_type='MAC',
        save_path='./generated/mac/',
        font_style=FONT_STYLE,
        data_count=30000,
        is_aa=False,
        short_text=True,
        text_length_range=[9, 14],
        font_color = (255, 255, 255),
        fill_background = (0, 0, 0),
        load_from= None
    )
