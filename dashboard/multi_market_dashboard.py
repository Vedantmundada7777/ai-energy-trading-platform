import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
import random

st.set_page_config(layout="wide")
st.title("⚡ AI ENERGY TRADING TERMINAL")

# ======================================================
# API FUNCTION
# ======================================================

@st.cache_data(ttl=3600)
def get_real_market_prices(region):

    url = "https://api.eia.gov/v2/electricity/rto/region-data/data/"

    params = {
        "api_key": "o1V9lQ00lcmcI7fZYyXQPnBWPfo7cJZA5r9bHGm3",
        "frequency": "hourly",
        "data[0]": "value",
        "facets[respondent][]": region,
        "facets[type][]": "D",
        "length": 48
    }

    try:
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return None

        data = response.json()

        rows = data.get("response", {}).get("data", [])

        demand = []

        for r in rows:
            v = r.get("value")
            if v is not None:
                demand.append(float(v))

        if len(demand) < 24:
            return None

        demand = demand[:24]

        # convert demand → price proxy
        min_d = min(demand)
        max_d = max(demand)

        prices = []

        for d in demand:
            normalized = (d - min_d) / (max_d - min_d + 1e-6)
            price = 30 + normalized * 40
            prices.append(price)

        return prices

    except:
        return None


# ======================================================
# MARKET SIMULATOR
# ======================================================

class MarketSimulator:

    def generate_day(self):

        base = 50

        pricesA = [base + random.gauss(0,5) for _ in range(24)]
        pricesB = [base + random.gauss(0,8) for _ in range(24)]
        pricesC = [base + random.gauss(0,10) for _ in range(24)]

        return pricesA, pricesB, pricesC


# ======================================================
# BATTERY MODEL
# ======================================================

class Battery:

    def __init__(self):
        self.capacity = 100
        self.soc = 50

    def charge(self):
        self.soc = min(self.capacity, self.soc + 5)

    def discharge(self):
        self.soc = max(0, self.soc - 5)


class BatteryFleet:

    def __init__(self, n):
        self.batteries = [Battery() for _ in range(n)]

    def step(self, action, price):

        profit = 0

        for battery in self.batteries:

            if action == 1:
                battery.charge()
                profit -= price * 0.1

            elif action == -1:
                battery.discharge()
                profit += price * 0.1

        return profit


# ======================================================
# RL AGENT
# ======================================================

class RLAgent:

    def choose_action(self, price, soc):

        if price < 45 and soc < 80:
            return 1

        elif price > 55 and soc > 20:
            return -1

        else:
            return 0


# ======================================================
# TABS
# ======================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "⚡ Simulation",
    "📊 History",
    "📈 Analytics",
    "🧠 AI Advisor",
    "🔮 Market Forecast",
    "⚡ Arbitrage Detector"
])

# ======================================================
# ======================================================
# TAB 1 — SIMULATION
# ======================================================

with tab1:

    st.sidebar.header("Simulation Controls")

    fleet_size = st.sidebar.slider("Fleet Size",1,50,10)
    days = st.sidebar.slider("Simulation Days",1,30,5)

    run = st.sidebar.button("Run Simulation")

    simulator = MarketSimulator()
    fleet = BatteryFleet(fleet_size)
    agent = RLAgent()

    price_history=[]
    soc_history=[]
    profit_history=[]
    actions=[]
    profit=0

    if run:

        # ------------------------------------------------
        # FETCH REAL GRID DATA
        # ------------------------------------------------

        demand = get_real_market_prices("PJM")

        if demand:

            pricesA = demand
            pricesB = [p + random.uniform(-3,3) for p in demand]
            pricesC = [p + random.uniform(-5,5) for p in demand]

            st.success("Using real grid demand data from EIA")

        else:

            pricesA, pricesB, pricesC = simulator.generate_day()

            st.warning("API unavailable — using simulated market data")

        # ------------------------------------------------
        # RUN SIMULATION
        # ------------------------------------------------

        for d in range(days):

            for h in range(24):

                prices=[pricesA[h],pricesB[h],pricesC[h]]

                avg_price=np.mean(prices)

                soc=fleet.batteries[0].soc

                action=agent.choose_action(avg_price,soc)

                buy_price=min(prices)
                sell_price=max(prices)

                if action==1:
                    price=buy_price
                elif action==-1:
                    price=sell_price
                else:
                    price=avg_price

                step_profit=fleet.step(action,price)

                profit+=step_profit

                price_history.append(avg_price)
                soc_history.append(soc)
                profit_history.append(profit)
                actions.append(action)

        # ------------------------------------------------
        # SUMMARY METRICS
        # ------------------------------------------------

        col1,col2,col3=st.columns(3)

        col1.metric("Fleet Size",fleet_size)
        col2.metric("Simulation Days",days)
        col3.metric("Total Profit",f"${profit:,.2f}")

        # ------------------------------------------------
        # DAILY MARKET PRICE VISUALIZATION
        # ------------------------------------------------

        st.subheader("Daily Market Prices")

        hours=list(range(24))

        for day in range(days):

            start=day*24
            end=start+24

            day_prices=price_history[start:end]

            fig=go.Figure()

            fig.add_trace(go.Scatter(
                x=hours,
                y=day_prices,
                mode="lines+markers",
                name=f"Day {day+1}"
            ))

            fig.update_layout(
                title=f"Market Price — Day {day+1}",
                xaxis_title="Hour",
                yaxis_title="Price ($)",
                height=350
            )

            st.plotly_chart(fig,use_container_width=True)

        # ------------------------------------------------
        # BATTERY SOC CHART
        # ------------------------------------------------

        fig2=go.Figure()

        fig2.add_trace(go.Scatter(
            y=soc_history,
            mode="lines",
            name="Battery SOC"
        ))

        fig2.update_layout(
            title="Battery State of Charge",
            xaxis_title="Time Step",
            yaxis_title="SOC"
        )

        st.plotly_chart(fig2,use_container_width=True)

        # ------------------------------------------------
        # PROFIT CHART
        # ------------------------------------------------

        fig3=go.Figure()

        fig3.add_trace(go.Scatter(
            y=profit_history,
            mode="lines",
            name="Profit"
        ))

        fig3.update_layout(
            title="Cumulative Profit",
            xaxis_title="Time Step",
            yaxis_title="Profit ($)"
        )

        st.plotly_chart(fig3,use_container_width=True)
        # ------------------------------------------------
