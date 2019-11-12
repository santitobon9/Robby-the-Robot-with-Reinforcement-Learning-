import numpy as np
from numpy.random import choice
import math
import random
import matplotlib.pyplot as plt

#Q_matrix = np.random.randint(1, size=(100, 5))

#print (Q_matrix)

class Robot:
    def __init__(self, x=0, y=0, reward=0, collection=0): #constructor
        self.x = x
        self.y = y

#Sensor Functions
    def senseCurr(self, grid):
        return grid[self.x][self.y]
    def senseNorth(self, grid):
        return grid[self.x][self.y+1]
    def senseSouth(self, grid):
        return grid[self.x][self.y-1]
    def senseEast(self, grid):
        return grid[self.x+1][self.y]
    def senseWest(self, grid):
        return grid[self.x-1][self.y]

#Action Functions
    def pickUp(self, grid): #pick up a can
        if (grid[self.x][self.y] == 1):
            grid[self.x][self.y] = 0
            return True #if action was successful
        else:
            return False
    def moveNorth(self, grid): #move north on the grid
        if (self.senseNorth(grid) == 3):
            return False
        self.y += 1
        return True #if action was successful
    def moveSouth(self, grid): #move south on the grid
        if (self.senseSouth(grid) == 3):
            return False
        self.y -= 1
        return True #if action was successful
    def moveEast(self, grid): #move east on the grid
        if (self.senseEast(grid) == 3):
            return False
        self.x += 1
        return True #if action was successful
    def moveWest(self, grid): #move est on the grid
        if (self.senseWest(grid) == 3):
            return False
        self.x -= 1
        return True #if action was successful
    
#Other Functions    
    def convertState(self, grid): #represents state as a tuple
        stateVector = (self.senseCurr(grid), self.senseNorth(grid), self.senseSouth(grid), self.senseEast(grid), self.senseWest(grid))
        return stateVector
    
    def selectAction(self, curr_state, Q_matrix, epsilon):
        if (random.randint(1,100) <= (100*epsilon)):
            action = random.randint(0,4)
            return action
        poss_actions = list() #list of possible action's q values
        PU = Q_matrix[curr_state][0] #pick up q value
        poss_actions.append(PU)
        N = Q_matrix[curr_state][1] #move north q value
        poss_actions.append(N)
        S = Q_matrix[curr_state][2] #move south q value
        poss_actions.append(S)
        E = Q_matrix[curr_state][3] #move east q value
        poss_actions.append(E)
        W = Q_matrix[curr_state][4] #move west q value
        poss_actions.append(W)
        Max = max(poss_actions) #the max q value of all possible actions
        if (Max == N):
            action = 1
        if (Max == PU):
            action = 0
        elif (Max == S):
            action = 2
        elif (Max == E):
            action = 3
        elif (Max == W):
            action = 4
        return action
    
    def performAction (self, action, grid): #perform the action that was selected
        if (action == 0): #Pick up
            success = self.pickUp(grid)
            if (success == True):
                self.collection += 1
                return 10
            else:
                return -1
        elif (action == 1): #move North
            success = self.moveNorth(grid)
            if (success == True):
                return 0
            else:
                return -5
        elif (action == 2): #move South
            success = self.moveSouth(grid)
            if (success == True):
                return 0
            else:
                return -5
        elif (action == 3): #move East
            success = self.moveEast(grid)
            if (success == True):
                return 0
            else:
                return -5
        elif (action == 4): #move West
            success = self.moveWest(grid)
            if (success == True):
                return 0
            else:
                return -5
        
    def Episode (self, grid, Q_matrix, epsilon): 
        M = 200 #number of reps
        n = 0.2 #learning rate
        y = 0.9 
        i = 0 #starting rep
        while (i < M):
            curr_state = self.convertState(grid)
            if curr_state not in Q_matrix: #if first time seeing state then add to Q_matrrix
                Q_matrix[curr_state] = np.zeros(5)
            action = self.selectAction(curr_state, Q_matrix, epsilon)
            reward = self.performAction(action, grid)
            self.reward += reward
            new_state = self.convertState(grid)
            if new_state not in Q_matrix: #if first time seeing state then add to Q_matrrix
                Q_matrix[new_state] = np.zeros(5)
            Q_matrix[curr_state][action] = Q_matrix[curr_state][action] + n*(reward + y * max(Q_matrix[new_state]) - Q_matrix[curr_state][action])
            i+=1
            
    def Train (self, Q_matrix):
        N = 10000 #number of reps for training
        k = 0 #starting rep
        epsilon = 0.1 #greedy action selection
        reward_list = list()
        while (k < N):
            grid = np.random.randint(2, size=(12, 12)) #creates grid
            for i, g in enumerate(grid):
                for j, gr in enumerate(grid[i]):
                    if (j == 0 or j == 11 or i == 0 or i == 11):
                        grid[i][j] = 3
            self.x = random.randint(1,10)
            self.y = random.randint(1,10)
#            print ("Before:")
#            print (grid)
            self.collection = 0
            self.reward = 0
            self.Episode (grid, Q_matrix, epsilon)
#            print ("After:")
#            print (grid)
            print ("Cans Collected:")
            print (self.collection)
            print ("Total Reward:")
            print (self.reward)
            print ("Points lost:")
            lost = ((self.collection * 10) - self.reward)
            print (lost)
            print ("Iteration:")
            print (k)
            k+=1
            if ((N-k) % 50 == 0): #every 50 reps reduce the epsilon value by .001
                epsilon -= 0.001
                reward_list.append(self.reward)
        print ("Average Reward(Training):")
        print (sum(reward_list)/(N/50))
        plt.plot(reward_list)
        fig = plt.figure()
        plt.show()
        
    def testEpisode (self, grid, Q_matrix, epsilon):
        M = 200 #number of reps
        i = 0 #starting rep
        while (i < M):
            curr_state = self.convertState(grid)
            action = self.selectAction(curr_state, Q_matrix, epsilon)
            reward = self.performAction(action, grid)
            self.reward += reward
            i+=1
                
    def Test (self, Q_matrix):
        N = 1000 #number of reps for testing
        k = 0 #starting rep
        epsilon = 0.1 #greedy action selection
        reward_list = list()
        while (k < N):
            grid = np.random.randint(2, size=(12, 12)) #creates grid
            for i, g in enumerate(grid):
                for j, gr in enumerate(grid[i]):
                    if (j == 0 or j == 11 or i == 0 or i == 11):
                        grid[i][j] = 3
            self.x = random.randint(1,10)
            self.y = random.randint(1,10)
            self.collection = 0
            self.reward = 0
            self.testEpisode (grid, Q_matrix, epsilon)
            reward_list.append(self.reward)
            k+=1
        print ("Average Reward(Test):")
        print (sum(reward_list)/N)
        plt.plot(reward_list)
        fig = plt.figure()
        plt.show()
        
        
        
Q_matrix = {}

#print (Q_matrix)    

Robby = Robot()

#index = Robby.convertState()

#print(Robby.x)
#print(Robby.y)
#print(index)
Robby.Train(Q_matrix) #trains Robby
Robby.Test(Q_matrix) #tests Robby
#print (Q_matrix)

#print (Robby.x)
#print (Robby.y)
#print (Robby.reward)



    

