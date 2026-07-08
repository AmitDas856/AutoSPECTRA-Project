"""Sequence model for AutoSPECTRA: an LSTM over CAN frame windows.
Owner: Maheswari (Sequence/Anomaly). Block-2 comparison model.

This is the third detection family in the project. The CNN treats a window of
frames as an image; this model instead reads the window as an ordered sequence,
one frame at a time, and lets an LSTM learn the temporal pattern. Injected
attacks disturb the timing and value rhythm of the stream, and a recurrent
model is a natural fit for that.

The input is the same per-file window used by the CNN, so the two models are
compared on identical data. No image encoding here: the LSTM reads the raw
normalised (WINDOW, n_features) window directly.

Needs PyTorch (already in requirements.txt). Runs on CPU; the net is small.
"""

import numpy as np
import torch
import torch.nn as nn

WINDOW = 32       # frames per sequence (matches the CNN default for a fair compare)
N_CLASSES = 5     # Normal, DoS, Fuzzy, Gear, RPM
N_FEATURES = 9    # can_id + 8 data bytes


def normalise_window(window):
    """Scale each feature column of one window to 0..1, per window.

    Same self-contained per-window scaling the CNN uses, so no scale
    information leaks between windows or across the train/test split.
    Returns shape (WINDOW, n_features) ready for the LSTM.
    """
    w = window.astype("float32")
    mn = w.min(axis=0)
    mx = w.max(axis=0)
    rng = np.where(mx > mn, mx - mn, 1.0)   # constant column -> avoid divide-by-zero
    return (w - mn) / rng


class SeqLSTM(nn.Module):
    """A small LSTM classifier. One recurrent layer keeps it CPU-friendly.

    The LSTM reads the window frame by frame and builds a hidden state; the
    final hidden state is a summary of the whole window, which a small linear
    head maps to the five classes. Understand each part for the viva:
      - input_size  = features per frame (9)
      - hidden_size = size of the memory vector the LSTM carries
      - batch_first = our tensors are (batch, time, features)
    """
    def __init__(self, in_features=N_FEATURES, hidden=64, n_classes=N_CLASSES):
        super().__init__()
        self.lstm = nn.LSTM(input_size=in_features, hidden_size=hidden,
                            num_layers=1, batch_first=True)
        self.head = nn.Sequential(
            nn.Linear(hidden, 32), nn.ReLU(),
            nn.Linear(32, n_classes),
        )

    def forward(self, x):
        # x: (batch, WINDOW, n_features)
        out, (h_n, c_n) = self.lstm(x)
        last = h_n[-1]              # final layer's last hidden state: (batch, hidden)
        return self.head(last)


def train_one_epoch(model, X, y, lr=1e-3):
    """One full-batch step. Returns the loss. The real loop (minibatches,
    epochs) is in train_seq.py; this is only for the smoke test below."""
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    model.train()
    opt.zero_grad()
    loss = loss_fn(model(X), y)
    loss.backward()
    opt.step()
    return float(loss.detach())


if __name__ == "__main__":
    # Smoke test with random sequences, so a fresh clone can prove the model
    # runs before any data is downloaded. Mirrors cv_model.py's smoke test.
    N = 64
    X = torch.randn(N, WINDOW, N_FEATURES)
    y = torch.randint(0, N_CLASSES, (N,))
    model = SeqLSTM()
    print("loss after one step:", train_one_epoch(model, X, y))

    one = np.random.rand(WINDOW, N_FEATURES)
    print("normalised window shape:", normalise_window(one).shape)   # (32, 9)
