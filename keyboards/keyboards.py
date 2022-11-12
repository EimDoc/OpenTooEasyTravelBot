from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

bd_button = KeyboardButton('/Лучшее_предложение')
lp_button = KeyboardButton('/Низкая_цена')
hp_button = KeyboardButton('/Высокая_цена')
history_button = KeyboardButton('/История')
help_button = KeyboardButton('/Помощь')
markup.insert(lp_button)
markup.insert(hp_button)
markup.insert(bd_button)
markup.insert(history_button)
markup.add('Стоп')
markup.add(help_button)

