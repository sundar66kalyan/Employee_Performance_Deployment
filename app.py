# ==========================================================
# Employee Performance Prediction System
# ==========================================================
# IABAC Capstone Project
# Author : Kalyana Sundar
# ==========================================================

import os
import sys
import time
import joblib
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Employee Performance Prediction",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

CONFIG_FOLDER = os.path.join(PROJECT_ROOT, "config")
MODELS_FOLDER = os.path.join(PROJECT_ROOT, "models")
DATA_FOLDER = os.path.join(PROJECT_ROOT, "data", "processed")

if CONFIG_FOLDER not in sys.path:
    sys.path.append(CONFIG_FOLDER)

# ==========================================================
# Logo
# ==========================================================

# Logo path: D:\Employee_Performance_Deployment\assets\images\logo.png
logo_path = os.path.join(
    PROJECT_ROOT,
    "assets",
    "images",
    "logo.png"
)

# Check if logo exists and display it
if os.path.exists(logo_path):
    st.image(
        logo_path,
        width=180
    )
else:
    # Try alternative path without images folder
    alt_logo_path = os.path.join(
        PROJECT_ROOT,
        "assets",
        "logo.png"
    )
    if os.path.exists(alt_logo_path):
        st.image(
            alt_logo_path,
            width=180
        )
    else:
        st.warning("Logo not found. Please add logo.png to assets/images/ folder")

