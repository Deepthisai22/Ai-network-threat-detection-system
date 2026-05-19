import streamlit as st
import requests
import pandas as pd
from groq import Groq
import os
from dotenv import load_dotenv
import plotly.express as px
import time
from fpdf import FPDF

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Streamlit page settings
st.set_page_config(
    page_title="Network Traffic AI Security",
    page_icon="🚦",
    layout="wide"
)

# Main title
st.title("🚦 Network Traffic AI Security Dashboard")

st.subheader("📡 Real-Time Traffic Monitor")

traffic_placeholder = st.empty()

st.markdown("""
This AI system analyzes network traffic
and predicts whether traffic is:

- ✅ Normal
- ⚠ Abnormal / Attack
""")

# Input section
st.subheader("Enter Traffic Features")

feature_0 = st.number_input(
    "Connection Duration",
    value=0
)

feature_1 = st.number_input(
    "Protocol Type (TCP=1, UDP=2)",
    value=1
)

feature_2 = st.number_input(
    "Service Requests",
    value=20
)

feature_3 = st.number_input(
    "Login Attempts",
    value=9
)

feature_4 = st.number_input(
    "Data Packets",
    value=491
)

# Remaining features
remaining_features = [0] * 38

# Final feature list
features = [
    feature_0,
    feature_1,
    feature_2,
    feature_3,
    feature_4
] + remaining_features

# Simulated live traffic values
live_data = pd.DataFrame({
    "Time": list(range(1, 11)),
    "Traffic": [10, 15, 8, 20, 17, 30, 25, 35, 28, 40]
})

traffic_chart = px.line(
    live_data,
    x="Time",
    y="Traffic",
    title="Live Network Traffic"
)

traffic_placeholder.plotly_chart(
    traffic_chart,
    use_container_width=True
)

# Prediction button
if st.button("Predict Traffic"):

    payload = {
        "features": features
    }

    try:
        # Call FastAPI backend
        response = requests.post(
            "https://your-render-url.onrender.com/predict",
            json=payload
        )

        result = response.json()

        prediction = result["prediction"]
        confidence = result["confidence"]

        # Prediction result
        st.subheader("Prediction Result")

        if prediction == "Attack":
            st.error(f"⚠ Attack Traffic Detected ({confidence}% confidence)")
        else:
            st.success(f"✅ Normal Traffic ({confidence}% confidence)")

        # Probability Chart
        chart_df = pd.DataFrame({
            "Category": ["Prediction Confidence"],
            "Value": [confidence]
        })

        fig = px.bar(
            chart_df,
            x="Category",
            y="Value",
            title="Attack Confidence Level",
            text="Value"
        )

        st.plotly_chart(fig, use_container_width=True)

        # AI Prompt
        prompt = f"""
        The machine learning model predicted the network traffic as: {prediction}.

        Explain in beginner-friendly language:

        1. What this prediction means
        2. Why it may be dangerous
        3. Possible cybersecurity risks
        4. Recommended actions
        5. Give simple real-world explanation
        """

        # Generate AI explanation using Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile"
        )

        ai_text = chat_completion.choices[0].message.content

        # Display AI explanation
        st.subheader("🤖 AI Explanation")

        st.write(ai_text)

        # PDF Report
        pdf = FPDF()

        pdf.add_page()

        pdf.set_font("Arial", size=16)

        pdf.cell(200, 10, txt="Traffic AI Security Report", ln=True, align='C')

        pdf.ln(10)

        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt=f"Prediction: {prediction}", ln=True)

        pdf.cell(200, 10, txt=f"Confidence: {confidence}%", ln=True)

        pdf.ln(10)

        pdf.multi_cell(0, 10, txt=ai_text)

        pdf.output("traffic_report.pdf")

        with open("traffic_report.pdf", "rb") as file:
            st.download_button(
                label="📄 Download PDF Report",
                data=file,
                file_name="traffic_report.pdf",
                mime="application/pdf"
            )

        # Traffic summary table
        st.subheader("Traffic Summary")

        summary_df = pd.DataFrame({
            "Feature": [
                "Connection Duration",
                "Protocol Type",
                "Service Requests",
                "Login Attempts",
                "Data Packets"
            ],
            "Value": [
                feature_0,
                feature_1,
                feature_2,
                feature_3,
                feature_4
            ]
        })

        st.table(summary_df)

    except Exception as e:
        st.error(f"Error: {e}")

        # ==============================
# AI Chatbot Assistant
# ==============================

st.subheader("🤖 Cybersecurity AI Assistant")

user_question = st.text_input(
    "Ask anything about cybersecurity:"
)

if st.button("Ask AI Assistant"):

    if user_question:

        chat_prompt = f"""
        You are a cybersecurity expert assistant.

        Answer this user question in simple beginner-friendly language:

        Question:
        {user_question}
        """

        try:

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": chat_prompt
                    }
                ],
                model="llama-3.3-70b-versatile"
            )

            ai_answer = chat_completion.choices[0].message.content

            st.subheader("🧠 AI Response")

            st.write(ai_answer)

        except Exception as e:
            st.error(f"Error: {e}")