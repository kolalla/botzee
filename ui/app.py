import streamlit as st
import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.game.scorecard import Scorecard, ScoreCategory, ScoreCalculator
from app.game.dice import DiceRoll, DiceManager
from app.game.game import GameState

st.set_page_config(page_title="Botzee - AI Yahtzee", layout="wide")

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
        st.session_state.chat_history = ["Botzee: What would you like to do next?"]
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

def display_turn_info():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### 🎯 Current Turn: **{st.session_state.current_turn}**")
    with col2:
        st.markdown(f"### 🎲 Rolls Left: **{st.session_state.rolls_left}**")

def display_dice():
    st.subheader("🎲 Current Dice Roll")
    
    if not st.session_state.current_dice:
        st.info("Click 'Roll Dice' to start your turn!")
    
    cols = st.columns(9)
    
    # Display dice with click selection
    for i in range(5):
        with cols[i]:
            if len(st.session_state.current_dice) > i:
                dice_value = st.session_state.current_dice[i]
                is_selected = i in st.session_state.selected_dice
                border_color = "#4CAF50" if is_selected else "#333"
                background_color = "#E8F5E8" if is_selected else "white"
                
                # Use checkbox for better visual feedback
                is_selected = st.checkbox(
                    f"Keep die {dice_value}", 
                    key=f"dice_{i}",
                    value=i in st.session_state.selected_dice,
                    label_visibility="hidden"
                )
                
                if is_selected and i not in st.session_state.selected_dice:
                    st.session_state.selected_dice.append(i)
                elif not is_selected and i in st.session_state.selected_dice:
                    st.session_state.selected_dice.remove(i)
                
                # Display dice with visual styling
                st.markdown(f"""
                    <div style="
                        width: 50px; 
                        height: 50px; 
                        border: 3px solid {border_color}; 
                        border-radius: 8px; 
                        display: flex; 
                        align-items: center; 
                        justify-content: center; 
                        font-size: 24px; 
                        font-weight: bold;
                        background-color: {background_color};
                        margin: 5px auto;
                        color: black;
                    ">
                        {dice_value}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="
                        width: 50px; 
                        height: 50px; 
                        border: 2px solid #ccc; 
                        border-radius: 8px; 
                        display: flex; 
                        align-items: center; 
                        justify-content: center; 
                        font-size: 24px; 
                        background-color: #f0f0f0;
                        margin: 5px;
                        color: #999;
                    ">?</div>
                """, unsafe_allow_html=True)
    
    # Action buttons
    with cols[6]:
        st.write("")  # Spacer
        
    with cols[7]:
        if not st.session_state.turn_started:
            if st.button("🎲 Roll Dice", type="primary"):
                start_turn()
        elif st.session_state.rolls_left > 0 and st.session_state.current_dice:
            if st.button("🎲 Next Roll", type="primary"):
                next_roll()
        else:
            st.button("🎲 No Rolls Left", disabled=True)
    
    with cols[8]:
        st.write("")  # Remove score turn button

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

def confirm_score_dialog(player_name, category, score, scorecard, dice_roll):
    st.session_state.confirm_score = {
        'player': player_name,
        'category': category,
        'score': score,
        'scorecard': scorecard,
        'dice_roll': dice_roll
    }

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

