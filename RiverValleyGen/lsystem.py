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

    # regex to extract number
    pat_number = r'\d+(?:.\d+)?'
    # regex to extract parameters
    pat_parameter = r'\w+(?:.\w+)?'

    # construct symbol data from string with regex
    def __init__(self, symbolString):
        # extract symbol from symbol string
        splitSymbol = re.match(self.pat_splitSymbolAndParameters, symbolString)

        if splitSymbol is not None:
            self.representation = splitSymbol.group(1)

            # if parameters exist extract them from symbol string into a list
            if splitSymbol.group(2) is not None:
                parameters = re.findall(self.pat_parameter, splitSymbol.group(2))
                # the parameters need to be integers
                self.parameters = [int(i) for i in parameters]
            else:
                self.parameters = None
        else:
            self.representation = None
            self.parameters = None

    # String representation
    def __str__(self):
        output =str(self.representation)
        if self.parameters is not None:
            output += ", " + str(self.parameters)
        return output

##############################################################
# Put all the rules into the ruleset class
##############################################################
def setRules(ruleSet):
    ruleSet.addRule("C",
                        [
                            (0.3, "C(10, 30)+C(10, 30)"),
                            (0.3, "C(10, 30)-C(10, 30)"),
                            (0.2, "C(10, 30)+C(10, 30)[-C(10, 30)]"),
                            (0.2, "C(10, 30)-C(10, 30)[+C(10, 30)]")
                        ]
                    )

##############################################################
# Stores and applies the rules for the l-system
##############################################################
class Rules:
    def __init__(self):
        self.rules = {}

    def addRule(self, label, rule):
        self.rules[label] = rule

    # apply context sensitive, parameterised, stochastic rules from a symbol
    def applyRule(self, symbol):
        production = ""

        # Check that this symbol has a rule
        if self.rules.has_key(symbol.representation):
            randomFloat = random.random()
            probability = 0

            # Use the accumulated probability to get the appropriate rule for the current random number
            for i in range(len(self.rules[symbol.representation])):
                probability += self.rules[symbol.representation][i][0]
                if randomFloat < probability:
                    return self.rules[symbol.representation][i][1]

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
