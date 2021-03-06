# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)

        successorGameState = currentGameState.generatePacmanSuccessor(action)  # current game state
        #print("successorGameState: ", successorGameState)

        newPos = successorGameState.getPacmanPosition()  # pacman position in the maze
        #print("newPos: ", newPos)

        newFood = successorGameState.getFood() # food position in the Pacman maze (prints out a list of boolean: T and F)
        #print("newFood: ", newFood)

        newGhostStates = successorGameState.getGhostStates()  # position of the ghost
        #print("newGhostStates: ", newGhostStates)

        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] # time that Ghost is scared when Pacman gets food
        #print("newScaredTimes: ", newScaredTimes)

        "*** YOUR CODE HERE ***"
        foodList = newFood.asList()  # makes a list of all food coordinates in the maze
        score = successorGameState.getScore()  # prioritize score for Pacman

        # prioritize closest food location; use a (for loop) for food locations
        for food in foodList:
            # manhattan Distance to nearest food based on current position
            foodDistance = util.manhattanDistance(food, newPos)
            # update score based on nearest food (Note: use reciprocals for important values)
            # reciprocals should be used for mapping of the maze and normalize values for the maze between 0 and 1,
            # in comparison to 1 and a large number (1,000,000) because you would need to also account for the locations
            # of the ghost.
            if (foodDistance != 0):
                score = score + (1.0/foodDistance)

        # Loop to find ghost locations
        for ghost in newGhostStates:
            # current position of ghost
            ghostLocation = ghost.getPosition()
            #distance to nearest ghost
            ghostDistance = util.manhattanDistance(ghostLocation, newPos)
            # if ghost distance is -1 then update score
            if (ghostDistance < -1):
                score = score + (1.0/ghostDistance)

        # return the score (prioritize food)
        return score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def minimax (agentIndex, depth, gameState):
            if depth == self.depth or gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState)
            nextAgent = agentIndex + 1

            #set to agent-0, pacman, if necessary and increase depth
            if gameState.getNumAgents() == nextAgent:
                nextAgent = 0
                depth += 1
            actions = gameState.getLegalActions(agentIndex)

            # Pacman; maximizer
            if agentIndex == 0:
                return max(minimax(nextAgent, depth, gameState.generateSuccessor(agentIndex, nextAction))
                           for nextAction in actions)
            # Ghost; minimizer
            else:
                return min(minimax(nextAgent, depth, gameState.generateSuccessor(agentIndex, nextAction))
                           for nextAction in actions)

        # initializing values
        bestAction = Directions.WEST
        maximum = float("-inf")

        # Calculating the best action
        for action in gameState.getLegalActions(0):
            value = minimax(1, 0, gameState.generateSuccessor(0, action))
            if value > maximum:
                maximum = value
                bestAction = action

        # Return the best action the Pacman should take
        return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def alphaBetaPrune(agentIndex, depth, gameState, alpha, beta):
            if depth == self.depth or gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState)

            nextAgent = agentIndex + 1

            # set to agent-0, pacman, if necessary and increase depth
            if gameState.getNumAgents() == nextAgent:
                nextAgent = 0
                depth += 1

            actions = gameState.getLegalActions(agentIndex)

            # Pacman; Maximizer
            if agentIndex == 0:
                maximum = float("-inf")
                for nextAction in actions:
                    maximum = max(maximum, alphaBetaPrune(nextAgent, depth, gameState.generateSuccessor(agentIndex, nextAction), alpha, beta))

            # Finding and returning the largest value
                    if maximum > beta:
                        return maximum
                    alpha = max(alpha, maximum)
                return maximum
            # Ghosts; Minimizer
            else:
                minimum = float("inf")
                for nextAction in actions:
                    minimum = min(minimum, alphaBetaPrune(nextAgent, depth, gameState.generateSuccessor(agentIndex, nextAction), alpha, beta))

            # Finding and returning the lowest value
                    if minimum < alpha:
                        return minimum
                    beta = min(beta, minimum)
                return minimum

        # initializing values
        bestAction = Directions.WEST
        maximum = float("-inf")
        alpha = float("-inf")
        beta = float("inf")

        # Calculating the best action
        for action in gameState.getLegalActions(0):
            value = alphaBetaPrune(1, 0, gameState.generateSuccessor(0, action), alpha, beta)
            if value > maximum:
                maximum = value
                bestAction = action

        # Pruning leaf nodes
            if maximum > beta:
                return maximum
            alpha = max(alpha, maximum)

        # Return the best action the Pacman should take
        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectimax(agentIndex, depth, gameState):
            if depth == self.depth or gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState)
            nextAgent = agentIndex + 1;

            # set to agent-0, pacman, if necessary and increase depth
            if gameState.getNumAgents() == nextAgent:
                nextAgent = 0;
                depth += 1

            actions = gameState.getLegalActions(agentIndex)

            # Pacman; maximizer
            if agentIndex == 0:
                return max(expectimax(nextAgent, depth, gameState.generateSuccessor(agentIndex, nextAction))
                           for nextAction in actions)
            # Ghosts; instead of min find the average of the leaf nodes
            else:
            # return the average, instead of min, of the leaf nodes for expectimax algorithm
            # get the sum of the leaf nodes and then divide it by the number of leaf nodes giving you the average
                return sum(expectimax(nextAgent, depth, gameState.generateSuccessor(agentIndex, newState))
                           for newState in actions) / len(actions)

        # initializing values
        bestAction = Directions.WEST
        maximum = float("-inf")

        # Calculating the best action
        for action in gameState.getLegalActions(0):
            value = expectimax(1, 0, gameState.generateSuccessor(0, action))
            if value > maximum:
                maximum = value
                bestAction = action

        # Return the best action the Pacman should take
        return bestAction

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: Building on top of the evaluation method made in the reflex agent problem. In order to get a score
    above 1000, you need to implement a solution in which Pacman will go for capsules and scared ghosts. By manipulating
    the point values that Pacman can get by using different actions, Pacman will try and maxmimize the amount of points
    he can get. So by adding more points towards power capsules and scared ghosts, Pacman will try and go for those
    capsules and scared ghost if the score is high enough for him to take that those actions.
    """
    "*** YOUR CODE HERE ***"

    newPos = currentGameState.getPacmanPosition()  # pacman position in the maze
    # print("newPos: ", newPos)

    newFood = currentGameState.getFood()  # food position in the Pacman maze (prints out a list of boolean: T and F)
    # print("newFood: ", newFood)

    newGhostStates = currentGameState.getGhostStates()  # position of the ghost
    # print("newGhostStates: ", newGhostStates)

    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]  # time that Ghost is scared when Pacman gets food
    # print("newScaredTimes: ", newScaredTimes)

    # prioritize closest food location; use a (for loop) for food locations
    foodList = newFood.asList()  # makes a list of all food coordinates in the maze
    score = currentGameState.getScore()  # prioritize score for Pacman

    # prioritize closest food location; use a (for loop) for food locations
    for food in foodList:
        # manhattan Distance to nearest food based on current position
        foodDistance = util.manhattanDistance(food, newPos)
        # update score based on nearest food (Note: use reciprocals for important values)
        # reciprocals should be used for mapping of the maze and normalize values for the maze between 0 and 1,
        # in comparison to 1 and a large number (1,000,000) because you would need to also account for the locations
        # of the ghost.
        if (foodDistance != 0):
            score = score + (1.0 / foodDistance)

    # Loop to find ghost locations and stay away from them
    ghostDistance = 0
    for ghost in newGhostStates:
        # current position of ghost
        ghostLocation = ghost.getPosition()
        # distance to nearest ghost
        ghostDistance = util.manhattanDistance(ghostLocation, newPos)
        # if ghost distance is -1 then update score
        if (ghostDistance < -1):
            score = score - (1.0 / ghostDistance)

    # Give Pacman an incentive to go for power capsules
    capsules = currentGameState.getCapsules()
    if capsules != 0:
        score = score * 10000

    # After Pacman gets a power capsule, he should go towards the scared ghost
    newScaredTimes = [ghostState.scaredTimer for ghostState in currentGameState.getGhostStates()]
    eatGhostReward = 0
    # Find the location of the closest ghost
    closestGhost = min([manhattanDistance(newPos, x.getPosition()) for x in newGhostStates])
    # if any ghost is scared then Pacman will go for it.
    if min(newScaredTimes) > 0:
        eatGhostReward = 1 / float(closestGhost)
        score = score * eatGhostReward * 10

    # return the score
    return score

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
