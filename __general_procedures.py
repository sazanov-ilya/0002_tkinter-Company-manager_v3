import ctypes
import re
import hashlib


# conn_description = re.sub('[\n]', ' ', (self.txt_conn_description.get('1.0', tk.END)))
def get_text_in_one_line(text):
    return re.sub('[\n]', ' ', text).strip()


def compute_md5_hash(my_string):
    m = hashlib.md5()
    m.update(my_string.encode('utf-8'))
    return m.hexdigest()


# Для Copy-Paste в раскладке RU
def is_ru_lang_keyboard():
    """ Проверка текущей раскладки ввода на RU """
    u = ctypes.windll.LoadLibrary("user32.dll")
    pf = getattr(u, "GetKeyboardLayout")
    return hex(pf(0)) == '0x4190419'


# Для Copy-Paste в раскладке RU
def keys(event):
    """ Определяем метод keys() с учетом раскладки """
    if is_ru_lang_keyboard():
        if event.keycode == 86:
            event.widget.event_generate("<<Paste>>")
        if event.keycode == 67:
            event.widget.event_generate("<<Copy>>")
        if event.keycode == 88:
            event.widget.event_generate("<<Cut>>")
        if event.keycode == 65535:
            event.widget.event_generate("<<Clear>>")
        if event.keycode == 65:
            event.widget.event_generate("<<SelectAll>>")