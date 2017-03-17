import random
from random import randint
import pdb
import numpy as np
import enum
from enum import Enum
import copy	
from pprint import pprint

class Player(Enum):
	Empty = 0
	Computer = 1
	User = 2

class Stats:
	gamesPlayed = 0
	gamesStartedByComputer = 0
	gamesWonByComputer = 0
	gamesWonByUser = 0
	gamesDrawn = 0
		
	def recordGame(self, startedBy, wonBy):
	
		# How many games played
		self.gamesPlayed += 1
		
		# Who started
		if (startedBy == Player.Computer):
			self.gamesStartedByComputer += 1
			
		# Who won
		if (wonBy == Player.Computer):
			self.gamesWonByComputer += 1
		elif (wonBy == Player.User):
			self.gamesWonByUser += 1
		elif (wonBy == Player.Empty):
			self.gamesDrawn += 1
			
	def printStats(self):
		print ("Games Played:", self.gamesPlayed, \
		" Draw:", (self.gamesDrawn * 100/self.gamesPlayed), \
		"% Computer Won:", (self.gamesWonByComputer * 100/self.gamesPlayed), \
		"% User Won:", (self.gamesWonByUser * 100/self.gamesPlayed), \
		"%")
		
	def resetStats(self):
		self.gamesPlayed = 0
		self.gamesStartedByComputer = 0
		self.gamesWonByComputer = 0
		self.gamesWonByUser = 0
		self.gamesDrawn = 0

class Move:	
	def __init__(self, player, row, column):
		self.player = player
		self.row = row
		self.column = column

gridLength = 3
gamma = 0.8
winScore = 100
lossScore = 0
initialScore = 50
Qscores = {}
stats = Stats()
		
def debug():
	pdb.set_trace()

def isGameOver(grid):
	if (hasPlayerWon(grid, Player.Computer)):
		return True, Player.Computer
	elif (hasPlayerWon(grid, Player.User)):
		return True, Player.User
	elif isGridFull(grid):
		return True, Player.Empty
	else:
		return False, Player.Empty
		
	
def hasPlayerWon(grid, player):
	if ((grid[0][0] == player and grid[0][1] == player and grid[0][2] == player) or # 1st row
		(grid[1][0] == player and grid[1][1] == player and grid[1][2] == player) or # 2st row
		(grid[2][0] == player and grid[2][1] == player and grid[2][2] == player) or # 3st row
		(grid[0][0] == player and grid[1][0] == player and grid[2][0] == player) or # 1st column
		(grid[0][1] == player and grid[1][1] == player and grid[2][1] == player) or # 2st column
		(grid[0][2] == player and grid[1][2] == player and grid[2][2] == player) or # 3st column
		(grid[0][0] == player and grid[1][1] == player and grid[2][2] == player) or # forward diagonal
		(grid[0][2] == player and grid[1][1] == player and grid[2][0] == player)): # backward diagonal
		return True
	else: 
		return False
		
def isGridFull(grid):	
	return not (Player.Empty in np.array(grid))
	
def QscoreForGrid(grid):
	if (hasPlayerWon(grid, Player.Computer)):
		return winScore
	elif (hasPlayerWon(grid, Player.User)):
		return lossScore
	else:
		serialized = serializeGrid(grid)
		return Qscores.get(serialized, initialScore)
	
def updateQscores(grid, score):
	global Qscores
	serializedGrid = serializeGrid(grid)
	Qscores[serializedGrid] = score
	
def serializeGrid(grid):
	serialized = ""
	for i in range(gridLength):
		for j in range(gridLength):
			serialized += str(grid[i][j].value)
	
	return serialized

def updateGridDueToMove(grid, move):
	updatedGrid = copy.deepcopy(grid)
	if (updatedGrid[move.row][move.column] == Player.Empty):
		updatedGrid[move.row][move.column] = move.player
	return updatedGrid
	
def possibleMovesForPlayer(grid, player):
	moves = []
	for i in range(gridLength):
		for j in range(gridLength):
			if (grid[i][j] == Player.Empty):
				move = Move(player, i, j)
				moves.append(move)
	return moves
	
