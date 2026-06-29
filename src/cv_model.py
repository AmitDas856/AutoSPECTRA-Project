"""
AutoSPECTRA — Computer-Vision detector: CAN frames -> image -> CNN.
Owner: Ad (CV + Lead). This is the HEADLINE model and the Block-2 (CV) requirement.

SKELETON. Finish the TODOs, run one training pass on synthetic data, then swap in
Amit's real time-ordered split next week. You must be able to explain the image
encoding and the CNN in the viva — see LEARNING-HELPERS/CONCEPT-PRIMER.md.

Idea: a CNN is good at spatial patterns, but CAN traffic is a stream. So we turn a
WINDOW of consecutive frames into a small image, where attack patterns become
visible shapes, and let the CNN classify the window.

Needs PyTorch: uncomment torch in requirements.txt, then `pip install torch`.
Runs on CPU — keep the net tiny.
"""

import numpy as np
import torch
import torch.nn as nn

WINDOW = 32      # frames per image (try 16/32/64 later — this is your ablation)
N_CLASSES = 5    # Normal, DoS, Fuzzy, Gear, RPM


def frames_to_image(window: np.ndarray) -> np.ndarray:
    """
    Turn one window of CAN frames into a 2D grayscale image.
    `window` shape = (WINDOW, n_features) e.g. [can_id_norm, d0..d7 normalised].
    Return shape = (1, H, W) for a single-channel image.

    Simplest first version (do this, get it working, then experiment):
      - normalise each feature to 0..1
      - the window IS the image: rows = time, cols = features
    Stretch (better marks): a recurrence plot of the CAN-ID sequence (à la Rec-CNN).
    """
    w = window.astype("float32")
    mn = w.min(axis=0)
    mx = w.max(axis=0)
    rng = np.where(mx > mn, mx - mn, 1.0)   # avoid divide-by-zero
    img = (w - mn) / rng                     # scale every column to 0..1
    return img[None, :, :]                   # add the channel dim -> (1, H, W)


class TinyCNN(nn.Module):
    """A small CPU-friendly CNN. Understand each layer (the viva will ask)."""
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
    """One pass. Returns mean loss. Wire a real DataLoader once it works."""
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    model.train()
    opt.zero_grad()
    out = model(X)                      # X: (N,1,H,W)
    loss = loss_fn(out, y)              # y: (N,) class ids
    loss.backward(); opt.step()
    return float(loss)


if __name__ == "__main__":
    # Smoke test with random "images" so you confirm the net runs before real data.
    N, H, W = 64, WINDOW, 9
    X = torch.randn(N, 1, H, W)
    y = torch.randint(0, N_CLASSES, (N,))
    model = TinyCNN()
    print("loss after one step:", train_one_epoch(model, X, y))

    # Prove the encoder works on frame-like data (swap in Amit's real frames next week)
    fake_frames = np.random.rand(WINDOW, 9)        # 9 features
    img = frames_to_image(fake_frames)
    print("image shape:", img.shape)               # expect (1, 32, 9)
