import numpy as np
import game


def eval_funct(state):
    # Firstly we'll evaluate just the difference between the two kalahas
    score1 = state[1,6] - state[0,0] #kalaha's difference is a direct indicator of how good we are playing
    
    #take opponent seeds chances
    score2 = 0
    if state[1,0] == 5 and state[1,5] == 0:
        score2 += 5
        if state[1,0]==4 and state[1,4] == 0:
            score2 += 5
            if state[1,0]==3 and state[1,3] == 0:
                score2 += 5
                if state[1,0]==2 and state[1,2] == 0:
                    score2 += 5
                    if state[1,0]==1 and state[1,1] == 0:
                        score2 += 5
    if state[1,1] == 4 and state[1,5] == 0:
        score2 += 5
        if state[1,1]==3 and state[1,4] == 0:
            score2 += 5
            if state[1,1]==2 and state[1,3] == 0:
                score2 += 5
                if state[1,1]==1 and state[1,2] == 0:
                    score2 += 5
                    
    if state[1,2] == 3 and state[1,5] == 0:
        score2 += 5
        if state[1,2]==2 and state[1,4] == 0:
            score2 += 5
            if state[1,2]==1 and state[1,3] == 0:
                score2 += 5
                
    if state[1,3] == 2 and state[1,5] == 0:
        score2 += 5
        if state[1,3]==1 and state[1,4] == 0:
            score2 += 5
    if state[1,4] == 1 and state[1,5] == 0:
        score2 += 5
    
    #repeated turn chances   
    score3 = 0
    if state[1,0] == 6:
        score3 += 5
        if state[1,1]==5:
            score3 += 5
            if state[1,2]==4:
                score3 += 5
                if state[1,3]==3:
                    score3 += 5
                    if state[1,4]==2:
                        score3 += 5
                        if state[1,5]==1:
                            score3 += 5    
     
    return score1*0.2 + score2*0.3 + score3*0.5

def plan_a_turn(state, action): #expand the tree
    repeat = True
    while repeat:
        if game.is_valid(state, action):
            new_state, last_position = game.update_state(state, action)
            new_state = game.take_opponent_seeds(new_state, last_position)
            new_state, final = game.is_final(new_state)
            repeat = game.repeat_turn(last_position, final)
        if repeat:
            state = new_state.copy()
            action = np.random.randint(0, 6)
            
    return new_state

def alphabeta(state, depth, isMaxPlayer, alpha, beta):
    
# Based on Minimax algorithm with alpha-beta pruning evaluating the tree at depth "d" as maximum.

    #If we reach a final state, get this score:
    state, final = game.is_final(state)
    if final:
        if state[1,6] > state[0,0]:
            return 100, -1
        
        if state[0,0] > state[1,6]:
            return -100, -1
        else:
            return 0, -1
        
    if depth == 0:
        return eval_funct(state), -1
    
    #Otherwise, we receive the state and expand it performing the actions:
    
    #Minimax
    if isMaxPlayer:

        value = -99999
        value_actions = np.zeros(6)                    
        for action in range(6): 
            if game.is_valid(state,action):
                new_state = plan_a_turn(state, action)
                value_from_MIN, _ = alphabeta(game.flip_board(new_state), depth-1, False, alpha, beta)
                #print(value_from_MIN)
                value = np.max([value, value_from_MIN])# in arguments, "False" indicate that we are sending these paramiters to MIN, so the opponent, that's why we flipp the board.
                value_actions[action] = value
                if value >= beta:
                    break # Beta cutt-off
                alpha = np.max([alpha, value])
            else:
                value_actions[action] = -1000
                    
        return value, value_actions
                

                
    else: #isMinPlayer
        value = 99999
        value_actions = np.zeros(6)                    
        for action in range(6): 
            if game.is_valid(state,action):
                new_state = plan_a_turn(state, action)
                value_from_MAX, _ = alphabeta(game.flip_board(new_state), depth-1, True, alpha, beta)
                #print(value_from_MAX)
                value = np.min([value, value_from_MAX])# in arguments, "False" indicate that we are sending these paramiters to MIN, so the opponent, that's why we flipp the board.
                value_actions[action] = value
                if value <= alpha:
                    break # Alpha cutt-off
                beta = np.min([beta, value])
            else:
                value_actions[action] = -1000
                    
        return value, value_actions
  

#%%
