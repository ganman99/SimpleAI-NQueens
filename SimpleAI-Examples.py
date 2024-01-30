

from __future__ import print_function
import random
from time import time
from array import *
from simpleai.search.viewers import BaseViewer
import math
from simpleai.search import SearchProblem , astar , breadth_first , uniform_cost , depth_first,limited_depth_first , iterative_limited_depth_first , greedy , genetic , hill_climbing,hill_climbing_random_restarts

class NQueens(SearchProblem):
    initial_state = ""
    def __init__(self, N):
        self.rows = N
        self._set_state()
        super(NQueens, self).__init__(initial_state=self.initial_state)
        self._action=[0]*int(self.rows)*int(self.rows)
        tempnum = 0
        for i in range(1,self.rows+1):
            for j in range(0,self.rows):
                self._action[tempnum]=str(i)+str(j)
                tempnum = tempnum +1
    def actions(self , state):
        return self._action
    def result(self , state , action):
        stateList = list(state)
        stateList[int(action[1])]=action[0]
        returnState = ""
        for i in range(0,len(state)):
            returnState = returnState + stateList[i]
        return returnState
    def is_goal(self,state):
        return self._count_attacking_pairs(state) == 0
    def heuristic(self,state):
        return self._count_attacking_pairs(state)
    def value(self , state):
        return -self._count_attacking_pairs(state)
    def crossover(self, state1 , state2):
        cut_point = random.randint(0, self.rows-1)
        child = state1[:cut_point] + state2[cut_point:]
        return child
    def mutate(self , state):
        mutation = str(random.randint(1,self.rows))
        mutation_point = random.randint(0, self.rows-1)
        mutated = ''.join([state[i] if i != mutation_point else mutation
                           for i in range(len(state))])
        return mutated 
    def __str__(self):
        return f"N: {self.rows}, state: {self.initial_state}"
    def _set_state(self):
        while True :
            print("How do want to set state?")
            print("1. Set state manually")
            print("2. Set state randomly")
            x = str(input("Enter selection: "))
            if x.__eq__("1"):
                self.initial_state = str(input("Enter state: "))
                if self._is_valid(self.initial_state):
                    print("Invalid")
                    continue
                break                                    
            elif x.__eq__("2") :
                self.initial_state = self.generate_random_state()
                break
            else:
                print("Invalid state . Try Again.")
                continue
    def generate_random_state(self):
        state = ""
        for i in range(0,self.rows):
            state = state + str(random.randint(1,self.rows))
        return state
    def _is_valid(self,state):
        if len(state) != self.rows:
            return True    
        for i in range(0, len(state)):
            case_1_valid = True
            for j in range(1, (self.rows)+1):
                if str(state[i]) == str(j):
                    case_1_valid = False
                    break
            if case_1_valid:
                return True
        return False   
    def _count_attacking_pairs(self, state1):
        stateList=[0]*int(self.rows)
        for i in range(0 , len(state1)):
            stateList[i] = state1[i]
        state_matrix = [[0]*int(self.rows) for _ in range(int(self.rows))]
        state = list(stateList)
        for i in range(0,self.rows):
            state_matrix[int(state[i])-1][i]=1
        state_matrix.reverse()
        attacks = 0
        for i in range(0 , len(state)):
            tempnum = 0
            for j in range(0 , len(state)):
                if state_matrix[i][j] == 1:
                    tempnum = tempnum + 1
            if tempnum>1:
                attacks = attacks + math.comb(tempnum,2)
        tempnum = 0
        temp_attacks = 0
        for i in range(0 , len(state)):
            tempnum = i
            temp_attacks = 0
            for j in range(0 , len(state)):
                if tempnum < 0:
                    break
                try:
                    if state_matrix[tempnum][j] == 1 :
                        temp_attacks = temp_attacks+1
                except:
                    break
                tempnum = tempnum-1
            if temp_attacks>1:
                attacks = attacks + math.comb(temp_attacks,2)
        for j in range(1 , len(state)):
            tempnum = j
            temp_attacks = 0
            for i in range(len(state)-1 , -1 , -1):
                if tempnum == len(state) :
                    break
                if state_matrix[i][tempnum] == 1 :
                    temp_attacks = temp_attacks+1
                tempnum = tempnum+1
            if temp_attacks>1:
                attacks = attacks + math.comb(temp_attacks,2)
        for i in range(0 , len(state)):
            tempnum = i
            temp_attacks = 0
            for j in range(len(state)-1 , -1 , -1):
                if tempnum < 0:
                    break
                try:
                    if state_matrix[tempnum][j] == 1 :
                        temp_attacks = temp_attacks+1
                except:
                    break
                tempnum = tempnum-1
            if temp_attacks>1:
                attacks = attacks + math.comb(temp_attacks,2)        
        for j in range(len(state)-2 , -1 , -1):
            tempnum = j
            temp_attacks = 0
            for i in range(len(state)-1 , -1 , -1):                                
                if tempnum < 0  :
                    break
                if state_matrix[i][tempnum] == 1 :
                    temp_attacks = temp_attacks+1
                tempnum = tempnum-1
            if temp_attacks>1:
                attacks = attacks + math.comb(temp_attacks,2)
        return attacks
    
problem = NQueens(5) 
print(problem) 
print("Which algorithm do you want to search?")
searh_alg = str(input("Please choose one of them.(BFS , DFS , LDF , ILDF , UCS , Greedy , Astar , Genetic , Hill Climbing , Hill Climbing Random Restart): "))
my_viewer = BaseViewer()

control = True

if(searh_alg == "BFS"):
    start = time()
    result = breadth_first(problem , viewer=my_viewer)
elif(searh_alg == "DFS"):
    start = time()
    result = depth_first(problem , graph_search=True, viewer=my_viewer)
elif(searh_alg == "LDF"):
    start = time()
    depth_limit = int(input("What should depth limit be?: "))
    result = limited_depth_first(problem,depth_limit, viewer=my_viewer)
elif(searh_alg == "ILDF"):
    start = time()
    result = iterative_limited_depth_first(problem, viewer=my_viewer)
elif(searh_alg == "UCS"):
    start = time()
    result = uniform_cost(problem, viewer=my_viewer)
elif(searh_alg == "Greedy"):
    start = time()
    result = greedy(problem, viewer=my_viewer)
elif(searh_alg == "Astar"):
    start = time()
    result = astar(problem, viewer=my_viewer)
elif(searh_alg == "Genetic"):
    start = time()
    result = genetic(problem,population_size=1000, viewer=my_viewer)
elif(searh_alg == "Hill Climbing"):
    start = time()
    result = hill_climbing(problem, viewer=my_viewer)
elif(searh_alg == "Hill Climbing Random Restart"):
    restartLimit = int(input("Restarts Limit?: "))
    start = time()
    result = hill_climbing_random_restarts(problem, restarts_limit=restartLimit,viewer=my_viewer)
else:
    control = False
if(control):
    print("Resulting path:")
    print(result.path())
    elapsed = time() - start
    print("Resulting state: "+result.path()[-1][1])
    print("Total Cost: "+str(len(result.path())))
    print("Viewer stats:")
    print(my_viewer.stats)
    print("Time taken: " + str(elapsed) + " seconds")
    if problem.is_goal(result.path()[-1][1]):
        print("Correct solution?: True")
    else:
        print("Correct solution?: False")
else:
    print("Entered wrong input.")
    
    