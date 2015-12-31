import re
import dice

# !roll
roll_command_regex = re.compile(ur'(?P<roll_command>^[!]\w+)', re.IGNORECASE)


class Parser:
    def __init__(self):
        self.roll_command_regex = roll_command_regex

    @staticmethod
    def parse_for_command(text):
        if re.search(roll_command_regex, text):
            return Parser.parse_roll_command(text)
        else:
            return None

    @staticmethod
    def parse_roll_command(text):
        # print 'Parsing roll command "{0}" ... '.format(text)
        regex = re.compile(ur'(?P<roll_command>^[!]\w+)\s*'
                           ur'(?P<number_of_dice>\d+)[d](?P<dice_sides>\d+)\s*'
                           ur'(?P<modifier>(?P<modifier_operator>[-+*/])\s*(?P<modifier_value>\d+))*', re.IGNORECASE)
        match = re.search(regex, text)
        if match:
            number_of_dice = match.group('number_of_dice')
            dice_sides = match.group('dice_sides')
            modifier_operator = match.group('modifier_operator')
            modifier_value = match.group('modifier_value')

            # print 'Match: {0}'.format(match.group())
            return dice.roll(number_of_dice, dice_sides, modifier_operator, modifier_value)
        else:
            print 'Invalid roll command syntax'
            return None
