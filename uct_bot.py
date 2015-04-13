import time
import random

THINK_DURATION = 1


class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """
    def __init__(self, move = None, parent = None, state = None):
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.get_moves() # future child nodes
        self.playerJustMoved = state.get_whos_turn() # the only part of the state that the Node needs later
        
    def UCTSelectChild(self): # UCB
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        # choose the most urgent child giving a evaluation function
        # def lamba (c):
        print "Select child"
        s = sorted(self.childNodes, key = lambda c: (float)(c.wins/c.visits) + sqrt(2*log(self.visits)/c.visits))[-1]

        return s # a tuple
    
    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move = m, parent = self, state = s) # n = new Node (xx, xx, xx)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n # return a child node from s (state)
    
    def Update(self, result): # is called when backpropagating
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1 # update the n visits of current state
        self.wins += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
             s += c.TreeToString(indent+1)
        return s

    def IndentString(self,indent):
        s = "\n"
        for i in range (1,indent+1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
             s += str(c) + "\n"
        return s



def think(state, quip):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
    Return the best move from the rootstate.
    Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""
    rootnode = Node(state = state)	
    t_start = time.time()
    t_deadline = t_start + THINK_DURATION
    iterations = 0
    node = rootnode
    while True:
        
        stateCopy = state.copy()
        t_now = time.time()
        if t_now > t_deadline:
            break

	    # Select
        while node.untriedMoves == [] and node.childNodes != []: # node is fully expanded and non-terminal
            node = node.UCTSelectChild() # based on UCB, x + c * sqrt (2ln * Pvisited/ stateVisited)
            stateCopy.apply_move(node.move)  #


	    # Expand
        if node.untriedMoves != []: # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves) 
            stateCopy.apply_move(m)
            #print "M: ", m
            node = node.AddChild(m,stateCopy) # add child and descend tree

	    # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while stateCopy.get_moves() != []: # while state is non-terminal
            stateCopy.apply_move(random.choice(stateCopy.get_moves()))

	    # Backpropagate
        while node != None: # backpropagate from the expanded node and work back to the root node
            node.Update(stateCopy.get_result(node.playerJustMoved)) # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parentNode

	# Output some information about the tree - can be omitted
	# if (verbose): print rootnode.TreeToString(0)
	# else: print rootnode.ChildrenToString() 

	return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move # return the move that was most visited




