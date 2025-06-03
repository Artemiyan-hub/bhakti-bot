from dotenv import load_dotenv
load_dotenv()
import os
import telebot

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

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
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    books = ["Слово Хранителя Преданности", "Бхагавад Гита", "Шримад Бхагаватам", "Чайтанья Чаритамрита", "Брихад Бхагаватамрита", "Эволюция сознательного"]
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
        bot.send_message(
            message.chat.id,
            "📘 Информация о Бхакти-йоге для чайников",
            reply_markup=main_reply_keyboard()
        )

    elif text == "📚 Книжная полка":
        bot.send_message(
            message.chat.id,
            "📚 Выберите книгу:",
            reply_markup=books_menu_keyboard()
        )

    elif text in ["Слово Хранителя Преданности", "Бхагавад Гита", "Шримад Бхагаватам", "Чайтанья Чаритамрита", "Брихад Бхагаватамрита", "Эволюция сознательного"]:
        file_path = f"books/{text}.pdf"
        if os.path.exists(file_path):
            with open(file_path, 'rb') as doc:
                bot.send_document(message.chat.id, doc, caption=f"📖 {text}")
        else:
            bot.send_message(message.chat.id, f"Файл книги '{text}' пока недоступен.")
        bot.send_message(
            message.chat.id,
            "📚 Выберите другую книгу или вернитесь в меню:",
            reply_markup=books_menu_keyboard()
        )

    elif text == "🎧 Лекции":
        bot.send_message(
            message.chat.id,
            "🎧 Лекции: (Ссылки и аудио будут добавлены позже)",
            reply_markup=main_reply_keyboard()
        )

    elif text == "📦 Заказать книги":
        bot.send_message(
            message.chat.id,
            "📦 Чтобы заказать книги, свяжитесь с нами: @your_contact",
            reply_markup=main_reply_keyboard()
        )

    elif text == "🗓 Ближайшие мероприятия":
        bot.send_message(
            message.chat.id,
            "🗓 Информация о ближайших мероприятиях скоро появится!",
            reply_markup=main_reply_keyboard()
        )

    elif text == "💡 Прочее":
        bot.send_message(
            message.chat.id,
            "💡 Дополнительные опции в разработке.",
            reply_markup=main_reply_keyboard()
        )

    elif text == "🔙 Главное меню":
        bot.send_message(
            message.chat.id,
            "Возврат в главное меню:",
            reply_markup=main_reply_keyboard()
        )

    else:
        bot.send_message(
            message.chat.id,
            "Пожалуйста, используйте кнопки меню ниже.",
            reply_markup=main_reply_keyboard()
        )

bot.polling(none_stop=True)
