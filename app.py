import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# -------------------------------------------------------------------
# 1. SECURE ENVIRONMENT SETUP
# -------------------------------------------------------------------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ GEMINI_API_KEY not found! Please ensure it is defined in your local .env file.")

# -------------------------------------------------------------------
# 2. STREAMLIT FRONTEND PAGE CONFIGURATION
# -------------------------------------------------------------------
st.set_page_config(page_title="PhysiqueAI - Body Scanner & Diet Generator", layout="wide")

st.title("🏋️ PhysiqueAI: Visual Body Scanner & Diet Planner")
st.markdown("Upload a full-body photo to receive AI body composition assessments and personalized Indian diet plans.")

# -------------------------------------------------------------------
# 3. USER INPUT FORM (Model Selector, Personal Details & Preferences)
# -------------------------------------------------------------------
st.sidebar.header("⚙️ Model Configuration")
model_choice = st.sidebar.selectbox(
    "Select Gemini Model",
    ["Gemini 3.5 Flash", "Gemini 3.5 Flash-Lite"],
    help="Gemini 3.5 Flash provides maximum accuracy; 3.5 Flash-Lite offers faster, low-cost responses."
)

# Map UI label to Gemini Model API Name
model_mapping = {
    "Gemini 3.5 Flash": "gemini-3.5-flash",
    "Gemini 3.5 Flash-Lite": "gemini-3.5-flash-lite"
}
selected_model_id = model_mapping[model_choice]

st.sidebar.header("📊 Personal Details")
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
age = st.sidebar.number_input("Age (Years)", min_value=15, max_value=80, value=25)
height_cm = st.sidebar.number_input("Height (cm)", min_value=100.0, max_value=230.0, value=175.0)
weight_kg = st.sidebar.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)

activity_level = st.sidebar.selectbox(
    "Activity Level",
    [
        "Sedentary (Little or no exercise)",
        "Lightly Active (1-3 days/week)",
        "Moderately Active (3-5 days/week)",
        "Very Active (6-7 days/week)"
    ]
)

goal = st.sidebar.selectbox("Goal", ["Fat Loss (Weight Loss)", "Muscle Gain (Bulking)", "Maintenance"])
diet_type = st.sidebar.selectbox("Dietary Preference", ["Vegetarian", "Non-Vegetarian", "Eggetarian"])
region = st.sidebar.selectbox("Cuisine Style", ["South Indian", "North Indian", "General Indian"])

# -------------------------------------------------------------------
# 4. MATHEMATICAL COMPUTATIONS (BMI, BMR, TDEE & Target Calories)
# -------------------------------------------------------------------
height_m = height_cm / 100.0
bmi = weight_kg / (height_m ** 2)

# Mifflin-St Jeor Formula for BMR
if gender == "Male":
    bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
else:
    bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

# Activity Multipliers for TDEE
activity_multipliers = {
    "Sedentary (Little or no exercise)": 1.2,
    "Lightly Active (1-3 days/week)": 1.375,
    "Moderately Active (3-5 days/week)": 1.55,
    "Very Active (6-7 days/week)": 1.725
}
tdee = bmr * activity_multipliers[activity_level]

# Calorie Deficit/Surplus Calculation
if goal == "Fat Loss (Weight Loss)":
    target_calories = tdee - 400
elif goal == "Muscle Gain (Bulking)":
    target_calories = tdee + 300
else:
    target_calories = tdee

# -------------------------------------------------------------------
# 5. DASHBOARD LAYOUT: UPLOADER & METRICS DISPLAY
# -------------------------------------------------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📷 Upload Full-Body Photo")
    uploaded_file = st.file_uploader("Upload image (JPG/PNG)", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Physique Photo", use_container_width=True)

with col2:
    st.subheader("📈 Calculated Health Metrics")
    st.metric(label="BMI (Body Mass Index)", value=f"{bmi:.1f} kg/m²")
    st.metric(label="Estimated BMR (Basal Metabolism)", value=f"{int(bmr)} kcal/day")
    st.metric(label="Maintenance Calories (TDEE)", value=f"{int(tdee)} kcal/day")
    st.metric(label=f"Target Daily Calories ({goal})", value=f"{int(target_calories)} kcal/day")

# -------------------------------------------------------------------
# 6. MULTIMODAL AI VISION ANALYSIS & DIET CHART GENERATION
# -------------------------------------------------------------------
st.divider()
analyze_button = st.button("🚀 Analyze Physique & Generate Plan")

if analyze_button:
    if not api_key:
        st.error("API Key missing! Please make sure your .env file contains GEMINI_API_KEY.")
    elif uploaded_file is None:
        st.error("Please upload a full-body picture first.")
    else:
        with st.spinner(f"Analyzing physique using {model_choice}..."):
            try:
                prompt = f"""
                You are an expert sports nutritionist and AI physique analysis expert.
                Analyze the provided full-body image along with the following user metrics:
                - Gender: {gender}, Age: {age}
                - Height: {height_cm} cm, Weight: {weight_kg} kg
                - Calculated BMI: {bmi:.1f}
                - Target Daily Calories: {int(target_calories)} kcal for {goal}
                - Diet Preference: {diet_type} ({region} style)

                Provide a structured response containing:
                1. **Physique & Body Fat Assessment**:
                   - Estimated visual Body Fat percentage range based on vascularity, definition, and frame structure.
                   - Summary of muscle definition and posture.
                2. **Calorie & Macro Breakdown**:
                   - Recommended Protein (grams), Carbs (grams), and Fats (grams) to hit {int(target_calories)} kcal.
                3. **Custom 1-Day Indian Diet Plan ({diet_type} - {region})**:
                   - Breakfast (approx calories & protein)
                   - Lunch (approx calories & protein)
                   - Evening Snack (approx calories & protein)
                   - Dinner (approx calories & protein)
                4. **Actionable Training Tip**: One key tip on hydration or training to optimize progress toward the goal.
                """

                # Instantiate the selected model (gemini-3.5-flash or gemini-3.5-flash-lite)
                model = genai.GenerativeModel(selected_model_id)
                response = model.generate_content([prompt, image])

                st.success(f"Analysis Complete (Model: {model_choice})!")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"An error occurred during AI analysis: {str(e)}")