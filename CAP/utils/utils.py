from typing import List
import torch
import numpy as np


class WordToTensor2D:
    def __init__(self, case_sensitive: bool = False, pad_size: int = -1, device: str = 'cuda'):
        """
        Create a word to tensor converter operate with 2D array
        :param case_sensitive: Convert text with sensitive cases
        :param pad_size: Padding size after end of text.
        :param device: return tensor type 'cpu' or 'cuda''
        """
        self.case_sensitive = case_sensitive
        self.pad_size = pad_size
        self.vocab = vocabs
        self.device = device

        # Token
        self.unk_token = self.vocab['<UNK>']
        self.pad_token = self.vocab['<PAD>']

    def convert(self, words: List[str]) -> torch.Tensor:
        """
        convert list of words to tensor
        :param words: List of words
        :return: Converted tensors
        """
        indices = []

        for word in words:
            indices_ = []

            if not self.case_sensitive:
                word = word.upper()

            for char in word:
                if char not in self.vocab:  # If char is not in vocabulary (Unknown character)
                    indices_.append(self.unk_token)
                else:
                    indices_.append(self.vocab[char])

            if self.pad_size != -1:  # Add pad token
                indices_ += [self.pad_token for _ in range(self.pad_size - len(indices_))]

            indices.append(indices_)

        return torch.tensor(indices, dtype=torch.long, device=self.device)


class WordToTensor1D:
    def __init__(self, case_sensitive: bool = False, pad_size: int = -1, device: str = 'cuda'):
        """
        Create a word to tensor converter operate with 1D array
        :param case_sensitive: Convert text with sensitive cases
        :param pad_size: Padding size after end of text.
        :param device: return tensor type 'cpu' or 'cuda''
        """
        self.case_sensitive = case_sensitive
        self.pad_size = pad_size
        self.vocab = vocabs
        self.device = device

        # Token
        self.unk_token = self.vocab['<UNK>']
        self.pad_token = self.vocab['<PAD>']

    def convert(self, word: str) -> torch.Tensor:
        """
        convert word to tensor
        :param word: String words
        :return: Converted tensor
        """
        indices = []

        if isinstance(word, float) or isinstance(word, int):
            word = str(word)

        if not self.case_sensitive:
            word = word.upper()

        if len(word) > self.pad_size:
            word = word[:self.pad_size]

        for char in word:
            if char not in self.vocab:  # If char is not in vocabulary (Unknown character)
                indices.append(self.unk_token)
            else:
                indices.append(self.vocab[char])

        if self.pad_size != -1:  # Add pad token
            indices += [self.pad_token for _ in range(self.pad_size - len(indices))]

        return torch.tensor(indices, dtype=torch.long, device=self.device)


vocabs = {
    ' ': 0, '0': 1, '1': 2, '2': 3, '3': 4, '4': 5, '5': 6, '6': 7, '7': 8, '8': 9, '9': 10, '!': 11, '"': 12,
    '#': 13, '$': 14, '%': 15, '&': 16, "'": 17, '(': 18, ')': 19, '*': 20, '+': 21, ',': 22, '-': 23, '.': 24,
    '/': 25, ':': 26, ';': 27, '<': 28, '=': 29, '>': 30, '?': 31, '@': 32, '[': 33, '\\': 34, ']': 35, '^': 36,
    '_': 37, '`': 38, '{': 39, '|': 40, '}': 41, '~': 42, 'A': 43, 'B': 44, 'C': 45, 'D': 46, 'E': 47, 'F': 48,
    'G': 49, 'H': 50, 'I': 51, 'J': 52, 'K': 53, 'L': 54, 'M': 55, 'N': 56, 'O': 57, 'P': 58, 'Q': 59, 'R': 60,
    'S': 61, 'T': 62, 'U': 63, 'V': 64, 'W': 65, 'X': 66, 'Y': 67, 'Z': 68, '<PAD>': 69, '<UNK>': 70
}
