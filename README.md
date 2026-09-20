# 🏋️ PhysiqueAI

AI-Powered Visual Body Analysis & Personalized Indian Diet Planner

## Overview

PhysiqueAI is an AI-powered fitness and nutrition application built
with Streamlit and Google Gemini.

Users can enter their personal information, upload a body image,
select their fitness goal and diet preferences, and receive an
AI-generated Indian diet plan.

## Features

- User profile input
- BMI calculation
- BMR calculation
- TDEE estimation
- AI-powered visual analysis
- Google Gemini integration
- Personalized Indian diet plans
- Multiple diet styles
- Fitness goal customization
- Dietary preference customization

## Tech Stack

- Python
- Streamlit
- Google Gemini
- Pillow
- python-dotenv

## 🚀 Installation & Setup

### 1. Clone the Repository

Clone the PhysiqueAI repository from GitHub:

**GitHub Repository:**  
https://github.com/ShivarathriKarthik/physique-ai-body-analysis

```bash
git clone https://github.com/ShivarathriKarthik/physique-ai-body-analysis.git
cd physique-ai-body-analysis
```

### 2. Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv .venv
```

#### Windows

```bash
.venv\Scripts\activate
```

#### macOS / Linux

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

> **Note:** Make sure the dependency file is named `requirements.txt`.

### 4. Configure the Gemini API Key

PhysiqueAI uses the Google Gemini API for AI-powered visual analysis and personalized diet-plan generation.

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

You can use `.env.example` as a reference.

**Important:** Never upload your `.env` file or your actual API key to GitHub.

### 5. Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

### 🔄 Application Workflow

```text
User
  ↓
Enter Height, Weight, Age & Other Details
  ↓
Select Fitness Goal
  ↓
Select Dietary Preference
  ↓
Upload Body Image
  ↓
BMI / BMR / TDEE Calculation
  ↓
Google Gemini Visual Analysis
  ↓
Personalized Fitness & Nutrition Analysis
  ↓
Select Diet Style
  ↓
Generate Personalized Indian Diet Plan
```

### 📁 Project Structure

```text
physique-ai-body-analysis/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
└── assets/
    └── screenshots/
```

### 🔐 Environment Variables

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | Google Gemini API key used for AI analysis and diet-plan generation |

### ⚠️ Security

Never commit the following files or information to GitHub:

```text
.env
API keys
Personal user images
.venv/
__pycache__/
Temporary files
```

The `.gitignore` file is configured to prevent sensitive and unnecessary files from being committed.

### 📌 Disclaimer

PhysiqueAI provides AI-generated fitness and nutrition information for educational and informational purposes only. Visual analysis is not a medical diagnosis or a clinically validated body-composition assessment. Users should consult a qualified healthcare professional or registered dietitian for personalized medical or nutritional advice.
