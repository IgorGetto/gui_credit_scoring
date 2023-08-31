# ID,Customer_ID,Month,Name,Age,SSN,Occupation,Annual_Income,Monthly_Inhand_Salary,Num_Bank_Accounts,Num_Credit_Card,Interest_Rate,
# Num_of_Loan,Type_of_Loan,Delay_from_due_date,Num_of_Delayed_Payment,Changed_Credit_Limit,Num_Credit_Inquiries,Credit_Mix,Outstanding_Debt,
# Credit_Utilization_Ratio,Credit_History_Age,Payment_of_Min_Amount,Total_EMI_per_month,Amount_invested_monthly,Payment_Behaviour,Monthly_Balance,Credit_Score


import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import itertools
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import make_pipeline

# importing the required modules
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

# загружаем данные для обучения модели
df = pd.read_csv("train.csv")
# берем от них только 10 000 значений и убираем лишние колонки и дубликаты клиентов по именам
df = df[:10000]
df_new = df.drop(columns=["ID", "Customer_ID", "Month","Num_Bank_Accounts", "Num_Credit_Card", 'Num_of_Loan',
                           "Type_of_Loan", "Changed_Credit_Limit", "Num_Credit_Inquiries", "Credit_Mix", 'SSN',
                           "Credit_Utilization_Ratio", "Amount_invested_monthly", "Occupation",
                          'Credit_History_Age', 'Payment_of_Min_Amount', 'Payment_Behaviour', 'Total_EMI_per_month'])
df_new = df_new.drop_duplicates(subset=['Name'])


# для обучения модели нужны только числовые значения - переводим результат скоринга в шкалу от 0 до 2
df_new['Credit_Score'] = df_new['Credit_Score'].replace('Good', '2')
df_new['Credit_Score'] = df_new['Credit_Score'].replace('Standard', '1')
df_new['Credit_Score'] = df_new['Credit_Score'].replace('Poor', '0')

# df_new['Age'] = df_new['Age'].str.replace(r"[^\d\.]", "", regex=True)

# преобразуем данные в числовой формат - убираем лишнее по типу (пример: '28__' в '28')
df_new = df_new.replace(r"[^\d\.]", "", regex=True)

# убираем аномалии в возрасте
df_new = df_new[pd.to_numeric(df_new['Age']) < 100]
df_new = df_new[pd.to_numeric(df_new['Age']) > 0]

# убираем все данные с пропусками
df_new = df_new.dropna()

# print(df_new)

# создаем данные для обучения нашей модели
x = df_new.drop(columns=['Credit_Score', 'Name'])
y = df_new["Credit_Score"]

# разбиваем их на тренировочные и тестовые для проверки качества модели
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=.05, random_state=1)

# создаем pipeline и 'стандартизатор' для наших данных - чтобы он привел их в стандартизированный вид для модели логистической регрессии
pipe = make_pipeline(StandardScaler(), LogisticRegression())

# тренируем-обучаем нашу модели
pipe.fit(X_train, y_train)

# смотрим качество модели
print(pipe.score(X_test, y_test))

# y_pred = pipe.predict(X_test)
# print(y_pred)

# создаем функцию для новых клиентов, которую будем использовать в нашем приложении.
def prediction(data):
    print('predict')
    y_pred = pipe.predict(data)
    return y_pred

