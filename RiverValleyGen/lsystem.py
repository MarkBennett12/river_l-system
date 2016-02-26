import turtle
import random
import re

##############################################################
# Stores a symbol and any associated parameters
# Generates the symbol data from a string on construction
##############################################################
class ParameterisedSymbol:
    # regex to extract symbols plus parameters
    pat_parameterList = r'\(.*?\)'
    pat_baseSymbols = r'[\[\]+-C]'
    pat_symbolAndParameters = r'(?:' + pat_baseSymbols +')' + '(?:' + pat_parameterList + ')?'
    pat_splitSymbolAndParameters = r'(' + pat_baseSymbols +')' + '(' + pat_parameterList + ')?'

    # regex to extract numbers
    pat_int = r'\d+'
    pat_float = r'\d+\.\d+'
    pat_number = pat_int + r'|' + pat_float
    
    # regex to extract parameter variables, these must have specific values, currently 'o' for order
    pat_variable = r'[os]'
    
    # regex to extract parameters
    pat_parameter = pat_variable + r'|' + pat_number

    # construct symbol data from string with regex
    def __init__(self, symbolString):
        # extract symbol from symbol string
        splitSymbol = re.match(self.pat_splitSymbolAndParameters, symbolString)

        if splitSymbol is not None:
            self.representation = splitSymbol.group(1)

            # if parameters exist extract them from symbol string into a list
            if splitSymbol.group(2) is not None:
                self.parameters = re.findall(self.pat_parameter, splitSymbol.group(2))
            else:
                self.parameters = None
        else:
            self.representation = None
            self.parameters = None

    # String representation
    def __str__(self):
        output = str(self.representation)
        if self.parameters is not None:
            output += "("
            for i in range(len(self.parameters)):
                output += self.parameters[i]
                if i < len(self.parameters):
                    output += ","
            output += ")"
        return output

##############################################################
# Put all the rules into the ruleset class
##############################################################
def setRules(ruleSet):
    ruleSet.addRule("C",
                        [
                            (0.3, "C(o, s)+C(o, s)"),
                            (0.3, "C(o, s)-C(o, s)"),
                            (0.2, "C(o, s)+C(o, s)[-C(o, 30)]"),
                            (0.2, "C(o, s)-C(o, s)[+C(o, 30)]")
                        ]
                    )

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
        if self.rules.has_key(symbol.representation):
            randomFloat = random.random()
            probability = 0

            # Check we have some parameters
            if symbol.parameters is not None:
                self.processParameters(symbol.parameters)

            # Use the accumulated probability to get the appropriate rule for the current random number
            for i in range(len(self.rules[symbol.representation])):
                probability += self.rules[symbol.representation][i][0]
                if randomFloat < probability:
                    # instanciate the rule body parameter variables with thier numeric values
                    ruleBody = re.sub(r'o', str(self.parameterValues[0]), self.rules[symbol.representation][i][1])
                    ruleBody = re.sub(r's', str(self.parameterValues[1]), ruleBody)
                    return ruleBody

        else:
            return symbol.representation

##############################################################
# Run the l-system
##############################################################
def lsystem(axiom, rules, iterations):
    production = ""

    symbols = re.findall(ParameterisedSymbol.pat_symbolAndParameters, axiom)

    for i in range(len(symbols)): 
        # Expand symbol get parameters if any
        current = ParameterisedSymbol(symbols[i])
        # apply any applicable production rules
        production += rules.applyRule(current)

    # Recursive l-system implementation, stop when iterations equals zero
    if iterations > 0:
        return lsystem(production, rules, iterations - 1)
    else:
        return production
