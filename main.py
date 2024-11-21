import telebot
import datetime
import json

# Замените YOUR_BOT_API_KEY на ваш реальный API ключ
bot = telebot.TeleBot("7711721243:AAFr11zdBENTd75dMjXCvCg0nSoojXAa2-U")

# База данных для хранения данных пользователей
user_data = {}

# Команда start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Нажмите на кнопку 'Начать', чтобы вычислить ваши PAWS токены.")

# Обработчик взаимодействий (когда приходит сообщение от пользователя)
@bot.message_handler(func=lambda message: True)
def handle_user_interaction(message):
    # Данные, отправленные из веб-приложения (просто для примера)
    data = message.text  # Пример данных, которые вы можете отправить из вашего приложения
    
    try:
        interaction_data = json.loads(data)
        interaction_timestamp = interaction_data['interactionTimestamp']
        action = interaction_data['action']
        
        user_id = message.from_user.id
        
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
                bot.reply_to(message, "Поздравляем! Вы заработали 1000 PAWS токенов! 🐾")
            else:
                remaining_days = 365 - time_difference.days
                bot.reply_to(message, f"Вы заработаете 1000 PAWS через {remaining_days} дней.")
        else:
            bot.reply_to(message, "Неизвестное действие.")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {str(e)}")

# Запуск бота
bot.polling()

