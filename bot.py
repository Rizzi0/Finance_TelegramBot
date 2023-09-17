import datetime
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from config import TOKEN
from defs import save_transaction, history_transactions
from keyboard_buttons import main_kb, expenses_kb, income_kb, history_kb


# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)

# Кнопки для основной клавиатуры

category = ['Еда', 'Дом', 'Транспорт', 'Развлечения', 'Другое', 'Зарплата', 'Дополнительный доход', 'Другое']


# Инициализируем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Обработка команды /start
@dp.message_handler(lambda message: message.text in ['/start', 'Назад'])
async def on_start(message: types.Message):

    await message.answer("Привет! Это бот для учета расходов и доходов.", reply_markup = main_kb)


@dp.message_handler(lambda message: message.text == 'Расходы' or message.text == 'Доходы')
async def record(message: types.Message):
    global current_type
    if message.text == 'Расходы':
        current_type = 'Расходы'
        await message.answer('Выберите категорию:', reply_markup = expenses_kb)
    elif message.text == 'Доходы': 
        current_type = 'Доходы'
        await message.answer('Выберите категорию:', reply_markup = income_kb)



@dp.message_handler(lambda message: message.text in category)
async def expense(message: types.Message):
    global selected_category

    selected_category = message.text
    if current_type == 'Доходы':
        await message.answer(f'Введите сколько вы заработали в категрии "{selected_category}"')
    else:
        await message.answer(f'Введите сколько вы потратили в категрии "{selected_category}"')

@dp.message_handler(lambda message: message.text.isdigit())
async def handle_expense_amount(message: types.Message):
    chat_id = message.chat.id
    formatted_date = datetime.date.today()
    expense_amount = int(message.text)

    save_transaction(chat_id, current_type, selected_category, expense_amount, formatted_date)
    await message.answer(f'{current_type[:-1]} {expense_amount} в категории "{selected_category}" сохранен!')

@dp.message_handler(lambda message: message.text == 'История')
async def record(message: types.Message):
    await message.answer('Выберите за какой период:', reply_markup = history_kb)

@dp.message_handler(lambda message: message.text == 'Сегодня' or message.text == 'Месяц' or message.text == 'Год')
async def record(message: types.Message):
    time = datetime.date.today()

    if message.text == 'Сегодня':
        time = time
        await message.answer(history_transactions(time))
    elif message.text == 'Месяц':
        time = time.month
        await message.answer(history_transactions(time))

    elif message.text == 'Год':
        time = time.year
        await message.answer(history_transactions(time))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)