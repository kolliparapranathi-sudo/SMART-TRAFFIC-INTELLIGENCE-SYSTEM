# ===============================
# 🚦 Smart Traffic Dashboard
# ===============================

import streamlit as st
import numpy as np
import pickle

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="Traffic Intelligence System", layout="wide")

# ------------------------------
# DARK UI STYLE
# ------------------------------
st.markdown("""
    <style>
    body {
        background-color: #0E1117;
        color: white;
    }

    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 12px;
        height: 3em;
        width: 100%;
        font-size: 18px;
        font-weight: bold;
    }

    .stSlider label {
        color: #00C9A7;
        font-weight: bold;
    }

    .css-1d391kg {
        background-color: #111827;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------
# LOAD MODEL
# ------------------------------
model = pickle.load(open("traffic_model.pkl", "rb"))

# ------------------------------
# TITLE
# ------------------------------
st.markdown("<h1 style='text-align:center;color:#FF4B4B;'>🚦 Smart Traffic Intelligence System</h1>", unsafe_allow_html=True)
st.write("### Machine Learning Based Traffic Prediction Dashboard")

# ------------------------------
# SIDEBAR NAVIGATION
# ------------------------------
page = st.sidebar.radio("📌 Navigate", ["Prediction", "Live Graph"])

# ======================================================
# 🚀 PAGE 1: PREDICTION
# ======================================================
if page == "Prediction":

    st.subheader("🚗 Enter Traffic Details")

    col1, col2 = st.columns(2)

    with col1:
        traffic_volume = st.slider("Traffic Volume", 0, 10000, 5000)
        hour = st.slider("Hour of Day", 0, 23, 12)

    with col2:
        temp = st.slider("Temperature (K)", 250, 320, 290)
        clouds = st.slider("Cloud Coverage (%)", 0, 100, 50)

    # ------------------------------
    # FEATURE ENGINEERING
    # ------------------------------
    rush_hour = 1 if hour in [7,8,9,17,18,19] else 0
    weekend = 1 if hour >= 18 else 0

    hour_sin = np.sin(2 * np.pi * hour / 24)
    hour_cos = np.cos(2 * np.pi * hour / 24)

    features = np.array([[traffic_volume, hour_sin, hour_cos, rush_hour, weekend, temp, clouds]])

    # ------------------------------
    # PREDICT BUTTON
    # ------------------------------
    if st.button("🚀 Predict Traffic"):

        prediction = model.predict(features)

        # Try probabilities
        try:
            probs = model.predict_proba(features)[0]
        except:
            probs = [0.33, 0.33, 0.33]

        st.write("## 🚀 Prediction Result")

        if prediction[0] == 0:
            st.success("🟢 Low Traffic")
        elif prediction[0] == 1:
            st.warning("🟡 Medium Traffic")
        else:
            st.error("🔴 High Traffic")

        # Confidence display
        st.write("### 🔎 Confidence Level")
        st.progress(float(max(probs)))

        st.write(f"Low: {probs[0]:.2f}")
        st.write(f"Medium: {probs[1]:.2f}")
        st.write(f"High: {probs[2]:.2f}")

    # ------------------------------
    # METRICS DISPLAY
    # ------------------------------
    st.write("---")
    st.subheader("📊 Current Inputs")

    col3, col4, col5 = st.columns(3)

    col3.metric("Traffic Volume", traffic_volume)
    col4.metric("Hour", hour)
    col5.metric("Temperature", temp)

# ======================================================
# 📊 PAGE 2: GRAPH (SEPARATE FILE)
# ======================================================
elif page == "Live Graph":

    import graph_page