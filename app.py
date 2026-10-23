import streamlit as st
import random
import time
import base64
import html
from pathlib import Path
from main import QUESTIONS

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="An IQ Too High",
    page_icon="🐦‍⬛",
    layout="wide", # changed to wide to fit side memes
    initial_sidebar_state="collapsed"
)

# AUDIO
BASE_DIR = Path(__file__).resolve().parent
CORRECT_AUDIO_DIR = BASE_DIR / "correct_audio"
INCORRECT_AUDIO_DIR = BASE_DIR / "incorrect_audio"
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a"}

def get_audio_files(directory):
    if not directory.is_dir():
        return []
    return [
        path for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS
    ]

CORRECT_AUDIO_FILES = get_audio_files(CORRECT_AUDIO_DIR)
INCORRECT_AUDIO_FILES = get_audio_files(INCORRECT_AUDIO_DIR)
FALLBACK_CORRECT_AUDIO = BASE_DIR / "i_got_this.mp3"
FALLBACK_INCORRECT_AUDIO = BASE_DIR / "fahh_sound.mp3"

def get_audio_base64(file_path):
    try:
        with file_path.open("rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            mime_type = {
                ".mp3": "audio/mpeg",
                ".wav": "audio/wav",
                ".ogg": "audio/ogg",
                ".m4a": "audio/mp4",
            }.get(file_path.suffix.lower(), "audio/mpeg")
            return f"data:{mime_type};base64,{b64}"
    except (OSError, ValueError):
        return ""

def choose_feedback_audio(is_correct):
    audio_files = CORRECT_AUDIO_FILES if is_correct else INCORRECT_AUDIO_FILES
    fallback = FALLBACK_CORRECT_AUDIO if is_correct else FALLBACK_INCORRECT_AUDIO
    if audio_files:
        return random.choice(audio_files)
    return fallback

# ==========================================
# MEME URLs
# ==========================================
MEMES = [
    "https://media.giphy.com/media/d3mlE7uhX8KFgEmY/giphy.gif", # Roll Safe
    "https://media.giphy.com/media/ne3xrYlWtQFtC/giphy.gif", # Math Lady
    "https://media.giphy.com/media/26ufdipQqU2lhNA4g/giphy.gif", # Mind Blown
    "https://media.giphy.com/media/NTur7XlVDUdqM/giphy.gif", # This is fine
    "https://media.giphy.com/media/W36QenlR6jdqQOWKrV/giphy.gif", # Woman Yelling At Cat
    "https://media.giphy.com/media/3oEjI789af0AVurF60/giphy.gif",  # Ancient Aliens
    "https://media.giphy.com/media/smW5FBep69d3q/giphy.gif",   # One Does Not Simply
    "https://media.giphy.com/media/QUY2pzDAKVpX3QacCg/giphy.gif"  # Mocking Spongebob
]

