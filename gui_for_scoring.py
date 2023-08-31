import tkinter as tk
import pandas as pd
import sqlite3
from sqlite3 import Error
import scoring

# создаем окно приложения
window = tk.Tk()
window.title('Scoring')
window.geometry('400x600')

# название базы данных и также создаем датафрейм для удобства
db_name = 'clients.db'
new_clients = pd.DataFrame([], index=[], columns=['Age', 'Annual_Income', 'Monthly_Inhand_Salary', 'Interest_Rate',
                                                  'Delay_from_due_date', 'Num_of_Delayed_Payment', 'Outstanding_Debt',
                                                  'Monthly_Balance'])


# подключение и запрос к базе
def run_query(query, parameters=()):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parameters)
        conn.commit()
    return result

count = 0

# получаем данные введенные в окне
def get_info():
    global count
    new_clients.loc[len(new_clients.index)] = [age.get(), Annual_Income.get(), Monthly_Inhand_Salary.get(), Interest_Rate.get(),
                                               Delay_from_due_date.get(), Num_of_Delayed_Payment.get(), Outstanding_Debt.get(),
                                               Monthly_Balance.get()]
    print(new_clients)

    # запускаем нашу модель из программы scoring.py
    result = scoring.prediction(new_clients)
    print(result)

    # выводим результат на экран
    result_label = tk.Label(window, text=f'Result is {result} \n(0 is bad, 1 is ok, 2 is good)')
    result_label.place(x=130, y=550)

    # сохраняем результат в базу данных с помощью запроса и нашей функции run_squery
    query = 'INSERT INTO clients VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    parameters = (age.get(), Annual_Income.get(), Monthly_Inhand_Salary.get(), Interest_Rate.get(), Delay_from_due_date.get(),
                  Num_of_Delayed_Payment.get(), Outstanding_Debt.get(), Monthly_Balance.get(),  str(result[count]))
    run_query(query, parameters)
    # считаем каждого добавленного клиента, чтобы выводить правильный результат
    count += 1

    # выводим наполнение бд в консоль (если надо)
    # query = 'SELECT * FROM clients ORDER BY age DESC'
    # db_rows = run_query(query)
    # for row in db_rows:
    #     print('Новая строка')
    #     for i in range(1, 10):
    #         print(row[i], end='')


# создаем поля ввода и кнопку на экране

age = tk.Entry(window, width=30)
age.place(x=160, y=50)
age_label = tk.Label(window, text='Age')
age_label.place(x=10, y=50)

Annual_Income = tk.Entry(window, width=30)
Annual_Income.place(x=160, y=100)
Annual_Income_label = tk.Label(window, text='Annual Income')
Annual_Income_label.place(x=10, y=100)

Monthly_Inhand_Salary = tk.Entry(window, width=30)
Monthly_Inhand_Salary.place(x=160, y=150)
Monthly_Inhand_Salary_label = tk.Label(window, text='Monthly Inhand Salary')
Monthly_Inhand_Salary_label.place(x=10, y=150)

Interest_Rate = tk.Entry(window, width=30)
Interest_Rate.place(x=160, y=200)
Interest_Rate_label = tk.Label(window, text='Interest Rate')
Interest_Rate_label.place(x=10, y=200)

Delay_from_due_date = tk.Entry(window, width=30)
Delay_from_due_date.place(x=160, y=250)
Delay_from_due_date_label = tk.Label(window, text='Delay from due date')
Delay_from_due_date_label.place(x=10, y=250)

Num_of_Delayed_Payment = tk.Entry(window, width=30)
Num_of_Delayed_Payment.place(x=160, y=300)
Num_of_Delayed_Payment_label = tk.Label(window, text='Num of Delayed Payment')
Num_of_Delayed_Payment_label.place(x=10, y=300)

Outstanding_Debt = tk.Entry(window, width=30)
Outstanding_Debt.place(x=160, y=350)
Outstanding_Debt_label = tk.Label(window, text='Outstanding Debt')
Outstanding_Debt_label.place(x=10, y=350)

Monthly_Balance = tk.Entry(window, width=30)
Monthly_Balance.place(x=160, y=400)
Monthly_Balance_label = tk.Label(window, text='Monthly Balance')
Monthly_Balance_label.place(x=10, y=400)

accept_button = tk.Button(window, text='Accept', width=10, command=get_info)
accept_button.place(x=150, y=500)

window.mainloop()
