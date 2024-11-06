import sqlite3
import telebot
from telebot import types
import sqlite3
from datetime import datetime

# Создание базы данных и таблицы
conn = sqlite3.connect('cartridges.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cartridge_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        office TEXT NOT NULL,
        model TEXT NOT NULL,
        replacement_date TEXT NOT NULL
    )
''')
conn.close()

# Ваш токен
API_TOKEN = '7812404465:AAH16zFpZwagNTTQGu7RstW7YsKpVghVNxQ'

bot = telebot.TeleBot(API_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Для добавления записи введите в формате: \n"
                                      "'кабинет, модель, дата(ГГГГ-ММ-ДД)'. Например: \n"
                                      "'109, CE285X, 2024-11-06'")

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        # Разделение сообщения на части
        parts = message.text.split(',')
        if len(parts) != 3:
            raise ValueError("Некорректный формат. Попробуйте еще раз.")
        
        # Извлечение данных
        office = parts[0].strip()
        model = parts[1].strip()
        date_str = parts[2].strip()
        
        # Преобразование даты в правильный формат
        datetime.strptime(date_str, '%Y-%m-%d')  # Проверка формата даты
        
        # Добавление записи в базу данных
        conn = sqlite3.connect('cartridges.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cartridge_records (username, office, model, replacement_date)
            VALUES (?, ?, ?, ?)
        ''', (message.from_user.username or "Unknown", office, model, date_str))
        conn.commit()
        conn.close()
        
        bot.send_message(message.chat.id, "Запись успешно добавлена!")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

# Запуск бота
bot.polling(none_stop=True)