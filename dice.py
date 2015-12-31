from random import randint


class Dice:
    def __init__(self):
        self.name = 'Dice'

    # Returns a single roll of a die with the specified number of sides
    @staticmethod
    def roll_die(sides):
        return randint(1, sides)

    # Returns the total result (sum) of the specified number of die rolls with the given die
    @staticmethod
    def roll_dice(number, sides):
        rolls = []
        for _ in range(number):
            rolls.append(Dice.roll_die(sides))
        # print 'Rolls: {0} = {1}'.format(rolls, sum(rolls))
        return sum(rolls)

    @staticmethod
    def apply_modifier_to_result(result, operator, modifier):
        # original_result = result
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

    # Roll the dice, apply the modifiers, return the result
    @staticmethod
    def roll(number, sides, operator, modifier):
        number = int(number)
        sides = int(sides)
        result = Dice.roll_dice(number, sides)
        if operator and modifier:
            modifier = int(modifier)
            #print 'Modifying total of {0} by {1} {2}'.format(result, operator, modifier)
            result = Dice.apply_modifier_to_result(result, operator, modifier)
        return result
