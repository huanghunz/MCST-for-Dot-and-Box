
def think(state, quip):

	# copy the current state to simulate the possible moves of one step
	# then return the move of the highest score 

 	moves = state.get_moves()

	bestMove = moves[0]
	bestScore = float('-inf')

	me = state.get_whos_turn()

	# state.getScore returns a list of (player, score)
	# outcome returns the socre of current player 
	def outcome(score):
		if me == 'red':
			return score['red'] - score['blue']
		else:
			return score['blue'] - score['red']

  	for move in moves:

  		# make a copy of current state to simulate the move
	  	stateCopy = state.copy() 
		stateCopy.apply_move(move)

	  	currentScore = outcome(stateCopy.get_score())

	  	if currentScore > bestScore:
	  		bestScore = currentScore
	  		bestMove = move

	#print "Picking %s with expected score %f" % (str(bestMove), bestScore)
	return bestMove
