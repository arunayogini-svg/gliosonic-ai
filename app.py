import streamlit as st
import time
import pandas as pd
import numpy as np

# Page Configuration for a Premium Medical App look
st.set_page_config(
    page_title="GlioSonic AI - Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Judges
st.markdown("""
    <style>
    .main-title { font-size:42px !important; font-weight: bold; color: #1E3A8A; }
    .subtitle { font-size:18px !important; color: #4B5563; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# App Header
st.markdown('<p class="main-title">🧠 GlioSonic AI Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Advanced Ultrasound-Induced Blood-Brain Barrier (BBB) Kinetic Timeline Modeler for Glioblastoma Treatment</p>', unsafe_allow_html=True)
st.markdown("---")

# 📊 SIDEBAR - CONTROLS & USER INPUTS
st.sidebar.header("🔬 Treatment Parameter Input")
patient_name = st.sidebar.text_input("Patient ID / Name:", "GS-2026-Alpha")
tumor_volume = st.sidebar.number_input("Tumor Volume (cm³):", min_value=0.1, max_value=150.0, value=25.0, step=0.1)

st.sidebar.markdown("### 🔊 Ultrasound Settings")
ultrasound_freq = st.sidebar.slider("Acoustic Frequency (MHz):", 0.2, 2.5, 1.0, 0.1)
acoustic_pressure = st.sidebar.slider("Acoustic Pressure (MPa):", 0.1, 1.5, 0.4, 0.05)

st.sidebar.markdown("### 🫧 Microbubble Agent")
microbubble_dose = st.sidebar.slider("Microbubble Dose (μL/kg):", 1.0, 10.0, 5.0, 0.5)

# 🧠 AI KINETICS PREDICTION ENGINE (Mathematical Model Simulation)
# Mechanical Index calculation (Crucial safety metric in ultrasound)
mechanical_index = acoustic_pressure / np.sqrt(ultrasound_freq)

# Calculate BBB opening duration based on physical parameters
# Base duration modified by parameters
base_window = 120 # mins
calculated_duration = int(base_window * (microbubble_dose / 5.0) * (acoustic_pressure / 0.4) * (1.0 / ultrasound_freq))
calculated_duration = max(10, min(calculating_duration, 360)) # Bound between 10m and 6h

# Drug Delivery Efficiency Estimation
delivery_efficiency = min(100, int((acoustic_pressure * microbubble_dose * 20) / ultrasound_freq))

# 🚨 UNIQUE FEATURE: SAFETY AND MECHANICAL INDEX CHECK FOR JUDGES
st.subheader("📋 AI Predictive Analysis & Safety Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Predicted BBB Open Window", value=f"{calculated_duration} mins")
with col2:
    st.metric(label="Est. Drug Delivery Efficiency", value=f"{delivery_efficiency} %")
with col3:
    st.metric(label="Mechanical Index (MI)", value=f"{mechanical_index:.2f}")
with col4:
    # Safety Validation Logic
    if mechanical_index > 0.6:
        st.error("⚠️ CRITICAL: Risk of Tissue Damage (MI Too High)")
        safety_status = "Unsafe"
    elif mechanical_index < 0.2:
        st.warning("⚠️ INSUFFICIENT: BBB might not open effectively")
        safety_status = "Ineffective"
    else:
        st.success("✅ OPTIMAL: Safe & Effective Range")
        safety_status = "Optimal"

st.markdown("---")

# 📈 UNIQUE FEATURE: DUAL-KINETIC CHART (Permeability & Drug Concentration)
st.subheader("📈 Multi-Parametric Kinetic Timeline Graph")
st.write("This interactive chart models BBB opening percentage alongside targeted drug concentration over a 6-hour timeline.")

# Generate continuous curve data for the graph
time_steps = np.arange(0, 360, 5)
permeability_curve = []
drug_curve = []

for t in time_steps:
    # Model BBB Permeability Curve
    if t < 15:
        p = 0
    elif t <= 45:
        p = 100 * (1 - np.exp(-(t-15)/10)) # Sharp rise
    elif t <= calculated_duration:
        p = 100 - 15 * ((t-45)/calculated_duration) # Slow decay while open
    else:
        p = 100 * np.exp(-(t-calculated_duration)/15) # Safe closing curve
    
    # Model Drug Concentration Curve (Dependent on permeability)
    if t < 20:
        d = 0
    elif t <= calculated_duration:
        d = delivery_efficiency * (1 - np.exp(-(t-20)/30))
    else:
        d = delivery_efficiency * np.exp(-(t-calculated_duration)/40)
        
    permeability_curve.append(max(0, p))
    drug_curve.append(max(0, d))

# Combine into a pandas DataFrame
chart_df = pd.DataFrame({
    'Time (Minutes)': time_steps,
    'BBB Permeability (%)': permeability_curve,
    'Target Drug Concentration (%)': drug_curve
}).set_index('Time (Minutes)')

# Plot interactive line chart
st.line_chart(chart_df)

# ⏳ INTERACTIVE REAL-TIME LIVE SIMULATION
st.subheader("⏳ Live Treatment Simulation Sequence")
if st.button("🚀 Execute GlioSonic Protocol Simulation"):
    progress_bar = st.progress(0)
    status = st.empty()
    
    status.info("Initializing Focused Ultrasound System... Calibrating Transducers...")
    progress_bar.progress(15)
    time.sleep(1)
    
    status.info("Infusing Microbubble Contrast Agents... Monitoring Systemic Circulation...")
    progress_bar.progress(40)
    time.sleep(1)
    
    if safety_status == "Unsafe":
        status.error(f"Simulation Halted! Mechanical Index ({mechanical_index:.2f}) exceeds safe human threshold. Adjust pressure.")
        progress_bar.progress(40)
    else:
        status.success(f"Acoustic Cavitation Achieved! Blood-Brain Barrier opened successfully for targeted window.")
        progress_bar.progress(75)
        time.sleep(1.5)
        status.success(f"Treatment Sequence Completed. Expected therapeutic window: {calculated_duration} minutes.")
        progress_bar.progress(100)

st.markdown("---")

# 💾 UNIQUE FEATURE: DATA EXPORT FOR CLINICAL USE
st.subheader("💾 Clinical Report Generation")
report_data = pd.DataFrame({
    "Parameter": ["Patient ID", "Tumor Volume (cm³)", "Frequency (MHz)", "Acoustic Pressure (MPa)", "Microbubble Dose (μL/kg)", "Mechanical Index", "Safety Status", "Est. Open Window (mins)"],
    "Value": [patient_name, tumor_volume, ultrasound_freq, acoustic_pressure, microbubble_dose, f"{mechanical_index:.2f}", safety_status, calculated_duration]
})

# Export button
csv = report_data.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Export Clinical Simulation Report (CSV)",
    data=csv,
    file_name=f"GlioSonic_Report_{patient_name}.csv",
    mime='text/csv',
)

st.caption("🔒 GlioSonic AI Prototype | Developed for Competition Showcase 2026. All simulation models are based on theoretical acoustic cavitation physics.")