# ==========================================================
# Global Animated Theme (CSS + JavaScript)
# ==========================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* ---------- Keyframes ---------- */

    @keyframes fadeInUp {
        0%   { opacity: 0; transform: translateY(30px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeIn {
        0%   { opacity: 0; }
        100% { opacity: 1; }
    }

    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes pulseGlow {
        0%   { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.55); }
        70%  { box-shadow: 0 0 0 20px rgba(102, 126, 234, 0); }
        100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0); }
    }

    @keyframes floatY {
        0%   { transform: translateY(0px); }
        50%  { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }

    @keyframes shimmer {
        0%   { background-position: -500px 0; }
        100% { background-position: 500px 0; }
    }

    @keyframes popIn {
        0%   { opacity: 0; transform: scale(0.8); }
        70%  { opacity: 1; transform: scale(1.05); }
        100% { opacity: 1; transform: scale(1); }
    }

    @keyframes barFill {
        0%   { width: 0%; }
        100% { width: var(--target-width); }
    }

    @keyframes slideInLeft {
        0%   { opacity: 0; transform: translateX(-30px); }
        100% { opacity: 1; transform: translateX(0); }
    }

    @keyframes slideInRight {
        0%   { opacity: 0; transform: translateX(30px); }
        100% { opacity: 1; transform: translateX(0); }
    }

    @keyframes bounceIn {
        0%   { opacity: 0; transform: scale(0.3); }
        50%  { opacity: 1; transform: scale(1.05); }
        70%  { transform: scale(0.9); }
        100% { transform: scale(1); }
    }

    @keyframes rotateGlow {
        0%   { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    @keyframes textGlow {
        0%   { text-shadow: 0 0 10px rgba(102, 126, 234, 0.3); }
        50%  { text-shadow: 0 0 20px rgba(102, 126, 234, 0.6), 0 0 40px rgba(6, 182, 212, 0.3); }
        100% { text-shadow: 0 0 10px rgba(102, 126, 234, 0.3); }
    }

    @keyframes borderGlow {
        0%   { border-color: rgba(102, 126, 234, 0.2); }
        50%  { border-color: rgba(102, 126, 234, 0.6); }
        100% { border-color: rgba(102, 126, 234, 0.2); }
    }

    @keyframes securityShield {
        0%   { transform: scale(1); }
        50%  { transform: scale(1.1); }
        100% { transform: scale(1); }
    }

    /* ---------- Animated Hero Header ---------- */

    .hero-header {
        background: linear-gradient(270deg, #667eea, #764ba2, #06b6d4, #667eea);
        background-size: 400% 400%;
        animation: gradientShift 10s ease infinite, fadeInUp 0.8s ease;
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }

    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotateGlow 20s linear infinite;
    }

    .hero-header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: 0.5px;
        position: relative;
        z-index: 1;
    }

    .hero-header p {
        font-size: 1.1rem;
        opacity: 0.95;
        margin-top: 0.5rem;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }

    .hero-icon {
        display: inline-block;
        animation: floatY 3s ease-in-out infinite;
        font-size: 3rem;
        position: relative;
        z-index: 1;
    }

    /* ---------- Animated Metric Cards ---------- */

    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 18px;
        padding: 1.3rem 1rem;
        text-align: center;
        animation: fadeInUp 0.6s ease;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: default;
    }

    .glass-card:hover {
        transform: translateY(-8px) scale(1.03);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
        border-color: rgba(102, 126, 234, 0.5);
    }

    .glass-card .value {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #667eea, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .glass-card .label {
        font-size: 0.9rem;
        opacity: 0.8;
        margin-top: 0.3rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    /* ---------- Section fade-in wrapper ---------- */

    .fade-section {
        animation: fadeInUp 0.7s ease;
    }

    .slide-left {
        animation: slideInLeft 0.6s ease;
    }

    .slide-right {
        animation: slideInRight 0.6s ease;
    }

    /* ---------- Result badge ---------- */

    .result-badge {
        display: inline-block;
        padding: 0.6rem 1.6rem;
        border-radius: 999px;
        font-weight: 700;
        font-size: 1.1rem;
        animation: bounceIn 0.6s cubic-bezier(0.26, 1.6, 0.4, 1);
    }

    .badge-excellent {
        background: linear-gradient(90deg, #22c55e, #16a34a);
        color: white;
        animation: pulseGlow 2s ease-in-out infinite;
    }

    .badge-good {
        background: linear-gradient(90deg, #f59e0b, #d97706);
        color: white;
    }

    .badge-low {
        background: linear-gradient(90deg, #ef4444, #b91c1c);
        color: white;
        animation: pulseGlow 2s ease-in-out infinite;
    }

    /* ---------- Animated confidence bars ---------- */

    .conf-row {
        margin-bottom: 0.8rem;
        animation: fadeInUp 0.5s ease;
    }

    .conf-track {
        background: rgba(120, 120, 120, 0.15);
        border-radius: 999px;
        height: 16px;
        overflow: hidden;
        width: 100%;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }

    .conf-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #667eea, #06b6d4);
        background-size: 200% 100%;
        animation: barFill 1.2s ease forwards, shimmer 2.5s linear infinite;
        width: 0%;
        transition: width 0.5s ease;
    }

    .conf-label {
        display: flex;
        justify-content: space-between;
        font-size: 0.95rem;
        margin-bottom: 4px;
        font-weight: 500;
    }

    .conf-label span:last-child {
        font-weight: 700;
        color: #667eea;
    }

    /* ---------- Buttons ---------- */

    div.stButton > button, div.stDownloadButton > button {
        border-radius: 14px !important;
        font-weight: 700 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: none !important;
        background: linear-gradient(90deg, #667eea, #06b6d4) !important;
        color: white !important;
        padding: 0.75rem 2rem !important;
        font-size: 1.05rem !important;
        letter-spacing: 0.5px !important;
    }

    div.stButton > button:hover, div.stDownloadButton > button:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.5);
    }

    div.stButton > button:active {
        transform: scale(0.95);
    }

    /* ---------- Sidebar styling ---------- */

    section[data-testid="stSidebar"] {
        animation: fadeIn 0.6s ease;
        background: linear-gradient(180deg, #0f0c29, #302b63, #24243e);
    }

    section[data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }

    section[data-testid="stSidebar"] .stRadio label {
        font-size: 1.05rem;
        font-weight: 500;
        padding: 0.3rem 0;
    }

    section[data-testid="stSidebar"] .stRadio label:hover {
        color: #667eea !important;
        transform: translateX(5px);
        transition: all 0.2s ease;
    }

    /* ---------- Success/Warning/Error boxes ---------- */

    .stSuccess, .stWarning, .stError {
        border-radius: 12px !important;
        animation: fadeInUp 0.5s ease !important;
        border-left: 5px solid !important;
    }

    .stSuccess {
        border-left-color: #22c55e !important;
    }

    .stWarning {
        border-left-color: #f59e0b !important;
    }

    .stError {
        border-left-color: #ef4444 !important;
    }

    /* ---------- Input fields ---------- */

    .stNumberInput, .stSelectbox, .stSlider {
        animation: fadeInUp 0.5s ease;
    }

    /* ---------- Spinner ---------- */

    .stSpinner > div {
        border-color: #667eea !important;
        border-top-color: transparent !important;
        animation: rotateGlow 1s linear infinite !important;
    }

    /* ---------- Security Badge ---------- */

    .security-badge {
        display: inline-block;
        background: rgba(34, 197, 94, 0.15);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 20px;
        padding: 0.2rem 0.8rem;
        font-size: 0.7rem;
        color: #22c55e;
        animation: securityShield 3s ease-in-out infinite;
        margin-left: 0.3rem;
    }

    /* ---------- Animated Footer ---------- */

    .footer-container {
        text-align: center;
        padding: 1.5rem 0;
        animation: fadeInUp 0.8s ease;
    }

    .footer-title {
        color: #667eea;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        animation: textGlow 3s ease-in-out infinite;
    }

    .footer-name {
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0.5rem 0;
        background: linear-gradient(90deg, #667eea, #06b6d4, #764ba2);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 5s ease infinite;
    }

    .footer-role {
        font-size: 1.05rem;
        color: #888;
        margin-bottom: 1.5rem;
    }

    .footer-links {
        margin: 1.5rem 0;
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
    }

    .footer-link {
        color: #667eea;
        text-decoration: none;
        font-weight: 600;
        font-size: 1.05rem;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        animation: fadeInUp 0.6s ease;
        display: inline-block;
    }

    .footer-link:hover {
        transform: scale(1.08);
        border-color: #667eea;
        background: rgba(102, 126, 234, 0.1);
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.2);
        color: #667eea;
    }

    .footer-divider {
        max-width: 400px;
        margin: 1.5rem auto;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        animation: borderGlow 3s ease-in-out infinite;
    }

    .footer-cert {
        font-size: 1rem;
        color: #999;
        animation: textGlow 4s ease-in-out infinite;
        font-weight: 600;
        padding: 0.3rem 0;
    }

    .footer-tech {
        font-size: 0.9rem;
        color: #aaa;
        margin: 0.5rem 0;
    }

    .footer-copyright {
        font-size: 0.85rem;
        color: #777;
        margin-top: 0.5rem;
    }

    /* Animated badge for technologies */
    .tech-badge {
        display: inline-block;
        background: rgba(102, 126, 234, 0.15);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 20px;
        padding: 0.2rem 0.8rem;
        margin: 0.2rem;
        font-size: 0.8rem;
        color: #667eea;
        animation: fadeInUp 0.5s ease;
        transition: all 0.3s ease;
    }

    .tech-badge:hover {
        transform: scale(1.05);
        background: rgba(102, 126, 234, 0.25);
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.2);
    }

    /* Secure link styling */
    .secure-link {
        position: relative;
    }

    .secure-link::after {
        content: '🔒';
        font-size: 0.7rem;
        margin-left: 0.3rem;
        animation: securityShield 3s ease-in-out infinite;
    }

    </style>
    """,
    unsafe_allow_html=True
)


def glass_metric(value: str, label: str, delay: float = 0.0) -> str:
    """Return HTML for one animated glass-style metric card."""
    return f"""
    <div class="glass-card" style="animation-delay:{delay}s;">
        <div class="value">{value}</div>
        <div class="label">{label}</div>
    </div>
    """


def animated_confidence_bar(label: str, pct: float, delay: float = 0.0) -> str:
    """Return HTML for one animated, shimmering confidence bar."""
    return f"""
    <div class="conf-row" style="animation-delay:{delay}s;">
        <div class="conf-label">
            <span>{label}</span>
            <span>{pct:.1f}%</span>
        </div>
        <div class="conf-track">
            <div class="conf-fill" style="--target-width:{pct}%; animation-delay:{delay}s;"></div>
        </div>
    </div>
    """


def fire_confetti():
    """Inject a canvas-confetti burst -- used for the top-performer result."""
    st.markdown(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.2/dist/confetti.browser.min.js"></script>
        <script>
        (function() {
            const duration = 2500;
            const end = Date.now() + duration;
            (function frame() {
                confetti({ 
                    particleCount: 5, 
                    angle: 60, 
                    spread: 70, 
                    origin: { x: 0, y: 0.6 },
                    colors: ['#22c55e', '#667eea', '#06b6d4', '#f59e0b', '#ef4444']
                });
                confetti({ 
                    particleCount: 5, 
                    angle: 120, 
                    spread: 70, 
                    origin: { x: 1, y: 0.6 },
                    colors: ['#22c55e', '#667eea', '#06b6d4', '#f59e0b', '#ef4444']
                });
                if (Date.now() < end) {
                    requestAnimationFrame(frame);
                }
            })();
        })();
        </script>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# Import Project Modules
# ==========================================================

try:
    from preprocessing import (
        preprocess_employee,
        load_feature_template
    )

    st.sidebar.success("✅ Configuration Loaded")

except Exception as e:
    st.error(f"❌ Configuration Error:\n{e}")
    st.stop()

# ==========================================================
# Load Model
# ==========================================================

MODEL_PATH = os.path.join(
    MODELS_FOLDER,
    "Best_Model.pkl"
)

try:
    model = joblib.load(MODEL_PATH)
    st.sidebar.success("✅ Best Model Loaded")

except Exception as e:
    st.error(f"❌ Unable to load model:\n{e}")
    st.stop()

# ==========================================================
# Load Feature Template
# ==========================================================

try:
    feature_columns = load_feature_template()
    st.sidebar.success("✅ Feature Template Loaded")

except Exception as e:
    st.error(f"❌ Feature Template Error:\n{e}")
    st.stop()

# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.title("📊 Employee Analytics")
st.sidebar.markdown("---")

# Developer Section
st.sidebar.subheader("👨‍💻 Developer")
st.sidebar.write("**Kalyana Sundar**")
st.sidebar.write("AI Engineer | ML | Data Science")
st.sidebar.markdown("---")

# Social Links with Security Badges
st.sidebar.markdown("### 🌐 Connect")
st.sidebar.markdown(
    """
📂 **GitHub**  
https://github.com/sundar66kalyan/Employee_Performance_Deployment 🔒
"""
)
st.sidebar.markdown(
    """
💼 **LinkedIn**  
https://www.linkedin.com/in/kalyana-sundar-912403285 🔒
"""
)
st.sidebar.markdown("---")

# Navigation
page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📈 Prediction",
        "ℹ About Project"
    ]
)

# ==========================================================
# Home Page
# ==========================================================

if page == "🏠 Home":

    st.markdown(
        """
        <div class="hero-header">
            <div class="hero-icon">🏢</div>
            <h1>Employee Performance Prediction System</h1>
            <p>AI-Powered HR Analytics · IABAC Certified Data Scientist Capstone Project</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Application Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(glass_metric("1200", "Dataset Records", 0.0), unsafe_allow_html=True)
    with col2:
        st.markdown(glass_metric("28", "Features", 0.1), unsafe_allow_html=True)
    with col3:
        st.markdown(glass_metric("10", "Algorithms", 0.2), unsafe_allow_html=True)
    with col4:
        st.markdown(glass_metric("Gradient\nBoosting", "Best Model", 0.3), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # What is this app?
    st.markdown('<div class="fade-section">', unsafe_allow_html=True)
    st.subheader("🎯 What is this Application?")
    st.write("""
    This is an **AI-powered HR Analytics tool** that predicts employee performance ratings 
    using Machine Learning. It helps organizations make data-driven decisions about their 
    workforce.
    """)

    st.subheader("💡 Why Use This App?")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **For HR Managers:**
        - 🎯 Identify high-potential employees
        - 📊 Make data-driven promotion decisions
        - 🏆 Recognize top performers
        - 💰 Optimize compensation strategies
        """)
    with col2:
        st.markdown("""
        **For Business Leaders:**
        - 📈 Workforce planning
        - 🎓 Employee development programs
        - 🔄 Retention strategies
        - 📉 Performance improvement planning
        """)

    st.subheader("🚀 Key Features")
    features = [
        "✅ **Instant Predictions** - Get performance ratings in seconds",
        "✅ **Interactive Dashboard** - Visual insights at a glance",
        "✅ **Confidence Scores** - Understand prediction certainty",
        "✅ **Feature Importance** - See what drives performance",
        "✅ **HR Recommendations** - Actionable next steps",
        "✅ **Download Reports** - Export results for documentation"
    ]
    for feature in features:
        st.write(feature)

    # How to use
    st.subheader("📋 How to Use This Application")
    st.markdown("""
    **Step 1:** Navigate to the **Prediction** page using the sidebar menu

    **Step 2:** Fill in the employee information form:
    - Personal details (Age, Gender, Education, Marital Status)
    - Professional details (Department, Job Role, Experience)
    - Work parameters (Travel, Overtime, Salary Hike, etc.)

    **Step 3:** Click **✨ Predict Performance** button

    **Step 4:** Review the results:
    - 📊 **Prediction Dashboard** - Performance rating and status
    - 📈 **Confidence Score** - How certain the prediction is
    - 🎯 **Feature Importance** - What influenced the prediction
    - 💼 **HR Recommendations** - Suggested actions
    - 📄 **Download Report** - Save results for your records
    """)

    st.subheader("📊 Model Information")
    st.info(str(model))

    st.subheader("📁 Dataset Overview")
    st.write("""
    • **Records** : 1200 employees  
    • **Features** : 28 attributes  
    • **Target** : PerformanceRating (2-Needs Improvement, 3-Good, 4-Excellent)  
    • **Problem Type** : Multi-Class Classification  
    """)

    st.subheader("🧠 Algorithms Evaluated")
    algorithms = [
        "Logistic Regression", "Decision Tree", "Random Forest", 
        "Extra Trees", "AdaBoost", "Gradient Boosting", "XGBoost",
        "LightGBM", "CatBoost", "Support Vector Machine"
    ]
    for algorithm in algorithms:
        st.write(f"✅ {algorithm}")

    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# About Project
# ==========================================================

elif page == "ℹ About Project":

    st.markdown(
        """
        <div class="hero-header">
            <div class="hero-icon">📖</div>
            <h1>About This Project</h1>
            <p>Capstone Project · IABAC Certified Data Scientist</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="fade-section">', unsafe_allow_html=True)

    st.subheader("🎯 Business Problem")
    st.write("""
    Organizations struggle to objectively assess employee performance and identify 
    high-potential talent. This project uses Machine Learning to predict employee 
    performance ratings, enabling data-driven HR decisions.
    """)

    st.subheader("💼 Business Objectives")
    st.write("""
    - **Promotion Planning** - Identify candidates for advancement  
    - **Performance Monitoring** - Track and predict performance trends  
    - **Employee Development** - Design targeted training programs  
    - **Workforce Planning** - Optimize resource allocation  
    - **Retention Strategy** - Identify and retain top talent  
    """)

    st.subheader("🏆 Project Highlights")
    st.write("""
    ✔ 1200 Employee Records  
    ✔ 28 Features  
    ✔ 10 Machine Learning Algorithms  
    ✔ Hyperparameter Tuning  
    ✔ Gradient Boosting Final Model  
    ✔ Explainable AI using Feature Importance  
    ✔ 89% Model Accuracy  
    """)

    st.subheader("🔄 Machine Learning Workflow")
    st.write("""
    1. **Data Preprocessing** - Cleaning, encoding, scaling  
    2. **Exploratory Data Analysis** - Patterns, correlations, distributions  
    3. **Feature Engineering** - Creating meaningful features  
    4. **Model Training** - Evaluating 10 algorithms  
    5. **Hyperparameter Tuning** - Optimizing performance  
    6. **Model Selection** - Best performer (Gradient Boosting)  
    7. **Deployment** - Streamlit web application  
    """)

    st.subheader("🛠 Technology Stack")
    col1, col2 = st.columns(2)
    with col1:
        st.write("""
        **Data Science & ML:**
        - Python 3.9+
        - Pandas
        - NumPy
        - Scikit-Learn
        - XGBoost
        - LightGBM
        - CatBoost
        """)
    with col2:
        st.write("""
        **Web Application:**
        - Streamlit
        - Plotly
        - HTML/CSS
        - JavaScript
        - Joblib
        """)

    st.subheader("👨‍💻 Developer Information")
    st.write("**Kalyana Sundar**")
    st.write("AI Engineer | Machine Learning | Data Science")
    st.markdown("📂 **GitHub:** https://github.com/sundar66kalyan/Employee_Performance_Deployment 🔒")
    st.markdown("💼 **LinkedIn:** https://www.linkedin.com/in/kalyana-sundar-912403285 🔒")

    st.subheader("📚 References")
    st.write("""
    - IABAC Certified Data Scientist Curriculum
    - HR Analytics: Employee Performance Dataset
    - Scikit-Learn Documentation
    - Streamlit Documentation
    """)

    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# Prediction Page
# ==========================================================

elif page == "📈 Prediction":

    st.markdown(
        """
        <div class="hero-header">
            <div class="hero-icon">📈</div>
            <h1>Employee Performance Prediction</h1>
            <p>Enter employee details to get an instant performance prediction</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="fade-section">', unsafe_allow_html=True)
    st.subheader("📝 Employee Information")
    st.info("💡 Fill in all fields below. The more accurate your inputs, the better the prediction.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="slide-left">', unsafe_allow_html=True)
        age = st.number_input("📅 Age", min_value=18, max_value=60, value=30, help="Employee age in years")
        gender = st.selectbox("👤 Gender", ["Male", "Female"])
        education = st.selectbox(
            "🎓 Education Background",
            ["Life Sciences", "Medical", "Marketing", "Technical Degree",
             "Human Resources", "Other"]
        )
        marital = st.selectbox("💑 Marital Status", ["Single", "Married", "Divorced"])
        department = st.selectbox(
            "🏢 Department",
            ["Sales", "Development", "Research & Development",
             "Human Resources", "Finance", "Data Science"]
        )
        job_role = st.selectbox(
            "💼 Job Role",
            ["Sales Executive", "Developer", "Manager", "Research Scientist",
             "Laboratory Technician", "Healthcare Representative",
             "Sales Representative", "Manufacturing Director", "Human Resources"]
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="slide-right">', unsafe_allow_html=True)
        travel = st.selectbox("✈️ Business Travel", ["Travel_Rarely", "Travel_Frequently", "Non-Travel"])
        overtime = st.selectbox("⏰ OverTime", ["No", "Yes"], help="Does employee work overtime regularly?")
        attrition = st.selectbox("🔄 Attrition", ["No", "Yes"], help="Has employee considered leaving?")
        distance = st.slider("🏠 Distance From Home", 1, 30, 10, help="Distance in miles from home to office")
        salary_hike = st.slider("💰 Salary Hike %", 10, 30, 15, help="Last salary hike percentage")
        experience = st.slider("📊 Total Experience", 0, 40, 10, help="Total years of work experience")
        company_years = st.slider("🏢 Years at Company", 0, 40, 5, help="Number of years with current company")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    predict = st.button("✨ Predict Performance", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================================
    # Employee Dictionary
    # ==========================================================

    if predict:

        employee = {
            "Age": age,
            "Gender": gender,
            "EducationBackground": education,
            "MaritalStatus": marital,
            "EmpDepartment": department,
            "EmpJobRole": job_role,
            "BusinessTravelFrequency": travel,
            "DistanceFromHome": distance,
            "EmpEducationLevel": 3,
            "EmpEnvironmentSatisfaction": 3,
            "EmpHourlyRate": 60,
            "EmpJobInvolvement": 3,
            "EmpJobLevel": 2,
            "EmpJobSatisfaction": 3,
            "NumCompaniesWorked": 2,
            "OverTime": overtime,
            "EmpLastSalaryHikePercent": salary_hike,
            "EmpRelationshipSatisfaction": 3,
            "TotalWorkExperienceInYears": experience,
            "TrainingTimesLastYear": 2,
            "EmpWorkLifeBalance": 3,
            "ExperienceYearsAtThisCompany": company_years,
            "ExperienceYearsInCurrentRole": 3,
            "YearsSinceLastPromotion": 1,
            "YearsWithCurrManager": 3,
            "Attrition": attrition
        }

        # Animated processing
        with st.spinner("🧠 Analyzing employee data..."):
            employee_features = preprocess_employee(employee, feature_columns)
            time.sleep(0.8)
        
        with st.spinner("🤖 Making prediction..."):
            prediction = model.predict(employee_features)
            time.sleep(0.5)

        rating = int(prediction[0])

        # ==========================================================
        # Prediction Dashboard
        # ==========================================================

        st.markdown("---")
        st.markdown('<div class="fade-section">', unsafe_allow_html=True)
        st.header("📊 Prediction Dashboard")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("⭐ Performance Rating", rating, delta="Scale: 2-4")

        with col2:
            if rating == 4:
                st.markdown('<span class="result-badge badge-excellent">🌟 Excellent Performer</span>', unsafe_allow_html=True)
                fire_confetti()
                st.balloons()
            elif rating == 3:
                st.markdown('<span class="result-badge badge-good">👍 Good Performer</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="result-badge badge-low">⚠️ Needs Improvement</span>', unsafe_allow_html=True)

        with col3:
            st.info("🤖 Model: Gradient Boosting")

        st.markdown('</div>', unsafe_allow_html=True)

        # ==========================================================
        # Prediction Confidence (Animated Bars)
        # ==========================================================

        try:
            probability = model.predict_proba(employee_features)[0]

            st.markdown("---")
            st.markdown('<div class="fade-section">', unsafe_allow_html=True)
            st.subheader("📊 Prediction Confidence")

            st.write("""
            Below are the confidence scores for each possible performance rating. 
            Higher percentages indicate greater certainty in the prediction.
            """)

            labels = [
                "⭐ Rating 2 - Needs Improvement", 
                "⭐⭐⭐ Rating 3 - Good Performer", 
                "⭐⭐⭐⭐ Rating 4 - Excellent Performer"
            ]
            
            bars_html = ""
            for i, lbl in enumerate(labels):
                pct = round(float(probability[i]) * 100, 2)
                bars_html += animated_confidence_bar(lbl, pct, delay=i * 0.15)

            st.markdown(bars_html, unsafe_allow_html=True)

            # Add summary insight
            max_idx = probability.argmax()
            max_pct = round(float(probability[max_idx]) * 100, 2)
            rating_labels = {0: "Needs Improvement", 1: "Good Performer", 2: "Excellent Performer"}
            st.info(f"💡 **Most Likely:** {rating_labels[max_idx]} with {max_pct}% confidence")
            
            st.markdown('</div>', unsafe_allow_html=True)

        except Exception:
            st.info("ℹ️ This model does not support probability prediction.")

        # ==========================================================
        # Performance Gauge Chart
        # ==========================================================

        st.markdown("---")
        st.markdown('<div class="fade-section">', unsafe_allow_html=True)
        st.subheader("🎯 Performance Gauge")

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number+delta",
                value=rating,
                delta={
                    "reference": 3, 
                    "increasing": {"color": "#22c55e"}, 
                    "decreasing": {"color": "#ef4444"},
                    "font": {"size": 20}
                },
                number={"font": {"size": 60, "color": "#667eea"}},
                title={"text": "Performance Rating", "font": {"size": 18}},
                gauge={
                    "axis": {"range": [2, 4], "tickvals": [2, 3, 4]},
                    "bar": {"color": "#667eea", "thickness": 0.4},
                    "bgcolor": "rgba(0,0,0,0)",
                    "steps": [
                        {"range": [2, 2.5], "color": "rgba(239, 68, 68, 0.25)"},
                        {"range": [2.5, 3.5], "color": "rgba(245, 158, 11, 0.25)"},
                        {"range": [3.5, 4], "color": "rgba(34, 197, 94, 0.25)"}
                    ],
                    "threshold": {
                        "line": {"color": "#06b6d4", "width": 5},
                        "thickness": 0.85,
                        "value": rating
                    }
                }
            )
        )
        gauge.update_layout(
            transition={"duration": 1000, "easing": "elastic"},
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            height=350,
        )

        st.plotly_chart(gauge, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ==========================================================
        # Feature Importance
        # ==========================================================

        st.markdown("---")
        st.markdown('<div class="fade-section">', unsafe_allow_html=True)
        st.subheader("🔍 Top Important Features")
        
        st.write("""
        These are the most influential factors that determined the prediction. 
        Understanding these can help HR teams focus on key areas for employee development.
        """)

        importance = pd.DataFrame({
            "Feature": employee_features.columns,
            "Importance": model.feature_importances_
        })
        importance = importance.sort_values("Importance", ascending=False).head(10)

        fig_importance = px.bar(
            importance.sort_values("Importance"),
            x="Importance",
            y="Feature",
            orientation="h",
            color="Importance",
            color_continuous_scale=["#667eea", "#06b6d4"],
            title="<b>Feature Impact on Performance</b>",
            labels={"Importance": "Relative Importance", "Feature": ""}
        )
        fig_importance.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            coloraxis_showscale=False,
            transition={"duration": 800, "easing": "cubic-in-out"},
            margin=dict(l=10, r=10, t=40, b=10),
            height=400,
            xaxis=dict(showgrid=True, gridcolor="rgba(200,200,200,0.1)"),
        )
        st.plotly_chart(fig_importance, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ==========================================================
        # Employee Summary
        # ==========================================================

        st.markdown("---")
        st.markdown('<div class="fade-section">', unsafe_allow_html=True)
        st.subheader("📋 Employee Details Summary")

        summary = pd.DataFrame(employee.items(), columns=["Feature", "Value"])
        st.dataframe(
            summary, 
            use_container_width=True,
            hide_index=True,
            column_config={
                "Feature": st.column_config.TextColumn("Feature", width="medium"),
                "Value": st.column_config.TextColumn("Value", width="large")
            }
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # ==========================================================
        # HR Recommendations
        # ==========================================================

        st.markdown("---")
        st.markdown('<div class="fade-section">', unsafe_allow_html=True)
        st.subheader("💼 HR Recommendations")

        if rating == 4:
            st.success("""
            ### 🌟 Excellent Performer

            **Recommended Actions:**
            - 🎯 **Promotion Candidate** - Ready for leadership roles
            - 📈 **Leadership Development** - Invest in executive training
            - 💰 **Retention Strategy** - High priority employee to retain
            - 🏆 **Recognition Program** - Public acknowledgment and rewards
            - 📊 **Mentorship Role** - Utilize as mentor for junior staff
            """)
        elif rating == 3:
            st.warning("""
            ### 👍 Good Performer

            **Recommended Actions:**
            - 📚 **Skill Enhancement** - Identify and develop skill gaps
            - 🔄 **Quarterly Review** - Regular performance check-ins
            - 🎓 **Additional Training** - Professional development courses
            - 🚀 **Career Development** - Create growth pathway
            - 🤝 **Coaching** - Assign mentor for guidance
            """)
        else:
            st.error("""
            ### ⚠️ Needs Improvement

            **Recommended Actions:**
            - 📋 **Performance Improvement Plan** - Structured development plan
            - 👨‍🏫 **Manager Coaching** - One-on-one coaching sessions
            - 📚 **Technical Training** - Skill-specific training programs
            - 📊 **Monthly Monitoring** - Frequent performance reviews
            - 🤝 **Feedback Sessions** - Regular constructive feedback
            """)

        st.markdown('</div>', unsafe_allow_html=True)

        # ==========================================================
        # Download Report
        # ==========================================================

        st.markdown("---")
        st.markdown('<div class="fade-section">', unsafe_allow_html=True)
        st.subheader("📄 Export Report")

        report = summary.copy()
        report["Predicted Rating"] = rating
        report["Recommendation"] = "Excellent Performer" if rating == 4 else "Good Performer" if rating == 3 else "Needs Improvement"

        csv = report.to_csv(index=False)

        st.download_button(
            label="⬇️ Download Prediction Report",
            data=csv,
            file_name=f"Employee_Prediction_Report_{time.strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
            help="Download the complete prediction report as CSV for documentation"
        )
        st.caption("📌 The report includes all employee details, prediction results, and recommendations.")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# Animated Footer with Secure Links
# ==========================================================

st.markdown("---")

# Using st.columns for better control and rendering
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("### 👨‍💻 Developed By")
    st.markdown("## Kalyana Sundar")
    st.markdown("*AI Engineer | Machine Learning | Data Science*")
    
    st.markdown("---")
    
    # Create two columns for the buttons with security indicators
    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1:
        st.link_button(
            "🔗 GitHub 🔒", 
            "https://github.com/sundar66kalyan/Employee_Performance_Deployment", 
            use_container_width=True,
            help="Secure GitHub repository link"
        )
    
    with btn_col2:
        st.link_button(
            "💼 LinkedIn 🔒", 
            "https://www.linkedin.com/in/kalyana-sundar-912403285", 
            use_container_width=True,
            help="Secure LinkedIn profile link"
        )
    
    st.markdown("---")
    
    # Security notice
    st.caption("🔒 All links are secured with HTTPS encryption")
    
    # Animated certification text using markdown with HTML
    st.markdown(
        """
        <div style="text-align: center; animation: textGlow 4s ease-in-out infinite;">
            <strong style="color: #999; font-size: 1rem;">IABAC Certified Data Scientist Capstone Project</strong>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Technology badges
    st.markdown(
        """
        <div style="text-align: center; margin: 0.5rem 0;">
            <span style="display: inline-block; background: rgba(102, 126, 234, 0.15); border: 1px solid rgba(102, 126, 234, 0.3); border-radius: 20px; padding: 0.2rem 0.8rem; margin: 0.2rem; font-size: 0.8rem; color: #667eea;">Python</span>
            <span style="display: inline-block; background: rgba(102, 126, 234, 0.15); border: 1px solid rgba(102, 126, 234, 0.3); border-radius: 20px; padding: 0.2rem 0.8rem; margin: 0.2rem; font-size: 0.8rem; color: #667eea;">Scikit-Learn</span>
            <span style="display: inline-block; background: rgba(102, 126, 234, 0.15); border: 1px solid rgba(102, 126, 234, 0.3); border-radius: 20px; padding: 0.2rem 0.8rem; margin: 0.2rem; font-size: 0.8rem; color: #667eea;">Streamlit</span>
            <span style="display: inline-block; background: rgba(102, 126, 234, 0.15); border: 1px solid rgba(102, 126, 234, 0.3); border-radius: 20px; padding: 0.2rem 0.8rem; margin: 0.2rem; font-size: 0.8rem; color: #667eea;">Plotly</span>
            <span style="display: inline-block; background: rgba(102, 126, 234, 0.15); border: 1px solid rgba(102, 126, 234, 0.3); border-radius: 20px; padding: 0.2rem 0.8rem; margin: 0.2rem; font-size: 0.8rem; color: #667eea;">Gradient Boosting</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.caption("© 2026 Kalyana Sundar")