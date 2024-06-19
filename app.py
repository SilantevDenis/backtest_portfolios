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
        if price.size > 0:
            total_value += quantity * price[0]
    return total_value

# Интерфейс для выбора монет и параметров инвестирования
st.sidebar.title("Портфели")

num_portfolios = st.sidebar.number_input("Количество портфелей", min_value=1, value=2)
portfolios = []

for i in range(num_portfolios):
    st.sidebar.header(f"Портфель {i + 1}")
    coins = st.sidebar.multiselect(f"Выберите монеты для портфеля {i + 1}", data['Coin'].unique(), key=f"coins_{i}")
    portfolios.append(coins)

st.sidebar.header("Параметры инвестирования")
start_date = st.sidebar.date_input("Начальная дата", default_start_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("Конечная дата", default_end_date, min_value=min_date, max_value=max_date)
monthly_investment = st.sidebar.number_input("Сумма инвестирования за период", min_value=0.0, value=100.0)

investment_period = st.sidebar.selectbox("Период инвестирования", ['День', 'Неделя', 'Месяц', 'Год'])

# Определяем частоту инвестирования
if investment_period == 'День':
    freq = 'D'
elif investment_period == 'Неделя':
    freq = 'W'
elif investment_period == 'Месяц':
    freq = 'MS'
elif investment_period == 'Год':
    freq = 'YS'

# Кнопка для запуска анализа
if st.sidebar.button("Анализировать"):
    portfolios_values = [[] for _ in range(num_portfolios)]
    no_investment_values = []
    total_invested = 0

    # Начальные пустые портфели
    portfolios_dicts = [{} for _ in range(num_portfolios)]

    # Даты для анализа
    dates = pd.date_range(start=start_date, end=end_date, freq=freq)

    for date in dates:
        for i in range(num_portfolios):
            portfolios_dicts[i] = update_portfolio(portfolios_dicts[i], portfolios[i], date, data, monthly_investment)
            value = calculate_portfolio_value(portfolios_dicts[i], date, data)
            portfolios_values[i].append(value)

        total_invested += monthly_investment
        no_investment_values.append(total_invested)
    
    # Визуализация
    plt.figure(figsize=(14, 7))
    for i in range(num_portfolios):
        plt.plot(dates, portfolios_values[i], label=f'Портфель {i + 1}')
    plt.plot(dates, no_investment_values, label='Без инвестиций', linestyle='--')
    plt.title('Изменение портфеля')
    plt.xlabel('Дата')
    plt.ylabel('Стоимость портфеля')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

    # Отображение итоговой стоимости и доходности
    st.write("## Итоговая стоимость и доходность портфелей")
    for i in range(num_portfolios):
        final_value = portfolios_values[i][-1]
        total_profit = final_value - total_invested
        profit_percent = (total_profit / total_invested) * 100
        st.write(f"Портфель {i + 1}:")
        st.write(f"Итоговая стоимость: ${final_value:.2f}")
        st.write(f"Общая прибыль: ${total_profit:.2f} ({profit_percent:.2f}%)")
