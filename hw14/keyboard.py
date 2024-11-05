from telebot import types


def create_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('UZS → USD')
    btn2 = types.KeyboardButton('USD → UZS')
    keyboard.add(btn1, btn2)
    return keyboard
def about_me():
    Keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('обо мне')
    Keyboard.add(btn1)
    return Keyboard
