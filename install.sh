#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_NAME="nbaasc"
INSTALL_DIR="$HOME/.local/bin"
TARGET_PATH="$INSTALL_DIR/$APP_NAME"
USER_RC="$HOME/.bashrc"
PATH_LINE='export PATH="$HOME/.local/bin:$PATH"'

mkdir -p "$INSTALL_DIR"

cat > "$TARGET_PATH" <<EOF
#!/usr/bin/env bash
set -euo pipefail

exec python3 "$REPO_DIR/gui.py" "\$@"
EOF

chmod +x "$TARGET_PATH"

if ! grep -qxF "$PATH_LINE" "$USER_RC" 2>/dev/null; then
  printf '\n%s\n' "$PATH_LINE" >> "$USER_RC"
fi

printf 'Installed %s to %s\n' "$APP_NAME" "$TARGET_PATH"
printf 'Run it from anywhere with: %s\n' "$APP_NAME"
printf 'If PATH was not updated in your current shell, run: source ~/.bashrc\n'