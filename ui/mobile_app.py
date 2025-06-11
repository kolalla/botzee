import streamlit as st
import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.game.scorecard import Scorecard, ScoreCategory, ScoreCalculator
from app.game.dice import DiceRoll, DiceManager
from app.game.game import GameState

# Mobile-specific page config
st.set_page_config(
    page_title="Botzee - AI Yahtzee", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Mobile-first CSS styling
def load_mobile_css():
    st.markdown("""
    <style>
    /* iPhone 14/15 specific styling */
    .main .block-container {
        max-width: 390px;
        padding: 1rem 0.5rem;
        margin: 0 auto;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Mobile header */
    .mobile-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Turn info styling */
    .turn-info {
        background: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .turn-player {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2c3e50;
    }
    
    .rolls-left {
        background: #e74c3c;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
    }
    
    /* Dice container */
    .dice-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .dice-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .dice-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.25rem;
    }
    
    .die {
        width: 50px;
        height: 50px;
        border: 3px solid #333;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: bold;
        background: white;
        color: black;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .die.selected {
        border-color: #27ae60;
        background: #e8f5e8;
        transform: scale(1.05);
    }
    
    .die.empty {
        border-color: #bdc3c7;
        background: #ecf0f1;
        color: #95a5a6;
    }
    
    /* Action buttons */
    .action-buttons {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    
    /* Scorecard styling */
    .scorecard {
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .scorecard-header {
        background: #3498db;
        color: white;
        padding: 1rem;
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    .scorecard-tabs {
        display: flex;
        background: #f8f9fa;
    }
    
    .scorecard-tab {
        flex: 1;
        padding: 0.75rem;
        text-align: center;
        border: none;
        background: #f8f9fa;
        cursor: pointer;
        font-weight: bold;
        border-bottom: 3px solid transparent;
        transition: all 0.2s;
    }
    
    .scorecard-tab.active {
        background: white;
        border-bottom-color: #3498db;
        color: #3498db;
    }
    
    .score-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #ecf0f1;
    }
    
    .score-row:last-child {
        border-bottom: none;
    }
    
    .score-category {
        font-weight: 500;
        color: #2c3e50;
    }
    
    .score-value {
        font-weight: bold;
        color: #27ae60;
        min-width: 40px;
        text-align: right;
    }
    
    .score-button {
        background: #3498db;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        cursor: pointer;
        font-size: 0.9rem;
        transition: all 0.2s;
    }
    
    .score-button:hover {
        background: #2980b9;
        transform: scale(1.05);
    }
    
    .total-row {
        background: #f8f9fa;
        font-weight: bold;
        color: #2c3e50;
    }
    
    /* Confirmation dialog */
    .confirm-dialog {
        background: white;
        border: 3px solid #e74c3c;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .confirm-title {
        color: #e74c3c;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .confirm-buttons {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-top: 1rem;
    }
    
    /* Chat section */
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .chat-messages {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        max-height: 150px;
        overflow-y: auto;
        margin-bottom: 1rem;
    }
    
    /* Touch-friendly buttons */
    .stButton > button {
        height: 44px;
        border-radius: 22px;
        font-weight: bold;
        border: none;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
    }
    
    /* Responsive text */
    @media (max-width: 390px) {
        .main .block-container {
            padding: 0.5rem 0.25rem;
        }
        
        .die {
            width: 45px;
            height: 45px;
            font-size: 18px;
        }
        
        .turn-player {
            font-size: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    if 'player1_scorecard' not in st.session_state:
        st.session_state.player1_scorecard = Scorecard()
    if 'player2_scorecard' not in st.session_state:
        st.session_state.player2_scorecard = Scorecard()
    if 'botzee_scorecard' not in st.session_state:
        st.session_state.botzee_scorecard = Scorecard()
    if 'dice_manager' not in st.session_state:
        st.session_state.dice_manager = DiceManager()
    if 'current_dice' not in st.session_state:
        st.session_state.current_dice = []
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = ["Botzee: Ready to play! Tap 'Roll Dice' to start."]
    if 'current_turn' not in st.session_state:
        st.session_state.current_turn = "Player 1"
    if 'rolls_left' not in st.session_state:
        st.session_state.rolls_left = 3
    if 'selected_dice' not in st.session_state:
        st.session_state.selected_dice = []
    if 'turn_started' not in st.session_state:
        st.session_state.turn_started = False
    if 'confirm_score' not in st.session_state:
        st.session_state.confirm_score = None
    if 'active_scorecard_tab' not in st.session_state:
        st.session_state.active_scorecard_tab = "Player 1"

def display_mobile_header():
    st.markdown("""
    <div class="mobile-header">
        <h2>🎲 Botzee</h2>
        <p>AI-Powered Yahtzee</p>
    </div>
    """, unsafe_allow_html=True)

def display_turn_info():
    st.markdown(f"""
    <div class="turn-info">
        <div class="turn-player">🎯 {st.session_state.current_turn}'s Turn</div>
        <div class="rolls-left">🎲 {st.session_state.rolls_left} left</div>
    </div>
    """, unsafe_allow_html=True)

def display_mobile_dice():
    if not st.session_state.current_dice:
        st.info("👆 Tap 'Roll Dice' to start your turn!")
    
    # Dice grid
    dice_html = '<div class="dice-container"><div class="dice-grid">'
    
    for i in range(5):
        if len(st.session_state.current_dice) > i:
            dice_value = st.session_state.current_dice[i]
            is_selected = i in st.session_state.selected_dice
            selected_class = "selected" if is_selected else ""
            
            dice_html += f'''
            <div class="dice-item">
                <div class="die {selected_class}" onclick="toggleDie({i})">
                    {dice_value}
                </div>
            </div>
            '''
        else:
            dice_html += '''
            <div class="dice-item">
                <div class="die empty">?</div>
            </div>
            '''
    
    dice_html += '</div>'
    
    # Action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if not st.session_state.turn_started:
            if st.button("🎲 Roll Dice", type="primary", use_container_width=True):
                start_turn()
        elif st.session_state.rolls_left > 0 and st.session_state.current_dice:
            if st.button("🎲 Next Roll", type="primary", use_container_width=True):
                next_roll()
        else:
            st.button("🎲 No Rolls Left", disabled=True, use_container_width=True)
    
    with col2:
        if st.session_state.current_dice and st.session_state.turn_started:
            if st.button("📊 View Scores", use_container_width=True):
                st.info("👇 Tap a score below to choose!")
    
    dice_html += '</div>'
    
    # Add JavaScript for dice selection
    dice_html += f'''
    <script>
    function toggleDie(index) {{
        // This would need to be handled through Streamlit callbacks
        // For now, we'll use the checkbox approach below
    }}
    </script>
    '''
    
    st.markdown(dice_html, unsafe_allow_html=True)
    
    # Dice selection checkboxes (hidden but functional)
    if st.session_state.current_dice:
        st.write("**Keep these dice for next roll:**")
        cols = st.columns(5)
        for i, die_value in enumerate(st.session_state.current_dice):
            with cols[i]:
                is_selected = st.checkbox(
                    f"{die_value}", 
                    key=f"mobile_dice_{i}",
                    value=i in st.session_state.selected_dice
                )
                
                if is_selected and i not in st.session_state.selected_dice:
                    st.session_state.selected_dice.append(i)
                elif not is_selected and i in st.session_state.selected_dice:
                    st.session_state.selected_dice.remove(i)

def display_mobile_scorecard():
    st.markdown('<div class="scorecard">', unsafe_allow_html=True)
    st.markdown('<div class="scorecard-header">📊 Scorecard</div>', unsafe_allow_html=True)
    
    # Tabs for each player
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Player 1", key="tab_p1", use_container_width=True):
            st.session_state.active_scorecard_tab = "Player 1"
    with col2:
        if st.button("Player 2", key="tab_p2", use_container_width=True):
            st.session_state.active_scorecard_tab = "Player 2"
    with col3:
        if st.button("Botzee", key="tab_botzee", use_container_width=True):
            st.session_state.active_scorecard_tab = "Botzee"
    
    # Get the active scorecard
    if st.session_state.active_scorecard_tab == "Player 1":
        active_card = st.session_state.player1_scorecard
        can_score = st.session_state.current_turn == "Player 1"
    elif st.session_state.active_scorecard_tab == "Player 2":
        active_card = st.session_state.player2_scorecard
        can_score = st.session_state.current_turn == "Player 2"
    else:
        active_card = st.session_state.botzee_scorecard
        can_score = st.session_state.current_turn == "Botzee"
    
    st.markdown(f"### {st.session_state.active_scorecard_tab}")
    
    # Upper section
    st.markdown("**Upper Section**")
    upper_categories = [
        ("Ones", ScoreCategory.ONES),
        ("Twos", ScoreCategory.TWOS),
        ("Threes", ScoreCategory.THREES),
        ("Fours", ScoreCategory.FOURS),
        ("Fives", ScoreCategory.FIVES),
        ("Sixes", ScoreCategory.SIXES)
    ]
    
    for name, category in upper_categories:
        display_score_row(name, category, active_card, can_score)
    
    # Upper totals
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Upper Total:**")
    with col2:
        st.write(f"**{active_card.get_upper_section_total()}**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Bonus (+35):**")
    with col2:
        st.write(f"**{active_card.get_upper_section_bonus()}**")
    
    # Lower section
    st.markdown("**Lower Section**")
    lower_categories = [
        ("Three of a Kind", ScoreCategory.THREE_OF_A_KIND),
        ("Four of a Kind", ScoreCategory.FOUR_OF_A_KIND),
        ("Full House", ScoreCategory.FULL_HOUSE),
        ("Small Straight", ScoreCategory.SMALL_STRAIGHT),
        ("Large Straight", ScoreCategory.LARGE_STRAIGHT),
        ("Yahtzee", ScoreCategory.YAHTZEE),
        ("Chance", ScoreCategory.CHANCE)
    ]
    
    for name, category in lower_categories:
        display_score_row(name, category, active_card, can_score)
    
    # Final totals
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Yahtzee Bonus:**")
    with col2:
        st.write(f"**{active_card.get_yahtzee_bonus_total()}**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**GRAND TOTAL:**")
    with col2:
        st.write(f"**{active_card.get_grand_total()}**")
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_score_row(name, category, scorecard, can_score):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write(name)
    
    with col2:
        score = scorecard.get_category_score(category)
        if score is not None:
            st.write(f"**{score}**")
        elif st.session_state.current_dice and can_score:
            dice_roll = DiceRoll(st.session_state.current_dice)
            possible_score = ScoreCalculator.calculate_score(category, dice_roll)
            if st.button(f"Score {possible_score}", key=f"score_{st.session_state.active_scorecard_tab}_{category.value}", use_container_width=True):
                confirm_score_dialog(st.session_state.active_scorecard_tab, category, possible_score, scorecard, dice_roll)
        else:
            st.write("—")

def confirm_score_dialog(player_name, category, score, scorecard, dice_roll):
    st.session_state.confirm_score = {
        'player': player_name,
        'category': category,
        'score': score,
        'scorecard': scorecard,
        'dice_roll': dice_roll
    }

def display_confirmation_dialog():
    if st.session_state.confirm_score:
        confirm_data = st.session_state.confirm_score
        
        st.markdown('<div class="confirm-dialog">', unsafe_allow_html=True)
        st.markdown('<div class="confirm-title">Confirm Score</div>', unsafe_allow_html=True)
        
        st.write(f"Score **{confirm_data['score']}** points for **{confirm_data['category'].value.replace('_', ' ').title()}** as **{confirm_data['player']}**?")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, Score It", type="primary", use_container_width=True):
                confirm_data['scorecard'].score_category(confirm_data['category'], confirm_data['dice_roll'])
                end_turn()
        with col2:
            if st.button("❌ No, Choose Again", use_container_width=True):
                st.session_state.confirm_score = None
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        return True
    return False

def display_mobile_chat():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown("### 💬 Chat with Botzee")
    
    # Chat messages
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    for message in st.session_state.chat_history[-3:]:  # Show last 3 messages
        st.write(message)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.text_input("Your message:", placeholder="Ask Botzee for help...", label_visibility="collapsed")
    if st.button("Send", use_container_width=True) and user_input:
        st.session_state.chat_history.append(f"You: {user_input}")
        st.session_state.chat_history.append("Botzee: Great question! I'm learning to give better advice.")
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def start_turn():
    roll_result = st.session_state.dice_manager.roll_all_dice()
    st.session_state.current_dice = roll_result.values
    st.session_state.rolls_left = 2
    st.session_state.selected_dice = []
    st.session_state.turn_started = True
    st.rerun()

def next_roll():
    if st.session_state.rolls_left > 0:
        keep_indices = st.session_state.selected_dice
        roll_result = st.session_state.dice_manager.reroll_dice(keep_indices)
        st.session_state.current_dice = roll_result.values
        st.session_state.rolls_left -= 1
        st.session_state.selected_dice = []
        st.rerun()

def end_turn():
    turns = ["Player 1", "Player 2", "Botzee"]
    current_index = turns.index(st.session_state.current_turn)
    next_index = (current_index + 1) % len(turns)
    st.session_state.current_turn = turns[next_index]
    st.session_state.rolls_left = 3
    st.session_state.current_dice = []
    st.session_state.selected_dice = []
    st.session_state.turn_started = False
    st.session_state.confirm_score = None
    st.rerun()

def main():
    load_mobile_css()
    initialize_session_state()
    
    display_mobile_header()
    
    # Show confirmation dialog if needed
    if not display_confirmation_dialog():
        display_turn_info()
        
        st.markdown("---")
        display_mobile_dice()
        
        st.markdown("---")
        display_mobile_scorecard()
        
        st.markdown("---")
        display_mobile_chat()

if __name__ == "__main__":
    main()