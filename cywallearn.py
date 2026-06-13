#!/usr/bin/env python3
"""
CYWALLEARN UNHACKED - Password Generator
"Unhackable by Design - Secured by Cywallearn"
Version 1.0.0 - Termux Ready
Compatible with: Termux, Linux, macOS, Windows
"""

import sys
import os
import math
import time
import json
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules'))

try:
    from generator import CywalGenerator, MemorableGenerator
    from analyzer import CywalAnalyzer
except ImportError as e:
    print(f"[!] Error loading modules: {e}")
    print("[!] Make sure the 'modules' directory is present.")
    sys.exit(1)


# Terminal Colors
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    GRAY = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

if os.name == 'nt':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        for attr in dir(Colors):
            if not attr.startswith('_') and isinstance(getattr(Colors, attr), str):
                setattr(Colors, attr, '')


# Branding Banner
BANNER = f"""
{Colors.BRIGHT_CYAN}{Colors.BOLD}
   /$$$$$$$$ /$$       /$$$$$$$  /$$$$$$$  /$$$$$$ /$$$$$$$$ /$$$$$$$$
  | $$_____/| $$      | $$__  $$| $$__  $$|_  $$_/| $$_____/|__  $$__/
  | $$      | $$      | $$  \\ $$| $$  \\ $$  | $$  | $$         | $$
  | $$$$$   | $$      | $$  | $$| $$$$$$$/  | $$  | $$$$$      | $$
  | $$__/   | $$      | $$  | $$| $$__  $$  | $$  | $$__/      | $$
  | $$      | $$      | $$  | $$| $$  \\ $$  | $$  | $$         | $$
  | $$      | $$$$$$$$| $$$$$$$/| $$  | $$ /$$$$$$| $$$$$$$$   | $$
  |__/      |________/|_______/ |__/  |__/|______/|________/   |__/{Colors.RESET}
{Colors.BRIGHT_GREEN}{Colors.BOLD}
              UNHACKED PASSWORD GENERATOR v1.0.0{Colors.RESET}
{Colors.GRAY}         "Unhackable by Design - Secured by Cywallearn"{Colors.RESET}
"""


# Utility Functions

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title, color=Colors.BRIGHT_CYAN):
    width = 56
    border = color + Colors.BOLD + "+" + "=" * (width - 2) + "+" + Colors.RESET
    print(f"\n{border}")
    print(f"{color}{Colors.BOLD}|{title:^{width-2}s}|{Colors.RESET}")
    print(f"{border}\n")


def get_input(prompt_text, color=Colors.BRIGHT_GREEN, allow_empty=False):
    while True:
        print(f"{color}[?] {prompt_text}{Colors.RESET}")
        print(f"{color}[>]{Colors.RESET} ", end='')
        value = input().strip()
        if value or allow_empty:
            return value
        print(f"{Colors.YELLOW}[!] Input cannot be empty.{Colors.RESET}")


def select_option(prompt_text, options, color=Colors.BRIGHT_GREEN):
    print(f"{color}[?] {prompt_text}{Colors.RESET}")
    for i, option in enumerate(options, 1):
        print(f"    {Colors.BRIGHT_YELLOW}[{i}]{Colors.RESET} {option}")
    print(f"{color}[>]{Colors.RESET} ", end='')

    while True:
        try:
            choice = input().strip()
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx]
            print(f"  {Colors.YELLOW}[!] Enter 1-{len(options)}.{Colors.RESET} [>] ", end='')
        except ValueError:
            print(f"  {Colors.YELLOW}[!] Invalid.{Colors.RESET} [>] ", end='')


def press_enter():
    print(f"\n{Colors.GRAY}[ Press Enter to continue... ]{Colors.RESET}", end='')
    input()


# Application

