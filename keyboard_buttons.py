from aiogram import types


# Основная клавиатура
main_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

main_kb.add('Расходы', 'Доходы', 'История')



# Клавиатура истории
history_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

history_kb.add('Сегодня', 'Месяц', 'Год', 'Период')
# Кнопки для клавиатуры расходов
expenses_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

expenses_kb.add('Еда', 'Дом', 'Транспорт', 'Развлечения', 'Другое')
expenses_kb.add('Назад')

# Кнопки для клавиатуры Доходов
income_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

income_kb.add('Зарплата', 'Дополнительный доход', 'Другое')
income_kb.add('Назад')