from create_bot import data_base, my_bot
from aiogram import types, Dispatcher
from keyboards.keyboards import markup


async def show_history(message: types.Message):
    id = message.from_user.id
    try:
        name = ''.join(('id', str(id)))
        response = data_base.get_values(name)
        for elem in response:
            text = 'Команда: {command}\nДата: {date}\n{description}'.format(
                command=elem[0],
                date=elem[1],
                description=elem[2])

            await my_bot.send_message(chat_id=id, text=text)
        await my_bot.send_message(chat_id=message.from_user.id,
                                  text='Команды:\n'
                                       '/Низкая_цена - наименьшая цена\n'
                                       '/Высокая_цена - наивысшая цена\n'
                                       '/Лучшее_предложение - цена и расстояние до центра\n'
                                       '/История - вывод истории поиска\n'
                                       '/Помощь - помощь\n'
                                       'В любой момент выполнения команды вы можете ввести слово "стоп" и команда прервётся')
    except Exception:
        await my_bot.send_message(chat_id=id, text='Ваша история пуста', reply_markup=markup)
        await my_bot.send_message(chat_id=message.from_user.id,
                                  text='Команды:\n'
                                       '/Низкая_цена - наименьшая цена\n'
                                       '/Высокая_цена - наивысшая цена\n'
                                       '/Лучшее_предложение - цена и расстояние до центра\n'
                                       '/История - вывод истории поиска\n'
                                       '/Помощь - помощь\n'
                                       'В любой момент выполнения команды вы можете ввести слово "стоп" и команда прервётся')
        print('Ошибка получения значений у таблицы пользователя')


def register_history_handlers(dp: Dispatcher):
    dp.register_message_handler(show_history, commands=['История'])