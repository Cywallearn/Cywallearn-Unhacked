
  /$$$$$$$$ /$$       /$$$$$$$  /$$$$$$$  /$$$$$$ /$$$$$$$$ /$$$$$$$$
 | $$_____/| $$      | $$__  $$| $$__  $$|_  $$_/| $$_____/|__  $$__/
 | $$      | $$      | $$  \ $$| $$  \ $$  | $$  | $$         | $$
 | $$$$$   | $$      | $$  | $$| $$$$$$$/  | $$  | $$$$$      | $$
 | $$__/   | $$      | $$  | $$| $$__  $$  | $$  | $$__/      | $$
 | $$      | $$      | $$  | $$| $$  \ $$  | $$  | $$         | $$
 | $$      | $$$$$$$$| $$$$$$$/| $$  | $$ /$$$$$$| $$$$$$$$   | $$
 |__/      |________/|_______/ |__/  |__/|______/|________/   |__/


# Cywallearn Unhacked 🔐

**The World's Most Advanced Password Generator — Unhackable by Design.**

> "Unhackable by Design - Secured by Cywallearn"

## 🚀 Overview

Cywallearn Unhacked is a **military-grade password generator** that combines **cryptographically secure randomness** (Python `secrets` module) with a unique **personal touch algorithm** to create passwords that are:

- **Virtually Unbreakable** — High entropy, resistant to brute force, dictionary, and mask attacks
- **Uniquely Yours** — Incorporates your personal details in a way that doesn't compromise security
- **Beautifully Presented** — Rich terminal UI with color-coded strength indicators

## ✨ Features

| Feature | Description |
|---------|-------------|
| **🔑 Standard Generator** | 5 cryptographically secure passwords at once |
| **🧠 Memorable Generator** | Easy-to-remember yet highly secure passwords |
| **🔍 Password Analyzer** | Deep analysis: entropy, crack time, pattern detection |
| **👤 Personal Touch** | Your name, hobbies, birth year influence structure — not the entropy |
| **⚡ Termux Compatible** | Runs perfectly on Android via Termux |
| **🛡️ Zero Dependencies** | Uses only Python standard library (secrets, hashlib, hmac) |
| **📊 Crack Time Estimates** | SHA256, MD5, bcrypt, NTLM, Argon2 estimates |
| **🔬 Pattern Detection** | Finds sequential, repeated, keyboard patterns |
| **📜 History Logging** | Tracks your generated passwords (in-memory only) |
| **🎨 Rich Terminal UI** | Colors, gauges, formatted tables |

## 📥 Installation

### Termux (Android)

```bash
# Update packages
pkg update -y && pkg upgrade -y

# Install Python
pkg install python -y

# Clone the repository
git clone https://github.com/cywallearn/cywallearn-unhacked.git

# Navigate to directory
cd cywallearn-unhacked

# Make executable
chmod +x cywallearn.py

# Run
python3 cywallearn.py
```

### Linux / macOS

```bash
# Clone
git clone https://github.com/cywallearn/cywallearn-unhacked.git

# Navigate
cd cywallearn-unhacked

# Make executable
chmod +x cywallearn.py

# Run
./cywallearn.py

# Optional: Install globally
sudo ln -sf $(pwd)/cywallearn.py /usr/local/bin/cywallearn
cywallearn
```

### Windows

```cmd
# Download or clone the repository
cd cywallearn-unhacked

# Run with Python
python cywallearn.py
```

### Using pip

```bash
pip install cywallearn-unhacked
```

## 🎮 Usage

```
┌─[?] What is your name?
└─➤ John

┌─[?] What year were you born?
└─➤ 1995

┌─[?] Choose password length:
│   8-12  : Standard security
│   12-16 : Strong security (recommended)
│   16-32 : Maximum security
└─➤ 12
```

Then choose from the main menu:

```
  [1] Generate Passwords       - Create unhackable passwords
  [2] Analyze a Password       - Test strength of any password
  [3] Generate Memorable       - Easy to recall, hard to crack
  [4] View History             - Recently generated passwords
  [5] Reset My Details         - Re-enter personal information
  [6] Settings                 - Change password preferences
  [0] Exit                     - Quit Cywallearn Unhacked
```

## 🧠 How It Works

### Cryptographic Core
All randomness comes from Python's `secrets` module — the same CSPRNG used for cryptographic key generation. No `random` module is used anywhere.

### Personal Touch Algorithm
Your personal details (name, birth year, hobbies) create a seed via **SHA-512 hashing**. This seed influences *which character pools* are selected at each position — but the actual characters chosen within those pools are **cryptographically random**.

This means:
- Two different people get completely different passwords
- Same person generates different passwords every time
- Even knowing someone's personal details doesn't help an attacker

### Entropy Calculation
Full Shannon entropy is calculated with pattern penalties:
- Sequential patterns → -15% entropy
- Repeated characters → -20% entropy
- Keyboard patterns → -25% entropy
- Common passwords → -50% entropy

### Crack Time Estimates
Estimates time to crack with modern GPU hardware across multiple hash types:
- **MD5**: 1 trillion hashes/second
- **NTLM**: 1 trillion hashes/second
- **SHA-256**: 50 billion hashes/second
- **bcrypt (cost 10)**: 1,000 hashes/second
- **Argon2id**: 100 hashes/second

## 📊 Example Output

```
╔══════════════════════════════════════════════════════╗
║           CYWALLEARN UNHACKED - ANALYSIS            ║
╚══════════════════════════════════════════════════════╝

Password    : •••••••••••• (hidden)
Length      : 16 characters
Entropy     : 106.32 bits

  ╔═══ STRENGTH ═══╗
  ║    Excellent    ║
  ║  Score: 95/100  ║
  ║  █████████░░░░  ║
  ╚═════════════════╝

⏱  Crack Time Estimates:
  ▸ sha256     : 543 million years
  ▸ md5_fast   : 27 million years
  ▸ ntlm       : 27 million years
  ▸ bcrypt_10  : 1.3 quadrillion years
  ▸ argon2     : 13.6 quadrillion years
```

## 🔒 Security Philosophy

1. **No External Dependencies** — Every line is auditable in this repo
2. **Local Only** — Your personal data never leaves your machine
3. **No Telemetry** — No tracking, no analytics, no phone home
4. **Cryptographically Secure** — Uses OS-level CSPRNG, not pseudo-random
5. **Open Source** — Fully transparent algorithm

## 📁 Project Structure

```
cywallearn-unhacked/
├── cywallearn.py          # Main entry point with interactive UI
├── modules/
│   ├── __init__.py        # Package init
│   ├── generator.py       # Core password generation engine
│   └── analyzer.py        # Password strength analyzer
├── install.sh             # Termux/Linux installer
├── setup.py               # Python package setup
├── requirements.txt       # Dependencies (none required)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🛠️ Requirements

- **Python 3.6+** (no additional packages required)
- Works on: Termux, Linux, macOS, Windows

## 🤝 Contributing

Contributions are welcome! If you'd like to improve Cywallearn Unhacked:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## 📜 License

MIT License — See [LICENSE](LICENSE) file for details.

## 🌐 Connect

- **GitHub**: [github.com/cywallearn/cywallearn-unhacked](https://github.com/cywallearn/cywallearn-unhacked)
- **Author**: Cywallearn

---

<p align="center">
  <strong>🔐 Stay Unhackable. Stay Cywallearn.</strong>
</p>
