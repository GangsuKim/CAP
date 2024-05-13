from torch.utils.data import Dataset
from CAP.utils.utils import WordToTensor1D


class CAPDataSet(Dataset):
    def __init__(self, data, pad_size: int = -1, is_train: bool = True, transform=None, case_sensitive: bool = False):
        self.data = data
        self.length = len(data)
        self.is_train = is_train
        self.transform = transform
        self.pad_size = pad_size
        self.word2tensor = WordToTensor1D(case_sensitive=case_sensitive, pad_size=pad_size, device='cuda')

    def __getitem__(self, idx):

        word = self.data[idx][0] if self.is_train else self.data[idx]

        if self.is_train:
            if self.transform is not None:
                word = self.transform(word, self.data[idx][1])

            return self.word2tensor.convert(word), self.data[idx][1]
        return self.word2tensor.convert(word)

    def __len__(self):
        return self.length
