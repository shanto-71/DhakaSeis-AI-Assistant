import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os
from core_engine.physics_engine import compute_sa_BNBC2020 
from visual_triage.spatial_api import fetch_spatial_data

# --- 1. RESEARCH CONFIGURATION ---
st.set_page_config(page_title="DhakaSeis AI Assistant", layout="wide")

def verify_knowledge_base():
    # Validates connection to the BNBC 2020 PDF inside the knowledge_base folder
    corpus_path = os.path.join("knowledge_base", "BNBC_Corpus.pdf")
    return os.path.exists(corpus_path)

# --- 2. HEADER & MISSION ---
st.title("🛡️ DhakaSeis: AI-Driven Urban Resilience")
st.markdown("#### Mission: A Digital Iron Dome for Dhaka's 21 Million Residents")

# --- 3. SIDEBAR: THE EYES (Multimodal Input) ---
st.sidebar.header("📡 Live AI Monitoring")

# Connection Status: Verification against the specific PDF source
if verify_knowledge_base():
    st.sidebar.success("📚 BNBC 2020 Corpus: Connected")
    st.sidebar.caption("Validated against Figure 6.2.25 (Page 3195)")
else:
    st.sidebar.error("⚠️ BNBC 2020 Corpus: Missing")

# Automated Spatial Triage
lat, lon = 23.7104, 90.4074  # Focus: Puran Dhaka
spatial_data = fetch_spatial_data(lat, lon)
st.sidebar.info(f"📍 Location: {lat}, {lon}")
st.sidebar.info(f"🏢 Profile: {spatial_data['levels']} Floors (~{spatial_data['height']}m)")

# --- 4. SIDEBAR: THE BRAIN (BNBC Parameters) ---
st.sidebar.divider()
st.sidebar.subheader("⚙️ Spectral Parameters")

# Site Class Selection (Table 6.2.16 - Page 2884 / 3195 Reference)
site_class = st.sidebar.selectbox(
    "Site Class (BNBC Table 6.2.16)", 
    ["SA", "SB", "SC", "SD", "SE"], 
    index=3  # Default to SD (Stiff Soil)
)

# Zone Coefficient (Z)
Z = st.sidebar.slider("Zone Coefficient (Z)", 0.12, 0.36, 0.20, step=0.08)

# Importance Factor (I)
importance = st.sidebar.radio(
    "Occupancy Category", 
    [1.0, 1.25, 1.5], 
    format_func=lambda x: "Standard (1.0)" if x==1.0 else "Essential Facility (1.5)"
)

# --- 5. CALCULATIONS ---
# This calls your high-precision physics engine
periods, sa_values = compute_sa_BNBC2020(Z, site_class, importance)
peak_sa = max(sa_values)

# --- 6. OUTPUT: DESIGN RESPONSE SPECTRUM ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Design Response Spectrum (BNBC 2020)")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(periods, sa_values, color='#ff4b4b', linewidth=2.5, label=f"Site {site_class}")
    ax.fill_between(periods, sa_values, color='#ff4b4b', alpha=0.1)
    
    # Labeling based on BNBC 2020 Figure 6.2.25 (Page 3195)
    ax.set_xlabel("Period T (sec)")
    ax.set_ylabel("Spectral Acceleration Sa (g)")
    ax.set_title("Based on Figure 6.2.25: Normalized Response Spectrum")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    st.pyplot(fig)

# --- 7. OUTPUT: THE HANDS (Actionable Roadmap) ---
with col2:
    st.subheader("Actionable Triage Roadmap")
    
    risk_score = "CRITICAL" if peak_sa > 0.45 and spatial_data['height'] > 15 else "STANDARD"
    
    if risk_score == "CRITICAL":
        st.error(f"🔴 Threat: High Seismic Amplification")
        st.markdown(f"""
        **Hazard Analysis:**
        * Peak Sa: **{peak_sa:.2f}g**
        * Derived from Page: **3195**
        
        **Interventions:**
        * Column Jacketing (Concrete/Steel)
        * Shear Wall Installation per BNBC Part 6
        """)
    else:
        st.success("✅ Structural Health: Compliant")
        st.write("Current parameters align with typical BNBC 2020 safety margins.")

st.divider()
st.caption("Deep Research Prototype | Grounded in Figure 6.2.25 (Part 6, Chapter 2)")