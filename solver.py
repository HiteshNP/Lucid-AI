import streamlit as st
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import google.generativeai as genai
from PIL import Image
import base64
from io import BytesIO

# Configure Streamlit - this must be the first Streamlit command
st.set_page_config(layout="wide", page_title="Lucid-AI Math Solver")

# Custom CSS for dark mode
st.markdown("""
<style>
    .main {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .logo-title {
        text-align: center;
        padding: 2rem 0;
        background-color: #2D2D2D;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 2rem;
    }
    .content-section {
        background-color: #2D2D2D;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .answer-box {
        border: 1px solid #444444;
        border-radius: 5px;
        padding: 1rem;
        background-color: #363636;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF;
    }
    .stCheckbox {
        color: #FFFFFF;
    }
    .stMarkdown {
        color: #CCCCCC;
    }
</style>
""", unsafe_allow_html=True)

# Load and resize the logo image
logo = Image.open('Lucid_logo.png')
logo = logo.resize((150, 150))

# Convert logo to base64
buffered = BytesIO()
logo.save(buffered, format="PNG")
img_str = base64.b64encode(buffered.getvalue()).decode()

# Logo and title section
st.markdown(
    f"""
    <div class="logo-title">
        <img src="data:image/png;base64,{img_str}" width="150" height="150">
        <h1>Lucid-AI Math Solver</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Main content
st.markdown('<div class="content-section">', unsafe_allow_html=True)
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Live Camera Feed")
    run = st.checkbox('Activate Camera', value=False)
    FRAME_WINDOW = st.empty()

with col2:
    st.subheader("Math Problem Solution")
    output_text_area = st.empty()

st.markdown('</div>', unsafe_allow_html=True)

# Instructions
st.markdown('<div class="content-section">', unsafe_allow_html=True)
st.subheader("How to Use")
st.markdown("""
1. Activate the camera using the checkbox above.
2. Use your index finger to draw the math problem on the screen.
3. Show all five fingers to clear the drawing area.
4. Give a thumbs up to send the problem for solving.
5. The solution will appear in the 'Math Problem Solution' box.
""")
st.markdown('</div>', unsafe_allow_html=True)

# AI model configuration
genai.configure(api_key="AIzaSyDsH5N_thLzQY8XCrP-D37heC3boDfNXCY")  # Replace with your actual API key
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize the webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Initialize the HandDetector
detector = HandDetector(staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.7, minTrackCon=0.5)

def getHandInfo(img):
    if img is None:
        return None, None
    hands, img = detector.findHands(img, draw=False, flipType=True)
    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        fingers = detector.fingersUp(hand)
        return fingers, lmList
    else:
        return None, None

def draw(info, prev_pos, canvas):
    fingers, lmList = info
    current_pos = None
    if fingers == [0, 1, 0, 0, 0]:
        current_pos = lmList[8][0:2]
        if prev_pos is None:
            prev_pos = current_pos
        cv2.line(canvas, current_pos, prev_pos, (255, 0, 255), 10)
    elif fingers == [1, 1, 1, 1, 1]:  # All fingers up to clear the canvas
        canvas = np.zeros_like(canvas)
    return current_pos, canvas

def sendToAI(model, canvas, fingers):
    if fingers == [1, 0, 0, 0, 0]:  # Thumbs up to send to AI
        pil_image = Image.fromarray(canvas)
        response = model.generate_content(["Solve this math problem and provide a detailed explanation", pil_image])
        return response.text
    return ""

prev_pos = None
canvas = None
output_text = ""

while run:
    success, img = cap.read()
    
    if not success or img is None:
        st.warning("Failed to capture image from camera.")
        break
    
    img = cv2.flip(img, 1)
    if canvas is None:
        canvas = np.zeros_like(img)
    
    info = getHandInfo(img)
    if info:
        fingers, lmList = info
        prev_pos, canvas = draw(info, prev_pos, canvas)
        new_output_text = sendToAI(model, canvas, fingers)
        if new_output_text:
            output_text = new_output_text
    
    image_combined = cv2.addWeighted(img, 0.7, canvas, 0.3, 0)
    FRAME_WINDOW.image(image_combined, channels="BGR")
    
    if output_text:
        output_text_area.markdown(f'<div class="answer-box">{output_text}</div>', unsafe_allow_html=True)
    
    cv2.waitKey(1)

# Release the webcam when the app is stopped
if not run:
    cap.release()