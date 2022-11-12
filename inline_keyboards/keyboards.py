from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

yes_no_cb = CallbackData('yes_no', 'state')
ten_cb = CallbackData('ten', 'num')
twenty_five_cb = CallbackData('twenty_five', 'num')
min_price_cb = CallbackData('min_price', 'num')
max_price_cb = CallbackData('max_price', 'num')

yes_no_markup = InlineKeyboardMarkup()
yes = InlineKeyboardButton(text='да', callback_data=yes_no_cb.new('yes'))
yes_no_markup.insert(yes)
no = InlineKeyboardButton(text='нет', callback_data=yes_no_cb.new('no'))
yes_no_markup.insert(no)

ten_markup = InlineKeyboardMarkup()
for num in range(1, 11):
    button = InlineKeyboardButton(
        text=str(num),
        callback_data=ten_cb.new(str(num))
    )
    ten_markup.insert(button)

twenty_five_markup = InlineKeyboardMarkup(row_width=5)
for num in range(1, 26):
    button = InlineKeyboardButton(
        text=str(num),
        callback_data=twenty_five_cb.new(str(num))
    )
    twenty_five_markup.insert(button)

min_price_markup = InlineKeyboardMarkup()
for num in range(0, 151, 10):
    button = InlineKeyboardButton(text=str(num),
                                  callback_data=min_price_cb.new(str(num))
                                  )
    min_price_markup.insert(button)

max_price_markup = InlineKeyboardMarkup()
for num in range(0, 251, 10):
    button = InlineKeyboardButton(text=str(num),
                                  callback_data=max_price_cb.new(str(num))
                                  )
    max_price_markup.insert(button)

