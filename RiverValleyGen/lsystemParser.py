import re

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

##############################################################
# Takes a string representing a complete string and associated
# parameters and returns the symbols as a list of tuples containing
# the symbol and the parameters
##############################################################
def parseL_SystemString(l_systemString):
    symbolTupleArray = []
    symbols = re.findall(pat_symbolAndParameters, l_systemString)
    for symbol in symbols:
        symbolTupleArray.append(parseSymbol(symbol))
    return symbolTupleArray

##############################################################
# Takes a string representing a single symbol and associated
# parameters and returns the symbol as a tuple containing the
# symbol and the parameters
##############################################################
def parseSymbol(symbolString):
    # extract symbol from symbol string
    splitSymbol = re.match(pat_splitSymbolAndParameters, symbolString)

    if splitSymbol is not None:
        representation = splitSymbol.group(1)

        # if parameters exist extract them from symbol string into a list
        if splitSymbol.group(2) is not None:
            parameters = re.findall(pat_parameter, splitSymbol.group(2))
        else:
            parameters = None
    else:
        representation = None
        parameters = None
    return (representation, parameters)

##############################################################
# Takes a string representing the rule body containing
# unassigned variables, and a list of tuples representing
# variable names (symbols) and values to assign to the variables
# and converts all the variable symbols in the rule body into
# the corresponding values. the new rule body string is returned
##############################################################
def parameterSubstitutuion(ruleBody, parameterBindings):
    print "parameterSubstitutuion : rulebody = " + str(ruleBody) + ", parameterBindings = " + str(parameterBindings)
    substitutedString = ruleBody
    for parameter in parameterBindings:
        substitutedString = re.sub(parameter[0], str(parameter[1]), substitutedString)
    return substitutedString

