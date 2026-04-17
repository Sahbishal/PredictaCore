import streamlit as st
import pandas as pd
import requests
import altair as alt
import json
import os

# API URL Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="PredictaCore Dashboard", layout="wide")

st.title("🚀 PredictaCore: Turbine Engine Predictive Maintenance")

# Sidebar for turbine selection
st.sidebar.header("Machine Selection")
try:
    machines = requests.get(f"{API_URL}/machines").json()
    selected_machine = st.sidebar.selectbox("Choose a Turbine", machines)
except Exception as e:
    st.error(f"Could not connect to the backend at {API_URL}. Please ensure the FastAPI server is running.")
    st.stop()

# Load real-time stats
if selected_machine:
    status_response = requests.post(f"{API_URL}/status", json={"machine_id": selected_machine}).json()
    
    # Layout: Top row for status and latest metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Status", status_response['status'], delta=None if status_response['status'] == "Normal" else "Issue Detected", delta_color="inverse")
    
    with col2:
        st.metric("Temperature", f"{status_response['latest_stats']['temperature']:.2f} °C")
        
    with col3:
        st.metric("Vibration", f"{status_response['latest_stats']['vibration']:.2f} mm/s")
        
    with col4:
        st.metric("RPM", f"{status_response['latest_stats']['rpm']:.2f}")

    # Layout: Main content area
    st.divider()
    
    # Charts (using some mock historical data for visualization)
    st.subheader("Sensor Trends")
    try:
        history_response = requests.get(f"{API_URL}/history/{selected_machine}").json()
        machine_history = pd.DataFrame(history_response)
    except Exception as e:
        st.error("Could not fetch history data from the backend.")
        machine_history = pd.DataFrame()
    
    chart_data = machine_history.melt(id_vars=['timestamp'], value_vars=['temperature', 'vibration', 'pressure', 'oil_pressure'])
    
    chart = alt.Chart(chart_data).mark_line().encode(
        x='timestamp:T',
        y='value:Q',
        color='variable:N'
    ).properties(height=300).interactive()
    
    st.altair_chart(chart, use_container_width=True)
    
    # Maintenance Recommendations
    if status_response['anomalies']:
        st.warning(f"Anomalies detected: {', '.join(status_response['anomalies'])}")
        st.subheader("🛠️ Recommended Maintenance Procedures")
        for anomaly, steps in status_response['recommendations'].items():
            st.markdown(f"**Anomaly: {anomaly.replace('_', ' ').capitalize()}**")
            for step in steps:
                st.write(f"- {step}")
    else:
        st.success("No anomalies detected. Machine is operating within normal parameters.")

    st.divider()
    
    # Interactive Q&A
    st.subheader("💬 Maintenance Assistant (Ask Follow-up Questions)")
    user_question = st.text_input("Example: 'Why is high vibration dangerous?' or 'What should I do if the coolant level is fine but temperature is still high?'")
    
    if user_question:
        with st.spinner("Analyzing..."):
            qa_payload = {
                "machine_id": selected_machine,
                "question": user_question,
                "status": status_response['latest_stats'],
                "recommendations": status_response['recommendations']
            }
            try:
                qa_response = requests.post(f"{API_URL}/ask", json=qa_payload).json()
                st.info(f"**Assistant:** {qa_response['response']}")
            except Exception as e:
                st.error(f"Error connecting to the LLM agent at {API_URL}.")
