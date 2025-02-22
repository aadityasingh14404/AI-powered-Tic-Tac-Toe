import streamlit as st

# Initialize the game board
if 'board' not in st.session_state:
    st.session_state.board = [' ' for _ in range(9)]
if 'current_player' not in st.session_state:
    st.session_state.current_player = 'X'  # Human player starts

# Helper functions
def print_board(board):
    for row in [board[i*3:(i+1)*3] for i in range(3)]:
        st.write('| ' + ' | '.join(row) + ' |')

def check_winner(board, player):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    return any(board[i] == board[j] == board[k] == player for i, j, k in win_conditions)

def minimax(board, depth, is_maximizing):
    if check_winner(board, 'O'):
        return 1
    if check_winner(board, 'X'):
        return -1
    if ' ' not in board:
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

def best_move(board):
    best_score = -float('inf')
    move = 0
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    return move

# Main game loop
st.title('Tic-Tac-Toe with AI')

if st.button('Reset Game'):
    st.session_state.board = [' ' for _ in range(9)]
    st.session_state.current_player = 'X'

# Display the board
print_board(st.session_state.board)

# Handle player's move
if st.session_state.current_player == 'X':
    move = st.selectbox('Select your move (0-8)', range(9), key='player_move')
    if st.button('Make Move'):
        if st.session_state.board[move] == ' ':
            st.session_state.board[move] = 'X'
            if check_winner(st.session_state.board, 'X'):
                st.write("You win!")
                st.stop()
            elif ' ' not in st.session_state.board:
                st.write("It's a tie!")
                st.stop()
            else:
                st.session_state.current_player = 'O'

# Handle AI's move
if st.session_state.current_player == 'O':
    move = best_move(st.session_state.board)
    st.session_state.board[move] = 'O'
    if check_winner(st.session_state.board, 'O'):
        st.write("AI wins!")
        st.stop()
    elif ' ' not in st.session_state.board:
        st.write("It's a tie!")
        st.stop()
    else:
        st.session_state.current_player = 'X'

# Re-display the board after moves
print_board(st.session_state.board)
