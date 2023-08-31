import sqlite3
from sqlite3 import Error

# в этой программе создаем базу данных с нужными названиями столбцов


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r"clients.db"
    # описание столбцов - id и тд
    sql_create_table = """ CREATE TABLE IF NOT EXISTS clients (
                                        id integer PRIMARY KEY,
                                        Age text, 
                                        Annual_Income text,
                                        Monthly_Inhand_Salary text,
                                        Interest_Rate text,
                                        Delay_from_due_date text,
                                        Num_of_Delayed_Payment text,
                                        Outstanding_Debt text,
                                        Monthly_Balance text,
                                        Approved text
                                    ); """


    # подключение к базе
    conn = create_connection(database)

    # создание таблицы
    if conn is not None:
        create_table(conn, sql_create_table)
    else:
        print("Ошибка: не удалось подключиться к базе.")


if __name__ == '__main__':
    main()