class CywallearnApp:
    def __init__(self):
        self.user_data = {}
        self.preferences = {
            'length': 8,
            'use_symbols': True,
            'avoid_ambiguous': False,
            'use_personal_touch': True,
        }
        self.history = []

    def run(self):
        try:
            self._show_splash()
            self._collect_user_details()
            self._collect_preferences()
            self._main_menu()
        except KeyboardInterrupt:
            print(f"\n\n{Colors.BRIGHT_YELLOW}[!] Interrupted. Exiting...{Colors.RESET}")
            self._goodbye()
        except EOFError:
            print(f"\n\n{Colors.BRIGHT_YELLOW}[!] Exiting...{Colors.RESET}")
        sys.exit(0)

    def _show_splash(self):
        clear_screen()
        print(BANNER)
        time.sleep(0.5)
        print(f"{Colors.DIM}  Termux Compatible | Cross-Platform | Military-Grade Security{Colors.RESET}")
        print(f"{Colors.DIM}  Built with Python's 'secrets' module - Cryptographically Secure{Colors.RESET}\n")
        time.sleep(0.8)
        press_enter()

    def _collect_user_details(self):
        clear_screen()
        print_header("STEP 1: YOUR PERSONAL DETAILS", Colors.BRIGHT_CYAN)
        print(f"{Colors.GRAY}  These add your 'personal touch' to passwords.{Colors.RESET}")
        print(f"{Colors.GRAY}  Used locally only - NEVER stored or transmitted.{Colors.RESET}\n")

        self.user_data['name'] = get_input("What is your name?")
        self.user_data['nickname'] = get_input("Any nickname? (Enter to skip)", allow_empty=True)
        self.user_data['birth_year'] = get_input("Birth year? (e.g., 1995)")
        self.user_data['favorite_number'] = get_input("Favorite number? (e.g., 7, 21)")
        self.user_data['favorite_color'] = get_input("Favorite color?")
        self.user_data['pet'] = get_input("Pet name or favorite animal? (Enter to skip)", allow_empty=True)
        self.user_data['hobby'] = get_input("Favorite hobby or interest?")

        print(f"\n{Colors.BRIGHT_GREEN}  Personal details collected!{Colors.RESET}")
        time.sleep(0.8)

    def _collect_preferences(self):
        clear_screen()
        print_header("STEP 2: PASSWORD PREFERENCES", Colors.BRIGHT_MAGENTA)

        print(f"{Colors.BRIGHT_GREEN}[?] Choose password length:{Colors.RESET}")
        print(f"    8-12  : Standard security")
        print(f"    12-16 : Strong security (recommended)")
        print(f"    16-32 : Maximum security")
        print(f"{Colors.BRIGHT_GREEN}[>]{Colors.RESET} ", end='')
        while True:
            try:
                length = int(input().strip())
                if 6 <= length <= 64:
                    self.preferences['length'] = length
                    break
                print(f"  {Colors.YELLOW}Choose 6-64.{Colors.RESET} [>] ", end='')
            except ValueError:
                print(f"  {Colors.YELLOW}Enter a number.{Colors.RESET} [>] ", end='')

        sym = select_option("Include special characters (!@#$%^&* etc.)?", ["Yes - Maximum security", "No - Alphanumeric only"])
        self.preferences['use_symbols'] = sym.startswith("Yes")

        amb = select_option("Avoid ambiguous characters? (i,l,1,L,o,0,O)", ["No - Use all", "Yes - Avoid confusion"])
        self.preferences['avoid_ambiguous'] = amb.startswith("Yes")

        touch = select_option("Use personal touch?", ["Yes - Personal and unique", "No - Pure random"])
        self.preferences['use_personal_touch'] = touch.startswith("Yes")

        print(f"\n{Colors.BRIGHT_GREEN}  Preferences saved!{Colors.RESET}")
        time.sleep(0.8)

    def _main_menu(self):
        while True:
            clear_screen()
            print(BANNER)
            name = self.user_data.get('name', 'Unknown')
            print(f"{Colors.BRIGHT_CYAN}  User: {Colors.BRIGHT_WHITE}{name}{Colors.RESET}")
            print(f"{Colors.DIM}  {'-' * 50}{Colors.RESET}\n")

            print(f"    {Colors.BRIGHT_GREEN}[1]{Colors.RESET}  Generate Passwords")
            print(f"    {Colors.BRIGHT_CYAN}[2]{Colors.RESET}  Analyze a Password")
            print(f"    {Colors.BRIGHT_MAGENTA}[3]{Colors.RESET}  Generate Memorable")
            print(f"    {Colors.BRIGHT_YELLOW}[4]{Colors.RESET}  View History")
            print(f"    {Colors.BRIGHT_BLUE}[5]{Colors.RESET}  Reset My Details")
            print(f"    {Colors.BRIGHT_RED}[6]{Colors.RESET}  Settings")
            print(f"    {Colors.GRAY}[0]{Colors.RESET}  Exit\n")

            print(f"{Colors.BRIGHT_GREEN}[>]{Colors.RESET} ", end='')
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
                print(f"\n{Colors.YELLOW}[!] Invalid choice.{Colors.RESET}")
                time.sleep(0.8)

    def _generate_passwords(self):
        clear_screen()
        print_header("GENERATING UNHACKABLE PASSWORDS", Colors.BRIGHT_GREEN)

        generator = CywalGenerator(self.user_data, self.preferences)
        print(f"{Colors.GRAY}  Using cryptographically secure randomness + personal touch...{Colors.RESET}\n")
        time.sleep(0.3)

        results = generator.generate_multiple(5)

        for i, (password, metadata) in enumerate(results, 1):
            entropy = metadata.get('entropy_bits', 0)
            if entropy < 40: color = Colors.BRIGHT_RED
            elif entropy < 60: color = Colors.BRIGHT_YELLOW
            elif entropy < 80: color = Colors.BRIGHT_CYAN
            else: color = Colors.BRIGHT_MAGENTA

            ct = metadata.get('character_types', {})
            types_str = f"U:{ct.get('uppercase',0)} L:{ct.get('lowercase',0)} D:{ct.get('digits',0)} S:{ct.get('symbols',0)}"

            print(f"  {Colors.BRIGHT_WHITE}[{i}]{Colors.RESET} {color}{Colors.BOLD}{password}{Colors.RESET}")
            print(f"       {Colors.GRAY}Entropy: {entropy} bits | Length: {metadata['length']} | {types_str}{Colors.RESET}\n")

            self.history.append({
                'type': 'standard', 'password': password,
                'entropy': entropy, 'length': metadata['length'],
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            })

        time.sleep(0.3)
        print(f"  {Colors.BRIGHT_GREEN}Generated 5 passwords above{Colors.RESET}")

        ac = select_option("Analyze one?", ["No"] + [f"Password #{i}" for i in range(1, 6)])
        if ac != "No":
            idx = int(ac[-1]) - 1
            self._display_analysis(results[idx][0])

        more = select_option("Next?", ["Generate more", "Back to menu"])
        if more == "Generate more":
            self._generate_passwords()

    def _generate_memorable(self):
        clear_screen()
        print_header("MEMORABLE PASSWORDS - EASY TO REMEMBER, HARD TO CRACK", Colors.BRIGHT_MAGENTA)

        generator = MemorableGenerator(self.user_data, self.preferences)
        print(f"{Colors.GRAY}  Creating memorable-yet-secure passwords...{Colors.RESET}\n")
        time.sleep(0.3)

        results = []
        for i in range(5):
            password, metadata = generator.generate_memorable()
            results.append((password, metadata))

            entropy = metadata.get('entropy_bits', 0)
            if entropy < 40: color = Colors.BRIGHT_RED
            elif entropy < 60: color = Colors.BRIGHT_YELLOW
            elif entropy < 80: color = Colors.BRIGHT_CYAN
            else: color = Colors.BRIGHT_MAGENTA

            ct = metadata.get('character_types', {})
            types_str = f"U:{ct.get('uppercase',0)} L:{ct.get('lowercase',0)} D:{ct.get('digits',0)} S:{ct.get('symbols',0)}"

            print(f"  {Colors.BRIGHT_WHITE}[{i+1}]{Colors.RESET} {color}{Colors.BOLD}{password}{Colors.RESET}")
            print(f"       {Colors.GRAY}Entropy: {entropy} bits | Length: {metadata['length']} | {types_str}{Colors.RESET}\n")

            self.history.append({
                'type': 'memorable', 'password': password,
                'entropy': entropy, 'length': metadata['length'],
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            })

        ac = select_option("Analyze one?", ["No"] + [f"Password #{i}" for i in range(1, 6)])
        if ac != "No":
            idx = int(ac[-1]) - 1
            self._display_analysis(results[idx][0])

        more = select_option("Next?", ["Generate more memorable", "Back to menu"])
        if more == "Generate more memorable":
            self._generate_memorable()

    def _analyze_password(self):
        clear_screen()
        print_header("PASSWORD STRENGTH ANALYZER", Colors.BRIGHT_CYAN)
        print(f"{Colors.GRAY}  Analyze any password for strength, entropy, and crack resistance.{Colors.RESET}\n")

        password = get_input("Enter the password to analyze:", Colors.BRIGHT_YELLOW, allow_empty=False)
        self._display_analysis(password)
        press_enter()

    def _display_analysis(self, password):
        print(f"\n  {Colors.BOLD}Analyzing...{Colors.RESET}")
        time.sleep(0.3)

        steps = ["Character set...", "Entropy...", "Patterns...", "Crack time...", "Report..."]
        for s in steps:
            print(f"  {Colors.GRAY}{s}{Colors.RESET}")
            time.sleep(0.12)

        analyzer = CywalAnalyzer(password)
        analysis = analyzer.analyze()
        strength = analysis['strength']

        s_colors = {
            'Very Weak': Colors.BRIGHT_RED, 'Weak': Colors.BRIGHT_YELLOW,
            'Moderate': Colors.YELLOW, 'Strong': Colors.BRIGHT_GREEN,
            'Very Strong': Colors.BRIGHT_CYAN, 'Excellent': Colors.BRIGHT_MAGENTA,
            'Unbreakable': Colors.BRIGHT_MAGENTA,
        }
        s_color = s_colors.get(strength['level'], Colors.BRIGHT_WHITE)

        print(f"\n  {Colors.BOLD}{'=' * 52}{Colors.RESET}")
        print(f"  {Colors.BOLD}PASSWORD ANALYSIS RESULTS{Colors.RESET}")
        print(f"  {Colors.BOLD}{'=' * 52}{Colors.RESET}")

        print(f"\n  Length      : {analysis['password_length']} characters")
        print(f"  Charset Size: {analysis['charset_size']}")
        print(f"  Entropy     : {analysis['entropy_bits']} bits")
        print(f"  Unique chars: {analysis['unique_characters']} ({analysis['unique_ratio']*100:.0f}% diversity)\n")

        score = strength['score']
        bar = '#' * (score // 10) + '.' * (10 - score // 10)
        print(f"  {s_color}{Colors.BOLD}+--- STRENGTH ---+{Colors.RESET}")
        print(f"  {s_color}{Colors.BOLD}|  {strength['level']:^16s}  |{Colors.RESET}")
        print(f"  {s_color}{Colors.BOLD}|  Score: {score:3d}/100    |{Colors.RESET}")
        print(f"  {s_color}{Colors.BOLD}|  [{bar}]  |{Colors.RESET}")
        print(f"  {s_color}{Colors.BOLD}+-----------------+{Colors.RESET}\n")

        cd = analysis['character_distribution']
        print(f"  Character Distribution:")
        print(f"    Uppercase: {cd['uppercase']}")
        print(f"    Lowercase: {cd['lowercase']}")
        print(f"    Digits   : {cd['digits']}")
        print(f"    Symbols  : {cd['symbols']}\n")

        print(f"  Crack Time Estimates:")
        print(f"  (Time to crack with modern hardware)")
        for htype, est in analysis['crack_time_estimates'].items():
            print(f"    > {htype:12s}: {est['human_readable']}")
        print()

        if analysis['detected_patterns']:
            print(f"  Detected Patterns:")
            for p in analysis['detected_patterns']:
                print(f"    ! {p['pattern']}: {', '.join(str(m) for m in p['matches'])}")
            print()

        print(f"  Suggestions:")
        for s in analysis['suggestions']:
            print(f"    * {s}")

        print(f"\n  Hashes (first 2):")
        for algo, hv in list(analysis['hashes'].items())[:2]:
            print(f"    {algo:8s}: {hv[:48]}...")
        print(f"\n  {Colors.BOLD}{'=' * 52}{Colors.RESET}")

    def _view_history(self):
        clear_screen()
        print_header("PASSWORD GENERATION HISTORY", Colors.BRIGHT_YELLOW)

        if not self.history:
            print(f"  {Colors.YELLOW}No passwords generated yet.{Colors.RESET}")
            press_enter()
            return

        display = list(reversed(self.history[-15:]))
        print(f"  Showing last {len(display)} passwords:\n")

        for i, entry in enumerate(display, 1):
            entropy = entry.get('entropy', 0)
            if entropy < 40: color = Colors.BRIGHT_RED
            elif entropy < 60: color = Colors.BRIGHT_YELLOW
            elif entropy < 80: color = Colors.BRIGHT_CYAN
            else: color = Colors.BRIGHT_MAGENTA

            print(f"  [{i}] {color}{entry['password']}{Colors.RESET}")
            print(f"       Type: {entry['type']} | Length: {entry['length']} | Entropy: {entropy} bits | {entry['timestamp']}\n")

        print(f"  Total: {len(self.history)} passwords\n")

        ch = select_option("Clear history?", ["Keep", "Clear all"])
        if ch == "Clear all":
            self.history.clear()
            print(f"\n{Colors.BRIGHT_GREEN}  History cleared.{Colors.RESET}")

        press_enter()

    def _goodbye(self):
        clear_screen()
        print(f"""
{Colors.BRIGHT_CYAN}{Colors.BOLD}
   /$$$$$$$$ /$$       /$$$$$$$  /$$$$$$$  /$$$$$$ /$$$$$$$$ /$$$$$$$$
  | $$_____/| $$      | $$__  $$| $$__  $$|_  $$_/| $$_____/|__  $$__/
  | $$      | $$      | $$  \\ $$| $$  \\ $$  | $$  | $$         | $$
  | $$$$$   | $$      | $$  | $$| $$$$$$$/  | $$  | $$$$$      | $$
  | $$__/   | $$      | $$  | $$| $$__  $$  | $$  | $$__/      | $$
  | $$      | $$      | $$  | $$| $$  \\ $$  | $$  | $$         | $$
  | $$      | $$$$$$$$| $$$$$$$/| $$  | $$ /$$$$$$| $$$$$$$$   | $$
  |__/      |________/|_______/ |__/  |__/|______/|________/   |__/{Colors.RESET}
{Colors.BRIGHT_GREEN}{Colors.BOLD}
              Stay Unhackable. Stay Cywallearn.{Colors.RESET}
{Colors.GRAY}
              Thank you for using Cywallearn Unhacked!
         Strong passwords are the first line of defense.{Colors.RESET}
{Colors.BRIGHT_CYAN}              github.com/cywallearn/cywallearn-unhacked{Colors.RESET}
        """)
        time.sleep(2)


def main():
    try:
        app = CywallearnApp()
        app.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.BRIGHT_YELLOW}[!] Interrupted. Stay secure!{Colors.RESET}")
    except Exception as e:
        import traceback
        print(f"\n{Colors.BRIGHT_RED}[!] Error: {e}{Colors.RESET}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
