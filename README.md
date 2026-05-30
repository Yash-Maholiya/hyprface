# Hyprface

Facial authentication system for Linux. Works with any PAM-compatible lock screen, sudo, and login manager. Designed for Hyprland but not limited to it.

Not a demo — a production-oriented platform built for daily use.

---

## Features

- Face-based authentication using InsightFace (buffalo_l)
- PAM integration — sudo, login, lock screen
- Hyprlock integration out of the box
- Unix socket daemon — loads model once, stays ready
- Multiple user support
- Fully offline — no cloud, no telemetry
- Local storage — embeddings never leave your machine

---

## Requirements

- Python 3.11+
- gcc
- make
- v4l2-utils
- PAM development headers (`linux-pam` or `pam-devel`)
- A webcam

### Arch Linux

```bash
sudo pacman -S gcc make v4l-utils pam
```

### Ubuntu / Debian

```bash
sudo apt install gcc make v4l-utils libpam-dev
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Yash-Maholiya/hyprface.git
cd hyprface
```

### 2. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -e .
```

### 4. Build and install PAM module

```bash
cd pam
make
sudo ./install.sh
cd ..
```

The installer will ask which services to enable (sudo, login, polkit, hyprlock).

### 5. Configure camera

Run this once to detect and select your camera:

```bash
hyprface scan
```

### 6. Enroll your face

```bash
hyprface add
```

### 7. Start the daemon

The daemon must be running for all authentication to work. It loads the face recognition model once and stays ready.

```bash
hyprface start
```

To start automatically on login, add to your Hyprland autostart:

```
exec-once = /path/to/hyprface/.venv/bin/python -m src.service.daemon
```

---

## Usage

Commands must be run from the project directory with the virtual environment active.

```bash
hyprface scan        # detect and select camera (run once on setup)
hyprface doctor      # camera diagnostics
hyprface add         # enroll a new user
hyprface list        # list enrolled users
hyprface remove      # remove an enrolled user
hyprface verify      # verify face directly (without daemon)
hyprface start       # start authentication daemon
hyprface auth        # request auth from running daemon
```

### Recommended order for first-time setup

```
hyprface scan → hyprface add → hyprface start → hyprface auth
```

---

## How it works

```
Camera
  ↓
OpenCV — frame capture
  ↓
InsightFace buffalo_l — face detection + 512-dim embedding
  ↓
Cosine similarity — compared against enrolled embeddings
  ↓
Auth decision (threshold: 0.75)
  ↓
PAM or lock screen
```

Face embeddings are mathematical representations of your face — not images. They are stored locally in `data/users/` and never transmitted anywhere.

---

## PAM Integration

The installer supports enabling Hyprface for:

- `sudo`
- `login`
- `polkit`
- `hyprlock`

Face auth runs first. If it succeeds, password is skipped. If it fails or times out (7 seconds), password prompt appears normally.

To uninstall PAM integration:

```bash
cd pam
sudo ./uninstall.sh
```

Original PAM files are backed up as `*.hyprface.bak` before any modification.

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
- Daemon socket permissions set to 0600
- PAM config always keeps password as fallback
- Original PAM files are backed up before modification
- User data is gitignored and never committed

---

## Troubleshooting

**`hyprface: command not found`**
Make sure you installed with `pip install -e .` and your virtual environment is active.

**`No camera configured`**
Run `hyprface scan` first.

**`Authentication daemon not running`**
Start it with `hyprface start` before using `hyprface auth` or PAM integration.

**Face not detected during enrollment**
Make sure you are in good lighting and looking directly at the camera.

**Low confidence scores**
Re-enroll with varied poses and lighting using `hyprface remove` then `hyprface add`.

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

Pull requests are welcome. All contributions go through a pull request — direct pushes to `main` are not accepted.

Please keep the coding style consistent:
- No comments in code
- One responsibility per module
- Clean CLI output

---

## License

MIT
