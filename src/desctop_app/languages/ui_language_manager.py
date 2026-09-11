from pathlib import Path
import json

class UILanguageManager:
    def __init__(self, lang_file="en.json"):
        self.translations = {}
        self.current_lang_file = None
        self.load_language(lang_file)

    def load_language(self, lang_file):
        """Loads translations from a JSON file and updates the current_lang_file path."""
        abs_lang_file = Path(lang_file).resolve()
        try:
            with open(abs_lang_file, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
                self.current_lang_file = str(abs_lang_file)
        except FileNotFoundError:
            print(
                f"Warning: Translation file {
                    abs_lang_file
                } not found. Using empty translations."
            )
            self.translations = {}

    def get(self, key_path, **kwargs):
        """Get translation by dot-separated path, e.g., 'main_page.title'"""
        keys = key_path.split(".")
        value = self.translations

        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, key_path)
            else:
                return key_path

        if kwargs and isinstance(value, str):
            try:
                return value.format(**kwargs)
            except KeyError:
                return value

        return value
