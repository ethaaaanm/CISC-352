# solutions.py
# ------------
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

'''Implement the methods from the classes in inference.py here'''

import util
from util import manhattanDistance, raiseNotDefined
import random
import busters

def normalize(self):
    """
    Normalize the distribution such that the total value of all keys sums
    to 1. The ratio of values for all keys will remain the same. In the case
    where the total value of the distribution is 0, do nothing.

    >>> dist = DiscreteDistribution()
    >>> dist['a'] = 1
    >>> dist['b'] = 2
    >>> dist['c'] = 2
    >>> dist['d'] = 0
    >>> dist.normalize()
    >>> list(sorted(dist.items()))
    [('a', 0.2), ('b', 0.4), ('c', 0.4), ('d', 0.0)]
    >>> dist['e'] = 4
    >>> list(sorted(dist.items()))
    [('a', 0.2), ('b', 0.4), ('c', 0.4), ('d', 0.0), ('e', 4)]
    >>> empty = DiscreteDistribution()
    >>> empty.normalize()
    >>> empty
    {}
    """
    "*** YOUR CODE HERE ***"
    total = self.total()  # get the sum of all values

    # Avoid dividing by zero
    if (total == 0): 
        return

    # Normalize each value
    for key in self:  
        self[key] /= total  
    # raiseNotDefined()

def sample(self):
    """
    Draw a random sample from the distribution and return the key, weighted
    by the values associated with each key.

    >>> dist = DiscreteDistribution()
    >>> dist['a'] = 1
    >>> dist['b'] = 2
    >>> dist['c'] = 2
    >>> dist['d'] = 0
    >>> N = 100000.0
    >>> samples = [dist.sample() for _ in range(int(N))]
    >>> round(samples.count('a') * 1.0/N, 1)  # proportion of 'a'
    0.2
    >>> round(samples.count('b') * 1.0/N, 1)
    0.4
    >>> round(samples.count('c') * 1.0/N, 1)
    0.4
    >>> round(samples.count('d') * 1.0/N, 1)
    0.0
    """
    "*** YOUR CODE HERE ***"
    # Generate random point in the weighted range
    total = self.total() 
    rand_value = random.random() * total  

    # Increment cumulative weight
    cumulative = 0.0
    for key, weight in self.items():
        cumulative += weight 
        if (rand_value < cumulative):  # check if random number falls within range
            return key
    # raiseNotDefined()


def getObservationProb(self, noisyDistance, pacmanPosition, ghostPosition, jailPosition):
    """
    Return the probability P(noisyDistance | pacmanPosition, ghostPosition).
    """
    "*** YOUR CODE HERE ***"
    # Special Case: Ghost is in jail
    if (ghostPosition == jailPosition):
        return 1 if noisyDistance is None else 0

    # Special Case: Ghost is not in jail & distance none
    if noisyDistance is None:
        return 0.0
    
    trueDistance = manhattanDistance(pacmanPosition, ghostPosition) # compute manhattan distance
    return busters.getObservationProbability(noisyDistance, trueDistance)
    # raiseNotDefined()


def observeUpdate(self, observation, gameState):
    """
    Update beliefs based on the distance observation and Pacman's position.

    The observation is the noisy Manhattan distance to the ghost you are
    tracking.

    self.allPositions is a list of the possible ghost positions, including
    the jail position. You should only consider positions that are in
    self.allPositions.

    The update model is not entirely stationary: it may depend on Pacman's
    current position. However, this is not a problem, as Pacman's current
    position is known.
    """
    "*** YOUR CODE HERE ***"
    # Precondition: Check for jail condition first
    if observation is None:
        self.beliefs = util.Counter()
        self.beliefs[self.getJailPosition()] = 1.0
        return

    # Iterate over all positions 
    pacmanPosition = gameState.getPacmanPosition()
    jailPosition = self.getJailPosition()

    # Update beliefs with getObservationProb() function
    for position in self.allPositions:
        prob = self.getObservationProb(observation, pacmanPosition, position, jailPosition)
        self.beliefs[position] *= prob

    self.beliefs.normalize()
    # raiseNotDefined()


def elapseTime(self, gameState):
    """
    Predict beliefs in response to a time step passing from the current state.

    The transition model is not entirely stationary: it may depend on Pacman's
    current position. However, this is not a problem, as Pacman's current position is known.
    """
    newBeliefs = util.Counter()  # empty belief distribution

    # Iterate through all possible previous ghost positions
    for prevPos in self.allPositions:  
        newPosDist = self.getPositionDistribution(gameState, prevPos)  # transition model
        prevBelief = self.beliefs[prevPos]  # previous probability

        # Update belief at newPos
        for newPos, prob in newPosDist.items():  
            newBeliefs[newPos] += prevBelief * prob

    newBeliefs.normalize()  

    self.beliefs = newBeliefs
    #raiseNotDefined()