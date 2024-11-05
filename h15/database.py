
import sqlite3
from datetime import datetime

# Инициализация базы данных
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (user_id INTEGER PRIMARY KEY,
              username TEXT,
              phone TEXT,
              latitude REAL,
              longitude REAL,
              reg_date TIMESTAMP,
              language TEXT)''')
conn.commit()
conn.close()


def is_registered(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    return result is not None


import sqlite3


def choose_language(user_id, language):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Проверяем, существует ли пользователь в базе
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    existing_user = c.fetchone()

    if existing_user:
        # Если пользователь уже существует, обновляем его предпочтительный язык
        c.execute('UPDATE users SET language = ? WHERE user_id = ?', (language, user_id))
    else:
        # Если пользователя нет в базе, создаем новую запись с выбранным языком
        c.execute('''INSERT INTO users 
                    (user_id, language)
                    VALUES (?, ?)''', (user_id, language))

    conn.commit()
    conn.close()


def save_user_data(user_id, username, phone=None, latitude=None, longitude=None):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    existing_user = c.fetchone()

    if existing_user:
        update_fields = []
        update_values = []

        if username is not None:
            update_fields.append('username = ?')
            update_values.append(username)
        if phone is not None:
            update_fields.append('phone = ?')
            update_values.append(phone)
        if latitude is not None:
            update_fields.append('latitude = ?')
            update_values.append(latitude)
        if longitude is not None:
            update_fields.append('longitude = ?')
            update_values.append(longitude)

        if update_fields:
            query = f'''UPDATE users SET {', '.join(update_fields)}
                       WHERE user_id = ?'''
            update_values.append(user_id)
            c.execute(query, update_values)
    else:
        c.execute('''INSERT INTO users 
                    (user_id, username, phone, latitude, longitude, reg_date)
                    VALUES (?, ?, ?, ?, ?, ?)''',
                  (user_id, username, phone, latitude, longitude, datetime.now()))

    conn.commit()
    conn.close()


def get_user_info(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    return result

