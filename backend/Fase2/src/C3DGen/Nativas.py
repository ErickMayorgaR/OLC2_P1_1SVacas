def addTrue():
    funcionTrue = 'func print_true_armc(){\n'
    funcionTrue += addPrintf("c", "116")
    funcionTrue += addPrintf("c", "114")
    funcionTrue += addPrintf("c", "117")
    funcionTrue += addPrintf("c", "101")
    funcionTrue += '}\n\n'
    return funcionTrue

def addFalse():
    funcionFalse = 'func print_false_armc(){\n'
    funcionFalse += addPrintf("c", "102")
    funcionFalse += addPrintf("c", "97")
    funcionFalse += addPrintf("c", "108")
    funcionFalse += addPrintf("c", "115")
    funcionFalse += addPrintf("c", "101")
    funcionFalse += '}\n\n'
    return funcionFalse

def addMathError():
    functionMathError = 'func print_math_error_armc(){\n'
    functionMathError += addPrintf("c", "77")
    functionMathError += addPrintf("c", "97")
    functionMathError += addPrintf("c", "116")
    functionMathError += addPrintf("c", "104")
    functionMathError += addPrintf("c", "69")
    functionMathError += addPrintf("c", "114")
    functionMathError += addPrintf("c", "114")
    functionMathError += addPrintf("c", "111")
    functionMathError += addPrintf("c", "114")
    functionMathError += addPrintf("c", "10")
    functionMathError += '}\n\n'
    return functionMathError

def addBoundsError():
    functionBoundsError = 'func print_bounds_error_armc(){\n'
    functionBoundsError += addPrintf("c", "66")
    functionBoundsError += addPrintf("c", "111")
    functionBoundsError += addPrintf("c", "117")
    functionBoundsError += addPrintf("c", "110")
    functionBoundsError += addPrintf("c", "100")
    functionBoundsError += addPrintf("c", "115")
    functionBoundsError += addPrintf("c", "69")
    functionBoundsError += addPrintf("c", "114")
    functionBoundsError += addPrintf("c", "114")
    functionBoundsError += addPrintf("c", "111")
    functionBoundsError += addPrintf("c", "114")
    functionBoundsError += addPrintf("c", "10")
    functionBoundsError += '}\n\n'
    return functionBoundsError

def addPrintf(typePrint, value): #Añade un printf
    return 'fmt.Printf(\"%' + typePrint + '\",' + value + ');\n'