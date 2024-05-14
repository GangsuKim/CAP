"""
암호화 문자열, IP Address, MAC Address 생성
"""
import random
import hashlib
from typing import List
import os


def load_normal_word(data_count: int, min_length: int, max_length: int, word_path: str = '../data/normal') -> List[str]:
    """
    Load NORMAL (natural word) data from word collections
    :param data_count: Count of data
    :param min_length: Minimum length of texts
    :param max_length: Minimum length of texts
    :param word_path: Path of word collection
    :return:
    """
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


def create_hash_text(texts: List[str], enc_type: str = None, max_length: int = -1) -> List[str]:
    """
    Create hexadecimal dataset using NORMAL data
    :param texts: NORMAL words
    :param enc_type: Type of encryption method. If not, will be random generate.
    :param max_length: Max length of each text
    :return: List of hexadecimal words

    - Type of Encrypt : 'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512'
    """
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



def get_enc(enc_text: str, enc_type: str = None):
    """
    get encrypted text

    Args:
        enc_text: text to encrypt
        enc_type: type of encrypt

    - Type of Encrypt : 'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512'

    Returns: encrypted text

    """
    encode_text = enc_text.encode('utf-8')

    if enc_type is None: enc_type = random.choice(['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512'])

    password_hash = hashlib.new(enc_type)
    password_hash.update(encode_text)

    return password_hash.hexdigest()


def create_ip_text(data_count: int, ip_type: str = None, verbose: bool = True, **kwargs) -> List[str]:
    ip_data = []

    if verbose:
        print(f'[TEXT GENERATE] CREATE {data_count} {ip_type} texts.')

    for _ in range(data_count):
        ip_ = create_ip(ip_type, **kwargs)

        if ip_[0] == '0':
            continue

        ip_data.append(ip_)
        if verbose:
            print(f'[IP GENERATE] : {len(ip_data)} / {data_count}', end='\r')

    ip_data = list(dict.fromkeys(ip_data))  # 리스트 값들을 key 로 변경
    if verbose:
        print(f'[IP GENERATED] : {len(ip_data)} / {data_count}', end='\r')

    while len(ip_data) < data_count:
        ip_ = create_ip(ip_type, **kwargs)

        if ip_[0] == '0':
            continue

        if ip_ not in ip_data:
            ip_data.append(ip_)
            if verbose:
                print(f'[IP GENERATED] : {len(ip_data)} / {data_count}', end='\r')

    return ip_data


def create_ip(ip_type: str = None, short_text: bool = False, text_length_range: List[int] = None):
    if ip_type is None: ip_type = random.choice(['ipv4', 'ipv6'])

    if ip_type == 'ipv4':
        li = [str(random.randint(0, 255)) for _ in range(4)]
        res = '.'.join(li)
    elif ip_type == 'ipv6':
        li = []
        for _ in range(8):
            end_len = random.choice([2, 3, 4, 5, 6])
            li += [hex(random.randint(0, 4 ** 8 - 1))[2:end_len]]
        res = ':'.join(li)

        if short_text:
            text_len = random.choice(text_length_range)
            res = res[:text_len]

    else:
        raise Exception(f'Type of {ip_type} is not supportable')

    return res


def create_mac_text(data_count: int, verbose: bool = True) -> List[str]:
    mac_data = []

    for _ in range(data_count):
        mac_ = create_MAC()

        if mac_[0] == '0':
            continue

        mac_data.append(mac_)
        if verbose:
            print(f'[MAC GENERATE] : {len(mac_data)} / {data_count}', end='\r')

    mac_data = list(dict.fromkeys(mac_data))  # 리스트 값들을 key 로 변경
    if verbose:
        print(f'[MAC GENERATED] : {len(mac_data)} / {data_count}', end='\r')

    while len(mac_data) < data_count:
        mac_ = create_MAC()

        if mac_[0] == '0':
            continue

        if mac_ not in mac_data:
            mac_data.append(mac_)
            if verbose:
                print(f'[MAC GENERATED] : {len(mac_data)} / {data_count}', end='\r')

    return mac_data


def create_MAC(mode: int = 0):
    if mode == 0: mode = random.randint(1, 3)

    res = ''

    if mode == 1:
        res = '-'.join([hex(random.randint(0, 16 - 1))[2:] + hex(random.randint(0, 16 - 1))[2:] for _ in range(6)])
    elif mode == 2:
        res = ':'.join([hex(random.randint(0, 16 - 1))[2:] + hex(random.randint(0, 16 - 1))[2:] for _ in range(6)])
    elif mode == 3:
        res = '.'.join([hex(random.randint(0, 16 - 1))[2:] + hex(random.randint(0, 16 - 1))[2:] + hex(
            random.randint(0, 16 - 1))[2:] + hex(random.randint(0, 16 - 1))[2:] for _ in range(3)])

    if random.randint(0, 1) == 0:
        return res.upper()
    else:
        return res


if __name__ == '__main__':
    print(create_ip())
