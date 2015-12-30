from random import randint

# Returns a single roll of a die with the specified number of sides
def rollDie(sides):
    return randint(1, sides)


# Returns the total result (sum) of the specified number of die rolls with the given die
def rollDice(number, sides):
    rolls = []
    for _ in range(number):
        rolls.append(rollDie(sides))
    # print 'Rolls: {0} = {1}'.format(rolls, sum(rolls))
    return sum(rolls)


def applyModifierToResult(result, operator, modifier):
    original_result = result
    if operator == '+':
        result += modifier
    elif operator == '-':
        result -= modifier
    elif operator == '*':
        result *= modifier
    elif operator == '/' and modifier > 0:
        result /= modifier
    # print 'Modified: {0} {1} {2} = {3}'.format(original_result, operator, modifier, result)
    return result


def roll(number, sides, operator, modifier):
    number = int(number)
    sides = int(sides)
    modifier = int(modifier)
    result = rollDice(number, sides)
    if(operator and modifier):
        #print 'Modifying total of {0} by {1} {2}'.format(result, operator, modifier)
        result = applyModifierToResult(result, operator, modifier)
    return result

def test():
    return 'What is love?'