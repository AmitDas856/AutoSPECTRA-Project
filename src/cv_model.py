# cv_model.py - CAN windows as images + a tiny CNN. Ad (CV + Lead).
#
# a CNN wants spatial patterns but CAN traffic is a stream, so we take a
# WINDOW of consecutive frames and treat it as a small grayscale image:
# rows = time, cols = features. injected attacks change the id/payload
# rhythm and that shows up as visible texture the conv filters can grab.
# this is the block-2 (computer vision) component of the project.

import numpy as np
import torch
import torch.nn as nn

WINDOW = 32      # frames per image. 16/64 are the ablation - week 8
N_CLASSES = 5    # Normal, DoS, Fuzzy, Gear, RPM


def frames_to_image(window):
    """one window of frames -> one (1, H, W) image.

    window comes in as (WINDOW, n_features). every column gets scaled to
    0..1 independently, per window - keeps the encoding self-contained so
    theres no train/test scale leaking between windows."""
    w = window.astype("float32")
    mn = w.min(axis=0)
    mx = w.max(axis=0)
    rng = np.where(mx > mn, mx - mn, 1.0)   # constant column -> avoid /0
    img = (w - mn) / rng
    return img[None, :, :]                  # add channel dim -> (1, H, W)


def frames_to_recurrence(window):
    """recurrence plot of the frame sequence -> (1, W, W) image.

    the grid encoding keeps raw feature values; this one instead asks "when
    does the traffic repeat itself". R[i,j] = similarity of frame i and frame
    j. normal CAN traffic is periodic so it draws a regular texture; an
    injected burst breaks the period and the texture visibly changes - the
    rec-cnn idea from docs/LITERATURE.md. this is the ablation encoder,
    swap it in with:  python src/train_cnn.py 32 rec"""
    w = window.astype("float32")
    mn = w.min(axis=0)
    mx = w.max(axis=0)
    rng = np.where(mx > mn, mx - mn, 1.0)   # same per-window 0..1 scaling as the grid
    w = (w - mn) / rng
    # distance between every pair of frames, squashed to 0..1 similarity
    # (1 = identical frames, 0 = the furthest-apart pair in this window)
    d = np.sqrt(((w[:, None, :] - w[None, :, :]) ** 2).sum(-1))
    img = 1.0 - d / max(float(d.max()), 1e-6)
    return img[None, :, :].astype("float32")


class TinyCNN(nn.Module):
    # deliberately small so it trains on a laptop cpu in minutes.
    # two conv blocks pull local patterns, adaptive pool squashes to a
    # fixed 4x4 whatever the window size (so the ablation doesnt need a
    # new classifier head), then a small mlp does the 5-way call.
    def __init__(self, in_ch=1, n_classes=N_CLASSES):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(in_ch, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.AdaptiveAvgPool2d((4, 4)),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(), nn.Linear(32 * 4 * 4, 64), nn.ReLU(),
            nn.Linear(64, n_classes),
        )

    def forward(self, x):
        return self.classifier(self.features(x))


def train_one_epoch(model, X, y, lr=1e-3):
    # single full-batch step - only used by the smoke test below.
    # the real training loop (minibatches, epochs) lives in train_cnn.py
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    model.train()
    opt.zero_grad()
    out = model(X)                      # X: (N,1,H,W)
    loss = loss_fn(out, y)              # y: (N,) class ids
    loss.backward(); opt.step()
    return float(loss)


if __name__ == "__main__":
    # smoke test with random tensors - proves the net + encoder run at all
    # before any real data is involved. keep this, its the 10-second check
    # that a fresh clone works.
    N, H, W = 64, WINDOW, 9
    X = torch.randn(N, 1, H, W)
    y = torch.randint(0, N_CLASSES, (N,))
    model = TinyCNN()
    print("loss after one step:", train_one_epoch(model, X, y))

    fake_frames = np.random.rand(WINDOW, 9)        # 9 features
    img = frames_to_image(fake_frames)
    print("image shape:", img.shape)               # expect (1, 32, 9)
