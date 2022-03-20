import numpy as np
import os
import platform

def print_board(s, player = -1):
    print('')
    print("                  Kalaha board")
    print("                 {}".format("-Player 1 Turn-" if player==1 else "-Player 2 Turn-" if player ==2 else "  -Welcome!-"))
    print('')
  
    print('         5      4      3      2      1      0 ')
    print('-----------------------------------------------------------')
    for i in range(0, s.shape[0]):
        for j in range(s.shape[1]):
            print('  {}'.format(s[i][j]), end="  / ")
            if j ==6 and i == 0:
                print(" --\n --  /", end =' ')

    print('')
    
    print('-----------------------------------------------------------')
    print('         0      1      2      3      4      5 ')
    print('')
 
def initialize_game():
  state = np.array([[0,4,4,4,4,4,4],
                    [4,4,4,4,4,4,0]])
  return state
def set_player1():
    while True:
        os_name = platform.system()
        #print(os_name)
        if os_name == "Windows":
            os.system('cls')
        else:
            os.system('clear')
        print('')
        print('')
        print('-Welcome to Kalaha-')
        print('Choose an option to play agains our AI:')
        print('[1] - First player: AI')
        print('[2] - First player: Human (you!) ')
        print('')
        player = int(input('Enter your option: '))
        
        if player == 1 or player == 2:
            print('')
            break
    return player

def set_player2():
    while True:
        os_name = platform.system()
        #print(os_name)
        if os_name == "Windows":
            os.system('cls')
        else:
            os.system('clear')
        print('')
        print('')
        print('Choose the difficulty level of Player 2:')
        print('[1] - Tree Search AI')
        print('[2] - Random bot (noob level) ')
        print('')
        player = int(input('Enter your option: '))
        
        if player == 1 or player == 2:
            print('')
            break
    return player

def set_depth():
    while True:
        os_name = platform.system()
        #print(os_name)
        if os_name == "Windows":
            os.system('cls')
        else:
            os.system('clear')
        print('')
        print('')
        print('-- Depth for Alpha / Beta Pruning Algorithm --')
        print('This algorithm needs a "search depth" to be set.')
        print('Please choose a number greater or equal to 1')
        print('(...preferently up to 7)')
        print('')
        depth = int(input('Enter depth: '))
        if depth > 0:
            break
    return depth
def update_state(state, action):
    # here we need to code the game rules
    new_state = state.copy()
 
    
    if is_valid(state,action):

        n = state[1,action] # save the amount of seeds
        new_state[1,action] = 0 # empty the hole
        # put one seed on every hole including kalaha if apply
        i = 0
        while n != 0: # no seeds to distribute
            
            # update the next holes adding +1 until n = 0
            i += 1 
            if i < state.shape[1]-action: #we are still in the second row
                new_state[1, action + i] += 1
                last_position = [1, action + i]
                
            # we are in the first row
            elif i - (state.shape[1] - action -1) <= state.shape[1] - 1:# we sustract 1 because we don't count the kalaha's opponent
                new_state[0, -(i - (state.shape[1] - action -1))] += 1 #start to add+1 from left to right
                last_position = [0, -(i - (state.shape[1] - action-1)) % state.shape[1]]

            # we are in the second row
            elif i < state.shape[1] - action +(state.shape[1] -1) + (state.shape[1]): # add +1 to the second row (main player)
                new_state[1, (i - (state.shape[1] - action -1) - state.shape[1] )] += 1
                last_position = [1, (i - (state.shape[1] - action -1) - state.shape[1] )]

            # we are in the first row again
            elif i < (state.shape[1] -1) + state.shape[1] - action:# we sustract 1 because we don't count the kalaha's opponent
                new_state[0, -(i - (state.shape[1] - action -1))] += 1 #start to add+1 from left to right
                last_position = [0, -(i - (state.shape[1] - action-1)) % state.shape[1]]
            
            n -= 1 # substract 1 to the counter
        # if last_position == False:
        #         print('HEEERRRREEEEE!!!!')
        #         print('state', state)
        #         print('new state', new_state)
    
    return new_state, last_position

def is_final(state):
    # we have to define the goal states
    final_state = [0,0,0,0,0,0]
    if np.array_equal(state[0,1:7], final_state) or np.array_equal(state[1,0:6],final_state):
        state[0,0] += np.sum(state[0,1:7])
        state[0,1:7] = final_state
        state[1,6] += np.sum(state[1,0:6])
        state[1,0:6] = final_state
        
        return state, True
    else:
        return state, False

def is_valid(state, action):
    #we need to define when a move is valid
    if state[1,action] !=0 and action < 6: #an action can't be performed on an empty hole or greater than 5
        return True
    else:
        return False


def flip_board(state):
    #as the next decision depends only the current state, we can flip the board and take
    # decisions. This is usefull to code the game only from a 1 player perspective
    
    #here we invert the board player perspective
    switched_state = np.array([np.flip(state[1]),
                      np.flip(state[0])])
    
    return switched_state

def repeat_turn(last_position, final):
    if np.array_equal(last_position, [1,6]) and not final: #we are in our kalaha and we are not in the final state
        return True
    else:
        return False
        
def take_opponent_seeds(new_state, last_position): #not only take the opponents but ours.
    take_opponent_state = new_state.copy()
    
    # if we are not in our kalaha:
    if not np.array_equal(last_position,[1,6]):
        #if we are in the second row and the last updated hole is 1 and there are seed in the opponennt hole
        if last_position[0] == 1 and new_state[last_position[0],last_position[1]] == 1 and new_state[0,last_position[1]+1] > 0: 
            take_opponent_state[1,6] += new_state[0,last_position[1]+1]+1 #we store the opponent's seed on our kalaha (+1 because the out of phase) and +1 because our single seed
            take_opponent_state[0,last_position[1]+1] = 0 #we empty the opponent hole
            # and we do the same with our hole 
            take_opponent_state[1,last_position[1]] = 0
    return take_opponent_state
    
            
def play_a_turn(active_player, state, action):
    print('')
    print('')
    new_state, last_position = update_state(state, action)
    new_state = take_opponent_seeds(new_state, last_position)
    new_state, final = is_final(new_state)
    
    if active_player == 1:
        
        print('P1 selected action: ',action)
        print("This is the updated board after the action:")
        print_board(new_state, active_player)
    elif active_player == 2:
        
        print('P2 selected action: ',action)
        print("This is the updated board after the action:")
        print_board(flip_board(new_state), active_player)
    #print('Last position: ', last_position)
    repeat = repeat_turn(last_position, final)
    
    return new_state, final, repeat      


