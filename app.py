import streamlit as st
import os

# --- Configuration ---
VIDEO_FOLDER = "videos"

# --- Data: The "Database" ---
# You can move this to a json file later, but keep it here for speed.
EXERCISES = {
    "Push (Chest/Triceps)": {
        "Bench Press": {
            "video": "RDL.mov",
            "cues": [
                "Retract your scapula (pinch shoulder blades).",
                "Lower the bar to your nipple line.",
                "Drive your feet into the ground."
            ]
        },
        "Overhead Press": {
            "video": "ohp.mp4",
            "cues": [
                "Squeeze your glutes to protect your back.",
                "Move your head out of the way of the bar."
            ]
        }
    },
    "Legs (Quads/Hams)": {
        "Squat": {
            "video": "squat.mp4",
            "cues": [
                "Break at the hips and knees at the same time.",
                "Keep your chest up."
            ]
        }
    }
}

# --- The App Interface ---
st.set_page_config(page_title="My Gym Companion", page_icon="💪")

st.title("🏋️‍♀️ Let's Crush It")

# 1. Select the Workout Day
category = st.selectbox("What are we training today?", list(EXERCISES.keys()))

# 2. Select the Exercise
exercise_name = st.selectbox("Select Exercise", list(EXERCISES[category].keys()))

# Get the details
exercise_data = EXERCISES[category][exercise_name]
video_path = os.path.join(VIDEO_FOLDER, exercise_data["video"])

# 3. Display Content
st.header(exercise_name)

# Check if video exists to avoid errors
if os.path.exists(video_path):
    st.video(video_path)
else:
    st.warning(f"Video file not found: {video_path}")

# 4. Your Personal Cues
st.subheader("Your Cues:")
for cue in exercise_data["cues"]:
    st.markdown(f"- {cue}")

# Optional: Simple tracking (Session State)
if st.button(f"Completed {exercise_name} ✅"):
    st.balloons()
    st.success("Great job! Moving on...")