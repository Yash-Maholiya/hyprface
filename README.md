# Hyprface

Facial authentication system for Linux. Designed for Hyprland but works with any PAM-compatible lock screen, sudo, and login manager.

Not a demo — a production-oriented platform built for daily use.

---

## Features

- Face-based authentication using InsightFace (buffalo_l)
- PAM integration — sudo, login, lock screen
- Hyprlock integration out of the box
- Multiple user support
- Fully offline — no cloud, no telemetry
- Local data storage — embeddings never leave your machine
- Modular architecture — camera, recognition, auth, and service layers are independent

---

## Requirements

- Python 3.11+
- OpenCV
- InsightFace
- ONNX Runtime
- A webcam
- PAM development headers (for PAM module)
- gcc (for PAM module)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/hyprface.git
cd hyprface
```

### 2. Create virtual environment and install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 3. Build and install PAM module

```bash
cd pam
make
sudo ./install.sh
cd ..
```

### 4. Set up camera

```bash
hyprface scan
```

### 5. Enroll your face

```bash
hyprface add
```

### 6. Start the daemon

```bash
hyprface start
```

Add to Hyprland autostart:

```
exec-once = /path/to/hyprface/.venv/bin/python -m src.service.daemon
```

---

## Usage

```bash
hyprface add          # enroll a new user
hyprface verify       # verify face via camera
hyprface list         # list enrolled users
hyprface remove       # remove an enrolled user
hyprface start        # start authentication daemon
hyprface auth         # request auth from running daemon
hyprface scan         # configure camera
hyprface doctor       # camera diagnostics
```

---

## How it works

```
Camera
  ↓
OpenCV — frame capture
  ↓
InsightFace — face detection + 512-dim embedding
  ↓
Cosine similarity — compared against enrolled embeddings
  ↓
Auth decision — passed to PAM or lock screen
```

Face embeddings are mathematical representations of your face — not images. They are stored locally in `data/users/` and never transmitted anywhere.

---

## PAM Integration

The installer supports enabling Hyprface for:

- `sudo`
- `login`
- `polkit`
- `hyprlock`

Face auth runs first. If it succeeds, password is skipped. If it fails or times out, password prompt appears normally.

To uninstall PAM integration:

```bash
cd pam
sudo ./uninstall.sh
```

---

## Data storage

```
data/users/{username}/
├── profile.json       # username, created_at, sample count, model
└── embeddings.json    # list of 512-dim face embeddings
```

---

## Security

- All processing is local — no network calls
- Embeddings cannot be reversed into images
- Socket permissions are set to 0600
- PAM config always keeps password as fallback
- Original PAM files are backed up before modification

---

## Roadmap

### Phase 5 — Compatibility
- [ ] swaylock integration
- [ ] i3lock integration
- [ ] GDM support
- [ ] LightDM support
- [ ] SDDM login screen (system daemon)

### Phase 6 — Built-in lock screen
- [ ] Hyprface standalone lock screen
- [ ] No external lock screen dependency
- [ ] Wayland + X11 support
- [ ] PIN fallback

### Phase 7 — Security hardening
- [ ] Liveness detection
- [ ] Anti-spoofing
- [ ] Encrypted embeddings
- [ ] Authentication logs

### Phase 8 — Polish
- [ ] Per-user threshold tuning
- [ ] IR camera support
- [ ] Multi-factor authentication
- [ ] AUR package (hyprface-git)

---

## Contributing

Pull requests welcome. Please keep the coding style consistent — no comments in code, one responsibility per module, clean CLI output.

---

## License

MIT
