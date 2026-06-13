#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║           CYWALLEARN UNHACKED - Password Generator          ║
║         "Unhackable by Design - Secured by Cywallearn"      ║
║                   Version 1.0.0 - Termux Ready              ║
╚══════════════════════════════════════════════════════════════╝

A world-class password generator that combines personal touch
with cryptographically secure randomness to create passwords
that are both memorable and virtually unbreakable.

Compatible with: Termux, Linux, macOS, Windows
"""

import sys
import os
import time
import json
from typing import Dict, List, Optional, Tuple

# Add modules directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules'))

try:
    from generator import CywalGenerator, MemorableGenerator
    from analyzer import CywalAnalyzer
except ImportError as e:
    print(f"[!] Error loading modules: {e}")
    print("[!] Make sure the 'modules' directory is present.")
    sys.exit(1)


# ─── Terminal Colors ──────────────────────────────────────────────
class Colors:
    """Terminal color codes with Termux compatibility."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'

    # Foreground
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    GRAY = '\033[90m'

    # Bright
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    # Background
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

    @classmethod
    def strip(cls, text: str) -> str:
        """Remove ANSI escape sequences."""
        import re
        return re.sub(r'\033\[[0-9;]*m', '', text)


# Check if running on Windows without ANSI support
if os.name == 'nt':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        # Fallback: disable colors
        for attr in dir(Colors):
            if not attr.startswith('_') and isinstance(getattr(Colors, attr), str):
                setattr(Colors, attr, '')


# ─── Branding ─────────────────────────────────────────────────────
BANNER = f"""
{Colors.BRIGHT_CYAN}{Colors.BOLD}
     ██████╗██╗   ██╗██╗    ██╗ █████╗ ██╗     ██╗     ███████╗ █████╗ ██████╗ ███╗   ██╗
    ██╔════╝╚██╗ ██╔╝██║    ██║██╔══██╗██║     ██║     ██╔════╝██╔══██╗██╔══██╗████╗  ██║
    ██║      ╚████╔╝ ██║ █╗ ██║███████║██║     ██║     █████╗  ███████║██████╔╝██╔██╗ ██║
    ██║       ╚██╔╝  ██║███╗██║██╔══██║██║     ██║     ██╔══╝  ██╔══██║██╔══██╗██║╚██╗██║
    ╚██████╗   ██║   ╚███╔███╔╝██║  ██║███████╗███████╗███████╗██║  ██║██║  ██║██║ ╚████║
     ╚═════╝   ╚═╝    ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
{Colors.RESET}
{Colors.BRIGHT_GREEN}{Colors.BOLD}              🔐 UNHACKED PASSWORD GENERATOR v1.0.0 🔐{Colors.RESET}
{Colors.GRAY}              "Unhackable by Design - Secured by Cywallearn"{Colors.RESET}
"""


# ─── Utility Functions ───────────────────────────────────────────

