import streamlit as st
import os

# --- Configuration ---
VIDEO_FOLDER = "videos"

# --- App Config ---
st.set_page_config(
    page_title="Yingu's GYM Companion",
    page_icon="💪",
    layout="wide"  # 'wide' looks better for the grid view
)

# --- Custom Styling (The "Vibe") ---
# This CSS makes the buttons look like big, touch-friendly cards
st.markdown("""
    <style>
    div.stButton > button:first-child {
        width: 100%;
        height: 100px; /* Taller buttons for easy clicking */
        font-weight: bold;
        font-size: 20px;
        border-radius: 12px;
        border: 2px solid #f0f2f6;
        background-color: white;
        transition: transform 0.1s;
    }
    div.stButton > button:first-child:hover {
        border-color: #ff4b4b;
        color: #ff4b4b;
        background-color: #fff5f5;
    }
    div.stButton > button:first-child:active {
        transform: scale(0.98);
    }
    </style>
""", unsafe_allow_html=True)

# --- Data: The "Database" ---
EXERCISES = {
    "Leg Day 🍑": {
        "RDL": {
            "video": "RDL.mov",
            "cues": ["Hips back like a car door", "Soft knees", "Feel stretch"]
        },
    },
    "Push (Chest/Triceps)": {
        "Pec Deck Fly": {
            "video": "pec_deck.mov",
            "cues": ["保持內旋"]
        },
    },
    "Back (Pull)": {
        "Lat Pulldowns": {
            "video": "lat_pulldown.mov",
            "cues": ["捲腹力","手肘向下落","沉肩"]
        },
    }
}

# --- Session State (Memory) ---
# This allows us to "remember" which page we are on
if 'selected_day' not in st.session_state:
    st.session_state.selected_day = list(EXERCISES.keys())[0]
if 'selected_exercise' not in st.session_state:
    st.session_state.selected_exercise = None

# --- SIDEBAR (Navigation & Selfie) ---
with st.sidebar:
    # 1. Selfie Section
    # Checks if you uploaded a file named selfie.png or selfie.jpg
    if os.path.exists("selfie.png"):
        st.image("selfie.png", caption="❤️愛愛b", use_container_width=True)
    elif os.path.exists("selfie.jpg"):
        st.image("selfie.jpg", caption="❤️愛愛b", use_container_width=True)
    else:
        st.header("❤️愛愛b")
        st.caption("(Add a 'selfie.png' to the folder to see it here!)")

    st.write("---")

    # 2. Day Selector
    st.subheader("Workout Plan")
    for day in EXERCISES.keys():
        # If we click a day, reset the specific exercise view
        if st.button(day, key=f"nav_{day}", use_container_width=True):
            st.session_state.selected_day = day
            st.session_state.selected_exercise = None
            st.rerun()

# --- MAIN CONTENT AREA ---

# Logic: Are we looking at the Grid (None) or a Video (Selected)?
if st.session_state.selected_exercise is None:
    # === GRID VIEW ===
    st.title(f"📅 {st.session_state.selected_day}")
    st.write("Select an exercise to view the demo & cues:")
    st.write("")  # Spacer

    # Get exercises for current day
    day_data = EXERCISES[st.session_state.selected_day]

    # Create 3 columns for the grid
    cols = st.columns(3)

    # Loop through exercises and create buttons
    for index, (ex_name, ex_data) in enumerate(day_data.items()):
        col_index = index % 3
        with cols[col_index]:
            # The button acts as the "Card"
            if st.button(ex_name, use_container_width=True):
                st.session_state.selected_exercise = ex_name
                st.rerun()

else:
    # === DETAIL VIEW (Video Player) ===

    # 1. Back Button
    if st.button(f"← Back to {st.session_state.selected_day}"):
        st.session_state.selected_exercise = None
        st.rerun()

    # 2. Get Data
    ex_name = st.session_state.selected_exercise
    ex_data = EXERCISES[st.session_state.selected_day][ex_name]
    video_path = os.path.join(VIDEO_FOLDER, ex_data["video"])

    st.title(ex_name)

    # 3. Layout: Video on Left, Cues on Right (on large screens)
    col1, col2 = st.columns([2, 1])

    with col1:
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning(f"⚠️ Video not found: `{video_path}`")
            st.info("Tip: Add the .mp4 file to your 'videos' folder.")

    with col2:
        st.markdown("### 💡 Coach's Cues")
        for i, cue in enumerate(ex_data["cues"], 1):
            # Using success boxes makes them look like "Tips"
            st.success(f"**{i}.** {cue}")
