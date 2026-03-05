import sys
import os
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.market.multi_market_simulator import MultiMarketSimulator
from src.fleet_manager import BatteryFleet
from src.ai.rl_agent import RLAgent

st.set_page_config(layout="wide")

st.title("⚡ AI ENERGY TRADING TERMINAL")

# Sidebar Controls
st.sidebar.header("Simulation Controls")

fleet_size = st.sidebar.slider("Fleet Size", 1, 50, 10)
days = st.sidebar.slider("Simulation Days", 1, 30, 5)
volatility = st.sidebar.slider("Market Volatility", 0.1, 3.0, 1.0)

run = st.sidebar.button("Run Simulation")

# Initialize components
market = MultiMarketSimulator()
fleet = BatteryFleet(num_batteries=fleet_size)
agent = RLAgent()

price_history = []
soc_history = []
profit_history = []
actions = []

profit = 0

if run:

    for d in range(days):

        pricesA, pricesB, pricesC = market.generate_day()

        for h in range(24):

            prices = [pricesA[h], pricesB[h], pricesC[h]]

            avg_price = np.mean(prices)

            soc = fleet.batteries[0].soc

            state = agent.get_state(avg_price, soc)

            action = agent.choose_action(state)

            buy_price = min(prices)
            sell_price = max(prices)

            if action > 0:
                price = buy_price
            elif action < 0:
                price = sell_price
            else:
                price = avg_price

            step_profit = fleet.step_fleet(action, price)

            profit += step_profit

            price_history.append(avg_price)
            soc_history.append(fleet.batteries[0].soc)
            profit_history.append(profit)
            actions.append(action)

# Top metrics
col1, col2, col3 = st.columns(3)

col1.metric("Fleet Size", fleet_size)
col2.metric("Simulation Days", days)
col3.metric("Total Profit", f"${profit:,.0f}")

# Charts layout
colA, colB = st.columns(2)

# Market price chart
with colA:

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=price_history,
        mode="lines",
        name="Market Price"
    ))

    fig.update_layout(
        title="Electricity Market Price",
        xaxis_title="Hour",
        yaxis_title="Price"
    )

    st.plotly_chart(fig, use_container_width=True)

# SOC chart
with colB:

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        y=soc_history,
        mode="lines",
        name="Battery SOC"
    ))

    fig2.update_layout(
        title="Battery State of Charge",
        xaxis_title="Hour",
        yaxis_title="SOC"
    )

    st.plotly_chart(fig2, use_container_width=True)

# AI Actions
fig3 = go.Figure()

fig3.add_trace(go.Bar(
    y=actions,
    name="AI Action"
))

fig3.update_layout(
    title="AI Trading Actions (+charge / -sell)"
)

st.plotly_chart(fig3, use_container_width=True)

# Profit chart
fig4 = go.Figure()

fig4.add_trace(go.Scatter(
    y=profit_history,
    mode="lines",
    name="Profit"
))

fig4.update_layout(
    title="Cumulative Profit"
)

st.plotly_chart(fig4, use_container_width=True)

# Trading data table
df = pd.DataFrame({
    "Price": price_history,
    "SOC": soc_history,
    "Action": actions,
    "Profit": profit_history
})

st.subheader("Trading Log")

st.dataframe(df)

# Export report
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Trading Report",
    csv,
    "energy_trading_report.csv",
    "text/csv"
)