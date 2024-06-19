import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Загрузка данных из файла с указанием типов данных
data_path = '/mnt/data/combined_crypto_data.csv'
data = pd.read_csv(data_path, dtype={'Volume': 'str', 'Market Cap': 'str'})  # Укажите правильные типы данных для соответствующих столбцов

# Преобразование столбца 'Date' в формат datetime
data['Date'] = pd.to_datetime(data['Date'])

# Преобразование столбцов с числовыми значениями
for col in ['Close', 'Open', 'High', 'Low', 'Volume', 'Market Cap']:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Интерфейс для выбора монет
st.sidebar.title("Выбор монет")
st.sidebar.header("Набор 1")
coins_set1 = st.sidebar.multiselect("Выберите монеты для первого набора", data['Coin'].unique())
st.sidebar.header("Набор 2")
coins_set2 = st.sidebar.multiselect("Выберите монеты для второго набора", data['Coin'].unique())

# Интерфейс для выбора периода и суммы
st.sidebar.header("Параметры инвестирования")
start_date = st.sidebar.date_input("Начальная дата", datetime.date(2022, 1, 1))
end_date = st.sidebar.date_input("Конечная дата", datetime.date(2023, 1, 1))
monthly_investment = st.sidebar.number_input("Ежемесячная сумма инвестирования", min_value=0.0, value=100.0)

# Кнопка для запуска анализа
if st.sidebar.button("Анализировать"):
    # Функция для расчета стоимости портфеля
    def calculate_portfolio_value(data, coins, start_date, end_date, monthly_investment):
        dates = pd.date_range(start=start_date, end=end_date, freq='MS')
        portfolio_value = []
        total_invested = 0
        for date in dates:
            month_value = 0
            for coin in coins:
                coin_data = data[(data['Coin'] == coin) & (data['Date'] <= date)]
                if not coin_data.empty:
                    month_value += monthly_investment / len(coins) / coin_data.iloc[-1]['Close']
            total_invested += monthly_investment
            portfolio_value.append(month_value * coin_data.iloc[-1]['Close'] if month_value else 0)
        return pd.Series(portfolio_value, index=dates), total_invested

    # Расчет стоимости портфелей
    if coins_set1:
        portfolio_value1, total_invested1 = calculate_portfolio_value(data, coins_set1, start_date, end_date, monthly_investment)
        st.write("Портфель Набор 1:", portfolio_value1)
    else:
        st.error("Выберите хотя бы одну монету для Набора 1")
        portfolio_value1 = pd.Series()

    if coins_set2:
        portfolio_value2, total_invested2 = calculate_portfolio_value(data, coins_set2, start_date, end_date, monthly_investment)
        st.write("Портфель Набор 2:", portfolio_value2)
    else:
        st.error("Выберите хотя бы одну монету для Набора 2")
        portfolio_value2 = pd.Series()

    # Рассчитываем значение, если бы сумма просто накапливалась
    dates = pd.date_range(start=start_date, end=end_date, freq='MS')
    no_investment_value1 = [i * monthly_investment for i in range(1, len(dates) + 1)]
    no_investment_value2 = no_investment_value1  # одинаковое накопление для обоих наборов

    st.write("Без инвестиций Набор 1:", no_investment_value1)
    st.write("Без инвестиций Набор 2:", no_investment_value2)

    # Визуализация
    plt.figure(figsize=(14, 7))
    if not portfolio_value1.empty:
        plt.plot(portfolio_value1, label='Портфель Набор 1')
        plt.plot(dates, no_investment_value1, 'r--', label='Без инвестиций Набор 1')
    if not portfolio_value2.empty:
        plt.plot(portfolio_value2, label='Портфель Набор 2')
        plt.plot(dates, no_investment_value2, 'b--', label='Без инвестиций Набор 2')

    plt.title('Изменение портфеля')
    plt.xlabel('Дата')
    plt.ylabel('Стоимость портфеля')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
