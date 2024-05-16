# https://github.com/VamosC/CLIP4STR

import os.path as osp
import argparse

import torch

from PIL import Image
from torch.utils.data import DataLoader, Dataset
import torch

from strhub.data.module import SceneTextDataModule
from strhub.models.utils import load_from_checkpoint, parse_model_args
import pandas as pd
from tqdm import tqdm
from CAP import *
import numpy as np

from CAP.utils import *
seed_everything(14759)


@torch.inference_mode()
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--checkpoint', help="Model checkpoint (or 'pretrained=<model_id>')")
    parser.add_argument('--device', default='cuda')
    parser.add_argument('--model_type', default='L', help="Model type : 'L' or 'B'")
    parser.add_argument('--images_path', type=str, help='Images to read')
    parser.add_argument('--CAP', action='store_true')  # Inference data type
    parser.add_argument('--AA', action='store_true')  # Inference data type

    args, unknown = parser.parse_known_args()
    kwargs = parse_model_args(unknown)
    print(f'Additional keyword arguments: {kwargs}')

    # [CAP] Define CAP model
    if args.CAP:
        CAP_MODEL_PATH = 'PATH_TO_CAP_MODEL'
        CAP_model = CAPModel(71, 300, 500, 5, 6)
        CAP_model.load_state_dict(torch.load(CAP_MODEL_PATH))
        CAP_model.to(args.device)
        CAP_model.eval()

        word2tensor = WordToTensor1D(case_sensitive=False, pad_size=30, device=args.device)
        print(f'loading CAP checkpoint from {CAP_MODEL_PATH}')
    print(f'Using CAP is {args.CAP}')

    # [Anti-Aliasing] Define AA layer
    apply_aa = args.AA
    print(f'Using Anti-Aliasing is {args.AA}')

    # [CLIP4STR] load CLIP4STR model from checkpoint
    model_type = args.model_type
    weight_folder = 'PATH_TO_clip4str_MODEL'
    print(f'=================== Using CLIP4STR-{model_type} ===================')
    if model_type == 'L':
        checkpoint = osp.join(weight_folder, 'clip4str_large14x14_f125500adc.ckpt')
    elif model_type == 'B':
        checkpoint = osp.join(weight_folder, 'clip4str_base16x16_d70bde1f2d.ckpt')
    else:
        raise Exception(f'Model type {model_type} not exist.')

    args.checkpoint = checkpoint

    model = load_from_checkpoint(args.checkpoint, **kwargs).eval().to(args.device)
    img_transform = SceneTextDataModule.get_transform(model.hparams.img_size)

    # [CAP] Load character distribution
    normal_prior = np.load('../distributions/CAPv2_NORMAL_PRIOR.npy')
    hash_prior = np.load('./CAP/priors/CAPv2_HASH_PRIOR.npy')
    ipv4_prior = np.load('./CAP/priors/CAPv2_IPv4_PRIOR.npy')
    ipv6_prior = np.load('./CAP/priors/CAPv2_IPv6_PRIOR.npy')
    mac_prior = np.load('./CAP/priors/CAPv2_MAC_PRIOR.npy')

    files = sorted([x for x in os.listdir(args.images_path) if x.endswith('png') or x.endswith('jpeg') or x.endswith('jpg')])

    for fname in files:
        # Load image and prepare for input
        filename = os.path.join(args.images_path, fname)
        image = Image.open(filename).convert('RGB')
        image = img_transform(image).unsqueeze(0).to(args.device)

        p = model(image).softmax(-1)
        pred, p = model.tokenizer.decode(p)

        if args.CAP:
            logit = CAP_model(word2tensor.convert(pred[0]))
            logit_softmax = logit.softmax(dim=1)
            posterior = torch.matmul(logit_softmax, torch.Tensor(np.vstack([normal_prior, hash_prior, ipv4_prior, ipv6_prior, mac_prior])).to(args.device))
            p[:, :, 1:] *= (1 + SwapVocab2D(posterior, './CAP/VOCAB_CLIP4STR.npy')[:, 1:-2].unsqueeze(1).to(args.device))
            pred_cap, confidences = model.tokenizer.decode(p)

            print(f'{fname}: {pred[0]}, {pred_cap[0]}')
        else:
            print(f'{fname}: {pred[0]}')

if __name__ == '__main__':
    main()
