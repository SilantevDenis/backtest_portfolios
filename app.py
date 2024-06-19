import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Загрузка данных из файла
data_path = 'history_prices.csv'
data = pd.read_csv(data_path)

# Преобразование столбца 'Date' в формат datetime
data['Date'] = pd.to_datetime(data['Date'])

# Находим минимальную и максимальную даты в данных
min_date = data['Date'].min().date()
max_date = data['Date'].max().date()
default_end_date = max_date
default_start_date = max_date - datetime.timedelta(days=365)

# Интерфейс для выбора монет
st.sidebar.title("Выбор монет")
st.sidebar.header("Портфель 1")
coins_set1 = st.sidebar.multiselect("Выберите монеты для первого набора", data['Coin'].unique())
st.sidebar.header("Портфель 2")
coins_set2 = st.sidebar.multiselect("Выберите монеты для второго набора", data['Coin'].unique())

# Интерфейс для выбора периода и суммы
st.sidebar.header("Параметры инвестирования")
start_date = st.sidebar.date_input("Начальная дата", default_start_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("Конечная дата", default_end_date, min_value=min_date, max_value=max_date)
monthly_investment = st.sidebar.number_input("Ежемесячная сумма инвестирования", min_value=0.0, value=100.0)

# Кнопка для запуска анализа
if st.sidebar.button("Анализировать"):
    # Функция для обновления портфеля
    def update_portfolio(portfolio, coins, date, data, investment):
        coin_prices = data[(data['Coin'].isin(coins)) & (data['Date'] == date)]
        if coin_prices.empty:
            return portfolio
        num_coins = len(coin_prices)
        usd_per_coin = investment / num_coins
        for _, row in coin_prices.iterrows():
            coin = row['Coin']
            price = row['Close']
            quantity = usd_per_coin / price
            if coin in portfolio:
                portfolio[coin] += quantity
            else:
                portfolio[coin] = quantity
        return portfolio
    
    # Функция для расчета стоимости портфеля
    def calculate_portfolio_value(portfolio, date, data):
        total_value = 0
        for coin, quantity in portfolio.items():
            price = data[(data['Coin'] == coin) & (data['Date'] == date)]['Close'].values
            if price:
                total_value += quantity * price[0]
        return total_value

    # Начальные пустые портфели
    portfolio1 = {}
    portfolio2 = {}

    # Даты для анализа
    dates = pd.date_range(start=start_date, end=end_date, freq='MS')

    # Списки для хранения стоимости портфелей
    portfolio_values1 = []
    portfolio_values2 = []
    no_investment_values = []

    # Начальная сумма инвестиций
    total_invested = 0

    for date in dates:
        # Обновление портфелей
        portfolio1 = update_portfolio(portfolio1, coins_set1, date, data, monthly_investment)
        portfolio2 = update_portfolio(portfolio2, coins_set2, date, data, monthly_investment)
        
        # Расчет стоимости портфелей
        value1 = calculate_portfolio_value(portfolio1, date, data)
        value2 = calculate_portfolio_value(portfolio2, date, data)

        portfolio_values1.append(value1)
        portfolio_values2.append(value2)

        # Обновление суммы инвестиций без инвестирования
        total_invested += monthly_investment
        no_investment_values.append(total_invested)
    
    # Визуализация
    plt.figure(figsize=(14, 7))
    plt.plot(dates, portfolio_values1, label='Портфель Набор 1')
    plt.plot(dates, portfolio_values2, label='Портфель Набор 2')
    plt.plot(dates, no_investment_values, label='Без инвестиций', linestyle='--')
    plt.title('Изменение портфеля')
    plt.xlabel('Дата')
    plt.ylabel('Стоимость портфеля')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)