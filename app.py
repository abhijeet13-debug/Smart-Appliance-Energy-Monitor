import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Appliance Energy Monitor",
    layout="wide"
)

# ---------------- DARK CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0f1117;
}
[data-testid="stAppViewContainer"] {
    background-color: #0f1117;
}
h1,h2,h3,h4,h5,p,label {
    color:white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("⚡ Smart Appliance Energy Monitor")
st.caption("AI-based smart electricity monitoring")

# ---------------- SETTINGS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    rate = st.number_input("Rate/kWh (₹)", value=8)

with col2:
    days = st.number_input("Days", value=30)

with col3:
    uploaded_file = st.file_uploader("Upload CSV")

if uploaded_file is None:
    st.info("Upload CSV to continue")
    st.stop()

# ---------------- READ CSV ----------------
df = pd.read_csv(uploaded_file)

# Monthly kWh calculation
df["kwh_month"] = (df["power_watts"] * df["hours"] * days) / 1000
df["cost"] = df["kwh_month"] * rate

total_energy = df["kwh_month"].sum()
bill = df["cost"].sum()
carbon = total_energy * 0.82

# Efficiency score
if total_energy < 200:
    score = 90
elif total_energy < 400:
    score = 75
elif total_energy < 700:
    score = 50
else:
    score = 25

# ---------------- TOP CARDS ----------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("⚡ Monthly Energy", f"{total_energy:.2f} kWh")

with c2:
    st.metric("💰 Estimated Bill", f"₹{bill:.2f}")

with c3:
    st.metric("🌿 Carbon Footprint", f"{carbon:.1f} kg")

with c4:
    st.metric("⭐ Efficiency Score", f"{score}/100")

st.divider()

# ---------------- CHARTS ----------------
left, right = st.columns(2)

with left:
    st.subheader("Device Consumption")

    fig_bar = px.bar(
        df,
        x="device",
        y="kwh_month",
        color="device"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

with right:
    st.subheader("Energy Distribution")

    fig_pie = px.pie(
        df,
        names="device",
        values="kwh_month",
        hole=0.5
    )

    st.plotly_chart(fig_pie, use_container_width=True)

# ---------------- USAGE TREND ----------------
st.subheader("Usage Trend")

trend = np.random.randint(20, 30, days)

trend_df = pd.DataFrame({
    "Day": list(range(1, days + 1)),
    "Usage": trend
})

fig_line = px.line(
    trend_df,
    x="Day",
    y="Usage",
    markers=True
)

st.plotly_chart(fig_line, use_container_width=True)

# ---------------- LIVE LOAD ----------------
live_load = total_energy / days

st.subheader("📡 Live Load")

st.progress(min(live_load / 30, 1.0))

st.write(f"Current simulated load: {live_load:.2f} kWh/day")

# ---------------- AI RECOMMENDATIONS ----------------
st.subheader("🤖 AI Recommendations")

highest = df.sort_values("kwh_month", ascending=False).iloc[0]

st.warning(
    f"{highest['device']} is consuming the most energy."
)

if highest["device"] == "AC":
    st.info("Reduce AC usage by 2 hours/day to save electricity.")

if highest["device"] == "Heater":
    st.info("Reduce heater usage for better efficiency.")

st.success("Use LED bulbs to lower energy consumption.")

# ---------------- APPLIANCE RANKING ----------------
st.subheader("🏆 Appliance Ranking")

rank = df.sort_values("kwh_month", ascending=False)

st.dataframe(
    rank[["device", "kwh_month", "cost"]],
    use_container_width=True
)

# ---------------- DOWNLOAD CSV ----------------
csv = rank.to_csv(index=False)

st.download_button(
    "⬇ Download Results",
    csv,
    "energy_results.csv",
    "text/csv"
)