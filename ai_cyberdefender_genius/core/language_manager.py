"""
Language Manager Module
-----------------------

Manages application language settings based on the user's system OS default language.
Supports changing the language to any available language, including mother tongues like Hindi and others.
Includes a dictionary of supported languages and translations for UI and messages.
"""

import locale
import logging

class LanguageManager:
    def __init__(self):
        self.supported_languages = {
            # Comprehensive list of all ISO 639-1 language codes and names
            # Note: This list covers the majority of living languages but not all 7,168 known languages.
            # For full coverage, integration with external language databases or APIs is recommended.
            "af": "Afrikaans",
            "sq": "Albanian",
            "am": "Amharic",
            "ar": "Arabic",
            "hy": "Armenian",
            "az": "Azerbaijani",
            "eu": "Basque",
            "be": "Belarusian",
            "bn": "Bengali",
            "bs": "Bosnian",
            "bg": "Bulgarian",
            "ca": "Catalan",
            "ceb": "Cebuano",
            "ny": "Chichewa",
            "zh": "Chinese",
            "co": "Corsican",
            "hr": "Croatian",
            "cs": "Czech",
            "da": "Danish",
            "nl": "Dutch",
            "en": "English",
            "eo": "Esperanto",
            "et": "Estonian",
            "tl": "Filipino",
            "fi": "Finnish",
            "fr": "French",
            "fy": "Frisian",
            "gl": "Galician",
            "ka": "Georgian",
            "de": "German",
            "el": "Greek",
            "gu": "Gujarati",
            "ht": "Haitian Creole",
            "ha": "Hausa",
            "haw": "Hawaiian",
            "iw": "Hebrew",
            "hi": "Hindi",
            "hmn": "Hmong",
            "hu": "Hungarian",
            "is": "Icelandic",
            "ig": "Igbo",
            "id": "Indonesian",
            "ga": "Irish",
            "it": "Italian",
            "ja": "Japanese",
            "jw": "Javanese",
            "kn": "Kannada",
            "kk": "Kazakh",
            "km": "Khmer",
            "ko": "Korean",
            "ku": "Kurdish (Kurmanji)",
            "ky": "Kyrgyz",
            "lo": "Lao",
            "la": "Latin",
            "lv": "Latvian",
            "lt": "Lithuanian",
            "lb": "Luxembourgish",
            "mk": "Macedonian",
            "mg": "Malagasy",
            "ms": "Malay",
            "ml": "Malayalam",
            "mt": "Maltese",
            "mi": "Maori",
            "mr": "Marathi",
            "mn": "Mongolian",
            "my": "Myanmar (Burmese)",
            "ne": "Nepali",
            "no": "Norwegian",
            "ps": "Pashto",
            "fa": "Persian",
            "pl": "Polish",
            "pt": "Portuguese",
            "pa": "Punjabi",
            "ro": "Romanian",
            "ru": "Russian",
            "sm": "Samoan",
            "gd": "Scots Gaelic",
            "sr": "Serbian",
            "st": "Sesotho",
            "sn": "Shona",
            "sd": "Sindhi",
            "si": "Sinhala",
            "sk": "Slovak",
            "sl": "Slovenian",
            "so": "Somali",
            "es": "Spanish",
            "su": "Sundanese",
            "sw": "Swahili",
            "sv": "Swedish",
            "tg": "Tajik",
            "ta": "Tamil",
            "te": "Telugu",
            "th": "Thai",
            "tr": "Turkish",
            "uk": "Ukrainian",
            "ur": "Urdu",
            "uz": "Uzbek",
            "vi": "Vietnamese",
            "cy": "Welsh",
            "xh": "Xhosa",
            "yi": "Yiddish",
            "yo": "Yoruba",
            "zu": "Zulu"
        }
        self.current_language = self.detect_system_language()
        self.translations = self.load_translations(self.current_language)

    def detect_system_language(self):
        try:
            lang, _ = locale.getdefaultlocale()
            if lang:
                lang_code = lang.split('_')[0]
                if lang_code in self.supported_languages:
                    return lang_code
            return "en"  # Default to English if detection fails
        except Exception as e:
            logging.error(f"Language detection failed: {e}")
            return "en"

    def load_translations(self, lang_code):
        # Load translation dictionary for the given language code
        # Implement auto-fix and validation to prevent translation errors or security loopholes
        try:
            # Placeholder: Load translations from secure source
            translations = {}  # Load actual translations here
            # Auto-fix common issues in translations
            translations = self.auto_fix_translations(translations)
            return translations
        except Exception as e:
            logging.error(f"Failed to load translations for {lang_code}: {e}")
            return {}

    def auto_fix_translations(self, translations):
        # Placeholder: Implement auto-fix logic for translation dictionary
        # For example, remove harmful scripts, fix encoding issues, validate keys
        try:
            # Example fix: remove keys with suspicious content
            safe_translations = {}
            for k, v in translations.items():
                if "<script>" not in v.lower():
                    safe_translations[k] = v
            return safe_translations
        except Exception as e:
            logging.error(f"Auto-fix translations failed: {e}")
            return translations

    def set_language(self, lang_code):
        if lang_code in self.supported_languages:
            self.current_language = lang_code
            self.translations = self.load_translations(lang_code)
            logging.info(f"Language changed to {self.supported_languages[lang_code]}")
        else:
            logging.warning(f"Unsupported language code: {lang_code}")

    def translate(self, key):
        # Return translated string for the given key
        return self.translations.get(key, key)
