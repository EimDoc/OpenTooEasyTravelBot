from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import MediaGroup
from create_bot import my_bot, data_base
from misc.util import get_destination_id, check_hotels
from misc.variables import help_text
from datetime import datetime
from aiogram_calendar import SimpleCalendar, simple_cal_callback
from inline_keyboards.keyboards import yes_no_cb, yes_no_markup, ten_markup, ten_cb
from inline_keyboards.keyboards import twenty_five_markup, twenty_five_cb, min_price_markup, min_price_cb, max_price_markup, max_price_cb
from misc.util import cb
import asyncio


class FSMBestDeal(StatesGroup):
    city = State()
    dest_id = State()
    people_amount = State()
    date_start = State()
    date_end = State()
    min_price = State()
    max_price = State()
    distance = State()
    hotels = State()
    photos = State()
    photos_count = State()
    stop = State()


class TownError(Exception):
    pass


async def start(message: types.Message):
    await FSMBestDeal.city.set()
    await message.reply('Введите город:')


async def get_city(message: types.Message, state: FSMContext):
    await my_bot.send_message(chat_id=message.from_user.id,
                              text='Дождитесь вывода результатов.')
    markup = get_destination_id(message.text)
    try:
        await message.reply('Выберите ваш вариант:', reply_markup=markup)
        await FSMBestDeal.next()
    except Exception:
        await message.reply('Не удалось получить информацию по данному городу.')
        await my_bot.send_message(chat_id=message.from_user.id,
                                  text=help_text)
        await state.finish()



