
import game
import numpy as np
import player as p
import time

def run_experiment(iterations, p1_type, p2_type, depth1, depth2):  
  

  accumulated_time_p1 = []
  accumulated_time_p2 = []
  wins_p1_counter = 0
  wins_p2_counter = 0

  
  for i in range(iterations):

      p1_total_time = 0 # total time for player1
      p1_count = 0 # for numbers of turns (player1)
      p2_total_time = 0 # total time for player2
      p2_count = 0 # for numbers of turns(player2)
  
      # Initializing the Game
      state = game.initialize_game()
      #game.print_board(state)
  
      # setted for:
      # - P1: actions by AI, depth by user  
      # - P2: random actions
  
      while True:
          # we initialize these values at the beginning of each iteration
  
          repeat = True
          while repeat:
              #Player 1 turn
              start = time.time()
              player = 1
              # action = np.random.randint(0, 6)
              
              if p1_type == 1:
                  _, action_values = p.alphabeta(state, depth1, True, -np.Inf, np.Inf)
                  #print(action_values)
                  action = np.argmax(action_values)  
              else:
                  action = int(input("Your turn! Please choose an non-empty hole (starting from 0 to 5): "))
  
              
              if game.is_valid(state, action):
                  
                  new_state, final, repeat = game.play_a_turn(player, state, action)
                  p1_count += 1
                  end = time.time() 
                  p1_total_time += (end - start)
                  if final: #Clean the board
                      print('Game over!')
                      if new_state[0,0] > new_state[1,6]:
                          #print('The winner is: Player 2')
                          wins_p2_counter += 1
                      elif new_state[0,0] < new_state[1,6]:
                          #print('The winner is: Player 1') 
                          wins_p1_counter += 1
                      else:
                          print('We have a tie!!!')
                      break
                  elif repeat:
                      print('P1 repeat turn')
                      state = new_state.copy()
                  
          if final: break
          # flip the board from a player 2 perspective:
          fliped = game.flip_board(new_state)    
          
          # we initialize these values at the beginning of each iteration
  
          repeat = True
          while repeat:
              #Player 2 turn
              start = time.time()
              player = 2
              
              if p2_type == 1:
                  _, action_values = p.alphabeta(fliped, depth2, True, -np.Inf, np.Inf)
                  #print(action_values)
                  action = np.argmax(action_values)  
              else:
                  action = np.random.randint(0, 6)
          
              if game.is_valid(fliped, action):
                  
                  new_state, final,repeat = game.play_a_turn(player, fliped, action)
                  p2_count += 1
                  end = time.time() 
                  p2_total_time += (end - start)
                  if final: #Clean the board
                      print('Game over!')
                      if new_state[0,0] > new_state[1,6]:
                          #print('The winner is: Player 1') #inverted player (flipped board)
                          wins_p1_counter += 1

                      elif new_state[0,0] < new_state[1,6]:
                          #print('The winner is: Player 2')
                          wins_p2_counter += 1
                      else:
                          pass
                          #print('We have a tie!!!')
                      break
                  
                  elif repeat:
                      #print('P2 repeat turn')
                      p2_count += 1
                      fliped = new_state.copy()
                  
                  
  
          if final: break
          # Once we perform the player 2 turn, we flip the board again
          # to start another loop:
          state = game.flip_board(new_state)
      
    
      #print('')    
      #print("Player 1 total time per game: " +  str(np.round(p1_total_time,4))+ " seconds")
      #print("Player 1 number of turns: " +  str(p1_count))
      #print("Player 1 average time per turn: " +  str(np.round(p1_total_time/p1_count,4))+ " seconds")
      accumulated_time_p1.append(p1_total_time/p1_count)
      if p1_type == 1:
        #print('Player 1 considered depth search: ',depth1)
        #print('')    
        #print("Player 2 total time per game: " +  str(np.around(p2_total_time,4))+ " seconds")
        #print("Player 2 number of turns: " +  str(p2_count))
        #print("Player 2 average time per turn: " +  str(np.round(p2_total_time/p2_count,4))+ " seconds")
        accumulated_time_p2.append(p2_total_time/p2_count)
      if p2_type == 1:
        pass
        #print('Player 2 considered depth search: ',depth2)

  return   wins_p1_counter, wins_p2_counter, accumulated_time_p1, accumulated_time_p2

#Here we defined the player type (manually):

p1_type = 1 #AI
p2_type = 1 # AI
depth1 = 3
depth2 = 5
iterations = 100
wins_p1_counter, wins_p2_counter, accumulated_time_p1, accumulated_time_p2 = run_experiment(iterations, p1_type, p2_type, depth1, depth2)

#Let's put these arrays as a np.arrays...
accumulated_time_p1, accumulated_time_p2 = np.array(accumulated_time_p1), np.array(accumulated_time_p2)
#%%
average_wins_p1 = wins_p1_counter/iterations
average_wins_p2 = wins_p2_counter/iterations
average_draw = 1-average_wins_p1-average_wins_p2
average_time_p1 = np.average(accumulated_time_p1)/iterations
average_time_p2 = np.average(accumulated_time_p2)/iterations

print('depth1', depth1)
print('depth2', depth2)
print('average_wins_p1 [%]:', average_wins_p1*100)
print('average_wins_p2 [%]:', average_wins_p2*100)
print('average_draw [%]:', average_draw*100)
print('average_time_p1 [seconds]:', average_time_p1)
print('average_time_p2 [seconds]:', average_time_p2)



