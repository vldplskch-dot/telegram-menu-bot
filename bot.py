from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# === 1️⃣ ВСТАВ СВІЙ ТОКЕН БОТА ===
BOT_TOKEN = "7876590032:AAGneAOIE0gimvK4Z-r03f8JRqRqeUfhObM"

# === 2️⃣ НАЗВА ТВОГО КАНАЛУ (для створення лінків) ===
CHANNEL_USERNAME = "fortestloyal"  # без @

# === 3️⃣ ТЕМИ І ПОСТИ ===
# Формат: "Назва теми": [список URL постів у каналі]
TOPICS = {
    "📘 Тема 1": [
        f"https://t.me/{CHANNEL_USERNAME}/3",
        f"https://t.me/{CHANNEL_USERNAME}/12",
        f"https://t.me/{CHANNEL_USERNAME}/25",
    ],
    "🧩 Тема 2": [
        f"https://t.me/{CHANNEL_USERNAME}/4",
        f"https://t.me/{CHANNEL_USERNAME}/31",
    ],
    "🎯 Тема 3": [
        f"https://t.me/{CHANNEL_USERNAME}/5",
        f"https://t.me/{CHANNEL_USERNAME}/41",
        f"https://t.me/{CHANNEL_USERNAME}/42",
    ],
}

# === 4️⃣ ГОЛОВНЕ МЕНЮ ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = []
    for topic in TOPICS.keys():
        buttons.append([InlineKeyboardButton(topic, callback_data=f"topic|{topic}")])

    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("📚 Оберіть тему:", reply_markup=keyboard)


# === 5️⃣ ОБРОБКА ВИБОРУ ТЕМИ ===
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data.startswith("topic|"):
        topic = data.split("|", 1)[1]
        posts = TOPICS.get(topic, [])

        if not posts:
            await query.edit_message_text("У цій темі поки що немає постів.")
            return

        text_lines = [f"<b>{topic}</b>\n"]
        for idx, link in enumerate(posts, start=1):
            text_lines.append(f"{idx}. <a href='{link}'>Перейти до посту</a>")

        text_lines.append("\n🔙 /start — назад до меню")
        text = "\n".join(text_lines)

        await query.edit_message_text(
            text=text, parse_mode="HTML"
        )


# === 6️⃣ ЗАПУСК БОТА ===
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("✅ Бот запущений. Натисни Ctrl+C для зупинки.")
    app.run_polling()


if __name__ == "__main__":
    main()