# PRICE HEATMAP (TESLA STYLE GRID VIEW)
# ------------------------------------------------

st.subheader("Energy Price Heatmap")

# convert price history to matrix
price_matrix = []

for day in range(days):

    start = day * 24
    end = start + 24

    price_matrix.append(price_history[start:end])

price_matrix = np.array(price_matrix)

fig_heatmap = go.Figure(
    data=go.Heatmap(
        z=price_matrix,
        x=list(range(24)),
        y=[f"Day {i+1}" for i in range(days)],
        colorscale="Turbo",
        colorbar=dict(title="Price ($)")
    )
)

fig_heatmap.update_layout(
    title="Electricity Price Heatmap",
    xaxis_title="Hour of Day",
    yaxis_title="Simulation Day",
    height=500
)

st.plotly_chart(fig_heatmap, use_container_width=True)
# ======================================================
# TAB 2 — HISTORY
# ======================================================

with tab2:

    st.subheader("Simulation History")
    st.info("History connected to database in full SaaS version")


# ======================================================
# TAB 3 — ANALYTICS
# ======================================================

with tab3:

    st.subheader("Trading Analytics")

    if 'profit_history' in locals() and len(profit_history)>0:

        profits=np.array(profit_history)

        st.metric("Final Profit",f"${profits[-1]:,.2f}")

        fig=go.Figure()
        fig.add_histogram(x=profits)
        fig.update_layout(title="Profit Distribution")
        st.plotly_chart(fig,use_container_width=True)

    else:

        st.info("Run simulation first")


# ======================================================
# TAB 4 — AI ADVISOR
# ======================================================

with tab4:

    st.subheader("AI Decision Advisor")

    st.write("Recommended Strategy:")
    st.write("• Charge battery when price < $45")
    st.write("• Discharge when price > $55")
    st.write("• Hold otherwise")


# ======================================================
# TAB 5 — FORECAST
# ======================================================

with tab5:

    st.subheader("Market Forecast")

    simulator=MarketSimulator()

    pricesA,pricesB,pricesC=simulator.generate_day()

    prices=np.mean([pricesA,pricesB,pricesC],axis=0)

    forecast_horizon=st.slider("Forecast Hours",6,48,24)

    trend=np.polyfit(range(len(prices)),prices,1)

    forecast=[]

    for i in range(forecast_horizon):

        next_price=trend[0]*(len(prices)+i)+trend[1]
        forecast.append(next_price)

    fig=go.Figure()

    fig.add_trace(go.Scatter(y=prices,name="History"))
    fig.add_trace(go.Scatter(
        x=list(range(len(prices),len(prices)+forecast_horizon)),
        y=forecast,
        name="Forecast"
    ))

    st.plotly_chart(fig,use_container_width=True)


# ======================================================
# TAB 6 — ARBITRAGE DETECTOR
# ======================================================

with tab6:

    st.subheader("Market Arbitrage Opportunities")

    simulator=MarketSimulator()

    pricesA=get_real_market_prices("PJM")

    if pricesA:

        pricesB=[p+random.uniform(-3,3) for p in pricesA]
        pricesC=[p+random.uniform(-5,5) for p in pricesA]

    else:

        pricesA,pricesB,pricesC=simulator.generate_day()

    opportunities=[]

    for hour in range(24):

        prices={
            "PJM":pricesA[hour],
            "ERCOT":pricesB[hour],
            "CAISO":pricesC[hour]
        }

        buy_market=min(prices,key=prices.get)
        sell_market=max(prices,key=prices.get)

        spread=prices[sell_market]-prices[buy_market]

        if spread>5:

            opportunities.append({
                "Hour":hour,
                "Buy":buy_market,
                "Sell":sell_market,
                "Spread":round(spread,2)
            })

    if opportunities:

        df=pd.DataFrame(opportunities)
        st.dataframe(df)

    else:

        st.warning("No arbitrage opportunities found")
