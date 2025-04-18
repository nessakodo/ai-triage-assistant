import streamlit as st
from datetime import datetime
from classifier import classify_symptom

st.set_page_config(page_title="CareSense – Your AI Check-In", page_icon="🩺", layout="centered")

# Improved dark mode styling
st.markdown("""
    <style>
        html, body {
            background-color: #1e1e2f;
            color: #f0f0f0;
            font-family: 'Segoe UI', sans-serif;
        }
        .title {
            color: #91cfff;
            font-size: 36px;
            font-weight: 700;
            margin-top: 10px;
        }
        .box {
            background-color: #2a2a40;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            border: 1px solid #3e3e5e;
        }
        .urgent-high {
            color: #ff6b6b;
            font-weight: bold;
        }
        .urgent-medium {
            color: #f4c430;
            font-weight: bold;
        }
        .urgent-low {
            color: #5cd85c;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='title'>CareSense – Your AI Check-In</div>", unsafe_allow_html=True)
st.markdown("Describe your symptoms below to receive a personalized urgency estimate and care recommendation.")

# Persistent session state
if "history" not in st.session_state:
    st.session_state["history"] = []

# Input
symptom_input = st.text_area("Enter your symptoms:", height=150)

# Button
if st.button("🔍 Check Urgency"):
    if symptom_input.strip():
        result = classify_symptom(symptom_input)
        timestamp = datetime.now().strftime("%b %d, %Y at %I:%M %p")

        entry = {
            "text": symptom_input.strip(),
            "time": timestamp,
            **result
        }
        st.session_state["history"].append(entry)

        # Styling
        urgency_class = {
            "High Urgency": "urgent-high",
            "Medium Urgency": "urgent-medium",
            "Low Urgency": "urgent-low"
        }[result['urgency']]

        # Output
        st.markdown(f"<div class='box'>", unsafe_allow_html=True)
        st.markdown(f"### Urgency Level: <span class='{urgency_class}'>{result['urgency']}</span> ({round(result['confidence'], 2)}%)", unsafe_allow_html=True)
        st.markdown(f"**Recommended Care:** {result['care_type']}")
        st.markdown(f"**Suggested Specialty:** {result['specialty']}")
        st.markdown(f"<small>Logged on {timestamp}</small>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Recurring symptom detection
        texts = [h["text"] for h in st.session_state["history"]]
        repeated = any(texts.count(symptom_input.strip()) > 1 for h in texts)

        if repeated:
            st.warning("CareSense Insight: You've logged this symptom multiple times. If it's persisting, consider seeking medical advice.")

    else:
        st.warning("Please enter a symptom description.")

# Show history
if st.session_state["history"]:
    st.markdown("---")
    st.subheader("Previous Check-Ins")
    for i, h in enumerate(reversed(st.session_state["history"][-5:]), 1):
        color = {
            "High Urgency": "#ff6b6b",
            "Medium Urgency": "#f4c430",
            "Low Urgency": "#5cd85c"
        }[h['urgency']]
        st.markdown(f"""
            <div style='background-color:#262639;padding:15px;margin:10px 0;border-left: 5px solid {color};border-radius:5px;'>
                <strong>{h["time"]}</strong><br>
                <em>{h["text"]}</em><br>
                Urgency: <span style='color:{color};font-weight:bold'>{h["urgency"]}</span>
            </div>
        """, unsafe_allow_html=True)

# Disclaimer
st.markdown("""---  
*Disclaimer: This tool is for educational and experimental purposes only. It is not a substitute for professional medical advice. Always consult a licensed physician.*
""")
