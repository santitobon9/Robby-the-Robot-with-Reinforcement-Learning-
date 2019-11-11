import numpy as np
import math
#import matplotlib


goal = np.array([[1,2,3],
                 [4,5,6],
                 [7,8,0]])

def Is_Solvable(curr_list):
    inversion = 0
    for i in curr_list:
        j = i
        while (j < len(curr_list)):
            if (j == 0):
                break
            elif (curr_list[i] > curr_list[j]):
                inversion+=1
                break
            j+=1
#    print(inversion)
    if((inversion % 2)==0):
        print(inversion)
        return True
    else:
        return False
    
    

#can_solve = False
#while(can_solve != True):
#    start = np.random.choice(9, size=(3, 3), replace=False)
#    can_solve = Is_Solvable(start.flatten())

start = np.array([[0,1,3], #Both algorithms work with this start
                  [4,2,5],
                  [7,8,6]])

print("Goal:")
print (goal)
print("Start:")
print (start)


#goal = [1,2,3,4,5,6,7,8,0]
#start = np.random.choice(9, 9, replace=False)

def toString (matrix):
    string = ""
    for x in range(len(matrix)):
        for j in range(len(matrix[x])):
            string += str(matrix[x][j])
        
    return string

#str_goal = convert_toString (goal)
#str_start = convert_toString (start)
#print(str_goal)
#print(str_start)

def Man_Heuristic (curr, goal):
    h_value = 0
    for i in range(len(curr)): #loops through current matrix
        for j in range (len(curr[i])):
            
            for x in range(len(goal)): #loops through goal matrix
                for y in range (len(goal[x])):
                    if (goal[x][y] == curr[i][j]): #if a match in numbers
                        h_value += (math.sqrt(abs(x-i) + abs(y-j))) #add the distance from goal index
    return h_value

def Euc_Heuristic (curr, goal):
    h_value = 0
    for i in range(len(curr)): #loops through current matrix
        for j in range (len(curr[i])):
            
            for x in range(len(goal)): #loops through goal matrix
                for y in range (len(goal[x])):
                    if (goal[x][y] == curr[i][j]): #if a match in numbers
                        h_value += ((abs(x-i) + abs(y-j))) #add the distance from goal index
    return h_value
    
#my_value = Man_Heuristic (start, goal)
#print(my_value)

def move_up (matrix):
    curr = np.copy(matrix)
    for i in range(len(curr)): #loops through current matrix
        for j in range (len(curr[i])):
            if (curr[i][j]==0 and i>0):
                temp = curr[i-1][j]
                curr[i-1][j] = 0
                curr[i][j] = temp
                return curr
    return curr

def move_down (matrix):
    curr = np.copy(matrix)
    for i in range(len(curr)): #loops through current matrix
        for j in range (len(curr[i])):
            if (curr[i][j]==0 and i<2):
                temp = curr[i+1][j]
                curr[i+1][j] = 0
                curr[i][j] = temp
                return curr
    return curr

def move_right (matrix):
    curr = np.copy(matrix)
    for i in range(len(curr)): #loops through current matrix
        for j in range (len(curr[i])):
            if (curr[i][j]==0 and j<2):
                temp = curr[i][j+1]
                curr[i][j+1] = 0
                curr[i][j] = temp
                return curr
    return curr

def move_left (matrix):
    curr = np.copy(matrix)
    for i in range(len(curr)): #loops through current matrix
        for j in range (len(curr[i])):
            if (curr[i][j]==0 and j>0):
                temp = curr[i][j-1]
                curr[i][j-1] = 0
                curr[i][j] = temp
                return curr
    return curr
    
#option1 = move_up(start)
#option2 = move_down(start)
#option3 = move_right(start)
#option4 = move_left(start)

#print("Options")
#print(option1)
#print(option2)
#print(option3)
#print(option4)

def reconstruct_path(cameFrom, str_current):
    total_path = {str_current}
    for c in cameFrom:
        current = cameFrom[c]
        total_path.append(current)
    return total_path


def Best_First(start, goal):
    steps = 0
    current = start
    while (steps < 100):
        if (np.array_equal(current, goal)): #if at goal state
            return 1         
        options = [move_up(current), move_down(current), move_right(current), move_left(current)]
        lowest = -1
        curr_temp = current
        for opt in options:
            if (toString(opt) == toString(curr_temp)): #if the same as the current
                continue
            elif (lowest == -1):
                current = opt
                lowest = Euc_Heuristic(opt, goal)
            else:
                if (Euc_Heuristic(opt, goal) < lowest): 
                    current = opt
        print(current)
        steps+=1 
    print("too many steps")
    return 0

if (Best_First(start, goal)==1):
    print("Solution found")
    
def A_Star (start, goal): 
    closedSet = {} #states that have been evaluated
    str_start = toString(start)
    openSet = {str_start : start} #states that have been discovered but haven't been evaluated
    cameFrom = {}
    gScore = {str_start : 0}
    fScore = {str_start : Man_Heuristic (start, goal)}
    steps = 0
    
    while (len(openSet) > 0):
        if (steps > 99): #limit the number of steps
            #empty_set = {}
            print("too many steps")
            #return empty_set
            return 0
        lowest = -1
        #print("start looking at openSet")
        for s in openSet: #finds the state with the lowest fscore
            if (lowest == -1):
                current = openSet[s]
                lowest = fScore[toString(openSet[s])]
            else:
                if (fScore[toString(openSet[s])] < lowest): 
                    current = openSet[s]           
        print(current)
        if (np.array_equal(current, goal)): #It reached the goal state
            #print("It works")
            #return reconstruct_path(cameFrom, toString(current))
            return 1
        
        del openSet[toString(current)]
        closedSet[toString(current)] = current
        
        options = [move_up(current), move_down(current), move_right(current), move_left(current)] #possible neighbors
        
        for opt in options: #loops through the four possible neighbors that can be taken
            if (toString(opt) == toString(current)): #if the same as the current
                continue
            if (toString(opt) in closedSet): #if I have already evaluated this state
                continue
            opt_gScore = (gScore[toString(current)] + 1)
            if (toString(opt) not in openSet): #discovered a new state
                openSet[toString(opt)] = opt
            elif (opt_gScore >= gScore[toString(opt)]):
                continue
            cameFrom[toString(opt)] = toString(current)
            gScore[toString(opt)] = opt_gScore #calculates gscore
            fScore[toString(opt)] = gScore[toString(opt)] + Man_Heuristic(opt, goal) #calculates fscore
        steps+=1
        
if(A_Star(start, goal)==1):
    print("Solution found")
   