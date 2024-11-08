import streamlit as st

# Streamlit app configuration
st.title("Roulette Bet Strategy Simulation")
st.write("This app helps simulate the next bet size based on wins or losses.")

# Input for initial bet size
initial_bet = st.number_input("Enter your initial bet amount:", min_value=1, value=1)
if 'bet' not in st.session_state:
    st.session_state.bet = initial_bet

if 'bankroll' not in st.session_state:
    st.session_state.bankroll = 100  # Default bankroll, can be changed

# Display current state
st.write(f"Current Bet Size: ${st.session_state.bet}")
st.write(f"Current Bankroll: ${st.session_state.bankroll}")

# Buttons for "Win" and "Lose" outcomes
if st.button("Win"):
    st.session_state.bankroll += st.session_state.bet
    st.session_state.bet += 1  # Increase bet by 1 unit after a win
    st.write(f"WIN! New Bet Size: ${st.session_state.bet}")
    st.write(f"Updated Bankroll: ${st.session_state.bankroll}")

if st.button("Lose"):
    st.session_state.bankroll -= st.session_state.bet
    st.session_state.bet += 2  # Increase bet by 2 units after a loss
    st.write(f"LOSE. New Bet Size: ${st.session_state.bet}")
    st.write(f"Updated Bankroll: ${st.session_state.bankroll}")

# Reset button (optional)
if st.button("Reset"):
    st.session_state.bet = initial_bet
    st.session_state.bankroll = 100  # Reset to default value
    st.write("Bet and bankroll have been reset.")
    st.write(f"Reset Bet Size: ${st.session_state.bet}")
    st.write(f"Reset Bankroll: ${st.session_state.bankroll}")
