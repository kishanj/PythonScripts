import random
from random import randint
import pdb
import numpy as np

gamma = 0.8
goalReward = 100
states = range(0,6)
finalState = 5
Qmatrix = []
Rmatrix = []

def initRmatrix():
	return [ 
				[-1, -1, -1, -1, 0, -1],
				[-1, -1, -1, 0, -1, 100],
				[-1, -1, -1, 0, -1, -1],
				[-1, 0, 0, -1, 0, -1],
				[0, -1, -1, 0, -1, 100],
				[-1, 0, -1, -1, 0, 100]
			  ]

def initQmatrix():
	return [ 
				[-1, -1, -1, -1, 0, -1],
				[-1, -1, -1, 0, -1, 0],
				[-1, -1, -1, 0, -1, -1],
				[-1, 0, 0, -1, 0, -1],
				[0, -1, -1, 0, -1, 0],
				[-1, 0, -1, -1, 0, 0]
			  ]			

def maxQ(state):
	maxReward = max(Qmatrix[state])
	allActions = [i for i, x in enumerate(Qmatrix[state]) if x in set([maxReward])]
	action = random.choice(allActions)
	
	return action, maxReward
	

def init():

	global Rmatrix
	Rmatrix = initRmatrix()
	
	global Qmatrix
	Qmatrix = initQmatrix()

def learn():
	
	global Qmatrix
		
	for i in range(100):
		
		initialState = randint(0,finalState-1)

		currentState = initialState
		while currentState != finalState:
			allActions = [i for i,x in enumerate(Rmatrix[currentState]) if x in set([0, 100])]
			action = random.choice(allActions)
			nextState = action
			nextAction, reward = maxQ(nextState)
			Qmatrix[currentState][action] = Rmatrix[currentState][action] + gamma * reward
			currentState = nextState

def playOnce(initialState):
	
	traversedStates = [initialState]
	currentState = initialState
	while currentState != finalState:
		action, reward = maxQ(currentState)
		currentState = action
		traversedStates.append(currentState)
		
	return traversedStates
	
def play(numberOfTimes):
	for i in range(numberOfTimes):
		print(playOnce(randint(0,finalState-1)))

init()

print("BEFORE LEARNING")

print(np.matrix(Qmatrix))

play(10)

learn()

print("AFTER LEARNING")

print(np.matrix(Qmatrix))

play(10)
	
	
		
	
		
	
