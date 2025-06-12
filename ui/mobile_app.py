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

# PWA Configuration
def add_pwa_meta():
    st.markdown("""
    <link rel="manifest" href="./manifest.json">
    <meta name="theme-color" content="#667eea">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="Botzee">
    <link rel="apple-touch-icon" href="./icon-192x192.png">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    
    <script>
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', function() {
        navigator.serviceWorker.register('./service-worker.js')
          .then(function(registration) {
            console.log('ServiceWorker registration successful');
          }, function(err) {
            console.log('ServiceWorker registration failed: ', err);
          });
      });
    }
    </script>
    """, unsafe_allow_html=True)

# Mobile-first CSS styling
def load_mobile_css():
    st.markdown("""
    <style>
    /* iPhone 14/15 specific styling - more compact */
    .main .block-container {
        max-width: 390px;
        padding: 0.25rem 0.5rem;
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
    
    /* Dice area styling - white squares with rounded edges */
    .main .block-container > div > div:first-child .stColumn:nth-child(-n+5) .stButton > button {
        height: 60px;
        min-width: 60px;
        width: 60px;
        border-radius: 8px;
        font-size: 18px;
        font-weight: bold;
        margin: 0 auto;
        border: 2px solid #333;
        background: white !important;
        color: black !important;
    }
    
    /* Selected dice (primary buttons) - green background */
    .main .block-container > div > div:first-child .stColumn:nth-child(-n+5) .stButton > button[kind="primary"] {
        background: #27ae60 !important;
        border-color: #27ae60 !important;
        color: white !important;
    }
    
    /* Unselected dice (secondary buttons) - white background with black text */  
    .main .block-container > div > div:first-child .stColumn:nth-child(-n+5) .stButton > button[kind="secondary"] {
        background: white !important;
        border-color: #333 !important;
        color: black !important;
    }
    
    /* Empty dice slots - disabled styling */
    .main .block-container > div > div:first-child .stColumn:nth-child(-n+5) .stButton > button:disabled {
        background: #f8f9fa !important;
        border-color: #ddd !important;
        color: #ccc !important;
    }
    
    .main .block-container > div > div:first-child .stColumn:nth-child(-n+5) .stButton > button:hover:not(:disabled) {
        transform: scale(1.05);
        border-width: 3px;
    }
    
    /* Score buttons in scorecard - make them compact */
    /* Target buttons that contain score_ in their key (score buttons) */
    .stButton > button[data-testid*="score"] {
        background: transparent !important;
        border: none !important;
        color: #95a5a6 !important;
        font-style: italic !important;
        border-radius: 4px !important;
        padding: 1px 4px !important;
        height: 18px !important;
        min-height: 18px !important;
        max-height: 18px !important;
        font-size: 10px !important;
        line-height: 1 !important;
        margin: 0 !important;
        width: 100% !important;
    }
    
    .stButton > button[data-testid*="score"]:hover {
        background: #f8f9fa !important;
        color: #3498db !important;
        transform: none !important;
    }
    
    /* Scorecard table styling */
    .scorecard-table {
        border-collapse: collapse;
        width: 100%;
    }
    
    .scorecard-table td {
        border-right: 1px solid #e9ecef;
        padding: 0.25rem;
        text-align: center;
    }
    
    .scorecard-table td:last-child {
        border-right: none;
    }
    
    .potential-score {
        color: #95a5a6;
        font-style: italic;
        font-weight: normal;
        cursor: pointer;
    }
    
    .potential-score:hover {
        color: #3498db;
        text-decoration: underline;
    }
    
    /* Scorecard column barriers */
    .stColumn:not(:last-child) {
        border-right: 1px solid #e9ecef;
        padding-right: 0.5rem;
    }
    
    .stColumn {
        padding-left: 0.25rem;
        padding-right: 0.25rem;
        text-align: center;
    }
    
    /* Center align all scorecard numbers */
    .stColumn p, .stColumn div {
        text-align: center;
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

def get_dice_pips(value):
    """Return HTML for dice with correct number of pips using CSS grid."""
    base_style = "width: 50px; height: 50px; border: 3px solid #333; border-radius: 8px; background: white; display: grid; margin: 0 auto; position: relative;"
    
    # Define pip patterns using CSS grid
    if value == 1:
        return f'''<div style="{base_style} place-items: center;">
                    <div style="width: 8px; height: 8px; background: #333; border-radius: 50%;"></div>
                   </div>'''
    elif value == 2:
        return f'''<div style="{base_style} grid-template-columns: 1fr 1fr; place-items: center;">
                    <div style="width: 6px; height: 6px; background: #333; border-radius: 50%; margin-top: 8px;"></div>
                    <div style="width: 6px; height: 6px; background: #333; border-radius: 50%; margin-bottom: 8px;"></div>
                   </div>'''
    elif value == 3:
        return f'''<div style="{base_style} grid-template-columns: 1fr 1fr; place-items: center;">
                    <div style="width: 6px; height: 6px; background: #333; border-radius: 50%; margin-top: 6px;"></div>
                    <div style="width: 6px; height: 6px; background: #333; border-radius: 50%;"></div>
                    <div style="width: 6px; height: 6px; background: #333; border-radius: 50%; margin-bottom: 6px;"></div>
                   </div>'''
    elif value == 4:
        return f'''<div style="{base_style} grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; place-items: center; gap: 6px; padding: 8px;">
                    <div style="width: 6px; height: 6px; background: #333; border-radius: 50%;"></div>
                    <div style="width: 6px; height: 6px; background: #333; border-radius: 50%;"></div>
                    <div style="width: 6px; height: 6px; background: #333; border-radius: 50%;"></div>
                    <div style="width: 6px; height: 6px; background: #333; border-radius: 50%;"></div>
                   </div>'''
    elif value == 5:
        return f'''<div style="{base_style} grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr 1fr; place-items: center; gap: 2px; padding: 6px;">
                    <div style="width: 5px; height: 5px; background: #333; border-radius: 50%;"></div>
                    <div style="width: 5px; height: 5px; background: #333; border-radius: 50%;"></div>
                    <div></div>
                    <div style="width: 5px; height: 5px; background: #333; border-radius: 50%; grid-column: span 2; justify-self: center;"></div>
                    <div style="width: 5px; height: 5px; background: #333; border-radius: 50%;"></div>
                    <div style="width: 5px; height: 5px; background: #333; border-radius: 50%;"></div>
                   </div>'''
    elif value == 6:
        return f'''<div style="{base_style} grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr 1fr; place-items: center; gap: 4px; padding: 6px;">
                    <div style="width: 5px; height: 5px; background: #333; border-radius: 50%;"></div>
                    <div style="width: 5px; height: 5px; background: #333; border-radius: 50%;"></div>
                    <div style="width: 5px; height: 5px; background: #333; border-radius: 50%;"></div>
                    <div style="width: 5px; height: 5px; background: #333; border-radius: 50%;"></div>
                    <div style="width: 5px; height: 5px; background: #333; border-radius: 50%;"></div>
                    <div style="width: 5px; height: 5px; background: #333; border-radius: 50%;"></div>
                   </div>'''
    else:
        # Empty dice slot styling
        empty_style = base_style.replace("border: 3px solid #333", "border: 2px solid #bdc3c7").replace("background: white", "background: #ecf0f1") + " place-items: center;"
        return f'<div style="{empty_style}"><span style="color: #95a5a6; font-size: 20px;">?</span></div>'


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

def display_mobile_header():
    # Remove the header entirely for space saving
    pass

def display_turn_info():
    # Compact turn info in a single line with buttons
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        st.write(f"**🎯 {st.session_state.current_turn}**")
    
    with col2:
        if st.session_state.rolls_left == 0 and st.session_state.current_dice:
            st.write("**Choose your score!**")
        else:
            st.write(f"**Rolls left: {st.session_state.rolls_left}**")
    
    with col3:
        if not st.session_state.turn_started:
            if st.button("🎲 Roll Dice", type="primary", use_container_width=True):
                start_turn()
        elif st.session_state.rolls_left > 0 and st.session_state.current_dice:
            if st.button("🎲 Next Roll", type="primary", use_container_width=True):
                next_roll()
        else:
            st.button("🎲 No Rolls Left", disabled=True, use_container_width=True)


def display_mobile_dice():
    # Always show 5 dice at the top, regardless of game state
    cols = st.columns(5)
    
    # Create dice as clickable buttons
    for i in range(5):
        with cols[i]:
            if st.session_state.current_dice and len(st.session_state.current_dice) > i:
                # Show actual dice with values as buttons
                dice_value = st.session_state.current_dice[i]
                is_selected = i in st.session_state.selected_dice
                
                # Create dice button with selection styling
                button_type = "primary" if is_selected else "secondary"
                button_text = str(dice_value)
                
                if st.button(button_text, key=f"dice_btn_{i}", type=button_type, use_container_width=True):
                    # Toggle selection when clicked
                    if i in st.session_state.selected_dice:
                        st.session_state.selected_dice.remove(i)
                    else:
                        st.session_state.selected_dice.append(i)
                    st.rerun()
            else:
                # Empty dice slot - show blank disabled button
                st.button("", key=f"empty_dice_{i}", disabled=True, use_container_width=True)
    

def display_mobile_scorecard():
    # Traditional Yahtzee scorecard table layout
    
    # All scorecards and player info
    scorecards = [
        ("Player 1", st.session_state.player1_scorecard, st.session_state.current_turn == "Player 1"),
        ("Player 2", st.session_state.player2_scorecard, st.session_state.current_turn == "Player 2"),
        ("Botzee", st.session_state.botzee_scorecard, st.session_state.current_turn == "Botzee")
    ]
    
    # Score categories
    upper_categories = [
        ("Ones", ScoreCategory.ONES),
        ("Twos", ScoreCategory.TWOS),
        ("Threes", ScoreCategory.THREES),
        ("Fours", ScoreCategory.FOURS),
        ("Fives", ScoreCategory.FIVES),
        ("Sixes", ScoreCategory.SIXES)
    ]
    
    lower_categories = [
        ("Three of a Kind", ScoreCategory.THREE_OF_A_KIND),
        ("Four of a Kind", ScoreCategory.FOUR_OF_A_KIND),
        ("Full House", ScoreCategory.FULL_HOUSE),
        ("Small Straight", ScoreCategory.SMALL_STRAIGHT),
        ("Large Straight", ScoreCategory.LARGE_STRAIGHT),
        ("Yahtzee", ScoreCategory.YAHTZEE),
        ("Chance", ScoreCategory.CHANCE)
    ]
    
    # Create table header
    col_score, col_p1, col_p2, col_botzee = st.columns([2, 1, 1, 1])
    
    with col_score:
        st.markdown("**Category**")
    with col_p1:
        if scorecards[0][2]:  # is current turn
            st.markdown("**🎯 Player 1**")
        else:
            st.markdown("**Player 1**")
    with col_p2:
        if scorecards[1][2]:  # is current turn
            st.markdown("**🎯 Player 2**")
        else:
            st.markdown("**Player 2**")
    with col_botzee:
        if scorecards[2][2]:  # is current turn
            st.markdown("**🎯 Botzee**")
        else:
            st.markdown("**Botzee**")
    
    st.markdown("---")
    
    # Upper section
    st.markdown("**UPPER SECTION**")
    for name, category in upper_categories:
        display_table_score_row(name, category, scorecards)
    
    # Upper totals
    st.markdown("---")
    display_table_total_row("Upper Total", "get_upper_section_total", scorecards)
    display_table_total_row("Bonus (+35)", "get_upper_section_bonus", scorecards)
    
    st.markdown("---")
    st.markdown("**LOWER SECTION**")
    
    # Lower section
    for name, category in lower_categories:
        display_table_score_row(name, category, scorecards)
    
    # Final totals
    st.markdown("---")
    display_table_total_row("Yahtzee Bonus", "get_yahtzee_bonus_total", scorecards)
    display_table_total_row("**GRAND TOTAL**", "get_grand_total", scorecards, bold=True)

def display_table_score_row(name, category, scorecards):
    """Display a table row for score categories."""
    col_score, col_p1, col_p2, col_botzee = st.columns([2, 1, 1, 1])
    
    with col_score:
        st.write(name)
    
    # For each player column
    for i, (player_name, scorecard, can_score) in enumerate(scorecards):
        col = [col_p1, col_p2, col_botzee][i]
        with col:
            score = scorecard.get_category_score(category)
            if score is not None:
                # Confirmed score - bold and normal color
                st.markdown(f"**{score}**")
            elif st.session_state.current_dice and can_score:
                # Show potential score with custom HTML button
                dice_roll = DiceRoll(st.session_state.current_dice)
                possible_score = ScoreCalculator.calculate_score(category, dice_roll)
                
                # Create unique button ID
                button_id = f"score_{player_name.replace(' ', '_')}_{category.value}"
                
                # Simple Streamlit button - we'll use CSS to make it compact
                if st.button(f"{possible_score}", key=f"score_{player_name}_{category.value}", 
                           use_container_width=True):
                    confirm_score_dialog(player_name, category, possible_score, scorecard, dice_roll)
                    st.rerun()
            else:
                # Empty cell
                st.write("")

def display_table_total_row(label, method_name, scorecards, bold=False):
    """Display a table row for totals."""
    col_score, col_p1, col_p2, col_botzee = st.columns([2, 1, 1, 1])
    
    with col_score:
        if bold:
            st.markdown(label)
        else:
            st.write(label)
    
    # For each player column
    for i, (player_name, scorecard, can_score) in enumerate(scorecards):
        col = [col_p1, col_p2, col_botzee][i]
        with col:
            total = getattr(scorecard, method_name)()
            if bold:
                st.markdown(f"**{total}**")
            else:
                st.write(f"**{total}**")

def display_compact_score_row(name, category, scorecard, can_score, player_name):
    """Display a compact score row for the three-column layout."""
    score = scorecard.get_category_score(category)
    if score is not None:
        st.write(f"{name}: **{score}**")
    elif st.session_state.current_dice and can_score:
        dice_roll = DiceRoll(st.session_state.current_dice)
        possible_score = ScoreCalculator.calculate_score(category, dice_roll)
        if st.button(f"{name}: {possible_score}", key=f"score_{player_name}_{category.value}", use_container_width=True):
            confirm_score_dialog(player_name, category, possible_score, scorecard, dice_roll)
            st.rerun()
    else:
        st.write(f"{name}: —")

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
                st.rerun()
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
    # Compact chat section without white bars
    st.markdown("💬 **Chat with Botzee**")
    
    # Show only last 2 messages compactly
    for message in st.session_state.chat_history[-2:]:
        st.write(f"*{message}*")
    
    # Compact chat input
    col1, col2 = st.columns([3, 1])
    with col1:
        user_input = st.text_input("Message:", placeholder="Ask Botzee...", label_visibility="collapsed")
    with col2:
        if st.button("Send") and user_input:
            st.session_state.chat_history.append(f"You: {user_input}")
            st.session_state.chat_history.append("Botzee: Great question! I'm learning to give better advice.")
            st.rerun()

def start_turn():
    roll_result = st.session_state.dice_manager.roll_all_dice()
    st.session_state.current_dice = roll_result.values
    st.session_state.rolls_left = 2
    st.session_state.selected_dice = []
    st.session_state.turn_started = True
    st.rerun()

def next_roll():
    if st.session_state.rolls_left > 0:
        keep_indices = st.session_state.selected_dice.copy()
        roll_result = st.session_state.dice_manager.reroll_dice(keep_indices)
        st.session_state.current_dice = roll_result.values
        st.session_state.rolls_left -= 1
        # Keep the same selected dice indices after reroll
        st.session_state.selected_dice = keep_indices
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
    # Clear scoring options when turn ends
    if 'scoring_options' in st.session_state:
        st.session_state.scoring_options = {}
    st.rerun()

def main():
    add_pwa_meta()
    load_mobile_css()
    initialize_session_state()
    
    
    # Remove header for space
    # display_mobile_header()
    
    # Show confirmation dialog if needed
    if not display_confirmation_dialog():
        display_turn_info()
        
        # Remove dividing lines for more compact layout
        display_mobile_dice()
        display_mobile_scorecard()
        display_mobile_chat()

if __name__ == "__main__":
    main()