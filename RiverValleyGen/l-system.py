import turtle
import random
import re

class ParameterisedSymbol:
    
    # regex to extract symbols plus parameters
    pat_parameterList = r'\(.*?\)'
    pat_baseSymbols = r'[\[\]+-F]'
    pat_symbolAndParameters = r'(?:' + pat_baseSymbols +')' + '(?:' + pat_parameterList + ')?'
    pat_splitSymbolAndParameters = r'(' + pat_baseSymbols +')' + '(' + pat_parameterList + ')?'

    # regex to extract parameters
    pat_parameterValue = r'\d+(?:.\d+)?'

    def __init__(self, symbolString):
        # extract symbol from symbol string
        splitSymbol = re.match(self.pat_splitSymbolAndParameters, symbolString)
        self.mySymbol = splitSymbol.group(1)

        # if paraemters exist extract them from symbol string into a list
        if splitSymbol.group(2) is not None:
            parameters = re.findall(self.pat_parameterValue, splitSymbol.group(2))
            # the parameters need to be integers
            self.myParameterList = [int(i) for i in parameters]
        else:
            self.myParameterList = None

    def __str__(self):
        output =str(self.mySymbol)
        if self.myParameterList is not None:
            output += ", " + str(self.myParameterList)
        return output

# apply context sensitive, parameterised, stochastic rules
def applyRule(rules, symbol, preceeding, succeding):
    production = ""

    if rules.has_key(symbol.mySymbol):
        production += rules[symbol.mySymbol]
    else:
        production += symbol.mySymbol

    return production

# run l-system
def lsystem(axiom, rules, iterations):
    production = ""
    precedingSymbol = ''
    succeedingSymbol = ''
    
    symbols = re.findall(ParameterisedSymbol.pat_symbolAndParameters, axiom)
        
    for i in range(len(symbols)):
        
        # get the context
        if i > 0:
            precedingSymbol = symbols[i-1]
        if i < len(symbols) - 1:
            succeedingSymbol = symbols[i + 1]

        # Expand symbol get parameters if any
        current = ParameterisedSymbol(symbols[i])
        
        # Expand context
        preceding = None
        if len(precedingSymbol) > 0:
            preceding = ParameterisedSymbol(precedingSymbol)

        succeeding = None
        if len(succeedingSymbol) > 0:
            succeeding = ParameterisedSymbol(succeedingSymbol)

        # apply any applicable production rules
        production += applyRule(rules, current, preceding, succeeding)
        
    if iterations > 0:
        return lsystem(production, rules, iterations - 1)
    else:
        return production

# draw result
def draw(instructions):   
    stack = []
    
    turtle.up()
    turtle.setup(800, 600)
    turtle.setpos(0, -300)
    turtle.setheading(90)
    turtle.color("blue")
    turtle.down()

    # convert the l-system string to turtle instructions
    for symbol in re.findall(ParameterisedSymbol.pat_symbolAndParameters, instructions):
        minRange = 1
        maxRange = 10
        mode = 5
        expanded = ParameterisedSymbol(symbol)        
        
        if expanded.mySymbol == "F":
            if expanded.myParameterList is not None:
                minRange = expanded.myParameterList[0]
                maxRange = expanded.myParameterList[1]
            turtle.forward(random.randint(minRange, maxRange))
        if expanded.mySymbol == "+":
            if expanded.myParameterList is not None:
                minRange = expanded.myParameterList[0]
                maxRange = expanded.myParameterList[1]
                mode = expanded.myParameterList[1]
            turtle.left(random.triangular(minRange, maxRange, mode))
        if expanded.mySymbol == "-":
            if expanded.myParameterList is not None:
                minRange = expanded.myParameterList[0]
                maxRange = expanded.myParameterList[1]
                mode = expanded.myParameterList[1]
            turtle.right(random.triangular(minRange, maxRange, mode))
        if expanded.mySymbol == "[":
            stack.append(turtle.pos())
        if expanded.mySymbol == "]":
            pos = stack.pop()
            turtle.up()
            turtle.setpos(pos[0], pos[1])
            turtle.down()

axiom = "F"

# set up rules
rules = {}
rules["F"] = "F(10, 50)-(5, 65, 40)F(10, 50)+(5, 65, 40)F[+(5, 45, 20)F(10, 50)][-(5, 45, 20)F(10, 50)]"


productionString = lsystem(axiom, rules, 2)
print "reulting string = \n" + productionString + "\n"
draw(productionString)
