import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Traffic Graph", layout="wide")

# Dark theme styling
st.markdown("""
    <style>
    body {
        background-color: #0E1117;
        color: white;
    }
    .stSlider label {
        color: #00C9A7;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align:center;color:#00C9A7;'>📊 Live Traffic Visualization</h1>", unsafe_allow_html=True)

st.write("### Real-Time Traffic Simulation Graph")

# --------------------------
# USER INPUTS
# --------------------------
col1, col2 = st.columns(2)

with col1:
    traffic_volume = st.slider("Traffic Volume", 0, 10000, 5000)

with col2:
    hour = st.slider("Hour", 0, 23, 12)

# --------------------------
# LIVE GRAPH
# --------------------------
fig, ax = plt.subplots()

hours = list(range(24))

# Simulated curve (dynamic)
traffic_sim = [traffic_volume * (np.sin(h/3) + 1) for h in hours]

# Plot line
ax.plot(hours, traffic_sim, marker='o', linewidth=2)

# Highlight current input
ax.scatter(hour, traffic_volume, s=200)

ax.set_title("Live Traffic Pattern")
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Traffic Volume")

st.pyplot(fig)

# --------------------------
# EXTRA INFO
# --------------------------
st.write("---")

st.subheader("📈 Current Inputs")

col3, col4 = st.columns(2)

col3.metric("Traffic Volume", traffic_volume)
col4.metric("Selected Hour", hour)