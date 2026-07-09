import streamlit as st
import random
import time
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
        background: linear-gradient(135deg, rgba(15,12,41,0.95), rgba(48,43,99,0.95), rgba(36,36,62,0.95)), 
                    url('https://i.imgflip.com/1h7in3.jpg') repeat;
        background-size: 400% 400%, 300px 300px;
        background-blend-mode: overlay;
        animation: gradientBG 15s ease infinite;
        color: white;
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
        padding: 2.5rem;
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
        font-size: 1.2rem !important;
        padding: 0.8rem 2rem;
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
        font-size: 1.3rem;
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
        font-size: 5.5rem;
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
        .genz-title { font-size: 3.5rem; }
        .meme-side { display: none !important; }
    }

    .genz-subtitle {
        font-size: 1.5rem;
        text-align: center;
        color: #e4e4e7 !important;
        margin-bottom: 2rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* Question styling */
    .question-text {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        line-height: 1.3;
        background: -webkit-linear-gradient(#fff, #e4e4e7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Progress */
    .brain-level {
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 1.8rem;
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
        font-size: 3.5rem;
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
    if 'current_user_input' not in st.session_state:
        st.session_state.current_user_input = ""
    if 'left_meme' not in st.session_state:
        st.session_state.left_meme = random.choice(MEMES)
    if 'right_meme' not in st.session_state:
        st.session_state.right_meme = random.choice(MEMES)

def start_game():
    st.session_state.game_state = 'playing'
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.left_meme = random.choice(MEMES)
    st.session_state.right_meme = random.choice(MEMES)
    shuffled = list(QUESTIONS)
    random.shuffle(shuffled)
    st.session_state.active_questions = shuffled

def check_answer(user_input, correct_answers):
    user_input = str(user_input).strip().lower()
    for word in correct_answers:
        if word in user_input:
            return True
    return False

def submit_answer():
    q = st.session_state.active_questions[st.session_state.current_q_idx]
    user_val = st.session_state.current_user_input
    
    is_correct = check_answer(user_val, q['accept'])
    
    st.session_state.last_answer_correct = is_correct
    st.session_state.last_answer = q['answer']
    
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
    st.session_state.last_message = f"Skipped! {random.choice(ROASTS)}"
    st.session_state.last_answer = q['answer']
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
                <span style="font-size:1.2rem; color:#a1a1aa; font-weight:800;">{idx + 1} / {total}</span>
                <span><i class="fa-solid fa-brain" style="color:#f472b6;"></i></span>
            </div>
            <div class="progress-container">
                <div class="progress-bar" style="width: {progress_pct}%;"></div>
            </div>
        """)
        
        st.html(f"<div style='text-align:right; font-weight:900; font-size:1.5rem; color:#22D3EE; margin-bottom:1rem;'><i class='fa-solid fa-fire' style='color:#f97316;'></i> Score: {score}</div>")
        
        st.html(f"""
            <div class="glass-card">
                <div class="question-text">{q['question']}</div>
            </div>
        """)
        
        st.text_input("Your Answer", key="current_user_input", placeholder="Type your answer here...", on_change=submit_answer)
        
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
    
    meme_to_show = st.session_state.left_meme if is_correct else st.session_state.right_meme
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.html(f"""
            <div class="glass-card {card_class}">
                <img src="{meme_to_show}" class="meme-image" style="max-height: 250px; width: auto; margin-bottom: 2rem;">
                <h2 style="color:{color} !important; font-size:2.5rem; font-weight:900;">{icon} {st.session_state.last_message}</h2>
                <hr style="border-color: rgba(255,255,255,0.2); margin: 2rem 0;">
                <p style="font-size:1.5rem; color:#e4e4e7;"><strong>THE TRUTH:</strong><br><br>{st.session_state.last_answer}</p>
                {motivational_text}
            </div>
        """)
        
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
        st.html('<div class="genz-title" style="font-size:4rem;">GAME OVER</div>')
        
        st.html(f"""
            <div class="glass-card" style="margin-top:2rem;">
                {confetti_html}
                <img src="{random.choice(MEMES)}" class="meme-image" style="width:60%; margin: 0 auto 2rem auto; display:block;">
                <h1 style="font-size:5rem; margin:0; font-weight:900;">{score} / {total}</h1>
                <h3 style="color:#22D3EE; font-size:2rem;">Accuracy: {pct}%</h3>
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
