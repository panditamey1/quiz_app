import streamlit as st

@st.fragment
def bet_simulation():
    # Input widgets for bet parameters
    initial_bet = st.number_input("Enter your initial bet amount:", min_value=1, value=1)
    profit_target = st.number_input("Enter profit target for reset:", min_value=1, value=5)

    # Initialize session state variables if they don't exist
    if 'bet' not in st.session_state:
        st.session_state.bet = initial_bet
    if 'bankroll' not in st.session_state:
        st.session_state.bankroll = 100  # Default bankroll
    if 'starting_bankroll' not in st.session_state:
        st.session_state.starting_bankroll = st.session_state.bankroll

    # Messages to display after user interaction
    messages = []

    # Button for "Win" - simulates a win in the betting strategy
    if st.button("Win"):
        st.session_state.bankroll += st.session_state.bet
        st.session_state.bet += 1  # Increase bet by 1 unit after a win
        messages.append(f"WIN! New Bet Size: ${st.session_state.bet}")
        messages.append(f"Updated Bankroll: ${st.session_state.bankroll}")

        # Check if profit target is reached
        if st.session_state.bankroll >= st.session_state.starting_bankroll + profit_target:
            st.session_state.bet = initial_bet  # Reset bet to initial value
            st.session_state.starting_bankroll = st.session_state.bankroll  # Update starting bankroll
            messages.append(f"Profit target reached! Bet size reset to initial value: ${st.session_state.bet}")

    # Button for "Lose" - simulates a loss in the betting strategy
    if st.button("Lose"):
        st.session_state.bankroll -= st.session_state.bet
        st.session_state.bet += 2  # Increase bet by 2 units after a loss
        messages.append(f"LOSE. New Bet Size: ${st.session_state.bet}")
        messages.append(f"Updated Bankroll: ${st.session_state.bankroll}")

    # Optional Reset button to reset everything to default
    if st.button("Reset"):
        st.session_state.bet = initial_bet
        st.session_state.bankroll = 100  # Reset bankroll to default
        st.session_state.starting_bankroll = st.session_state.bankroll
        messages.append("Bet and bankroll have been reset.")
        messages.append(f"Reset Bet Size: ${st.session_state.bet}")
        messages.append(f"Reset Bankroll: ${st.session_state.bankroll}")

    # Display all messages at once to maintain alignment
    for msg in messages:
        st.write(msg)

# Call the fragment in the main app
if __name__ == "__main__":
    bet_simulation()
