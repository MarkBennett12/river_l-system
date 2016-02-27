from lsystem import *
from drawing import *

##############################################################
# The main script sets up the l-system then runs it
##############################################################
axiom = "C(4, 0)"

rules = Rules()
rules.addRule("C",
                    [
                        (0.3, "C(o, s)+C(o, s)"),
                        (0.3, "C(o, s)-C(o, s)"),
                        (0.2, "C(o, s)+C(o, s)[-C(o, 30)]"),
                        (0.2, "C(o, s)-C(o, s)[+C(o, 30)]")
                    ]
                )

width = 800
height = 600
initTurtle(width, height)

productionString = lsystem(axiom, rules, 3)
# print the string for debugging purposes
print "reulting string = " + productionString
draw(productionString, 8)
