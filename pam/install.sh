#!/usr/bin/env bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODULE_SRC="$SCRIPT_DIR/pam_hyprface.so"
MODULE_DEST="/usr/lib/security/pam_hyprface.so"
PAM_LINE="auth sufficient pam_hyprface.so"

if [ ! -f "$MODULE_SRC" ]; then
    echo "pam_hyprface.so not found. Run 'make' first."
    exit 1
fi

echo "Installing pam_hyprface.so..."
sudo cp "$MODULE_SRC" "$MODULE_DEST"
sudo chmod 755 "$MODULE_DEST"
echo "Installed to $MODULE_DEST"

echo ""
echo "Select services to enable Hyprface authentication:"
echo "  1) sudo"
echo "  2) login"
echo "  3) polkit"
echo "  4) hyprlock"
echo "  5) all"
echo ""
read -p "Enter choices (e.g. 1 3 or 5): " -a choices

enable_sudo=0
enable_login=0
enable_polkit=0
enable_hyprlock=0

for choice in "${choices[@]}"; do
    case $choice in
        1) enable_sudo=1 ;;
        2) enable_login=1 ;;
        3) enable_polkit=1 ;;
        4) enable_hyprlock=1 ;;
        5) enable_sudo=1; enable_login=1; enable_polkit=1; enable_hyprlock=1 ;;
    esac
done

insert_pam_line() {
    local file="$1"
    if grep -q "pam_hyprface" "$file"; then
        echo "  Already configured: $file"
        return
    fi
    sudo cp "$file" "$file.hyprface.bak"
    sudo sed -i "0,/^auth/s//auth [success=done ignore=ignore default=ignore] pam_hyprface.so\nauth/" "$file"
    echo "  Configured: $file"
}

if [ $enable_sudo -eq 1 ]; then
    echo "Enabling for sudo..."
    insert_pam_line /etc/pam.d/sudo
fi

if [ $enable_login -eq 1 ]; then
    echo "Enabling for login..."
    insert_pam_line /etc/pam.d/login
fi

if [ $enable_polkit -eq 1 ]; then
    echo "Enabling for polkit..."
    insert_pam_line /etc/pam.d/polkit-1
fi

if [ $enable_hyprlock -eq 1 ]; then
    echo "Enabling for hyprlock..."
    insert_pam_line /etc/pam.d/hyprlock
fi

echo ""
echo "Done. Hyprface daemon must be running for authentication to work."
echo "Backups saved as *.hyprface.bak"