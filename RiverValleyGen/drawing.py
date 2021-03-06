from lsystem import parseL_SystemString
from lsystemParser import parseL_SystemString, parameterSubstitutuion
import turtle
import random
import re

##############################################################
# initialise turtle
##############################################################
def initTurtle(windowWidth, windowHeight):
    turtle.mode("logo")
    turtle.color("blue")
    turtle.setup(windowWidth, windowHeight)

    # Start position at bottom centre of window
    turtle.up()
    turtle.setpos(0, -(windowHeight / 2))
    turtle.down()

##############################################################
# draw result
##############################################################
def draw(instructions, order):
    stack = []

    #### Variables concerned with river characteristics ####
    
    # Store the current base angle so we know when to stop decaying the angle
    baseAngle = 45
    # Supplies the 'mod' parameter to the random triangular function
    # to give an angle bias for river meanders
    currentAngle = 45

    # convert the l-system string to turtle instructions
    for symbol in parseL_SystemString(instructions):
        minRange = 1
        maxRange = 10
        mode = 5
        
        if symbol[0] == "C":
            #if expanded.parameters is not None:
            turtle.forward(random.randint(5, 30))
        if symbol[0] == "+":
            #if expanded.parameters is not None:
            #print "currentAngle = " + str(currentAngle)
            angleToTurn = random.triangular(0, 90, currentAngle)
            #print "angleToTurn = " + str(angleToTurn)
            turtle.left(angleToTurn)
        if symbol[0] == "-":
            #if expanded.parameters is not None:
            #print "currentAngle = " + str(currentAngle)
            angleToTurn = random.triangular(0, 90, currentAngle)
            #print "angleToTurn = " + str(angleToTurn)
            turtle.right(angleToTurn)
        if symbol[0] == "[":
            stack.append(turtle.pos())
        if symbol[0] == "]":
            pos = stack.pop()
            turtle.up()
            turtle.setpos(pos[0], pos[1])
            turtle.down()
