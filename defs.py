import psycopg2
import pandas as pd



def save_transaction(chat_id, current_type, selected_category, expense_amount,formatted_date):
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="Finance_TelegramBot",
        user="postgres",
        password="1234"
    )

    cursor = conn.cursor()

    insert_chat_query = """INSERT INTO transactions (user_id, type_transaction, category, spent, date_spent) VALUES(%s, %s, %s, %s, %s)
    """

    cursor.execute(insert_chat_query,(chat_id, current_type, selected_category, expense_amount, formatted_date))


    conn.commit()
    cursor.close()
    conn.close()


def history_transactions(time):
    conn = psycopg2.connect(
    host="127.0.0.1",
    database="Finance_TelegramBot",
    user="postgres",
    password="1234"
)

    cursor = conn.cursor()
    
    if len(str(time)) > 4:
        select_query = """SELECT type_transaction, category, spent FROM transactions WHERE date_spent = %s"""
    elif len(str(time)) == 1:
        select_query = """SELECT type_transaction, category, spent FROM transactions WHERE date_spent BETWEEN '2023-09-1' AND '2023-09-30' """
    elif len(str(time)) == 4:
        select_query = """SELECT type_transaction, category, spent FROM transactions WHERE date_spent BETWEEN '2023-1-1' AND '2023-12-31' """




    cursor.execute(select_query, (time,))

    result = pd.read_sql_query(select_query, conn)
    result = result.rename(columns={'type_transaction': 'Тип транзакции', 'category': 'Категория', 'spent': 'Сумма'})

    # Создаем словарь с функциями форматирования для каждого столбца
    formatters = {
        'Тип транзакции': lambda x: f'{x:<20}',
        'Категория': lambda x: f'{x:<20}',
        'Сумма': lambda x: f'{x:<20}'
    }

    # Применяем форматирование к DataFrame
    formatted_result = result.to_string(index=False, justify='left', formatters=formatters)

    print(formatted_result)

    conn.commit()
    cursor.close()
    conn.close()
    return result