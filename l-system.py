import turtle
import random
import re

rawSymbols = 'F'
symbolPattern = '[\+-' + rawSymbols + '\[\]]'
parameterPattern = '\d+'
parameterListPattern = '\(.+?\)'
parameterisedSymbolPattern = symbolPattern + parameterListPattern + '|' + symbolPattern

def getSymbolPlusArgs(symbol):
    symboldata = []
    if len(symbol) > 1:
        parameterisedSymbol = re.match(parameterisedSymbolPattern, symbol)
        rawsymbol = re.match(rawSymbols, parameterisedSymbol.group(0))
        symboldata.append(rawsymbol.group(0))
        if parameterisedSymbol is not None:
            parameters = re.findall(parameterPattern, symbol)
            if parameters is not None:
                symboldata.extend(parameters)
            else:
                print 'Error: Parameters not found in parameterised symbol '
        else:
            print 'Error: Invalid parameterised symbol'
    return symboldata

def lsystem(axiom, rules, iterations):
    production = ""
    for symbol in re.findall(parameterisedSymbolPattern, axiom):
        symbolPlusParams = getSymbolPlusArgs(symbol)
        print str(symbolPlusParams)
        if rules.has_key(symbol):
            production += rules[symbol]
        else:
            production += symbol
    if iterations > 0:
        return lsystem(production, rules, iterations - 1)
    else:
        return production

def draw(instructions):
    stack = []
    turtle.up()
    turtle.setup(800, 600)
    turtle.setpos(0, -300)
    turtle.setheading(90)
    turtle.color("blue")
    turtle.down()
    for symbol in re.findall(parameterisedSymbolPattern, instructions):
        symbolPlusParams = getSymbolPlusArgs(symbol)
        if len(symbolPlusParams) > 0:
            instruction = symbolPlusParams[0]
        else:
            instruction = symbol
            
        if instruction == "F":
            turtle.forward(random.triangular(5, 50))
        if instruction == "+":
            turtle.left(random.triangular(10, 50))
        if instruction == "-":
            turtle.right(random.triangular(10, 50))
        if instruction == "[":
            stack.append(turtle.pos())
        if instruction == "]":
            pos = stack.pop()
            turtle.up()
            turtle.setpos(pos[0], pos[1])
            turtle.down()

axiom = "F"
rules = {"F":"F-F+F[+F(30)][-F(30)]"}

#print lsystem(axiom, rules, 2)
draw(lsystem(axiom, rules, 2))
