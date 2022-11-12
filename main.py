from create_bot import dp
from aiogram.utils import executor


async def on_startup(_):
    print('Бот вышел в онлайн')


from handlers import user, lowprice, history, highprice, bestdeal


if __name__ == '__main__':
    user.register_user_handlers(dp)
    highprice.register_highprice_handler(dp)
    bestdeal.register_bestdeal_handler(dp)
    lowprice.register_lowprice_handler(dp)
    history.register_history_handlers(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)