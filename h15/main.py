import telebot
import database as db
import buttons as kb

TOKEN = '7804737490:AAFww263GimgmCuHLIdmZqAptxruMJPyqVk'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    if not db.is_registered(message.from_user.id):
        bot.reply_to(
            message,
            "Привет! Для использования бота необходимо зарегистрироваться.\n"
            "Для начала, отправьте свой номер телефона.",
            reply_markup=kb.create_contact_keyboard()
        )
        db.save_user_data(message.from_user.id, message.from_user.username)
    else:
        user_info = db.get_user_info(message.from_user.id)
        if user_info[2] is None:
            bot.reply_to(
                message,
                "Пожалуйста, отправьте свой номер телефона для завершения регистрации.",
                reply_markup=kb.create_contact_keyboard()
            )
        elif user_info[3] is None:
            bot.reply_to(
                message,
                "Пожалуйста, отправьте свою локацию для завершения регистрации.",
                reply_markup=kb.create_location_keyboard()
            )
        else:
            welcome_back(message)


def welcome_back(message):
    user_info = db.get_user_info(message.from_user.id)
    name = message.from_user.first_name
    bot.reply_to(
        message,
        f"С возвращением, {name}! 👋\n"
        "Выберите нужную опцию в меню:",
        reply_markup=kb.create_main_keyboard()
    )


@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    if message.contact is not None:
        phone = message.contact.phone_number
        db.save_user_data(message.from_user.id, message.from_user.username, phone=phone)
        bot.reply_to(
            message,
            "Спасибо! Теперь, пожалуйста, отправьте свою локацию.",
            reply_markup=kb.create_location_keyboard()
        )


@bot.message_handler(content_types=['location'])
def handle_location(message):
    if message.location is not None:
        db.save_user_data(
            message.from_user.id,
            message.from_user.username,
            latitude=message.location.latitude,
            longitude=message.location.longitude
        )
        bot.reply_to(
            message,
            "Регистрация успешно завершена! ✅\n"
            "Теперь выберите предпочитаемый язык.",
            reply_markup=kb.language_keyboard()  # Кнопки выбора языка
        )


@bot.message_handler(func=lambda message: message.text == "Мой профиль")
def show_profile(message):
    user_info = db.get_user_info(message.from_user.id)
    if user_info:
        profile_text = (
            f"📱 Ваш профиль:\n\n"
            f"Имя: {message.from_user.first_name}\n"
            f"Username: @{user_info[1]}\n"
            f"Телефон: {user_info[2]}\n"
            f"Дата регистрации: {user_info[5]}\n"
        )
        bot.reply_to(message, profile_text, reply_markup=kb.create_main_keyboard())


@bot.message_handler(func=lambda message: message.text in ["Русский", "English"])
def handle_language_choice(message):
    language = "ru" if message.text == "Русский" else "en"
    db.choose_language(message.from_user.id, language)  # Сохранение языка в базе
    bot.reply_to(
        message,
        f"Язык успешно установлен на {'Русский' if language == 'ru' else 'English'}!",
        reply_markup=kb.create_main_keyboard()
    )


bot.infinity_polling()
