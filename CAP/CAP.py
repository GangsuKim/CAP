import torch.nn as nn


class CAPModel(nn.Module):
    def __init__(self, vocab_size: int = 71, embedding_dim: int = 300, hidden_dim: int = 500, output_dim: int = 5, num_layers: int = 6, bidirectional: bool = True):
        super(CAPModel, self).__init__()
        self.vocab_size_ = vocab_size
        self.embedding_dim_ = embedding_dim
        self.hidden_dim_ = hidden_dim
        self.output_dim_ = output_dim
        self.bidirectional = bidirectional
        self.factor = 2 if self.bidirectional else 1

        self.embedding = nn.Embedding(self.vocab_size_, self.embedding_dim_)
        self.lstm = nn.LSTM(self.embedding_dim_, self.hidden_dim_, bidirectional=self.bidirectional, batch_first=True, num_layers=num_layers)
        self.fc1 = nn.Linear(self.hidden_dim_ * self.factor, int(self.hidden_dim_ // (2 / self.factor)))
        self.fc2 = nn.Linear(int(self.hidden_dim_ // (2 / self.factor)), self.output_dim_)

    def forward(self, x):
        x = self.embedding(x)
        lstm_out, _ = self.lstm(x)
        f1 = self.fc1(lstm_out[:, -1, :])
        out = self.fc2(f1)
        return out
