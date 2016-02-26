from lsystem import *
from drawing import *

##############################################################
# The main script sets up the l-system then runs it
##############################################################
axiom = "C(4, 0)"

rules = Rules()
setRules(rules)

width = 800
height = 600
initTurtle(width, height)

productionString = lsystem(axiom, rules, 3)
# print the string for debugging purposes
print "reulting string = " + productionString
draw(productionString, 8)
