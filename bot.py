import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

API_TOKEN = '6889882987:AAHjc1dn-04QRh6A3B1Q0xtV4mBPqfMBXS8'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Словарь для хранения выбранной роли пользователей
user_role = {}
user_login = {}
user_password = {}


@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Менеджер")
    markup.add("Клиент")

    await message.answer("Привет! Кем вы являетесь?", reply_markup=markup)


@dp.message_handler(lambda message: message.text.lower() in ["менеджер", "клиент"])
async def on_role_selected(message: types.Message):
    role = message.text.lower()
    user_role[message.from_user.id] = role

    # Убираем клавиатуру с выбором роли
    markup = types.ReplyKeyboardRemove()
    await message.answer(f"Вы выбрали {role}. Теперь введите свой логин:", reply_markup=markup)


@dp.message_handler(lambda message: message.from_user.id in user_role and message.from_user.id not in user_login)
async def on_login_entered(message: types.Message):
    user_id = message.from_user.id
    role = user_role.get(user_id)
    login = message.text
    user_login[user_id] = login
    await message.answer(f"Теперь введите пароль для роли {role}:")


@dp.message_handler(
    lambda message: message.from_user.id in user_role and message.from_user.id in user_login and message.from_user.id not in user_password)
async def on_password_entered(message: types.Message):
    user_id = message.from_user.id
    role = user_role.get(user_id)
    password = message.text
    user_password[user_id] = password
    await message.answer(f"Авторизация прошла успешно")

    if role == 'менеджер':
        # Добавляем клавиатуру для дальнейших действий менеджера
        action_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        action_markup.add("Отслеживание диалога с закрепленными клиентами")
        action_markup.add("Получение заполненной клиентом формы претензии")
        action_markup.add("Уведомления об обращении клиента к боту")
        action_markup.add("Подключение к чату с клиентом")
        await message.answer("Что бы вы хотели сделать?", reply_markup=action_markup)
    elif role == 'клиент':
        # Добавляем клавиатуру для дальнейших действий клиента
        client_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        client_markup.add("Сделать накладную")
        client_markup.add("Регистрация претензии по шаблону")
        await message.answer("Что бы вы хотели сделать?", reply_markup=client_markup)


@dp.message_handler(lambda message: message.text.lower() == "сделать накладную")
async def on_create_invoice(message: types.Message):
    user_id = message.from_user.id
    role = user_role.get(user_id)
    if role == 'клиент':
        # Здесь вы можете добавить логику для создания накладной клиентом
        markup = types.ReplyKeyboardRemove()
        await message.answer(f"Вы выбрали Сделать накладную", reply_markup=markup)

@dp.message_handler(lambda message: message.text.lower() == "регистрация претензии по шаблону")
async def on_claim_registration_template(message: types.Message):
    user_id = message.from_user.id
    role = user_role.get(user_id)
    if role == 'клиент':
        # Добавляем клавиатуру для выбора типа претензии
        claim_template_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        claim_template_markup.add("Нарушение сроков доставки")
        claim_template_markup.add("Порча вложения")
        claim_template_markup.add("Утеря вложения")
        claim_template_markup.add("Повреждение упаковки")
        await message.answer("Выберите тип претензии:", reply_markup=claim_template_markup)


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
