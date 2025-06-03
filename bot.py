import os
import telebot
from flask import Flask, request
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

def main_reply_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("📘 Бхакти-йога для чайников"),
        KeyboardButton("📚 Книжная полка"),
        KeyboardButton("🎧 Лекции"),
        KeyboardButton("📦 Заказать книги"),
        KeyboardButton("🗓 Ближайшие мероприятия"),
        KeyboardButton("💡 Прочее"),
        KeyboardButton("🔙 Главное меню")
    )
    return markup

def books_menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    books = [
        "Слово Хранителя Преданности",
        "Бхагавад Гита",
        "Шримад Бхагаватам",
        "Чайтанья Чаритамрита",
        "Брихад Бхагаватамрита",
        "Эволюция сознательного"
    ]
    for book in books:
        markup.add(KeyboardButton(book))
    markup.add(KeyboardButton("🔙 Главное меню"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать в бот Бхакти-йоги 🙏\nВыберите пункт меню:",
        reply_markup=main_reply_keyboard()
    )

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text

    if text == "📘 Бхакти-йога для чайников":
        bot.send_message(message.chat.id, "📘 Информация о Бхакти-йоге для чайников", reply_markup=main_reply_keyboard())

    elif text == "📚 Книжная полка":
        bot.send_message(message.chat.id, "📚 Выберите книгу:", reply_markup=books_menu_keyboard())

    elif text in [
        "Слово Хранителя Преданности", "Бхагавад Гита", "Шримад Бхагаватам",
        "Чайтанья Чаритамрита", "Брихад Бхагаватамрита", "Эволюция сознательного"
    ]:
        file_path = f"books/{text}.pdf"
        if os.path.exists(file_path):
            with open(file_path, 'rb') as doc:
                bot.send_document(message.chat.id, doc, caption=f"📖 {text}")
        else:
            bot.send_message(message.chat.id, f"Файл книги '{text}' пока недоступен.")
        bot.send_message(message.chat.id, "📚 Выберите другую книгу или вернитесь в меню:", reply_markup=books_menu_keyboard())

    elif text == "🎧 Лекции":
        bot.send_message(message.chat.id, "🎧 Лекции: (в разработке)", reply_markup=main_reply_keyboard())

    elif text == "📦 Заказать книги":
        bot.send_message(message.chat.id, "📦 Заказ книг: напишите @your_contact", reply_markup=main_reply_keyboard())

    elif text == "🗓 Ближайшие мероприятия":
        bot.send_message(message.chat.id, "🗓 Скоро появятся новые события!", reply_markup=main_reply_keyboard())

    elif text == "💡 Прочее":
        bot.send_message(message.chat.id, "💡 В разработке", reply_markup=main_reply_keyboard())

    elif text == "🔙 Главное меню":
        bot.send_message(message.chat.id, "Вы в главном меню:", reply_markup=main_reply_keyboard())

    else:
        bot.send_message(message.chat.id, "Выберите пункт из меню:", reply_markup=main_reply_keyboard())

@server.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

@server.route("/")
def index():
    return "Бот работает ✅"

if __name__ == "__main__":
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