async def callback_id(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['id'] == 'стоп':
        await state.finish()
        await callback_query.message.answer('Операция прервана')
        await callback_query.answer()
    else:
        async with state.proxy() as data:
            data['destination_id'] = callback_data['id']
            await callback_query.answer()
        await my_bot.delete_message(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id)
        await FSMBestDeal.next()
        await my_bot.send_message(chat_id=callback_query.from_user.id,
                                  text='Выберите кол-во людей, которые будут проживать.',
                                  reply_markup=ten_markup
                                  )


async def people(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        data['people'] = callback_data['num']
    await callback_query.answer()
    await my_bot.delete_message(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id
    )
    await FSMBestDeal.next()
    await my_bot.send_message(chat_id=callback_query.from_user.id,
                              text='Выберите дату приезда.',
                              reply_markup=await SimpleCalendar().start_calendar()
                              )


async def date_start(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query,
                                                              callback_data)

    if selected:
        async with state.proxy() as data:
         try:
            if date.date() < datetime.now().date():
                raise ValueError
            data['date_start'] = date.date()
            await callback_query.message.reply(f'Вы выбрали {date.date()} для заезда.')
         except ValueError:
            await callback_query.message.reply('Введено неверное значение!\nВыберите дату приезда ещё раз.',
                                               reply_markup=await SimpleCalendar().start_calendar()
                                               )
            return
         await FSMBestDeal.next()
         await my_bot.send_message(
             chat_id=callback_query.from_user.id,
             text='Выберите дату отъезда',
             reply_markup=await SimpleCalendar().start_calendar()
         )


async def date_end(callback_query: types.CallbackQuery, callback_data: dict,
                     state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query,
                                                              callback_data)

    if selected:
        async with state.proxy() as data:
            try:
                difference = date.date() - data['date_start']

                if difference.days < 0:
                    raise ValueError
                data['date_end'] = date.date()
                await callback_query.message.reply(f'Вы выбрали {date.date()} для выезда.')
            except ValueError:
                await callback_query.message.reply('Введено неверное значение!\nВыберите дату отъезда ещё раз.',
                                                   reply_markup=await SimpleCalendar().start_calendar()
                                                   )
                return
        await FSMBestDeal.next()
        await my_bot.send_message(chat_id=callback_query.from_user.id,
                                  text='Выберите минимальную цену в $',
                                  reply_markup=min_price_markup)


async def min_price(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['min_price'] = callback_data['num']
            await callback_query.answer()
            await my_bot.delete_message(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id)
    except ValueError:
        await callback_query.message.reply(('Попробуйте еще раз.'))

        return

    await FSMBestDeal.next()
    await my_bot.send_message(chat_id=callback_query.from_user.id,
                              text='Выберите максимальную цену в $', reply_markup=max_price_markup)


async def max_price(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    try:
        async with state.proxy() as data:
            if data['min_price'] > callback_data['num']:
                await my_bot.delete_message(
                    chat_id=callback_query.from_user.id,
                    message_id=callback_query.message.message_id)
                raise ValueError
            data['max_price'] = callback_data['num']
            await callback_query.answer()
            await my_bot.delete_message(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id)
    except ValueError:
        await my_bot.send_message(chat_id=callback_query.from_user.id,
                                  text='Было введено неверное значение!\n'
                                       'Попробуйте еще раз.',
                                  reply_markup=max_price_markup)
        return

    await FSMBestDeal.next()
    await my_bot.send_message(chat_id=callback_query.from_user.id,
                              text='Выберите максимальное расстояние до центра в км.',
                              reply_markup=ten_markup)


async def get_distance(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    try:
        dist = int(callback_data['num'])
        async with state.proxy() as data:
            data['distance'] = dist
            await callback_query.answer()
            await my_bot.delete_message(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id)
    except ValueError:
        await callback_query.message.reply(('Попробуйте еще раз.'))
        return
    await FSMBestDeal.next()
    await my_bot.send_message(chat_id=callback_query.from_user.id,
                              text='Выберите максимальное кол-во выводимых отелей.',
                              reply_markup=twenty_five_markup)


async def get_hotels_num(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['page_size'] = int(callback_data['num'])
            await callback_query.answer()
            await my_bot.delete_message(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id)
        except ValueError:
            await callback_query.message.reply('Попробуйте еще раз.')
            return

    await FSMBestDeal.next()
    await my_bot.send_message(chat_id=callback_query.from_user.id,
                              text='Выводить фото?', reply_markup=yes_no_markup)


async def stop_show_photos(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['state'] == 'yes':
        await FSMBestDeal.next()
        await callback_query.answer()
        await my_bot.send_message(chat_id=callback_query.from_user.id,
                                  text='Сколько фото вывести?',
                                  reply_markup=ten_markup)
    else:
        async with state.proxy() as data:
            try:
                querystring = {"destinationId": data['destination_id'],
                               "pageNumber": "1",
                               "pageSize": data['page_size'],
                               "checkIn": data['date_start'],
                               "checkOut": data['date_end'], "adults1": data['people'],
                               "sortOrder": 'DISTANCE_FROM_LANDMARK',
                               "locale": "ru_RU",
                               "currency": "USD",
                               "priceMin": data['min_price'],
                               "priceMax": data['max_price']}
                await my_bot.send_message(chat_id=callback_query.from_user.id,
                                          text='Дождитесь вывода результатов.')
                for elem in check_hotels(params=querystring):
                    await asyncio.sleep(1)
                    if data['distance'] >= elem[1]:
                        try:
                            await my_bot.send_message(chat_id=callback_query.from_user.id, text=elem[0])
                        except Exception:
                            await my_bot.send_message(chat_id=callback_query.from_user.id,
                                                      text='Не удается отправить отель')
                        name = ''.join(('id', str(callback_query.from_user.id)))
                        data_base.insert(name=name,
                                         command='/Лучшее_предложение',
                                         time=datetime.now(), description=elem[0], url=elem[2])
                    else:
                        break
                await my_bot.send_message(chat_id=callback_query.from_user.id, text='Результаты выведены.')
            except Exception:
                await callback_query.message.reply('Произошла непредвиденная ошибка.')
        await state.finish()

        await my_bot.send_message(chat_id=callback_query.from_user.id, text=help_text)
    await callback_query.answer()
    await my_bot.delete_message(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id)


async def photos_count(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        try:

            data['photos_count'] = int(callback_data['num'])
            await callback_query.answer()
            await my_bot.delete_message(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id)
            querystring = {"destinationId": data['destination_id'],
                           "pageNumber": "1",
                           "pageSize": data['page_size'],
                           "checkIn": data['date_start'],
                           "checkOut": data['date_end'], "adults1": data['people'],
                           "sortOrder": 'PRICE', "locale": "ru_RU",
                           "currency": "USD"}
            await my_bot.send_message(chat_id=callback_query.from_user.id,
                                      text='Дождитесь вывода результатов.')
            for elem in check_hotels(params=querystring, photos_count=data['photos_count']):
                if data['distance'] >= elem[2]:
                    try:
                        photos = MediaGroup()
                        photos.attach_photo(elem[1][0], elem[0])
                        for url in elem[1][1:]:
                            photos.attach_photo(url)
                    except TypeError:
                        continue
                    await asyncio.sleep(1)
                    try:
                        await my_bot.send_media_group(chat_id=callback_query.from_user.id,
                                                      media=photos)
                    except Exception:
                        await my_bot.send_message(chat_id=callback_query.from_user.id,
                                                  text='Не удается отправить отель')
                    name = ''.join(('id', str(callback_query.from_user.id)))
                    data_base.insert(name=name, command='/Лучшее_предложение',
                                    time=datetime.now(), description=elem[0], url=elem[3])
                else:
                    break
            await my_bot.send_message(chat_id=callback_query.from_user.id, text='Результаты выведены.')

        except ValueError:
            await callback_query.message.reply('Введено неверное значение!\nПопробуйте еще раз.')
            return
        await my_bot.send_message(chat_id=callback_query.from_user.id, text=help_text)
    await state.finish()


async def stop(message: types.Message, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state is None:
        return
    await state.finish()
    await message.reply('ОК')


def register_bestdeal_handler(dp: Dispatcher):
    dp.register_message_handler(start, commands=['Лучшее_предложение'], state=None)
    dp.register_message_handler(stop, commands=['стоп'], state="*")
    dp.register_message_handler(stop, Text(equals='стоп', ignore_case=True), state="*")
    dp.register_message_handler(get_city,state=FSMBestDeal.city)
    dp.register_callback_query_handler(callback_id, cb.filter(), state=FSMBestDeal.dest_id)
    dp.register_callback_query_handler(people, ten_cb.filter(), state=FSMBestDeal.people_amount)
    dp.register_callback_query_handler(date_start, simple_cal_callback.filter(), state=FSMBestDeal.date_start)
    dp.register_callback_query_handler(date_end, simple_cal_callback.filter(), state=FSMBestDeal.date_end)
    dp.register_callback_query_handler(min_price, min_price_cb.filter(), state=FSMBestDeal.min_price)
    dp.register_callback_query_handler(max_price, max_price_cb.filter(), state=FSMBestDeal.max_price)
    dp.register_callback_query_handler(get_distance, ten_cb.filter(), state=FSMBestDeal.distance)
    dp.register_callback_query_handler(get_hotels_num, twenty_five_cb.filter(), state=FSMBestDeal.hotels)
    dp.register_callback_query_handler(stop_show_photos, yes_no_cb.filter(), state=FSMBestDeal.photos)
    dp.register_callback_query_handler(photos_count, ten_cb.filter(), state=FSMBestDeal.photos_count)
