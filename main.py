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
        cabinet TEXT NOT NULL, 
        model TEXT NOT NULL,
        replacement_date TEXT NOT NULL,
        date_of_transfer TEXT,
        return_date TEXT,
        counter_before_replacement TEXT,
        counter_after_replacement TEXT,
        number_of_pages TEXT
    )
''')
conn.close()

# Ваш токен
API_TOKEN = 'TOKEN'

bot = telebot.TeleBot(API_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Для добавления записи введите в формате: \n"
                                      "'кабинет, модель, дата замены, передачи, возврата(ГГГГ-ММ-ДД)', счетчик до замены, счетчик после замены и количество отпечатанных страниц. Например: \n"
                                      "'109, CE285X, 2024-11-06'")

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        # Разделение сообщения на части
        parts = message.text.split(',')
        if len(parts) != 8:
            raise ValueError("Некорректный формат. Попробуйте еще раз.")
        
        # Извлечение данных
        cabinet = parts[0].strip()
        model = parts[1].strip()
        replacement_date = parts[2].strip()
        date_of_transfer = parts[3].strip()
        return_date = parts[4].strip()
        counter_before_replacement = int(parts[5].strip())
        counter_after_replacement = int(parts[6].strip())
        number_of_pages = int(parts[7].strip())
        
        # Преобразование дат в правильный формат и проверка формата даты
        try:
            datetime.strptime(replacement_date, '%Y-%m-%d')
            datetime.strptime(date_of_transfer, '%Y-%m-%d')
            datetime.strptime(return_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Некорректный формат даты. Используйте формат ГГГГ-ММ-ДД.")
       
        # Добавление записи в базу данных
        conn = sqlite3.connect('cartridges.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cartridge_records (
                username, cabinet, model, replacement_date, date_of_transfer, return_date, 
                counter_before_replacement, counter_after_replacement, number_of_pages
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            message.from_user.username or 'Unknown',
            cabinet, model, replacement_date, date_of_transfer, return_date,
            counter_before_replacement, counter_after_replacement, number_of_pages
        ))
        conn.commit()
        conn.close()
        
        bot.send_message(message.chat.id, "Запись успешно добавлена!")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

# Запуск бота
bot.polling(none_stop=True)
