# Contributing to Hyprface

## How to contribute

1. Fork the repository
2. Create a branch from `main`
3. Make your changes
4. Submit a pull request

Direct pushes to `main` are not accepted. All changes go through a pull request.

## Coding style

- No comments in code — code should be self-explanatory
- One responsibility per module
- Clean CLI output — no debug prints, no noise
- Type hints where possible
- Keep functions small

## Commit style

```
feat(module): short description
fix(module): short description
refactor(module): short description
chore: short description
```

Examples:
```
feat(recognition): add embedding cache
fix(daemon): handle camera disconnect gracefully
refactor(matcher): simplify cosine similarity
chore: update dependencies
```

## Project structure

```
src/auth/         — authentication logic and AuthResult
src/camera/       — camera discovery, capture, diagnostics
src/cli/          — CLI entry point and commands
src/config/       — config load and save
src/recognition/  — face detection, embedding, matching, database
src/service/      — Unix socket daemon and client
src/utils/        — environment setup and suppression helpers
pam/              — C PAM module, Makefile, install/uninstall scripts
```

## Running locally

```bash
git clone https://github.com/Yash-Maholiya/hyprface.git
cd hyprface
python -m venv .venv
source .venv/bin/activate
pip install -e .
hyprface scan
hyprface add
hyprface start &
hyprface auth
```
