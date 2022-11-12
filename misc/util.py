import requests
import json
import re
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import HOTELS_KEY


cb = CallbackData('dest_id', 'id')


def get_destination_id(town: str):
    global cb
    url = "https://hotels4.p.rapidapi.com/locations/search"
    querystring = {"query": town, "locale": "ru_RU"}

    headers = {
        "X-RapidAPI-Key": HOTELS_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers,
                                params=querystring)
    except Exception as exc:
        print('Ошибка в строке 17 файла util.py')
        raise exc

    response = json.loads(response.text)

    if response["suggestions"][0]["entities"]:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='Нет нужного варианта',
                                        callback_data=cb.new(id='стоп')))
        for city in response["suggestions"][0]["entities"]:
            text = city['caption']
            text = re.sub(r"<span class='highlighted'>", '', text)
            text = re.sub(r"</span>", '', text)
            button = InlineKeyboardButton(
                text=text,
                callback_data=cb.new(id=city['destinationId'])
            )
            markup.add(button)
        return markup
    return False


def check_hotels(params: dict, photos_count: int=None):
    url = "https://hotels4.p.rapidapi.com/properties/list"

    headers = {
        "X-RapidAPI-Key": HOTELS_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response = json.loads(response.text)
    except Exception as exc:
        print('Ошибка в строке 50 файла util.py')
        raise exc

    results = response['data']['body']['searchResults']['results']
    comp = re.compile('\W')
    for hotel in results:
        try:
            distance_to_center = float(comp.sub('.',
                                                hotel.get('landmarks')[0].get(
                                                    'distance').split()[0]))
        except Exception:
            distance_to_center = 0
        try:
            name = hotel.get('name', 'нет')
            address = hotel.get('address').get('streetAddress')
            star_rating = hotel.get('starRating')
            price = hotel.get('ratePlan').get('price').get('current')
            guest_rev = hotel.get('guestReviews', dict()).get('rating', 'нет')
            text = """Название отеля: {name}\nАдрес: {address}\nЗвезды: {stars}\nОценка посетителей: {guest}\nРасстояние до центра: {distance} км\nЦена за одну ночь: {one_night}
            """.format(
                name=name,
                address=address,
                stars=star_rating,
                guest=guest_rev,
                distance=distance_to_center,
                one_night=price)
        except (AttributeError, ValueError):
            text = 'Возникла ошибка при получении информации'

        if photos_count:
            try:
                resp_photo = get_photo(hotel['id'])['hotelImages'][:photos_count]
                photos = [resp_photo[num]['baseUrl'].format(size='y') for num
                          in range(photos_count)]
                yield text, photos, distance_to_center
            except Exception as exc:
                print('Возникло исключение {} в строках 90-96 файла util.py'.format(exc))
                yield 'Не удается отправить отель'
        else:
            yield text, distance_to_center


def get_photo(id: str):
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

    querystring = {"id": id}

    headers = {
        "X-RapidAPI-Key": HOTELS_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = json.loads(requests.get(url, headers=headers,
                                params=querystring).text)

    return response