def clear_screen():
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_slow(text: str, delay: float = 0.01):
    """Print text with a typewriter effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def print_header(title: str, color: str = Colors.BRIGHT_CYAN):
    """Print a section header."""
    width = 60
    print(f"\n{color}{Colors.BOLD}╔{'═' * (width - 2)}╗{Colors.RESET}")
    print(f"{color}{Colors.BOLD}║{title:^58s}║{Colors.RESET}")
    print(f"{color}{Colors.BOLD}╚{'═' * (width - 2)}╝{Colors.RESET}\n")


def get_input(prompt: str, color: str = Colors.BRIGHT_GREEN, allow_empty: bool = False) -> str:
    """Get user input with styled prompt."""
    print(f"{color}┌─[{Colors.BRIGHT_CYAN}?{color}] {prompt}{Colors.RESET}")
    print(f"{color}└─{Colors.BOLD}➤{Colors.RESET} ", end='')
    value = input().strip()
    if not value and not allow_empty:
        print(f"{Colors.YELLOW}  [!] Input cannot be empty. Please try again.{Colors.RESET}")
        return get_input(prompt, color, allow_empty)
    return value


def select_option(prompt: str, options: List[str], color: str = Colors.BRIGHT_GREEN) -> str:
    """Let user select from a list of options."""
    print(f"{color}┌─[{Colors.BRIGHT_CYAN}?{color}] {prompt}{Colors.RESET}")
    for i, option in enumerate(options, 1):
        print(f"{color}│   {Colors.BRIGHT_YELLOW}[{i}]{Colors.RESET} {option}")
    print(f"{color}└─{Colors.BOLD}➤{Colors.RESET} ", end='')

    while True:
        try:
            choice = input().strip()
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx]
            print(f"  {Colors.YELLOW}[!] Please enter a number between 1 and {len(options)}.{Colors.RESET}")
            print(f"  {Colors.BOLD}➤{Colors.RESET} ", end='')
        except ValueError:
            print(f"  {Colors.YELLOW}[!] Invalid input. Enter a number.{Colors.RESET}")
            print(f"  {Colors.BOLD}➤{Colors.RESET} ", end='')


def press_enter():
    """Wait for Enter key press."""
    print(f"\n{Colors.GRAY}  [ Press Enter to continue... ]{Colors.RESET}", end='')
    input()


# ─── Main Application ────────────────────────────────────────────

class CywallearnApp:
    """Main application class for Cywallearn Unhacked."""

    def __init__(self):
        self.user_data: Dict[str, str] = {}
        self.preferences: Dict = {
            'length': 8,
            'use_symbols': True,
            'avoid_ambiguous': False,
            'use_personal_touch': True,
        }
        self.history: List[Dict] = []

    def run(self):
        """Main application entry point."""
        try:
            self._show_splash()
            self._collect_user_details()
            self._collect_preferences()
            self._main_menu()
        except KeyboardInterrupt:
            print(f"\n\n{Colors.BRIGHT_YELLOW}  [!] Interrupted. Exiting...{Colors.RESET}")
            self._goodbye()
        except EOFError:
            print(f"\n\n{Colors.BRIGHT_YELLOW}  [!] Exiting...{Colors.RESET}")
        sys.exit(0)

    def _show_splash(self):
        """Show animated splash screen."""
        clear_screen()
        print(BANNER)
        time.sleep(0.5)
        print(f"{Colors.DIM}  ⚡ Termux Compatible | Cross-Platform | Military-Grade Security{Colors.RESET}")
        print(f"{Colors.DIM}  🔒 Built with Python's 'secrets' module - Cryptographically Secure{Colors.RESET}\n")
        time.sleep(0.8)
        press_enter()

    def _collect_user_details(self):
        """Collect personal details from user for password personalization."""
        clear_screen()
        print_header("🔐 STEP 1: YOUR PERSONAL DETAILS", Colors.BRIGHT_CYAN)
        print(f"{Colors.GRAY}  These details add your 'personal touch' to passwords.{Colors.RESET}")
        print(f"{Colors.GRAY}  They are used locally only and NEVER stored or transmitted.{Colors.RESET}\n")

        self.user_data['name'] = get_input("What is your name? (First name is enough)")
        self.user_data['nickname'] = get_input("Any nickname you go by? (or press Enter to skip)", allow_empty=True)
        self.user_data['birth_year'] = get_input("What year were you born? (e.g., 1995) - adds uniqueness")
        self.user_data['favorite_number'] = get_input("What's your favorite number? (e.g., 7, 21, 99)")
        self.user_data['favorite_color'] = get_input("What's your favorite color?")
        self.user_data['pet'] = get_input("Pet name or favorite animal? (or press Enter to skip)", allow_empty=True)
        self.user_data['hobby'] = get_input("What's your favorite hobby or interest?")

        print(f"\n{Colors.BRIGHT_GREEN}  ✅ Personal details collected! Your touch will make passwords unique.{Colors.RESET}")
        time.sleep(0.8)

    def _collect_preferences(self):
        """Collect password generation preferences."""
        clear_screen()
        print_header("⚙️  STEP 2: PASSWORD PREFERENCES", Colors.BRIGHT_MAGENTA)

        # Password length
        print(f"{Colors.BRIGHT_GREEN}┌─[{Colors.BRIGHT_CYAN}?{Colors.BRIGHT_GREEN}] Choose password length:{Colors.RESET}")
        print(f"{Colors.GRAY}│   8-12  : Standard security{Colors.RESET}")
        print(f"{Colors.GRAY}│   12-16 : Strong security (recommended){Colors.RESET}")
        print(f"{Colors.GRAY}│   16-32 : Maximum security{Colors.RESET}")
        print(f"{Colors.BRIGHT_GREEN}└─{Colors.BOLD}➤{Colors.RESET} ", end='')
        while True:
            try:
                length = int(input().strip())
                if 6 <= length <= 64:
                    self.preferences['length'] = length
                    break
                print(f"  {Colors.YELLOW}  [!] Choose between 6 and 64 characters.{Colors.RESET}")
                print(f"  {Colors.BOLD}➤{Colors.RESET} ", end='')
            except ValueError:
                print(f"  {Colors.YELLOW}  [!] Please enter a valid number.{Colors.RESET}")
                print(f"  {Colors.BOLD}➤{Colors.RESET} ", end='')

        # Include symbols
        sym_choice = select_option(
            "Include special characters (!@#$%^&* etc.)?",
            ["Yes - Maximum security", "No - Alphanumeric only"]
        )
        self.preferences['use_symbols'] = sym_choice.startswith("Yes")

        # Avoid ambiguous characters
        amb_choice = select_option(
            "Avoid ambiguous characters? (i, l, 1, L, o, 0, O)",
            ["No - Use all characters", "Yes - Avoid confusion"]
        )
        self.preferences['avoid_ambiguous'] = amb_choice.startswith("Yes")

        # Personal touch
        touch_choice = select_option(
            "Use personal touch in password generation?",
            ["Yes - Make it personal and unique", "No - Pure random only"]
        )
        self.preferences['use_personal_touch'] = touch_choice.startswith("Yes")

        print(f"\n{Colors.BRIGHT_GREEN}  ✅ Preferences saved! Ready to generate unhackable passwords.{Colors.RESET}")
        time.sleep(0.8)

    def _main_menu(self):
        """Display and handle the main menu."""
        while True:
            clear_screen()
            print(BANNER)
            print(f"{Colors.BRIGHT_CYAN}  👤 User: {Colors.BRIGHT_WHITE}{self.user_data.get('name', 'Unknown')}{Colors.RESET}")
            print(f"{Colors.DIM}  ─────────────────────────────────────────────{Colors.RESET}")
            print()

            menu_options = [
                f"{Colors.BRIGHT_GREEN}[1]{Colors.RESET}  {Colors.BOLD}Generate Passwords{Colors.RESET}      - Create unhackable passwords",
                f"{Colors.BRIGHT_CYAN}[2]{Colors.RESET}  {Colors.BOLD}Analyze a Password{Colors.RESET}     - Test strength of any password",
                f"{Colors.BRIGHT_MAGENTA}[3]{Colors.RESET}  {Colors.BOLD}Generate Memorable{Colors.RESET}    - Easy to recall, hard to crack",
                f"{Colors.BRIGHT_YELLOW}[4]{Colors.RESET}  {Colors.BOLD}View History{Colors.RESET}          - Recently generated passwords",
                f"{Colors.BRIGHT_BLUE}[5]{Colors.RESET}  {Colors.BOLD}Reset My Details{Colors.RESET}       - Re-enter personal information",
                f"{Colors.BRIGHT_RED}[6]{Colors.RESET}  {Colors.BOLD}Settings{Colors.RESET}              - Change password preferences",
                f"{Colors.GRAY}[0]{Colors.RESET}  {Colors.BOLD}Exit{Colors.RESET}                - Quit Cywallearn Unhacked",
            ]

            for option in menu_options:
                print(f"    {option}")

            print(f"\n{Colors.BRIGHT_GREEN}  └─{Colors.BOLD}➤{Colors.RESET} ", end='')

            choice = input().strip()

            if choice == '1':
                self._generate_passwords()
            elif choice == '2':
                self._analyze_password()
            elif choice == '3':
                self._generate_memorable()
            elif choice == '4':
                self._view_history()
            elif choice == '5':
                self._collect_user_details()
            elif choice == '6':
                self._collect_preferences()
            elif choice == '0':
                self._goodbye()
                break
            else:
                print(f"\n{Colors.YELLOW}  [!] Invalid choice. Try again.{Colors.RESET}")
                time.sleep(0.8)

    def _generate_passwords(self):
        """Generate and display passwords."""
        clear_screen()
        print_header("🔑 GENERATING UNHACKABLE PASSWORDS", Colors.BRIGHT_GREEN)

        generator = CywalGenerator(self.user_data, self.preferences)

        print(f"{Colors.GRAY}  Using cryptographically secure randomness + personal touch...{Colors.RESET}\n")
        time.sleep(0.3)

        results = generator.generate_multiple(5)

        for i, (password, metadata) in enumerate(results, 1):
            entropy = metadata.get('entropy_bits', 0)
            # Color coded by entropy
            if entropy < 40:
                color = Colors.BRIGHT_RED
            elif entropy < 60:
                color = Colors.BRIGHT_YELLOW
            elif entropy < 80:
                color = Colors.BRIGHT_CYAN
            else:
                color = Colors.BRIGHT_MAGENTA

            char_types = metadata.get('character_types', {})
            types_str = f"{char_types.get('uppercase', 0)}u {char_types.get('lowercase', 0)}l {char_types.get('digits', 0)}d {char_types.get('symbols', 0)}s"

            print(f"  {Colors.BRIGHT_WHITE}[{i}]{Colors.RESET} {color}{Colors.BOLD}{password}{Colors.RESET}")
            print(f"       {Colors.GRAY}Entropy: {entropy} bits | Length: {metadata['length']} | Types: {types_str}{Colors.RESET}\n")

            # Save to history
            self.history.append({
                'type': 'standard',
                'password': password,
                'entropy': entropy,
                'length': metadata['length'],
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            })

        time.sleep(0.3)
        print(f"  {Colors.BRIGHT_GREEN}✅ Generated 5 passwords above{Colors.RESET}")

        # Option to analyze one
        analyze_choice = select_option(
            "Analyze one of these passwords?",
            ["No, thanks", "Yes - analyze password #1",
             "Yes - analyze password #2", "Yes - analyze password #3",
             "Yes - analyze password #4", "Yes - analyze password #5"]
        )
        if analyze_choice != "No, thanks":
            idx = int(analyze_choice[-1]) - 1
            self._display_analysis(results[idx][0])

        # Option to regenerate
        regen = select_option("What next?", ["Generate more passwords", "Back to menu"])
        if regen == "Generate more passwords":
            self._generate_passwords()

    def _generate_memorable(self):
        """Generate memorable passwords with personal touch."""
        clear_screen()
        print_header("🧠 MEMORABLE PASSWORDS - EASY TO REMEMBER, HARD TO CRACK", Colors.BRIGHT_MAGENTA)

        generator = MemorableGenerator(self.user_data, self.preferences)

        print(f"{Colors.GRAY}  Creating memorable-yet-secure passwords from your personal data...{Colors.RESET}\n")
        time.sleep(0.3)

        results = []
        for i in range(5):
            password, metadata = generator.generate_memorable()
            results.append((password, metadata))

            entropy = metadata.get('entropy_bits', 0)
            if entropy < 40:
                color = Colors.BRIGHT_RED
            elif entropy < 60:
                color = Colors.BRIGHT_YELLOW
            elif entropy < 80:
                color = Colors.BRIGHT_CYAN
            else:
                color = Colors.BRIGHT_MAGENTA

            char_types = metadata.get('character_types', {})
            types_str = f"{char_types.get('uppercase', 0)}u {char_types.get('lowercase', 0)}l {char_types.get('digits', 0)}d {char_types.get('symbols', 0)}s"

            print(f"  {Colors.BRIGHT_WHITE}[{i+1}]{Colors.RESET} {color}{Colors.BOLD}{password}{Colors.RESET}")
            print(f"       {Colors.GRAY}Entropy: {entropy} bits | Length: {metadata['length']} | Types: {types_str}{Colors.RESET}\n")

            self.history.append({
                'type': 'memorable',
                'password': password,
                'entropy': entropy,
                'length': metadata['length'],
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            })

        analyze_choice = select_option(
            "Analyze one of these passwords?",
            ["No, thanks"] + [f"Yes - analyze #{i}" for i in range(1, 6)]
        )
        if analyze_choice != "No, thanks":
            idx = int(analyze_choice[-1]) - 1
            self._display_analysis(results[idx][0])

        regen = select_option("What next?", ["Generate more memorable passwords", "Back to menu"])
        if regen == "Generate more memorable passwords":
            self._generate_memorable()

    def _analyze_password(self):
        """Analyze a user-provided password."""
        clear_screen()
        print_header("🔍 PASSWORD STRENGTH ANALYZER", Colors.BRIGHT_CYAN)
        print(f"{Colors.GRAY}  Enter a password to analyze its strength, entropy, and crack resistance.{Colors.RESET}\n")

        password = get_input("Enter the password to analyze:", Colors.BRIGHT_YELLOW, allow_empty=False)

        self._display_analysis(password)

        press_enter()

    def _display_analysis(self, password: str):
        """Display detailed analysis for a password."""
        print(f"\n  {Colors.BOLD}Analyzing password...{Colors.RESET}")
        time.sleep(0.3)

        # Animated analysis
        steps = [
            "  Checking character set...",
            "  Calculating entropy...",
            "  Detecting patterns...",
            "  Estimating crack time...",
            "  Generating report...",
        ]
        for step in steps:
            print(f"  {Colors.GRAY}{step}{Colors.RESET}")
            time.sleep(0.15)

        analyzer = CywalAnalyzer(password)
        analysis = analyzer.analyze()
        strength = analysis['strength']

        # Color based on strength
        strength_colors = {
            'Very Weak': Colors.BRIGHT_RED,
            'Weak': Colors.BRIGHT_YELLOW,
            'Moderate': Colors.YELLOW,
            'Strong': Colors.BRIGHT_GREEN,
            'Very Strong': Colors.BRIGHT_CYAN,
            'Excellent': Colors.BRIGHT_MAGENTA,
            'Unbreakable': Colors.BRIGHT_MAGENTA + Colors.BLINK,
        }
        s_color = strength_colors.get(strength['level'], Colors.BRIGHT_WHITE)

        print(f"\n  {Colors.BOLD}{'═' * 56}{Colors.RESET}")
        print(f"  {Colors.BOLD}📊 PASSWORD ANALYSIS RESULTS{Colors.RESET}")
        print(f"  {Colors.BOLD}{'═' * 56}{Colors.RESET}")
        print(f"\n  {Colors.BRIGHT_WHITE}Password    :{Colors.RESET} {'•' * len(password)} (hidden for security)")
        print(f"  {Colors.BRIGHT_WHITE}Length      :{Colors.RESET} {analysis['password_length']} characters")
        print(f"  {Colors.BRIGHT_WHITE}Charset Size:{Colors.RESET} {analysis['charset_size']} (log₂ = {math.log2(max(analysis['charset_size'], 1)):.2f})")
        print(f"  {Colors.BRIGHT_WHITE}Entropy     :{Colors.RESET} {analysis['entropy_bits']} bits")
        print(f"  {Colors.BRIGHT_WHITE}Unique chars:{Colors.RESET} {analysis['unique_characters']} ({analysis['unique_ratio']*100:.0f}% diversity)")
        print()

        # Strength gauge
        score = strength['score']
        bar_filled = '█' * (score // 10)
        bar_empty = '░' * (10 - score // 10)
        print(f"  {s_color}{Colors.BOLD}  ╔═══ STRENGTH ═══╗{Colors.RESET}")
        print(f"  {s_color}{Colors.BOLD}  ║  {strength['level']:^16s}  ║{Colors.RESET}")
        print(f"  {s_color}{Colors.BOLD}  ║  Score: {score:3d}/100    ║{Colors.RESET}")
        print(f"  {s_color}{Colors.BOLD}  ║  {bar_filled}{bar_empty}  ║{Colors.RESET}")
        print(f"  {s_color}{Colors.BOLD}  ╚═══════════════════╝{Colors.RESET}")
        print()

        # Character distribution
        print(f"  {Colors.BRIGHT_WHITE}Character Distribution:{Colors.RESET}")
        print(f"    {Colors.BRIGHT_RED}█{Colors.RESET} Uppercase: {analysis['character_distribution']['uppercase']}")
        print(f"    {Colors.BRIGHT_GREEN}█{Colors.RESET} Lowercase: {analysis['character_distribution']['lowercase']}")
        print(f"    {Colors.BRIGHT_YELLOW}█{Colors.RESET} Digits   : {analysis['character_distribution']['digits']}")
        print(f"    {Colors.BRIGHT_CYAN}█{Colors.RESET} Symbols  : {analysis['character_distribution']['symbols']}")
        print()

        # Crack time estimates
        print(f"  {Colors.BRIGHT_WHITE}⏱  Crack Time Estimates:{Colors.RESET}")
        print(f"  {Colors.GRAY}  (Time to crack with modern hardware){Colors.RESET}")
        crack_times = analysis['crack_time_estimates']
        for hash_type, estimate in crack_times.items():
            # Color based on time
            ct = estimate['seconds']
            if ct < 60:
                c = Colors.BRIGHT_RED
            elif ct < 3600:
                c = Colors.BRIGHT_YELLOW
            elif ct < 86400:
                c = Colors.YELLOW
            elif ct < 31536000:
                c = Colors.BRIGHT_GREEN
            elif ct < 31536000 * 100:
                c = Colors.BRIGHT_CYAN
            else:
                c = Colors.BRIGHT_MAGENTA
            print(f"    {c}▸{Colors.RESET} {hash_type:12s}: {estimate['human_readable']}")

        print()

        # Patterns detected
        if analysis['detected_patterns']:
            print(f"  {Colors.BRIGHT_RED}⚠  Detected Patterns:{Colors.RESET}")
            for pattern in analysis['detected_patterns']:
                print(f"    • {pattern['pattern']}: {', '.join(str(m) for m in pattern['matches'])}")
            print()

        # Suggestions
        print(f"  {Colors.BRIGHT_WHITE}💡 Suggestions:{Colors.RESET}")
        for suggestion in analysis['suggestions']:
            if suggestion.startswith('✅'):
                print(f"    {Colors.BRIGHT_GREEN}{suggestion}{Colors.RESET}")
            else:
                print(f"    {Colors.YELLOW}• {suggestion}{Colors.RESET}")

        # Hashes
        print(f"\n  {Colors.DIM}Password Hashes (for password storage reference):{Colors.RESET}")
        for algo, hash_val in list(analysis['hashes'].items())[:2]:
            print(f"    {Colors.GRAY}{algo:8s}: {hash_val[:48]}...{Colors.RESET}")

        print(f"\n  {Colors.BOLD}{'═' * 56}{Colors.RESET}")

    def _view_history(self):
        """Display password generation history."""
        clear_screen()
        print_header("📜 PASSWORD GENERATION HISTORY", Colors.BRIGHT_YELLOW)

        if not self.history:
            print(f"  {Colors.YELLOW}No passwords generated yet. Generate some first!{Colors.RESET}")
            press_enter()
            return

        # Show last 15 entries
        display = self.history[-15:]
        display.reverse()

        print(f"  {Colors.DIM}Showing last {len(display)} passwords (most recent first):{Colors.RESET}\n")

        for i, entry in enumerate(display, 1):
            entropy = entry.get('entropy', 0)
            if entropy < 40:
                color = Colors.BRIGHT_RED
            elif entropy < 60:
                color = Colors.BRIGHT_YELLOW
            elif entropy < 80:
                color = Colors.BRIGHT_CYAN
            else:
                color = Colors.BRIGHT_MAGENTA

            print(f"  {Colors.DIM}[{i}]{Colors.RESET} {color}{entry['password']}{Colors.RESET}")
            print(f"       {Colors.GRAY}Type: {entry['type']} | Length: {entry['length']} | "
                  f"Entropy: {entropy} bits | {entry['timestamp']}{Colors.RESET}")
            print()

        print(f"  {Colors.BRIGHT_WHITE}Total passwords generated: {len(self.history)}{Colors.RESET}\n")

        # Option to clear history
        clear_choice = select_option(
            "Clear history?",
            ["Keep history", "Clear all history"]
        )
        if clear_choice == "Clear all history":
            self.history.clear()
            print(f"\n  {Colors.BRIGHT_GREEN}✅ History cleared.{Colors.RESET}")

        press_enter()

    def _goodbye(self):
        """Display goodbye message."""
        clear_screen()
        print(f"""
{Colors.BRIGHT_CYAN}{Colors.BOLD}
     ██████╗██╗   ██╗██╗    ██╗ █████╗ ██╗     ██╗     ███████╗ █████╗ ██████╗ ███╗   ██╗
    ██╔════╝╚██╗ ██╔╝██║    ██║██╔══██╗██║     ██║     ██╔════╝██╔══██╗██╔══██╗████╗  ██║
    ██║      ╚████╔╝ ██║ █╗ ██║███████║██║     ██║     █████╗  ███████║██████╔╝██╔██╗ ██║
    ██║       ╚██╔╝  ██║███╗██║██╔══██║██║     ██║     ██╔══╝  ██╔══██║██╔══██╗██║╚██╗██║
    ╚██████╗   ██║   ╚███╔███╔╝██║  ██║███████╗███████╗███████╗██║  ██║██║  ██║██║ ╚████║
     ╚═════╝   ╚═╝    ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
{Colors.RESET}
{Colors.BRIGHT_GREEN}{Colors.BOLD}
              🔐  Stay Unhackable. Stay Cywallearn.  🔐{Colors.RESET}
{Colors.GRAY}
              Thank you for using Cywallearn Unhacked!
         Remember: Strong passwords are the first line of defense.
{Colors.RESET}
{Colors.BRIGHT_CYAN}              🌐 github.com/cywallearn/cywallearn-unhacked{Colors.RESET}
        """)
        time.sleep(2)


# ─── Entry Point ─────────────────────────────────────────────────

def main():
    """Application entry point."""
    try:
        app = CywallearnApp()
        app.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.BRIGHT_YELLOW}  [!] Interrupted. Stay secure!{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.BRIGHT_RED}  [!] Error: {e}{Colors.RESET}")
        sys.exit(1)


if __name__ == '__main__':
    main()
