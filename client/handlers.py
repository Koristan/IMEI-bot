from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import requests
import config

# Определяем базовые переменные из config.py
api_url = config.BASE_URL
api_token = config.API_TOKEN
whitelist = config.WHITELIST

router = Router()

# Добавление нового юзера в вайтлист
@router.message(Command(commands=['auth']))
async def authorize(msg: Message):
    user_id = msg.from_user.id
    reply_message = "Вы уже авторизованы!"
    if (user_id not in whitelist):
        whitelist.append(user_id)
        reply_message = "Авторизован!"
    await msg.reply(reply_message)


# Базовый роутер
@router.message()
async def start_handler(msg: Message):

    # Проверка, есть ли пользователь в вайтлисте
    user_id = msg.from_user.id
    if check_whitelist(user_id):
        await msg.answer(f"Не авторизован!")
        return
    
    # Запрос к API
    try:
        data = {
            'imei_id': msg.text,
            'token': api_token
        }
        response = requests.get(f"{api_url}/api/check-imei/", params=data).json()
    except:
        return

    # Определение ответа для красивого вывода
    message = 'Вывод:\n'
    if 'errors' in response:
        message = 'Ошибка:\n'
    
    # Превращаем словарь в текст
    for key, value in response.items():
        if (str(type(value)) == "<class 'dict'>"):
            for _key, _value in value.items():
                message += f' - {_key}: {_value}\n'
        else:
            message += f'{key}: {value}\n'

    # Отправляем ответ в ТГ
    await msg.answer(message)


def check_whitelist(user_id):
    for el in whitelist:
        if (user_id == el):
            return False
    return True