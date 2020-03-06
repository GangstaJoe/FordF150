# Helper functions and classes
from collections import deque
import copy
import random

# Coordinates.  To create it, pass in a dictionary that has an x and a y value
class Coord:
    def __init__(self, d={'x': 0, 'y': 0}):
        self.x = d['x']
        self.y = d['y']

    def __str__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

# returns the resulting Coordinate for moving from start in direction
def moveTo(start, direction):
    loc2 = copy.deepcopy(start)

    if direction == "left":
        loc2.x = loc2.x - 1
    if direction == "right":
        loc2.x = loc2.x + 1
    if direction == "up":
        loc2.y = loc2.y - 1
    if direction == "down":
        loc2.y = loc2.y + 1
    return loc2


# Takes the start Coord, returns a list of possible directions that don't include obstacles
def getNewCoords(start, obstacles):
    newCoords = []

    newCoord = moveTo(start, "left")
    if not newCoord in obstacles:
        newCoords.append((newCoord, "left"))
    newCoord = moveTo(start, "right")
    if not newCoord in obstacles:
        newCoords.append((newCoord, "right"))
    newCoord = moveTo(start, "up")
    if not newCoord in obstacles:
        newCoords.append((newCoord, "up"))
    newCoord = moveTo(start, "down")
    if not newCoord in obstacles:
        newCoords.append((newCoord, "down"))

    random.shuffle(newCoords)
    return newCoords



# Takes Coordinate of head in start, list of Coordinates for targets, list of Coordinates for obstacles
# returns direction if there is one, or 'none' if there is not
def floodForTarget (start, targets, obstacles):
    head = (start, 'none')

    # locations to vist
    toVisit = deque()
    # Locations we've visited
    visited = set()
    # List of predecessors for each direction
    predecessorList = {}
    visited.add(head[0])

    # make sure the inital moves are good moves
    initialMoves = getNewCoords(head[0], obstacles)
    for m in initialMoves:
        if not m[0] in obstacles:
            toVisit.append(m)
            predecessorList[m] = head
            if m[0] in targets:
                return m[1]

    # While we still have places to go and things to see
    while len(toVisit) > 0:
        # get the next place to visit
        p = toVisit.popleft()
        # generate the moves from it
        moves = getNewCoords(p[0], obstacles)
        # for each move generated
        for m in moves:
            # if we've already visited, don't go back!
            if m[0] in visited:
                continue
            # add it to visited
            visited.add(m[0])
            # add it to our list to leave from
            toVisit.append(m)
            # make a note of its predecessor
            predecessorList[m] = p
            # if we have found a target to go after
            if m[0] in targets:
                # unwind to find the next move
                # self.debug('head:' + str(head[0]))
                while predecessorList[m] != head:
                    # self.debug('prevMove:'+str((predecessorList[m])[0]))
                    m = predecessorList[m]
                # return the move
                return m[1]
