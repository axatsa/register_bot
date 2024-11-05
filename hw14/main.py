import telebot
from telebot import types
import keyboard as kb

# Замените на ваш токен от @BotFather
TOKEN = '7804737490:AAFww263GimgmCuHLIdmZqAptxruMJPyqVk'
bot = telebot.TeleBot(TOKEN)

# Курс валюты
EXCHANGE_RATE = 12350


@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 Привет! Я бот для конвертации валют.\n\n"
        "Я могу конвертировать:\n"
        "• Сумы (UZS) в доллары (USD)\n"
        "• Доллары (USD) в сумы (UZS)\n\n"
        "Выберите тип конвертации 👇"
    )
    bot.reply_to(message, welcome_text, reply_markup=kb.create_keyboard())


@bot.message_handler(commands=['about_me'])
def about_me(message):
    text = 'Привет меня зовут Ахат. На данный момент работаю тьютором в техникуме'
    bot.reply_to(message, text)


@bot.message_handler(func=lambda message: message.text in ['UZS → USD', 'USD → UZS'])
def choose_conversion(message):
    if message.text == 'UZS → USD':
        msg = bot.reply_to(message, "Введите сумму в сумах (UZS):")
        bot.register_next_step_handler(msg, convert_sum_to_usd)
    else:
        msg = bot.reply_to(message, "Введите сумму в долларах (USD):")
        bot.register_next_step_handler(msg, convert_usd_to_sum)


def convert_sum_to_usd(message):
    amount_sum = float(message.text.replace(',', '.'))
    amount_usd = amount_sum / EXCHANGE_RATE
    response = (
        f"💱 Конвертация:\n\n"
        f"{amount_sum:,.2f} UZS = {amount_usd:,.2f} USD\n\n"
        f"Курс: 1 USD = {EXCHANGE_RATE:,} UZS"
    )
    bot.reply_to(message, response, reply_markup=kb.create_keyboard())


def convert_usd_to_sum(message):
    amount_usd = float(message.text.replace(',', '.'))
    amount_sum = amount_usd * EXCHANGE_RATE
    response = (
        f"💱 Конвертация:\n\n"
        f"{amount_usd:,.2f} USD = {amount_sum:,.2f} UZS\n\n"
        f"Курс: 1 USD = {EXCHANGE_RATE:,} UZS"
    )
    bot.reply_to(message, response, reply_markup=kb.create_keyboard())


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(
        message,
        "Используйте кнопки для выбора конвертации.",
        reply_markup=kb.create_keyboard()
    )


# Запуск бота
bot.infinity_polling()
