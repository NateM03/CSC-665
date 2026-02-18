# coinline.py

class State:
    def __init__(self, coins, pScore=0, aiScore=0, turn='player'): 
        self.coins = coins
        self.pScore = pScore
        self.aiScore = aiScore
        self.turn = turn


"""
Returns which player (either you or AI) who has the next turn.

In the initial game state, you (i.e. 'player') gets to pick first. 
Subsequently, the players alternate with each additional move.

If there no coins left, any return value is acceptable.
"""
# ========== IMPLEMENTED: Problem II, Part 1, Question 1 ==========
def player(state):
    return state.turn


"""
Returns the set of all possible actions available on the line of coins.

The actions function should return a list of all the possible actions that can be taken given a state.

Each action should be represented as a tuple (i, j) where i corresponds to the side of the line ('L', 'R')
and j corresponds to the number of coins to be picked (1, 2).

Possible moves depend on the numner of coins left.

Any return value is acceptable if there are no coins left.
"""
# ========== IMPLEMENTED: Problem II, Part 1, Question 2 ==========
def actions(state):
    if len(state.coins) == 0:
        return []
    
    possible_actions = []
    
    # Actions from the left side
    if len(state.coins) >= 1:
        possible_actions.append(('L', 1))
    if len(state.coins) >= 2:
        possible_actions.append(('L', 2))
    
    # Actions from the right side
    if len(state.coins) >= 1:
        possible_actions.append(('R', 1))
    if len(state.coins) >= 2:
        possible_actions.append(('R', 2))
    
    return possible_actions

"""
Returns the line of coins that results from taking action (i, j), without modifying the 
original coins' lineup.

If `action` is not a valid action for the board, you  should raise an exception.

The returned state should be the line of coins and scores that would result from taking the 
original input state, and letting the player whose turn it is pick the coin(s) indicated by the 
input action.

Importantly, the original state should be left unmodified. This means that simply updating the 
input state itself is not a correct implementation of this function. You'll likely want to make a 
deep copy of the state first before making any changes.
"""
# ========== IMPLEMENTED: Problem II, Part 1, Question 3 ==========
def succ(state, action):
    import copy
    
    # Create a deep copy of the state to avoid modifying the original
    new_state = copy.deepcopy(state)
    
    side, num_coins = action
    
    # Validate action
    if len(new_state.coins) < num_coins:
        raise ValueError(f"Cannot take {num_coins} coins when only {len(new_state.coins)} coins remain")
    
    if side not in ['L', 'R']:
        raise ValueError(f"Invalid side: {side}. Must be 'L' or 'R'")
    
    if num_coins not in [1, 2]:
        raise ValueError(f"Invalid number of coins: {num_coins}. Must be 1 or 2")
    
    # Calculate the value of coins to be taken
    if side == 'L':
        coins_taken = new_state.coins[:num_coins]
        new_state.coins = new_state.coins[num_coins:]
    else:  # side == 'R'
        coins_taken = new_state.coins[-num_coins:]
        new_state.coins = new_state.coins[:-num_coins]
    
    total_value = sum(coins_taken)
    
    # Add value to the appropriate player's score and switch turns
    if new_state.turn == 'player':
        new_state.pScore += total_value
        new_state.turn = 'AI'
    else:  # turn == 'AI'
        new_state.aiScore += total_value
        new_state.turn = 'player'
    
    return new_state

"""
Returns True if game is over, False otherwise.

If the game is over when there are no coins left.

Otherwise, the function should return False if the game is still in progress.
"""
# ========== IMPLEMENTED: Problem II, Part 1, Question 5 ==========
def terminal(state):
    return len(state.coins) == 0

"""
Returns the scores of the two players.

You may assume utility will only be called on a state if terminal(state) is True.
"""
# ========== IMPLEMENTED: Problem II, Part 1, Question 6 ==========
def utility(state):
    # Returns the utility from the player's perspective
    # Positive means player wins, negative means AI wins
    return state.pScore - state.aiScore

"""
Returns the winner of the game, if there is one.

- If the player has won the game, the function should return 'player'.
- If your AI program has won the game, the function should return AI.
- If there is no winner of the game (either because the game is in progress, or because it ended in a tie), the
  function should return None.
"""
# ========== IMPLEMENTED: Problem II, Part 1, Question 4 ==========
def winner(state):
    if not terminal(state):
        return None
    
    if state.pScore > state.aiScore:
        return 'player'
    elif state.aiScore > state.pScore:
        return 'AI'
    else:
        return None  # Tie
    


"""
Returns the best achivable value and the optimal action for the current player.

The move returned should be the optimal action (i, j) that is one of the allowable 
actions given a line of coins.

If multiple moves are equally optimal, any of those moves is acceptable.

If the board is a terminal board, the minimax function should return None.
"""
# ========== IMPLEMENTED: Problem II, Part 1, Question 7 ==========
def minimax(state, is_maximizing):
    # If terminal state, return utility and no action
    if terminal(state):
        return (utility(state), None)
    
    # Get all possible actions
    possible_actions = actions(state)
    
    if not possible_actions:
        return (utility(state), None)
    
    # Initialize best value based on whether we're maximizing or minimizing
    best_value = float('-inf') if is_maximizing else float('inf')
    best_action = None
    
    # Explore all possible actions
    for action in possible_actions:
        next_state = succ(state, action)
        # Recursively call minimax, alternating between maximizing and minimizing
        value, _ = minimax(next_state, not is_maximizing)
        
        # Update best value and action based on whether we're maximizing or minimizing
        if is_maximizing:
            if value > best_value:
                best_value = value
                best_action = action
        else:  # minimizing
            if value < best_value:
                best_value = value
                best_action = action
    
    return (best_value, best_action)


    