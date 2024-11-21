from telebot import TeleBot, types
import datetime
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# База данных для хранения данных пользователей
user_data = {}

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Добро пожаловать! Нажмите на кнопку 'Начать', чтобы вычислить ваши PAWS токены.")

async def handle_user_interaction(update: Update, context: CallbackContext):
    # Данные, отправленные из веб-приложения
    user_id = update.message.from_user.id
    data = update.message.text

    interaction_data = json.loads(data)
    interaction_timestamp = interaction_data['interactionTimestamp']
    action = interaction_data['action']
    
    if action == 'get_started':
        # Если это первое взаимодействие пользователя, сохраняем его время
        if user_id not in user_data:
            user_data[user_id] = {
                'first_interaction': interaction_timestamp,
                'total_paws': 0
            }

        # Рассчитываем разницу между текущим временем и временем первого взаимодействия
        first_interaction_time = datetime.datetime.fromisoformat(user_data[user_id]['first_interaction'])
        current_time = datetime.datetime.now()
        time_difference = current_time - first_interaction_time

        # Если прошло 365 дней, награждаем 1000 PAWS
        if time_difference.days >= 365:
            user_data[user_id]['total_paws'] = 1000  # Награда — 1000 PAWS
            await update.message.reply_text(f"Поздравляем! Вы заработали 1000 PAWS токенов! 🐾")
        else:
            remaining_days = 365 - time_difference.days
            await update.message.reply_text(f"Вы заработаете 1000 PAWS через {remaining_days} дней.")

async def main():
    # Ваш API ключ
    application = Application.builder().token("YOUR_BOT_API_KEY").build()
    
    # Обработчики команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_interaction))
    
    # Запуск бота
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

bot = TeleBot("7711721243:AAFr11zdBENTd75dMjXCvCg0nSoojXAa2-U")

@bot.message_handler(commands=["start"])
def start_handler(message):
    keyboard = types.InlineKeyboardMarkup()
    web_app = types.WebAppInfo("https://abduaziz001.github.io/Paws/")  # Укажите свою ссылку
    btn = types.InlineKeyboardButton("Open PAWS Mini App", web_app=web_app)
    keyboard.add(btn)
    bot.send_message(message.chat.id, "Welcome to PAWS!", reply_markup=keyboard)
    

# Имитация базы данных для хранения данных пользователя
user_data = {}

def handle_user_interaction(user_id, data):
    # Разбираем данные взаимодействия
    interaction_data = json.loads(data)
    interaction_timestamp = interaction_data['interactionTimestamp']
    action = interaction_data['action']
    
    if action == 'get_started':
        # Если это первое взаимодействие пользователя, сохраняем его время
        if user_id not in user_data:
            user_data[user_id] = {
                'first_interaction': interaction_timestamp,
                'total_paws': 0
            }

        # Рассчитываем разницу между текущим временем и временем первого взаимодействия
        first_interaction_time = datetime.datetime.fromisoformat(user_data[user_id]['first_interaction'])
        current_time = datetime.datetime.now()
        time_difference = current_time - first_interaction_time

        # Если прошло 365 дней, награждаем 1000 PAWS
        if time_difference.days >= 365:
            user_data[user_id]['total_paws'] = 1000  # Награда — 1000 PAWS
            print(f"Пользователь {user_id} заработал 1000 PAWS токенов!")

        return user_data[user_id]['total_paws']


bot.polling()
