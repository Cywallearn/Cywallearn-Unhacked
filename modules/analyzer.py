#!/usr/bin/env python3
# Cywallearn Unhacked - Password Strength Analyzer
# Provides deep analysis of password strength, entropy, and crack time estimates.

import math
import re
import hashlib
from typing import Dict, List, Tuple, Optional


class CywalAnalyzer:
    COMMON_PASSWORDS = {
        '123456', 'password', '12345678', 'qwerty', '123456789',
        '12345', '1234', '111111', '1234567', 'sunshine',
        'qwerty123', 'iloveyou', 'princess', 'admin', 'welcome',
        '666666', 'abc123', 'football', '123123', 'monkey',
        '654321', '!@#$%^&*', 'charlie', 'aa123456', 'donald',
        'password1', 'qwerty12345', '1234567890', 'letmein',
        'password123', 'dragon', 'baseball', 'ashley', 'batman',
        'trustno1', 'hunter', 'ranger', 'starwars', 'master',
    }

    PATTERNS = {
        'sequential_numbers': re.compile(r'(?:012|123|234|345|456|567|678|789|890|987|876|765|654|543|432|321|210)'),
        'sequential_letters': re.compile(r'(?:abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz|zyx|yxw|xwv|wvu|vut|uts|tsr|srq|rqp|qpo|pon|onm|nml|mlk|lkj|kji|jih|ihg|hgf|gfe|fed|edc|dcb|cba)'),
        'repeated_chars': re.compile(r'(.)\1{2,}'),
        'repeated_pairs': re.compile(r'(..)\1{2,}'),
        'keyboard_rows': re.compile(r'(?:qwerty|asdfgh|zxcvbn|qwertz|azerty|poiuyt|mnbvcx|lkjhgf)'),
        'dates': re.compile(r'(?:19|20)\d{2}[-/.]?(?:0[1-9]|1[0-2])[-/.]?(?:0[1-9]|[12]\d|3[01])'),
        'years': re.compile(r'(?:19|20)\d{2}'),
        'phone_like': re.compile(r'\d{10,11}'),
    }

    HASH_RATES = {
        'md5_fast': 1_000_000_000_000,
        'sha1_fast': 500_000_000_000,
        'sha256': 50_000_000_000,
        'bcrypt_05': 10_000,
        'bcrypt_10': 1_000,
        'bcrypt_12': 250,
        'argon2': 100,
        'pbkdf2_sha256': 500_000,
        'scrypt': 50_000,
        'ntlm': 1_000_000_000_000,
    }

    def __init__(self, password: str):
        self.password = password
        self.length = len(password)
        self.char_set_size = self._calculate_charset_size()
        self.entropy_bits = self._calculate_entropy()

    def _calculate_charset_size(self) -> int:
        size = 0
        has_lower = bool(re.search(r'[a-z]', self.password))
        has_upper = bool(re.search(r'[A-Z]', self.password))
        has_digit = bool(re.search(r'\d', self.password))
        has_symbol = bool(re.search(r'[^a-zA-Z0-9]', self.password))
        if has_lower: size += 26
        if has_upper: size += 26
        if has_digit: size += 10
        if has_symbol: size += 33
        return size if size > 0 else 26

    def _calculate_entropy(self) -> float:
        if self.length == 0:
            return 0.0
        full_entropy = self.length * math.log2(self.char_set_size)
        penalty = self._calculate_pattern_penalty()
        effective_entropy = full_entropy * (1 - penalty)
        return round(max(effective_entropy, full_entropy * 0.3), 2)

    def _calculate_pattern_penalty(self) -> float:
        penalty = 0.0
        password_lower = self.password.lower()

        if password_lower in self.COMMON_PASSWORDS:
            penalty += 0.5

        for pattern_name, regex in self.PATTERNS.items():
            if regex.search(self.password):
                if pattern_name in ['sequential_numbers', 'sequential_letters']:
                    penalty += 0.15
                elif pattern_name == 'repeated_chars':
                    penalty += 0.20
                elif pattern_name == 'repeated_pairs':
                    penalty += 0.15
                elif pattern_name == 'keyboard_rows':
                    penalty += 0.25
                elif pattern_name in ['dates', 'years']:
                    penalty += 0.10

        common_words = ['password', 'admin', 'user', 'login', 'pass', 'key',
                       'master', 'hello', 'world', 'love', 'life', 'hack',
                       'secure', 'code', 'test', 'demo', 'guest', 'root']
        for word in common_words:
            if word in password_lower:
                penalty += 0.10
                break

        if len(set(self.password)) <= self.length * 0.3:
            penalty += 0.15
        if self.password.islower() or self.password.isupper():
            penalty += 0.15
        if self.password.isalpha() or self.password.isdigit():
            penalty += 0.20

        return min(penalty, 0.7)

    def _estimate_crack_time(self, hash_type: str = 'sha256') -> Dict:
        rate = self.HASH_RATES.get(hash_type, 50_000_000_000)
        combinations = self.char_set_size ** self.length
        seconds = combinations / rate
        return {
            'hash_type': hash_type,
            'combinations': combinations,
            'seconds': seconds,
            'human_readable': self._format_duration(seconds),
            'brute_force': self._format_duration(combinations / rate),
            'dictionary': 'Instant' if self._is_common() else 'Resistant',
            'mask_attack': self._format_duration(combinations / (rate * 1000)),
        }

    def _is_common(self) -> bool:
        return self.password.lower() in self.COMMON_PASSWORDS

    def _format_duration(self, seconds: float) -> str:
        if seconds < 0:
            return "Instant"
        intervals = [
            ('century', 60 * 60 * 24 * 365 * 100),
            ('year', 60 * 60 * 24 * 365),
            ('month', 60 * 60 * 24 * 30),
            ('week', 60 * 60 * 24 * 7),
            ('day', 60 * 60 * 24),
            ('hour', 60 * 60),
            ('minute', 60),
            ('second', 1),
        ]
        if seconds < 1:
            return "Less than a second"
        if seconds < 60:
            return f"{int(seconds)} seconds"
        parts = []
        for name, duration in intervals:
            if seconds >= duration:
                count = int(seconds // duration)
                seconds %= duration
                if count > 0:
                    part = f"{count} {name}"
                    if count > 1:
                        part += "s"
                    parts.append(part)
                    if len(parts) >= 2:
                        break
        return ", ".join(parts) if parts else "Less than a second"

    def analyze(self) -> Dict:
        char_counts = {
            'lowercase': sum(1 for c in self.password if c.islower()),
            'uppercase': sum(1 for c in self.password if c.isupper()),
            'digits': sum(1 for c in self.password if c.isdigit()),
            'symbols': sum(1 for c in self.password if not c.isalnum()),
        }
        unique_ratio = len(set(self.password)) / max(self.length, 1)

        detected_patterns = []
        for pattern_name, regex in self.PATTERNS.items():
            matches = regex.findall(self.password)
            if matches:
                detected_patterns.append({
                    'pattern': pattern_name,
                    'matches': matches[:3]
                })

        crack_times = {}
        for hash_type in ['sha256', 'md5_fast', 'bcrypt_10', 'ntlm', 'argon2']:
            crack_times[hash_type] = self._estimate_crack_time(hash_type)

        strength = self._assess_strength()

        hashes = {
            'md5': hashlib.md5(self.password.encode()).hexdigest(),
            'sha1': hashlib.sha1(self.password.encode()).hexdigest(),
            'sha256': hashlib.sha256(self.password.encode()).hexdigest(),
            'sha512': hashlib.sha512(self.password.encode()).hexdigest(),
        }

        suggestions = self._generate_suggestions()

        return {
            'password_length': self.length,
            'charset_size': self.char_set_size,
            'entropy_bits': self.entropy_bits,
            'character_distribution': char_counts,
            'unique_characters': len(set(self.password)),
            'unique_ratio': round(unique_ratio, 2),
            'detected_patterns': detected_patterns,
            'is_common_password': self._is_common(),
            'strength': strength,
            'crack_time_estimates': crack_times,
            'hashes': hashes,
            'suggestions': suggestions,
        }

    def _assess_strength(self) -> Dict:
        entropy = self.entropy_bits
        if self.length < 6:
            level, score = "Very Weak", 10
        elif self.length < 8:
            level, score = "Weak", 25
        elif entropy < 40:
            level, score = "Moderate", 45
        elif entropy < 60:
            level, score = "Strong", 65
        elif entropy < 80:
            level, score = "Very Strong", 85
        elif entropy < 120:
            level, score = "Excellent", 95
        else:
            level, score = "Unbreakable", 100

        return {'level': level, 'score': score, 'entropy_bits': entropy}

    def _generate_suggestions(self) -> List[str]:
        suggestions = []
        if self.length < 8:
            suggestions.append("Increase password length to at least 12 characters.")
        elif self.length < 12:
            suggestions.append("Consider using 14+ characters for maximum security.")

        has_lower = any(c.islower() for c in self.password)
        has_upper = any(c.isupper() for c in self.password)
        has_digit = any(c.isdigit() for c in self.password)
        has_symbol = any(not c.isalnum() for c in self.password)

        if not has_upper:
            suggestions.append("Add uppercase letters.")
        if not has_lower:
            suggestions.append("Add lowercase letters.")
        if not has_digit:
            suggestions.append("Include numbers.")
        if not has_symbol:
            suggestions.append("Add special characters (@, #, $, etc.).")

        if self._is_common():
            suggestions.append("This password is in common password lists. Avoid it.")
        if self.PATTERNS['sequential_numbers'].search(self.password):
            suggestions.append("Avoid sequential numbers.")
        if self.PATTERNS['sequential_letters'].search(self.password):
            suggestions.append("Avoid sequential letters.")
        if self.PATTERNS['repeated_chars'].search(self.password):
            suggestions.append("Avoid repeating characters 3+ times.")
        if self.PATTERNS['keyboard_rows'].search(self.password.lower()):
            suggestions.append("Avoid keyboard patterns like 'qwerty'.")

        unique_ratio = len(set(self.password)) / max(self.length, 1)
        if unique_ratio < 0.5:
            suggestions.append("Use more unique characters.")

        if not suggestions:
            suggestions.append("Password is highly secure. Maintain this level!")

        return suggestions

    def generate_report(self) -> str:
        analysis = self.analyze()
        strength = analysis['strength']

        lines = []
        lines.append("=" * 60)
        lines.append("     CYWALLEARN UNHACKED - PASSWORD ANALYSIS REPORT")
        lines.append("=" * 60)
        lines.append("")
        lines.append(f"  Length            : {analysis['password_length']} characters")
        lines.append(f"  Character Set     : {analysis['charset_size']} unique characters")
        lines.append(f"  Unique Characters : {analysis['unique_characters']} ({analysis['unique_ratio']*100:.0f}% diversity)")
        lines.append(f"  Entropy           : {analysis['entropy_bits']} bits")
        lines.append("")
        lines.append(f"  Strength          : {strength['level']} ({strength['score']}/100)")
        lines.append("")
        lines.append("  -- Character Distribution --")
        lines.append(f"    Uppercase : {analysis['character_distribution']['uppercase']}")
        lines.append(f"    Lowercase : {analysis['character_distribution']['lowercase']}")
        lines.append(f"    Digits    : {analysis['character_distribution']['digits']}")
        lines.append(f"    Symbols   : {analysis['character_distribution']['symbols']}")
        lines.append("")
        lines.append("  -- Crack Time Estimates --")
        for hash_type, estimate in analysis['crack_time_estimates'].items():
            lines.append(f"    {hash_type:15s}: {estimate['human_readable']}")
        lines.append("")
        lines.append("  -- Password Hashes --")
        for algo, hash_val in analysis['hashes'].items():
            lines.append(f"    {algo:8s}: {hash_val}")

        if analysis['detected_patterns']:
            lines.append("")
            lines.append("  -- Detected Patterns --")
            for pattern in analysis['detected_patterns']:
                lines.append(f"    ! {pattern['pattern']}: {', '.join(str(m) for m in pattern['matches'])}")

        lines.append("")
        lines.append("  -- Suggestions --")
        for suggestion in analysis['suggestions']:
            lines.append(f"    * {suggestion}")

        lines.append("")
        lines.append("=" * 60)
        lines.append("  Generated by Cywallearn Unhacked - Password Security Suite")
        lines.append("=" * 60)
        return '\n'.join(lines)
