#!/bin/bash
# Cywallearn Unhacked - Termux Installer

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

clear
echo -e "${CYAN}${BOLD}"
echo "  /$$$$$$$$ /$$       /$$$$$$$  /$$$$$$$  /$$$$$$ /$$$$$$$$ /$$$$$$$$"
echo " | $$_____/| $$      | $$__  $$| $$__  $$|_  $$_/| $$_____/|__  $$__/"
echo " | $$      | $$      | $$  \ $$| $$  \ $$  | $$  | $$         | $$"
echo " | $$$$$   | $$      | $$  | $$| $$$$$$$/  | $$  | $$$$$      | $$"
echo " | $$__/   | $$      | $$  | $$| $$__  $$  | $$  | $$__/      | $$"
echo " | $$      | $$      | $$  | $$| $$  \ $$  | $$  | $$         | $$"
echo " | $$      | $$$$$$$$| $$$$$$$/| $$  | $$ /$$$$$$| $$$$$$$$   | $$"
echo " |__/      |________/|_______/ |__/  |__/|______/|________/   |__/"
echo -e "${NC}"
echo -e "${GREEN}${BOLD}     UNHACKED PASSWORD GENERATOR v1.0.0${NC}"
echo -e "${MAGENTA}${BOLD}     Termux Installation${NC}"
echo ""

if [ ! -d "/data/data/com.termux" ]; then
    echo -e "${YELLOW}[!] Not detected as Termux, but continuing...${NC}"
fi

echo -e "${CYAN}[*] Installing Cywallearn Unhacked...${NC}"

echo -e "${YELLOW}[1/3] Updating packages...${NC}"
pkg update -y 2>/dev/null || apt update -y 2>/dev/null || true

echo -e "${YELLOW}[2/3] Checking Python...${NC}"
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}  Python3 OK${NC}"
else
    pkg install python -y 2>/dev/null || apt install python3 -y 2>/dev/null || {
        echo -e "${RED}[!] Failed to install Python${NC}"; exit 1
    }
fi

echo -e "${YELLOW}[3/3] Setting up...${NC}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
chmod +x "$SCRIPT_DIR/cywallearn.py"

mkdir -p $PREFIX/bin 2>/dev/null
cat > $PREFIX/bin/cywallearn << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
DIR="/data/data/com.termux/files/home/cywallearn-unhacked"
if [ -f "$DIR/cywallearn.py" ]; then
    exec python3 "$DIR/cywallearn.py" "$@"
else
    echo "Error: cywallearn-unhacked not found in home directory."
    exit 1
fi
EOF
chmod +x $PREFIX/bin/cywallearn

echo ""
echo -e "${GREEN}${BOLD}  INSTALLATION COMPLETE!${NC}"
echo ""
echo -e "${CYAN}  Run:${NC}"
echo -e "  ${BOLD}python3 cywallearn.py${NC}"
echo -e "  ${BOLD}./cywallearn.py${NC}"
echo -e "  ${BOLD}cywallearn${NC} (from anywhere)"
echo ""
echo -e "${MAGENTA}  Stay Unhackable. Stay Cywallearn.${NC}"
