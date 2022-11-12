from aiogram import Dispatcher, types
from keyboards.keyboards import markup


async def say_hello(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!", reply_markup=markup)
    await message.reply('Команды:\n'
                        '/Низкая_цена - наименьшая цена\n'
                        '/Высокая_цена - наивысшая цена\n'
                        '/Лучшее_предложение - цена и расстояние до центра\n'
                        '/История - вывод истории поиска\n'
                        '/Помощь - помощь\n'
                        'В любой момент выполнения команды вы можете ввести слово "стоп" и команда прервётся')


async def help(message: types.Message):
    await message.reply('Команды:\n'
                        '/Низкая_цена - наименьшая цена\n'
                        '/Высокая_цена - наивысшая цена\n'
                        '/Лучшее_предложение - цена и расстояние до центра\n'
                        '/История - вывод истории поиска\n'
                        '/Помощь - помощь\n'
                        'В любой момент выполнения команды вы можете ввести слово "стоп" и команда прервётся')


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(say_hello, commands=['start'])
    dp.register_message_handler(help, commands=['Помощь'])
