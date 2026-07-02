import streamlit as st
import time

# Page Configuration
st.set_page_config(
    page_title="GlioSonic AI",
    page_icon="🧠",
    layout="centered"
)

# Main Title
st.title("🧠 GlioSonic AI")
st.subheader("Blood-Brain Barrier (BBB) Opening Kinetic Timeline")
st.write("Predictive modeling for ultrasound-induced BBB opening in Glioblastoma treatment.")

st.markdown("---")

# User Inputs (Sidebar)
st.sidebar.header("📊 Patient & Treatment Details")
patient_name = st.sidebar.text_input("Patient Name:", "Patient X")
ultrasound_freq = st.sidebar.slider("Ultrasound Frequency (MHz):", 0.5, 2.0, 1.0, 0.1)
microbubble_dose = st.sidebar.slider("Microbubble Dose (mg/kg):", 0.1, 1.0, 0.5, 0.05)

# Simple Simulation Logic for BBB Opening Duration
base_duration = 180  # Base 3 hours in minutes
calculated_duration = int(base_duration * (microbubble_dose / 0.5) * (1.0 / ultrasound_freq))

# Display Results
st.subheader(f"📋 Treatment Report: {patient_name}")

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Estimated BBB Open Duration", value=f"{calculated_duration} mins")
with col2:
    st.metric(label="Safety Status", value="Safe", delta="Optimal")

# Kinetic Timeline Visual Simulation
st.markdown("### ⏳ Kinetic Timeline Simulation")

progress_bar = st.progress(0)
status_text = st.empty()

# Simulation Button
if st.button("🚀 Start Simulation"):
    status_text.text("Initiating ultrasound burst... Opening Blood-Brain Barrier...")
    progress_bar.progress(25)
    time.sleep(1)
    
    status_text.text("BBB Open. Drug delivery window active...")
    progress_bar.progress(60)
    time.sleep(1)
    
    status_text.text(f"Maintaining open window for {calculated_duration} minutes...")
    progress_bar.progress(90)
    time.sleep(1)
    
    status_text.text("Ultrasound stopped. BBB closed successfully and safely.")
    progress_bar.progress(100)
    st.success("Kinetic timeline simulation completed successfully!")

st.markdown("---")
st.info("💡 Note: This application is a prototype simulation for the GlioSonic AI project.")

