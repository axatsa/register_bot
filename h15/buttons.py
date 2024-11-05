from telebot import types

def language_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Русский')  # Изменено на "Русский" и "English" для удобства пользователя
    btn2 = types.KeyboardButton('English')
    keyboard.add(btn1, btn2)
    return keyboard

def create_contact_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Отправить контакт 📱", request_contact=True)
    keyboard.add(button)
    return keyboard

def create_location_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Отправить локацию 📍", request_location=True)
    keyboard.add(button)
    return keyboard

def create_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button = types.KeyboardButton("Мой профиль")  # Создаем кнопку с текстом "Мой профиль"
    keyboard.add(button)
    return keyboard