def display_scorecard():
    st.subheader("📊 Yahtzee Scoresheet")
    
    player1_card = st.session_state.player1_scorecard
    player2_card = st.session_state.player2_scorecard
    botzee_card = st.session_state.botzee_scorecard
    
    col1, col2, col3, col4 = st.columns([3, 1.5, 1.5, 1.5])
    
    with col1:
        st.write("**Category**")
    with col2:
        st.write("**Player 1**")
    with col3:
        st.write("**Player 2**")
    with col4:
        st.write("**Botzee**")
    
    st.divider()
    
    upper_categories = [
        ("Ones", ScoreCategory.ONES),
        ("Twos", ScoreCategory.TWOS),
        ("Threes", ScoreCategory.THREES),
        ("Fours", ScoreCategory.FOURS),
        ("Fives", ScoreCategory.FIVES),
        ("Sixes", ScoreCategory.SIXES)
    ]
    
    for name, category in upper_categories:
        col1, col2, col3, col4 = st.columns([3, 1.5, 1.5, 1.5])
        
        with col1:
            st.write(name)
        
        with col2:
            score = player1_card.get_category_score(category)
            if score is not None:
                st.write(str(score))
            elif st.session_state.current_dice and st.session_state.current_turn == "Player 1":
                dice_roll = DiceRoll(st.session_state.current_dice)
                possible_score = ScoreCalculator.calculate_score(category, dice_roll)
                if st.button(f"Score {possible_score}", key=f"p1_{category.value}"):
                    confirm_score_dialog("Player 1", category, possible_score, player1_card, dice_roll)
            else:
                st.write("—")
        
        with col3:
            score = player2_card.get_category_score(category)
            if score is not None:
                st.write(str(score))
            elif st.session_state.current_dice and st.session_state.current_turn == "Player 2":
                dice_roll = DiceRoll(st.session_state.current_dice)
                possible_score = ScoreCalculator.calculate_score(category, dice_roll)
                if st.button(f"Score {possible_score}", key=f"p2_{category.value}"):
                    confirm_score_dialog("Player 2", category, possible_score, player2_card, dice_roll)
            else:
                st.write("—")
        
        with col4:
            score = botzee_card.get_category_score(category)
            if score is not None:
                st.write(str(score))
            elif st.session_state.current_dice and st.session_state.current_turn == "Botzee":
                dice_roll = DiceRoll(st.session_state.current_dice)
                possible_score = ScoreCalculator.calculate_score(category, dice_roll)
                if st.button(f"Score {possible_score}", key=f"botzee_{category.value}"):
                    confirm_score_dialog("Botzee", category, possible_score, botzee_card, dice_roll)
            else:
                st.write("—")
    
    col1, col2, col3, col4 = st.columns([3, 1.5, 1.5, 1.5])
    with col1:
        st.write("**Upper Total**")
    with col2:
        st.write(f"**{player1_card.get_upper_section_total()}**")
    with col3:
        st.write(f"**{player2_card.get_upper_section_total()}**")
    with col4:
        st.write(f"**{botzee_card.get_upper_section_total()}**")
    
    col1, col2, col3, col4 = st.columns([3, 1.5, 1.5, 1.5])
    with col1:
        st.write("**Bonus**")
    with col2:
        st.write(f"**{player1_card.get_upper_section_bonus()}**")
    with col3:
        st.write(f"**{player2_card.get_upper_section_bonus()}**")
    with col4:
        st.write(f"**{botzee_card.get_upper_section_bonus()}**")
    
    st.divider()
    
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
        col1, col2, col3, col4 = st.columns([3, 1.5, 1.5, 1.5])
        
        with col1:
            st.write(name)
        
        with col2:
            score = player1_card.get_category_score(category)
            if score is not None:
                st.write(str(score))
            elif st.session_state.current_dice and st.session_state.current_turn == "Player 1":
                dice_roll = DiceRoll(st.session_state.current_dice)
                possible_score = ScoreCalculator.calculate_score(category, dice_roll)
                if st.button(f"Score {possible_score}", key=f"p1_{category.value}"):
                    confirm_score_dialog("Player 1", category, possible_score, player1_card, dice_roll)
            else:
                st.write("—")
        
        with col3:
            score = player2_card.get_category_score(category)
            if score is not None:
                st.write(str(score))
            elif st.session_state.current_dice and st.session_state.current_turn == "Player 2":
                dice_roll = DiceRoll(st.session_state.current_dice)
                possible_score = ScoreCalculator.calculate_score(category, dice_roll)
                if st.button(f"Score {possible_score}", key=f"p2_{category.value}"):
                    confirm_score_dialog("Player 2", category, possible_score, player2_card, dice_roll)
            else:
                st.write("—")
        
        with col4:
            score = botzee_card.get_category_score(category)
            if score is not None:
                st.write(str(score))
            elif st.session_state.current_dice and st.session_state.current_turn == "Botzee":
                dice_roll = DiceRoll(st.session_state.current_dice)
                possible_score = ScoreCalculator.calculate_score(category, dice_roll)
                if st.button(f"Score {possible_score}", key=f"botzee_{category.value}"):
                    confirm_score_dialog("Botzee", category, possible_score, botzee_card, dice_roll)
            else:
                st.write("—")
    
    col1, col2, col3, col4 = st.columns([3, 1.5, 1.5, 1.5])
    with col1:
        st.write("**Yahtzee Bonus**")
    with col2:
        st.write(f"**{player1_card.get_yahtzee_bonus_total()}**")
    with col3:
        st.write(f"**{player2_card.get_yahtzee_bonus_total()}**")
    with col4:
        st.write(f"**{botzee_card.get_yahtzee_bonus_total()}**")
    
    col1, col2, col3, col4 = st.columns([3, 1.5, 1.5, 1.5])
    with col1:
        st.write("**Lower Total**")
    with col2:
        st.write(f"**{player1_card.get_lower_section_total()}**")
    with col3:
        st.write(f"**{player2_card.get_lower_section_total()}**")
    with col4:
        st.write(f"**{botzee_card.get_lower_section_total()}**")
    
    col1, col2, col3, col4 = st.columns([3, 1.5, 1.5, 1.5])
    with col1:
        st.write("**Grand Total**")
    with col2:
        st.write(f"**{player1_card.get_grand_total()}**")
    with col3:
        st.write(f"**{player2_card.get_grand_total()}**")
    with col4:
        st.write(f"**{botzee_card.get_grand_total()}**")

def display_chat():
    st.subheader("💬 Chat with Botzee")
    
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            st.write(message)
    
    user_input = st.text_input("Your message:", key="chat_input")
    if st.button("Send") and user_input:
        st.session_state.chat_history.append(f"You: {user_input}")
        st.session_state.chat_history.append("Botzee: I'm still learning! Let me know what you'd like to do.")
        st.rerun()

def main():
    st.title("🎲 Botzee - AI Yahtzee Game")
    
    initialize_session_state()
    
    # Show confirmation dialog if needed
    if st.session_state.confirm_score:
        confirm_data = st.session_state.confirm_score
        
        st.warning(f"**Confirm Score**")
        st.write(f"Score **{confirm_data['score']}** points for **{confirm_data['category'].value.replace('_', ' ').title()}** as **{confirm_data['player']}**?")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, Score It", type="primary"):
                confirm_data['scorecard'].score_category(confirm_data['category'], confirm_data['dice_roll'])
                end_turn()
        with col2:
            if st.button("❌ No, Choose Again"):
                st.session_state.confirm_score = None
                st.rerun()
        
        st.divider()
    
    display_turn_info()
    st.divider()
    display_dice()
    st.divider()
    display_scorecard()
    st.divider()
    display_chat()

if __name__ == "__main__":
    main()
