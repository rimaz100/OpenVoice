""" from https://github.com/keithito/tacotron """
# ------------------------------------------------------------
#  ⬇⬇  Arabic support added (arabic_cleaners & IPA)  ⬇⬇
# ------------------------------------------------------------
from openvoice.text import cleaners
from openvoice.text.symbols import symbols, language_tone_start_map

# (NEW) Arabic cleaners/phonemes
from openvoice.text.arabic import arabic_cleaners, arabic_to_lazy_ipa  # noqa: F401

# ------------------------------------------------------------
#  Mappings
# ------------------------------------------------------------
_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}

# ------------------------------------------------------------
#  Core helpers
# ------------------------------------------------------------
def _clean_text(text, cleaner_names):
    for name in cleaner_names:
        cleaner = getattr(cleaners, name, None)
        if cleaner is None:
            raise Exception(f"Unknown cleaner: {name}")
        text = cleaner(text)
    return text


# ------------------------------------------------------------
#  Public API
# ------------------------------------------------------------
def text_to_sequence(text, symbols=symbols, cleaner_names=("arabic_cleaners",)):
    """
    Converts text into a list of symbol IDs.
    Default cleaner is `arabic_cleaners`; override per‑call if needed.
    """
    sequence = []
    symbol_to_id = _symbol_to_id
    clean_text = _clean_text(text, cleaner_names)

    for char in clean_text:
        if char in symbol_to_id:
            sequence.append(symbol_to_id[char])
    return sequence


def cleaned_text_to_sequence(cleaned_text, symbols=symbols):
    symbol_to_id = _symbol_to_id
    return [symbol_to_id[c] for c in cleaned_text if c in symbol_to_id]


def cleaned_text_to_sequence_vits2(cleaned_text, tones, language, symbols, languages):
    symbol_to_id = _symbol_to_id
    language_id_map = {s: i for i, s in enumerate(languages)}
    phones = [symbol_to_id[c] for c in cleaned_text]
    tone_start = language_tone_start_map[language]
    tones = [t + tone_start for t in tones]
    lang_id = language_id_map[language]
    lang_ids = [lang_id] * len(phones)
    return phones, tones, lang_ids


def sequence_to_text(sequence):
    return "".join(_id_to_symbol[sid] for sid in sequence)
