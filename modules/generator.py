#!/usr/bin/env python3
# Cywallearn Unhacked - Core Password Generator Engine
# Generates cryptographically secure passwords with personal touch.

import secrets
import string
import hashlib
import hmac
import base64
from typing import Dict, List, Tuple, Optional


class CywalGenerator:
    LOWERCASE = string.ascii_lowercase
    UPPERCASE = string.ascii_uppercase
    DIGITS = string.digits
    SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?/~"
    AMBIGUOUS = "il1Lo0O"
    COMMON_PATTERNS = [
        "123", "abc", "qwerty", "asdf", "zxcv", "password", "admin",
        "letmein", "welcome", "monkey", "dragon", "master", "123456",
        "login", "starwars", "trustno1"
    ]

    def __init__(self, user_data: Dict[str, str], preferences: Dict):
        self.user_data = user_data
        self.preferences = preferences
        self.length = preferences.get('length', 8)
        self.use_symbols = preferences.get('use_symbols', True)
        self.avoid_ambiguous = preferences.get('avoid_ambiguous', False)
        self.use_personal_touch = preferences.get('use_personal_touch', True)

        self.char_pool = self.LOWERCASE + self.UPPERCASE + self.DIGITS
        if self.use_symbols:
            self.char_pool += self.SYMBOLS
        if self.avoid_ambiguous:
            for ch in self.AMBIGUOUS:
                self.char_pool = self.char_pool.replace(ch, '')

    def _secure_shuffle(self, data: str) -> str:
        lst = list(data)
        for i in range(len(lst) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            lst[i], lst[j] = lst[j], lst[i]
        return ''.join(lst)

    def _generate_seed_from_user(self) -> bytes:
        seed_parts = []
        for key in ['name', 'nickname', 'pet', 'hobby', 'favorite_color',
                     'favorite_number', 'birth_year', 'significant_year']:
            val = self.user_data.get(key, '')
            if val:
                seed_parts.append(str(val).strip().lower())
        raw_seed = '|'.join(seed_parts) if seed_parts else secrets.token_hex(16)
        return hashlib.sha512(raw_seed.encode('utf-8')).digest()

    def _derive_position_map(self, seed: bytes, length: int) -> List[int]:
        h = hmac.new(seed, b"position_map", hashlib.sha512).digest()
        pos_map = []
        for i in range(length):
            val = int.from_bytes(h[i % 64:(i % 64) + 2], 'big')
            pos_map.append(val)
        return pos_map

    def _ensure_character_types(self, password: List[str]) -> List[str]:
        has_lower = any(c in self.LOWERCASE for c in password)
        has_upper = any(c in self.UPPERCASE for c in password)
        has_digit = any(c in self.DIGITS for c in password)
        has_symbol = any(c in self.SYMBOLS for c in password) if self.use_symbols else True

        replacements = []
        if not has_lower:
            replacements.append(secrets.choice(self.LOWERCASE))
        if not has_upper:
            replacements.append(secrets.choice(self.UPPERCASE))
        if not has_digit:
            replacements.append(secrets.choice(self.DIGITS))
        if not has_symbol and self.use_symbols:
            replacements.append(secrets.choice(self.SYMBOLS))

        indices = list(range(len(password)))
        self._secure_shuffle_inplace(indices)
        for i, repl in enumerate(replacements):
            if i < len(indices):
                password[indices[i]] = repl
        return password

    def _secure_shuffle_inplace(self, lst: List) -> None:
        for i in range(len(lst) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            lst[i], lst[j] = lst[j], lst[i]

    def generate(self) -> Tuple[str, Dict]:
        length = self.length
        seed = self._generate_seed_from_user()
        pos_map = self._derive_position_map(seed, length)

        password_chars = []
        for i in range(length):
            if self.use_personal_touch and pos_map:
                pool_index = pos_map[i] % 4 if i < len(pos_map) else 0
                pool_selector = pool_index
            else:
                pool_selector = secrets.randbelow(4) if self.use_symbols else secrets.randbelow(3)

            if pool_selector == 0:
                pool = self.LOWERCASE
            elif pool_selector == 1:
                pool = self.UPPERCASE
            elif pool_selector == 2:
                pool = self.DIGITS
            else:
                pool = self.SYMBOLS if self.use_symbols else self.LOWERCASE

            if not pool:
                pool = self.LOWERCASE

            if self.use_personal_touch and pos_map:
                bias = pos_map[i % len(pos_map)] % len(pool) if pool else 0
                secure_choice = secrets.randbelow(len(pool))
                influenced_idx = (secure_choice + bias) % len(pool)
                password_chars.append(pool[influenced_idx])
            else:
                password_chars.append(secrets.choice(pool))

        password_chars = self._ensure_character_types(password_chars)
        self._secure_shuffle_inplace(password_chars)
        password = ''.join(password_chars)

        metadata = {
            'length': length,
            'character_types': self._count_types(password),
            'entropy_bits': self._calculate_entropy(password),
            'has_personal_touch': self.use_personal_touch,
        }
        return password, metadata

    def generate_multiple(self, count: int = 5) -> List[Tuple[str, Dict]]:
        return [self.generate() for _ in range(count)]

    def _count_types(self, password: str) -> Dict[str, int]:
        return {
            'lowercase': sum(1 for c in password if c in self.LOWERCASE),
            'uppercase': sum(1 for c in password if c in self.UPPERCASE),
            'digits': sum(1 for c in password if c in self.DIGITS),
            'symbols': sum(1 for c in password if c in self.SYMBOLS),
        }

    def _calculate_entropy(self, password: str) -> float:
        import math
        freq = {}
        for c in password:
            freq[c] = freq.get(c, 0) + 1
        entropy = 0.0
        length = len(password)
        for count in freq.values():
            p = count / length
            entropy -= p * math.log2(p)
        return round(entropy * length, 2)


class MemorableGenerator(CywalGenerator):
    def __init__(self, user_data: Dict[str, str], preferences: Dict):
        super().__init__(user_data, preferences)
        self.prefixes = ["Cy", "Xy", "Zy", "Ax", "Ex", "Ox", "Ry", "Vy", "Wy"]
        self.suffixes = ["on", "ix", "ax", "ux", "yn", "or", "an", "en", "um"]

    def generate_memorable(self) -> Tuple[str, Dict]:
        seed = self._generate_seed_from_user()
        name_part = ""
        if self.user_data.get('name'):
            name = self.user_data.get('name', '').lower()
            name_part = name[:3] if len(name) >= 3 else name

        hobby_part = ""
        if self.user_data.get('hobby'):
            hobby = self.user_data.get('hobby', '').lower()
            hobby_part = hobby[:3] if len(hobby) >= 3 else hobby

        base = name_part + hobby_part if name_part and hobby_part else ""
        if base:
            base = base.capitalize()
        else:
            base = secrets.choice(self.prefixes)

        suffix = secrets.choice(self.suffixes)

        number_str = ""
        if self.user_data.get('favorite_number'):
            number_str = str(self.user_data['favorite_number'])[:2]
        elif self.user_data.get('birth_year'):
            year = str(self.user_data['birth_year'])
            number_str = year[-2:]
        else:
            number_str = str(secrets.randbelow(90) + 10)

        special = secrets.choice(self.SYMBOLS) if self.use_symbols else secrets.choice(self.DIGITS)

        components = [base, suffix, number_str, special]
        self._secure_shuffle_inplace(components)
        password = ''.join(components)

        while len(password) < self.length:
            password += secrets.choice(self.char_pool)
        password = password[:self.length]

        pw_list = list(password)
        pw_list = self._ensure_character_types(pw_list)
        password = ''.join(pw_list)

        metadata = {
            'length': len(password),
            'character_types': self._count_types(password),
            'entropy_bits': self._calculate_entropy(password),
            'type': 'memorable',
            'has_personal_touch': True,
        }
        return password, metadata
