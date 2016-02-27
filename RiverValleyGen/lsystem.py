import turtle
import random
from lsystemParser import parseL_SystemString, parameterSubstitutuion

# String representation
def symbolToString(self, symbol):
    output = str(symbol[0])
    if symbol[1] is not None:
        output += "("
        for i in range(len(symbol[1])):
            output += symbol[1][i]
            if i < len(symbol[1]):
                output += ","
        output += ")"
    return output

##############################################################
# Stores and applies the rules for the l-system
##############################################################
class Rules:
    def __init__(self):
        self.rules = {}
        # store the previous iterations numeric value of a parameter to be applied to the next iterations variables
        self.parameterValues = [0, 0]

    def addRule(self, label, rule):
        self.rules[label] = rule

    # process the symbol parameters
    def processParameters(self, parameters):
        order = 0
        print str(parameters)
        if len(parameters) > 0:
            # order is represented by the first parameter
            order = parameters[0]
            # is it a variable?
            if order == 'o':
                # apply the previous parameter value to the current parameter variable
                self.parameterValues[0] = self.parameterValues[0]
            else:
                # get the numeric value of a parameter
                self.parameterValues[0] = order

    # apply context sensitive, parameterised, stochastic rules from a symbol
    def applyRule(self, symbol):
        print str(symbol)
        production = ""

        # Check that this symbol has a rule
        if self.rules.has_key(symbol[0]):
            randomFloat = random.random()
            probability = 0

            # Check we have some parameters
            if symbol[1] is not None:
                self.processParameters(symbol[1])

            # Use the accumulated probability to get the appropriate rule for the current random number
            for i in range(len(self.rules[symbol[0]])):
                probability += self.rules[symbol[0]][i][0]
                if randomFloat < probability:
                    # instanciate the rule body parameter variables with thier numeric values
                    ruleBody = parameterSubstitutuion(self.rules[symbol[0]][i][1], zip(['o', 's'], self.parameterValues))
                    return ruleBody

        else:
            return symbol[0]

##############################################################
# Run the l-system
##############################################################
def lsystem(axiom, rules, iterations):
    production = ""

    symbols = parseL_SystemString(axiom)
    print str(symbols)

    for symbol in symbols:
        # Expand symbol get parameters if any
        #current = parseSymbol(symbol)
        # apply any applicable production rules
        production += rules.applyRule(symbol)

    # Recursive l-system implementation, stop when iterations equals zero
    if iterations > 0:
        return lsystem(production, rules, iterations - 1)
    else:
        return production
