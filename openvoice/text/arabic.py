# openvoice/text/arabic.py
import re

# أرقام عربية -> كلمات (بسيطة)، تقدر تحسنها لاحقاً أو تستخدم مكتبة camel_tools
_ar_numbers = {
    '0': 'صفر', '1': 'واحد', '2': 'اثنان', '3': 'ثلاثة', '4': 'أربعة',
    '5': 'خمسة', '6': 'ستة', '7': 'سبعة', '8': 'ثمانية', '9': 'تسعة'
}

_DIACRITICS_RE = re.compile(r'[ًٌٍَُِّْـ]')
_NON_AR_CHARS_RE = re.compile(r'[^\u0600-\u06FF\s]')  # احفظ الحروف العربية فقط
_WHITESPACE_RE = re.compile(r'\s+')

def remove_diacritics(text: str) -> str:
    return re.sub(_DIACRITICS_RE, '', text)

def normalize_numbers_ar(text: str) -> str:
    # بس يحول كل رقم لاسم بالعربي (بسيط)
    return ''.join(_ar_numbers.get(ch, ch) for ch in text)

def arabic_basic_clean(text: str) -> str:
    # الترتيب هنا: إزالة التشكيل -> أرقام -> حروف بس -> مسافات
    text = remove_diacritics(text)
    text = normalize_numbers_ar(text)
    text = re.sub(_NON_AR_CHARS_RE, ' ', text)
    text = re.sub(_WHITESPACE_RE, ' ', text).strip()
    return text

# ممكن تكتب نسخة IPA لو حاب (placeholder):
def arabic_to_lazy_ipa(text: str) -> str:
    """
    لو حاب تستخدم mapping صوتي (phonemes) للعربي طوّر هنا.
    حالياً نرجع النص بعد التنظيف لأبسط تمثيل (char-level).
    """
    return arabic_basic_clean(text)

def arabic_cleaners(text: str) -> str:
    """Cleaner بسيط للـ cleaner_names = ['arabic_cleaners']"""
    return arabic_basic_clean(text)
