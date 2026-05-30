#!/usr/bin/env bash

set -e

MODULE_DEST="/usr/lib/security/pam_hyprface.so"
PAM_FILES=(/etc/pam.d/sudo /etc/pam.d/login /etc/pam.d/polkit-1 /etc/pam.d/hyprlock)

echo "Restoring PAM configs..."
for file in "${PAM_FILES[@]}"; do
    backup="$file.hyprface.bak"
    if [ -f "$backup" ]; then
        sudo cp "$backup" "$file"
        sudo rm "$backup"
        echo "  Restored: $file"
    fi
done

if [ -f "$MODULE_DEST" ]; then
    sudo rm "$MODULE_DEST"
    echo "Removed: $MODULE_DEST"
fi

echo "Done. Hyprface PAM integration removed."