def maxQ(grid, moves):
	movesWithMaxScore = []
	maxScore = lossScore
	
	for move in moves:
		updatedGrid = updateGridDueToMove(grid, move)
		score = QscoreForGrid(updatedGrid)
		if (score > maxScore):
			movesWithMaxScore = [move]
			maxScore = score
		elif (score == maxScore):
			movesWithMaxScore.append(move)
		
	return random.choice(movesWithMaxScore), maxScore
	
def minQ(grid, moves):
	movesWithMinScore = []
	minScore = winScore
	
	for move in moves:
		updatedGrid = updateGridDueToMove(grid, move)
		score = QscoreForGrid(updatedGrid)
		if (score < minScore):
			movesWithMinScore = [move]
			minScore = score
		elif (score == minScore):
			movesWithMinScore.append(move)
		
	return random.choice(movesWithMinScore), minScore	

def learnFromGameHistory(gameHistory):
	
	updateQscores(gameHistory[len(gameHistory)-1], QscoreForGrid(gameHistory[len(gameHistory)-1]))
	
	for i, game in reversed(list(enumerate(gameHistory))):
		if (i > 0):
			learn(gameHistory[i-1], gameHistory[i])
	
def initGrid():
	grid = [[Player.Empty for i in range(gridLength)] for j in range(gridLength)]
	return grid

def init():
	Qscores = {}

def makeEducatedMove(grid, player):	

	# All valid moves in the current state	
	moves = possibleMovesForPlayer(grid, player)
	
	# Move with best Qscore
	if (player == Player.Computer):
		move, score = maxQ(grid, moves)
	else:
		move, score = minQ(grid, moves)
		
	# Make move and update state
	updatedGrid = updateGridDueToMove(grid, move)
	
	return updatedGrid
	
def learn(grid, updatedGrid):
	
	# V(s) <-- V(s) + gamma * [V(s') - V(s)]
	currentStateScore = QscoreForGrid(grid)
	futureStateScore = QscoreForGrid(updatedGrid)
	currentStateScore = currentStateScore + gamma * (futureStateScore - currentStateScore)
	updateQscores(grid, currentStateScore)
	
def makeRandomValidMove(grid, player):
	
	# All possible moves 
	moves = possibleMovesForPlayer(grid, player)
	
	# Selected move
	move = random.choice(moves)
	
	# Update grid 
	updatedGrid = updateGridDueToMove(grid, move)
		
	return updatedGrid

def playOnce(learningMode, explorativeMode):
	global stats
	
	grid = initGrid()
	gameHistory = []
	
	startingPlayer = randint(1,2)	
	# startingPlayer = Player.Computer	
	
	player = Player(startingPlayer)
	
	gameOver, whoWon = isGameOver(grid)
	while (not gameOver):
		if (player == Player.Computer):
			if (learningMode and explorativeMode):
				grid = makeRandomValidMove(grid, Player.Computer)				
			else:
				grid = makeEducatedMove(grid, Player.Computer)
		else: 
			if (learningMode):
				grid = makeEducatedMove(grid, Player.User)
			else:
				grid = makeRandomValidMove(grid, Player.User)
				
		if (player == Player.Computer):
			player = Player.User
		else: 
			player = Player.Computer
			
		gameOver, whoWon = isGameOver(grid)
		gameHistory.append(grid)
		
	learnFromGameHistory(gameHistory)
	
	stats.recordGame(startingPlayer, whoWon)
	
def play(numberOfTimes, learningMode):
	for i in range(numberOfTimes):
		if ((not learningMode) and (stats.gamesPlayed % 5 == 0)):
			playOnce(learningMode, True)
		else:
			playOnce(learningMode, False)
			
		if (stats.gamesPlayed % 1000 == 0):
			stats.printStats()
	
init()

print ("LEARN")
play(10000, True)

stats.resetStats()

debug()

print ("PLAY")
play(1000, False)

