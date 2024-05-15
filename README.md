# CAP
> Official code of "Enhancing Optical Character Recognition Performance in the Cybersecurity Domain for Indicator of Compromise Analysis"  

Context-aware prior (CAP) network aims to improving optical character recognition (OCR) or scene text recognition (STR) performance in cyber-security doimin images such as thread reports. We deomnstrate our proposed method to improve recognition performance on normal texts(nantural texts), hexadecial encryption texts, IPv4, IPv6 addresses, and MAC address texts in image.

## Method
<img src="./CAP.png">

**\*Requires adapting CAP network right in to OCR/STR libries to update priors of each characters.**

## Installation
### Dependency
Requires <code>Python >= 3.8</code> and <code>PyTorch >= 1.12</code>. The following commands are tested on a Windows 10 with CUDA driver version <code>552.22</code> and CUDA version <code>11.3</code>.  

```
conda create -n cap python==3.8
conda activate cap
conda install pytorch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 cudatoolkit=11.3 -c pytorch
conda install jupyter
pip install -r requirements.txt
```

## Results
<h3>CAP-BiLSTM Model trained on generated data</h3>  

| OCR Libries                                                                                                            | Normal    | HASH      | IPv4      | IPv6      | MAC       |
|------------------------------------------------------------------------------------------------------------------------|-----------|-----------|-----------|-----------|-----------|
| [ASTER](https://github.com/open-mmlab/mmocr/blob/dev-1.x/configs/textrecog/aster/README.md)$^\dagger$                  | +0.27     | +9.95     | -3.64     | +1.7      | +0.96     |
| [CLIP4STR-B](https://github.com/VamosC/CLIP4STR)                                                                       | +0.56     | +1.67     | +0.01     | +1.58     | +0.95     |
| [CLIP4STR-L](https://github.com/VamosC/CLIP4STR)                                                                       | +0.60     | +1.31     | +0.02     | +1.45     | +2.03     |
| [CLOVA](https://github.com/clovaai/deep-text-recognition-benchmark)                                                    | +0.03     | -0.13     | -3.73     | -0.67     | -0.15     |
| [EasyOCR](https://github.com/JaidedAI/EasyOCR)                                                                         | -0.20     | +11.69    | +22.08    | +10.29    | +9.13     |
| [MAERec-B](https://github.com/open-mmlab/mmocr/blob/dev-1.x/configs/textrecog/maerec/README.md)$^\dagger$              | +0.06     | +4.08     | -0.01     | +3.70     | +6.52     |
| [MAERec-S](https://github.com/open-mmlab/mmocr/blob/dev-1.x/configs/textrecog/maerec/README.md)$^\dagger$              | +0.25     | +5.28     | -0.06     | +5.31     | +6.61     |
| [MASTER](https://github.com/open-mmlab/mmocr/blob/dev-1.x/configs/textrecog/master/README.md)$^\dagger$                | -0.24     | +3.52     | -1.73     | +0.85     | +0.63     |
| [NRTR](https://github.com/open-mmlab/mmocr/blob/dev-1.x/configs/textrecog/nrtr/README.md)$^\dagger$                    | +0.07     | +8.09     | +1.80     | +2.13     | +2.75     |
| [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)                                                                 | +0.15     | +1.28     | +0.07     | +3.02     | +0.35     |
| [RobustScanner](https://github.com/open-mmlab/mmocr/blob/dev-1.x/configs/textrecog/robust_scanner/README.md)$^\dagger$ | +0.40     | +12.39    | +11.98    | +7.64     | +4.62     |
| [SATRN](https://github.com/open-mmlab/mmocr/blob/dev-1.x/configs/textrecog/satrn/README.md)$^\dagger$                  | +1.21     | +12.13    | +1.46     | +5.53     | +2.34     |
| **Average**                                                                                                            | **+0.21** | **+6.45** | **+2.25** | **+4.71** | **+2.99** |

<h3>CAP-BERT Model trained with on generated data</h3>  

| OCR Libries                                                                                                            | Normal    | HASH      | IPv4      | IPv6      | MAC       |
|------------------------------------------------------------------------------------------------------------------------|-----------|-----------|-----------|-----------|-----------|
| [ASTER](https://github.com/open-mmlab/mmocr/blob/dev-1.x/configs/textrecog/aster/README.md)$^\dagger$                  | +0.27     | +11.31    | -2.86     | +3.74     | +0.97     |
| [CLIP4STR-B](https://github.com/VamosC/CLIP4STR)                                                                       | +0.27     | +0.95     | +0.01     | +0.80     | +0.90     |
| [CLIP4STR-L](https://github.com/VamosC/CLIP4STR)                                                                       | +0.32     | +0.92     | +0.02     | +0.93     | +0.89     |
| [CLOVA](https://github.com/clovaai/deep-text-recognition-benchmark)                                                    | +0.03     | -0.15     | -3.69     | -0.74     | -0.15     |
| [EasyOCR](https://github.com/JaidedAI/EasyOCR)                                                                         | -1.86     | +14.05    | +22.45    | +19.19    | +11.80    |
| [MAERec-B](https://github.com/open-mmlab/mmocr/blob/dev-1.x/configs/textrecog/maerec/README.md)$^\dagger$              | +0.06     | +4.13     | -0.01     | +3.74     | +6.51     |
| [MAERec-S](https://github.com/open-mmlab/mmocr/blob/dev-1.x/configs/textrecog/maerec/README.md)$^\dagger$              | +0.25     | +5.41     | -0.06     | +5.33     | +6.61     |
| [MASTER](https://github.com/open-mmlab/mmocr/blob/dev-1.x/configs/textrecog/master/README.md)$^\dagger$                | -0.24     | +3.55     | -1.26     | +1.98     | +0.62     |
| [NRTR](https://github.com/open-mmlab/mmocr/blob/dev-1.x/configs/textrecog/nrtr/README.md)$^\dagger$                    | +0.06     | +8.86     | +3.43     | +2.67     | +2.74     |
| [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)                                                                 | +0.09     | +1.31     | +0.07     | +3.03     | +0.35     |
| [RobustScanner](https://github.com/open-mmlab/mmocr/blob/dev-1.x/configs/textrecog/robust_scanner/README.md)$^\dagger$ | +0.40     | +12.63    | +11.19    | +8.10     | +4.43     |
| [SATRN](https://github.com/open-mmlab/mmocr/blob/dev-1.x/configs/textrecog/satrn/README.md)$^\dagger$                  | +1.21     | +13.07    | +3.87     | +5.74     | +2.31     |
| **Average**                                                                                                            | **+0.07** | **+6.34** | **+2.76** | **+4.54** | **+3.17** |

*Metirc : World-based Exactly Matching (WEM) score  
The OCR models marked with **dagger**$^\dagger$ were tested using models implemented using the [MMOCR library](https://github.com/open-mmlab/mmocr).


## Checkpoint

### Pre-train with generated dataset (FINE)
| Type      | weight                                                                                             | logs                                 | # params | Size     |
|-----------|----------------------------------------------------------------------------------------------------|--------------------------------------|--------|----------|
| LSTM-FINE | [Google Drive](https://drive.google.com/file/d/1IbgX0RjBreElrJBir3It_PsJxrBaVVXC/view?usp=sharing) | [logs](/logs/logs-cap-lstm-fine.txt) | 33.7M  | 128.8 MB |
| BERT-FINE | [Google Drive](https://drive.google.com/file/d/1beu9bkcLji_5eCMNYoRNaM_xuEHo-o00/view?usp=sharing) | [logs](/logs/logs-cap-bert-fine.txt) | 108.3M | 413.3 MB |

## Dataset

### Generate data
 - train : [Google Drive](https://drive.google.com/file/d/1qkWrw1Au5lqRUx8crFDirloGkQDGE2Ay/view?usp=sharing) (259.8 MB)
 - test : [Google Drive](https://drive.google.com/file/d/1TRX7go8yEF2jHTwO3CCTxZHjINYMrQwr/view?usp=sharing) (80.4 MB)

### Real-world data
 - test : [Google Drive](https://drive.google.com/file/d/1vmuwvu_ld0FpwDMKTUhZKi3XztrdB9fw/view?usp=sharing) (5.4 MB)