# ==========================================
# CUSTOM CSS INJECTION
# ==========================================
def inject_custom_css():
    st.html("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
    }

    /* Background Gradient with Meme overlay */
    .stApp {
        background: linear-gradient(135deg, rgba(15,12,41,0.98), rgba(48,43,99,0.97), rgba(36,36,62,0.98)),
                    url('https://i.imgflip.com/1h7in3.jpg') repeat;
        background-size: 400% 400%, 300px 300px;
        background-blend-mode: overlay;
        animation: gradientBG 15s ease infinite;
        color: white;
    }
    [data-testid="stAppViewContainer"] {
        background: rgba(8, 8, 20, 0.18);
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%, 0% 0%; }
        50% { background-position: 100% 50%, 50% 50%; }
        100% { background-position: 0% 50%, 0% 0%; }
    }

    /* Hide Streamlit elements */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    #MainMenu {visibility: hidden;}
    
    /* Global Text colors */
    p, h1, h2, h3, h4, h5, h6, label {
        color: white !important;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(20, 20, 30, 0.7);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 2px solid rgba(124, 58, 237, 0.3);
        border-radius: 30px;
        padding: clamp(1.5rem, 5vw, 2.5rem);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.6), inset 0 0 20px rgba(124, 58, 237, 0.1);
        margin-bottom: 2rem;
        text-align: center;
        transition: transform 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(34, 211, 238, 0.5);
        box-shadow: 0 15px 50px rgba(34, 211, 238, 0.2);
    }

    /* Buttons */
    div[data-testid="stButton"] button {
        background: linear-gradient(90deg, #7C3AED, #22D3EE);
        border: 2px solid transparent;
        border-radius: 24px;
        color: white;
        font-weight: 800;
        font-size: clamp(1rem, 3vw, 1.2rem) !important;
        padding: clamp(0.5rem, 2vw, 0.8rem) clamp(1rem, 4vw, 2rem);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 10px 20px rgba(124, 58, 237, 0.4);
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    div[data-testid="stButton"] button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 15px 30px rgba(34, 211, 238, 0.6);
        border: 2px solid #fff;
    }
    div[data-testid="stButton"] button:focus:not(:active) {
        color: white !important;
        background: linear-gradient(90deg, #7C3AED, #22D3EE) !important;
    }
    div[data-testid="stButton"] button p {
        font-size: clamp(1rem, 3vw, 1.3rem);
        margin: 0;
        font-weight: 800;
    }

    /* Text Input */
    div[data-testid="stTextInput"] input {
        background: rgba(0, 0, 0, 0.5) !important;
        border: 3px solid rgba(124, 58, 237, 0.5) !important;
        border-radius: 16px !important;
        color: white !important;
        padding: 1.2rem !important;
        font-size: 1.4rem !important;
        font-weight: 600;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: inset 0 4px 10px rgba(0,0,0,0.5);
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #22D3EE !important;
        background: rgba(0, 0, 0, 0.7) !important;
        box-shadow: 0 0 20px rgba(34, 211, 238, 0.6), inset 0 4px 10px rgba(0,0,0,0.5) !important;
        outline: none;
    }
    
    div[data-testid="stTextInput"] label {
        display: none;
    }

    /* Custom Text */
    .genz-title {
        font-size: clamp(2.5rem, 8vw, 5.5rem);
        font-weight: 900;
        background: -webkit-linear-gradient(45deg, #22D3EE, #7C3AED, #f472b6);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
        animation: gradientText 3s linear infinite;
        text-shadow: 0 10px 30px rgba(124,58,237,0.3);
        line-height: 1.2;
    }
    @keyframes gradientText {
      to { background-position: 200% center; }
    }
    
    @media (max-width: 800px) {
        .meme-side { display: none !important; }
        .genz-title { font-size: clamp(2rem, 10vw, 3.5rem); }
        .glass-card { margin-bottom: 1rem; }
        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
            gap: 0.75rem !important;
        }
        [data-testid="stHorizontalBlock"] > [data-testid="column"] {
            min-width: 100% !important;
            width: 100% !important;
            flex: 1 1 100% !important;
        }
        [data-testid="column"]:has(.meme-side) {
            display: none !important;
        }
        [data-testid="stRadio"] label {
            font-size: 1.2rem !important;
            line-height: 1.35 !important;
        }
        [data-testid="stRadio"] label p,
        [data-testid="stRadio"] label div {
            font-size: 1.05rem !important;
            line-height: 1.35 !important;
        }
        div[data-testid="stButton"] button {
            min-height: 3rem;
            font-size: 0.95rem !important;
            padding: 0.65rem 0.8rem;
        }
        .question-text {
            font-size: clamp(1.25rem, 6vw, 1.8rem);
            overflow-wrap: anywhere;
        }
        .meme-image {
            max-width: 100%;
            margin-top: 1rem;
        }
        .success-card,
        .shake {
            padding: 1.25rem !important;
        }
        [data-testid="stRadio"] [role="radiogroup"] {
            gap: 0.7rem;
        }
        [data-testid="stRadio"] [role="radiogroup"] > label {
            min-height: 4rem !important;
            padding: 0.7rem !important;
        }
        [data-testid="stRadio"] [role="radiogroup"] > label p,
        [data-testid="stRadio"] [role="radiogroup"] > label div,
        [data-testid="stRadio"] [role="radiogroup"] > label span {
            font-size: 1.35rem !important;
            font-weight: 700 !important;
        }
    }

    .genz-subtitle {
        font-size: clamp(1rem, 4vw, 1.5rem);
        text-align: center;
        color: #e4e4e7 !important;
        margin-bottom: 2rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* Question styling */
    .question-text {
        font-size: clamp(1.5rem, 5vw, 2.2rem);
        font-weight: 800;
        margin-bottom: 1.5rem;
        line-height: 1.3;
        background: -webkit-linear-gradient(#fff, #e4e4e7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .answer-heading {
        color: #cbd5e1 !important;
        font-size: 1.05rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        margin: 0 0 0.65rem;
        text-transform: uppercase;
    }

    [data-testid="stRadio"] label p,
    [data-testid="stRadio"] label div {
        font-size: 1.25rem !important;
        line-height: 1.45 !important;
    }

    [data-testid="stRadio"] [role="radiogroup"] {
        display: grid !important;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 1rem 1.25rem;
        width: 100%;
    }
    [data-testid="stRadio"] [role="radiogroup"] > label {
        align-items: center !important;
        background: rgba(20, 20, 30, 0.78) !important;
        border: 2px solid rgba(124, 58, 237, 0.45) !important;
        border-radius: 16px !important;
        box-sizing: border-box !important;
        color: white !important;
        cursor: pointer !important;
        display: flex !important;
        min-height: 5.25rem !important;
        padding: 0.9rem 1rem !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stRadio"] [role="radiogroup"] > label:hover {
        border-color: #22D3EE !important;
        background: rgba(34, 211, 238, 0.16) !important;
        transform: translateY(-2px);
    }
    [data-testid="stRadio"] [role="radiogroup"] > label p,
    [data-testid="stRadio"] [role="radiogroup"] > label div {
        color: white !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        line-height: 1.35 !important;
    }
    [data-testid="stRadio"] [role="radiogroup"] > label span {
        color: white !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        line-height: 1.35 !important;
    }
    .feedback-answer {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-radius: 14px;
        font-size: 1.2rem;
        margin: 1rem 0;
        padding: 1rem;
        text-align: left;
    }
    [data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked) {
        background: rgba(124, 58, 237, 0.5) !important;
        border-color: #22D3EE !important;
        box-shadow: 0 0 18px rgba(34, 211, 238, 0.35);
    }

    /* Progress */
    .brain-level {
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: clamp(1.2rem, 4vw, 1.8rem);
        margin-bottom: 8px;
        color: #fff;
    }
    .progress-container {
        width: 100%;
        background-color: rgba(0,0,0,0.4);
        border-radius: 20px;
        margin-bottom: 2rem;
        height: 16px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.5);
    }
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #7C3AED, #22D3EE, #f472b6);
        border-radius: 20px;
        transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 0 10px rgba(34, 211, 238, 0.8);
    }

    /* Feedback Animations */
    @keyframes shake {
      0% { transform: translate(2px, 2px) rotate(0deg); }
      10% { transform: translate(-2px, -4px) rotate(-2deg); }
      20% { transform: translate(-6px, 0px) rotate(2deg); }
      30% { transform: translate(6px, 4px) rotate(0deg); }
      40% { transform: translate(2px, -2px) rotate(2deg); }
      50% { transform: translate(-2px, 4px) rotate(-2deg); }
      60% { transform: translate(-6px, 2px) rotate(0deg); }
      70% { transform: translate(6px, 2px) rotate(-2deg); }
      80% { transform: translate(-2px, -2px) rotate(2deg); }
      90% { transform: translate(2px, 4px) rotate(0deg); }
      100% { transform: translate(2px, -4px) rotate(-2deg); }
    }
    .shake {
        animation: shake 0.5s;
        border: 3px solid #ef4444 !important;
        box-shadow: 0 0 40px rgba(239, 68, 68, 0.6), inset 0 0 20px rgba(239, 68, 68, 0.2) !important;
    }
    
    @keyframes popIn {
        0% { transform: scale(0.8); opacity: 0; }
        60% { transform: scale(1.1); }
        100% { transform: scale(1); opacity: 1; }
    }
    .success-card {
        border: 3px solid #22c55e !important;
        box-shadow: 0 0 40px rgba(34, 197, 94, 0.6), inset 0 0 20px rgba(34, 197, 94, 0.2) !important;
        animation: popIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    /* Rank Text */
    .rank-title {
        font-size: clamp(2rem, 6vw, 3.5rem);
        font-weight: 900;
        margin: 1.5rem 0;
        text-align: center;
        background: -webkit-linear-gradient(45deg, #f472b6, #7C3AED, #22D3EE);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientText 2s linear infinite;
    }
    
    .meme-image {
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        border: 2px solid rgba(255,255,255,0.1);
        width: 100%;
        margin-top: 2rem;
        transition: transform 0.3s ease;
    }
    .meme-image:hover {
        transform: scale(1.05) rotate(2deg);
    }

    </style>
    """)

# ==========================================
# GAME ASSETS & CONSTANTS
# ==========================================
COMPLIMENTS = [
    "Bro actually cooked <i class='fa-solid fa-fire'></i>",
    "Huge Brain Energy <i class='fa-solid fa-brain'></i>",
    "You're dangerous <i class='fa-solid fa-skull'></i>",
    "Cooked to perfection <i class='fa-solid fa-utensils'></i>",
    "W Answer <i class='fa-solid fa-crown'></i>",
    "Ain't no way you knew that <i class='fa-solid fa-bolt'></i>"
]

ROASTS = [
    "Google just unfollowed you <i class='fa-solid fa-skull-crossbones'></i>",
    "Skill issue detected <i class='fa-solid fa-robot'></i>",
    "Even my calculator knew that <i class='fa-solid fa-calculator'></i>",
    "Bro really typed that? <i class='fa-solid fa-face-sad-tear'></i>",
    "Negative aura points for this one <i class='fa-solid fa-arrow-trend-down'></i>",
    "NPC behavior confirmed <i class='fa-solid fa-user-astronaut'></i>"
]

MOTIVATIONS = [
    "You're surviving somehow.",
    "The questions are getting weirder.",
    "Still here? Respect.",
    "Halfway to losing your mind.",
    "Are you guessing? Be honest."
]

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
def init_state():
    if 'game_state' not in st.session_state:
        st.session_state.game_state = 'landing'  # landing, playing, feedback, game_over
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'current_q_idx' not in st.session_state:
        st.session_state.current_q_idx = 0
    if 'active_questions' not in st.session_state:
        st.session_state.active_questions = []
    if 'last_answer_correct' not in st.session_state:
        st.session_state.last_answer_correct = None
    if 'last_message' not in st.session_state:
        st.session_state.last_message = ""
    if 'last_answer' not in st.session_state:
        st.session_state.last_answer = ""
    if 'last_explanation' not in st.session_state:
        st.session_state.last_explanation = ""
    if 'last_selected_answer' not in st.session_state:
        st.session_state.last_selected_answer = ""
    if 'feedback_audio_path' not in st.session_state:
        st.session_state.feedback_audio_path = None
    if 'current_user_input' not in st.session_state:
        st.session_state.current_user_input = ""
    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = None
    if 'question_source' not in st.session_state:
        st.session_state.question_source = "Built-in fallback"
    if 'left_meme' not in st.session_state:
        st.session_state.left_meme = random.choice(MEMES)
    if 'right_meme' not in st.session_state:
        st.session_state.right_meme = random.choice(MEMES)

def start_game():
    st.session_state.game_state = 'playing'
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.selected_option = None
    st.session_state.left_meme = random.choice(MEMES)
    st.session_state.right_meme = random.choice(MEMES)
    st.session_state.active_questions = []
    for question in QUESTIONS:
        options = list(question["options"])
        random.shuffle(options)
        st.session_state.active_questions.append({
            "question": question["question"],
            "options": options,
            "correct_index": options.index(question["answer"]),
            "answer": question["answer"],
            "explanation": question["answer"],
        })
    random.shuffle(st.session_state.active_questions)
    st.session_state.question_source = "Hand-written questions"

def check_answer(user_input, correct_answers):
    user_input = str(user_input).strip().lower()
    for word in correct_answers:
        if word in user_input:
            return True
    return False

def submit_answer():
    q = st.session_state.active_questions[st.session_state.current_q_idx]
    selected_option = st.session_state.selected_option
    if selected_option is None:
        st.warning("Choose an option before submitting your answer.")
        return
    is_correct = bool(selected_option == q['correct_index'])
    
    st.session_state.last_answer_correct = is_correct
    st.session_state.last_selected_answer = q['options'][selected_option]
    st.session_state.last_answer = q['answer']
    st.session_state.last_explanation = q['explanation']
    st.session_state.feedback_audio_path = choose_feedback_audio(is_correct)
    
    if is_correct:
        st.session_state.score += 1
        st.session_state.last_message = random.choice(COMPLIMENTS)
    else:
        st.session_state.last_message = random.choice(ROASTS)
        
    st.session_state.game_state = 'feedback'
    st.session_state.current_user_input = ""

def skip_question():
    q = st.session_state.active_questions[st.session_state.current_q_idx]
    st.session_state.last_answer_correct = False
    st.session_state.last_selected_answer = "Skipped"
    st.session_state.last_message = f"Skipped! {random.choice(ROASTS)}"
    st.session_state.last_answer = q['answer']
    st.session_state.last_explanation = q['explanation']
    st.session_state.feedback_audio_path = choose_feedback_audio(False)
    st.session_state.game_state = 'feedback'
    st.session_state.current_user_input = ""

def next_question():
    st.session_state.current_q_idx += 1
    # Randomize memes on new question
    st.session_state.left_meme = random.choice(MEMES)
    st.session_state.right_meme = random.choice(MEMES)
    
    if st.session_state.current_q_idx >= len(st.session_state.active_questions):
        st.session_state.game_state = 'game_over'
    else:
        st.session_state.game_state = 'playing'
        st.session_state.selected_option = None

def get_rank(score, total):
    if score <= 5: return "<i class='fa-solid fa-robot'></i> Certified NPC"
    elif score <= 15: return "<i class='fa-solid fa-gem'></i> Rock Intelligence"
    elif score <= 25: return "<i class='fa-solid fa-user'></i> Average Human"
    elif score <= 35: return "<i class='fa-solid fa-brain'></i> Big Brain"
    elif score <= 45: return "<i class='fa-solid fa-crown'></i> Einstein's Cousin"
    else: return "<i class='fa-solid fa-building-shield'></i> FBI Wants To Recruit You"

# ==========================================
# UI RENDERING FUNCTIONS
# ==========================================

def render_landing():
    # Centered container
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.html('<div class="genz-title">An IQ Too High</div>')
        st.html('<div class="genz-subtitle">Think you\'re smarter than everyone? Let\'s find out.</div>')
        
        st.html(f"""
            <div class="glass-card" style="margin-top: 2rem;">
                <img src="{random.choice(MEMES)}" class="meme-image" style="width: 80%; margin: 0 auto 2rem auto; display: block;">
                <h3 style='text-align: center; font-weight: 800;'>Total Questions: {len(QUESTIONS)}</h3>
                <p style='text-align: center; color: #22D3EE !important; font-size: 1.2rem;'><em>Only 8% finish with more than 40 points.</em></p>
                <br>
        """)
        
        if st.button(":material/rocket_launch: START GAME"):
            start_game()
            st.rerun()
            
        st.html('</div>')

    # Floating Memes background effect
    st.html(f"""
        <div style="position:fixed; top:5%; left:5%; opacity:0.15; z-index:-1; animation: float 10s infinite ease-in-out;">
            <img src="{MEMES[0]}" width="200" style="border-radius:20px; transform: rotate(-15deg);">
        </div>
        <div style="position:fixed; top:60%; left:80%; opacity:0.15; z-index:-1; animation: float 12s infinite ease-in-out reverse;">
            <img src="{MEMES[1]}" width="250" style="border-radius:20px; transform: rotate(10deg);">
        </div>
        <div style="position:fixed; top:30%; left:85%; opacity:0.15; z-index:-1; animation: float 8s infinite ease-in-out;">
            <img src="{MEMES[2]}" width="180" style="border-radius:20px; transform: rotate(5deg);">
        </div>
        <div style="position:fixed; top:75%; left:10%; opacity:0.15; z-index:-1; animation: float 9s infinite ease-in-out;">
            <img src="{MEMES[3]}" width="220" style="border-radius:20px; transform: rotate(-5deg);">
        </div>
        <style>
        @keyframes float {{
            0% {{ transform: translateY(0px) scale(1); }}
            50% {{ transform: translateY(-30px) scale(1.05); }}
            100% {{ transform: translateY(0px) scale(1); }}
        }}
        </style>
    """)

def render_playing():
    idx = st.session_state.current_q_idx
    total = len(st.session_state.active_questions)
    score = st.session_state.score
    q = st.session_state.active_questions[idx]
    
    # 3 Column Layout for Memes on sides
    left_col, center_col, right_col = st.columns([1, 2.5, 1])
    
    with left_col:
        st.html(f'<div class="meme-side"><img src="{st.session_state.left_meme}" class="meme-image"></div>')
        
    with center_col:
        progress_pct = int((idx / total) * 100) if total > 0 else 0
        st.html(f"""
            <div class="brain-level">
                <span><i class="fa-solid fa-child-reaching"></i></span>
                <span style="font-size:1.2rem; color:#a1a1aa; font-weight:800;">Question {idx + 1} of {total}</span>
                <span><i class="fa-solid fa-brain" style="color:#f472b6;"></i></span>
            </div>
            <div class="progress-container">
                <div class="progress-bar" style="width: {progress_pct}%;"></div>
            </div>
        """)
        
        st.html(f"<div style='text-align:right; font-weight:900; font-size:1.5rem; color:#22D3EE; margin-bottom:1rem;'><i class='fa-solid fa-fire' style='color:#f97316;'></i> Score: {score}</div>")
        
        st.html(f"""
            <div class="glass-card">
                <div class="question-text">{html.escape(q['question'])}</div>
            </div>
        """)

        st.html("<div class='answer-heading'>Choose the best answer</div>")
        st.radio(
            "Choose the best answer:",
            range(len(q['options'])),
            format_func=lambda option_index: (
                f"{'ABCD'[option_index]}. {q['options'][option_index]}"
            ),
            key="selected_option",
            index=None,
        )
        
        st.html("<br>")
        
        c1, c2 = st.columns(2)
        with c1:
            st.button(":material/check_circle: SUBMIT", on_click=submit_answer, use_container_width=True)
        with c2:
            st.button(":material/skip_next: SKIP", on_click=skip_question, use_container_width=True)
                
        st.html("<br>")
        st.button(":material/exit_to_app: QUIT GAME", on_click=lambda: st.session_state.update(game_state='game_over'), use_container_width=True)
            
    with right_col:
        st.html(f'<div class="meme-side"><img src="{st.session_state.right_meme}" class="meme-image"></div>')

def render_feedback():
    idx = st.session_state.current_q_idx
    total = len(st.session_state.active_questions)
    
    show_motivation = (idx > 0 and (idx + 1) % 5 == 0)
    motivational_text = f"<p style='color:#a1a1aa; font-style:italic; margin-top:20px; font-size:1.3rem;'><i class='fa-solid fa-quote-left'></i> {random.choice(MOTIVATIONS)}</p>" if show_motivation else ""

    is_correct = st.session_state.last_answer_correct
    card_class = "success-card" if is_correct else "shake"
    icon = "<i class='fa-solid fa-check-circle'></i>" if is_correct else "<i class='fa-solid fa-circle-xmark'></i>"
    color = "#22c55e" if is_correct else "#ef4444"
    
    audio_src = get_audio_base64(st.session_state.feedback_audio_path)
    
    meme_to_show = st.session_state.left_meme if is_correct else st.session_state.right_meme
    
    audio_id = "feedback_audio"
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
            <audio id="{audio_id}" autoplay style="display:none;">
                <source src="{audio_src}" type="audio/mp3">
            </audio>
            <script>
                document.querySelectorAll("audio").forEach(function(existingAudio) {{
                    if (existingAudio.id !== "{audio_id}") {{
                        existingAudio.pause();
                        existingAudio.currentTime = 0;
                    }}
                }});
                var audioEl = document.getElementById("{audio_id}");
                if (audioEl) {{
                    audioEl.pause();
                    audioEl.currentTime = 0;
                    audioEl.load();
                    var playPromise = audioEl.play();
                    if (playPromise !== undefined) {{
                        playPromise.catch(function(error) {{
                            console.log("Autoplay prevented by browser:", error);
                        }});
                    }}
                }}
            </script>
            <div class="glass-card {card_class}">
                <img src="{meme_to_show}" class="meme-image" style="max-height: 250px; width: auto; margin-bottom: 2rem;">
                <h2 style="color:{color} !important; font-size:clamp(1.8rem, 5vw, 2.5rem); font-weight:900;">{icon} {st.session_state.last_message}</h2>
                <hr style="border-color: rgba(255,255,255,0.2); margin: 2rem 0;">
                <div class="feedback-answer"><strong>YOUR ANSWER</strong><br>{html.escape(st.session_state.last_selected_answer)}</div>
                <div class="feedback-answer"><strong>CORRECT ANSWER</strong><br>{html.escape(st.session_state.last_answer)}</div>
                <p style="font-size:1.1rem; color:#a1a1aa;"><strong>WHY:</strong><br>{html.escape(st.session_state.last_explanation)}</p>
                {motivational_text}
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(":material/arrow_forward: NEXT QUESTION"):
            next_question()
            st.rerun()

def render_game_over():
    score = st.session_state.score
    total = len(st.session_state.active_questions)
    pct = int((score / total) * 100) if total > 0 else 0
    rank = get_rank(score, total)
    
    confetti_html = ""
    if pct > 80:
        confetti_html = """
        <div style="text-align:center; font-size:4rem; animation: popIn 1s ease-out; margin-bottom: 1rem;">
            <i class='fa-solid fa-trophy' style="color: gold; text-shadow: 0 0 20px gold;"></i>
        </div>
        """
        st.balloons()
        
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.html('<div class="genz-title" style="font-size:clamp(3rem, 10vw, 5rem);">GAME OVER</div>')
        
        st.html(f"""
            <div class="glass-card" style="margin-top:2rem;">
                {confetti_html}
                <img src="{random.choice(MEMES)}" class="meme-image" style="width:60%; margin: 0 auto 2rem auto; display:block;">
                <h1 style="font-size:clamp(3.5rem, 12vw, 5rem); margin:0; font-weight:900;">{score} / {total}</h1>
                <h3 style="color:#22D3EE; font-size:clamp(1.5rem, 5vw, 2rem);">Accuracy: {pct}%</h3>
                <hr style="border-color:rgba(255,255,255,0.2); margin:2rem 0;">
                <p style="font-size:1.8rem; color:#a1a1aa; font-weight:800; text-transform:uppercase;">Your Rank</p>
                <div class="rank-title">{rank}</div>
            </div>
        """)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button(":material/restart_alt: RESTART"):
                start_game()
                st.rerun()
        with c2:
            if st.button(":material/home: HOME"):
                st.session_state.game_state = 'landing'
                st.rerun()

# ==========================================
# SIDEBAR
# ==========================================
def render_sidebar():
    with st.sidebar:
        st.html("<h2 style='text-align:center; font-weight:900;'><i class='fa-solid fa-chart-simple'></i> STATS</h2>")
        st.html("<hr>")
        
        if st.session_state.game_state in ['playing', 'feedback']:
            idx = st.session_state.current_q_idx
            total = len(st.session_state.active_questions)
            score = st.session_state.score
            
            st.metric("Current Score", f"{score} 🔥")
            st.metric("Questions Remaining", f"{total - idx}")
            st.metric("Total Questions", total)
            st.caption(f"Question source: {st.session_state.question_source}")
        else:
            st.write("Start a game to see stats!")
            
        st.html("<br><br><h3 style='font-weight:800;'><i class='fa-solid fa-lightbulb' style='color:#fbbf24;'></i> PRO TIPS</h3>")
        st.info("Don't overthink it. The answer is usually stupid.")
        st.info("Spelling doesn't have to be perfect, just get the keyword.")
        
        st.html("<div style='position:absolute; bottom:10px; width:100%; text-align:center; color:#a1a1aa;'><i class='fa-solid fa-code'></i> Made with bad decisions.</div>")

# ==========================================
# MAIN EXECUTION
# ==========================================
def main():
    init_state()
    inject_custom_css()
    render_sidebar()
    
    state = st.session_state.game_state
    
    if state == 'landing':
        render_landing()
    elif state == 'playing':
        render_playing()
    elif state == 'feedback':
        render_feedback()
    elif state == 'game_over':
        render_game_over()

if __name__ == "__main__":
    main()
