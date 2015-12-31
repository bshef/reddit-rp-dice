# reddit-rp-dice


## How to use
The bot will scan for comments in a given subreddit that contain valid commands, such as `!roll`,
and reply to those comments with the result of executing the specified command.


### Roll dice
`!roll 1d20` - rolls 1 20-sided die, and displays the result

`!roll 4d6` - rolls 4 6-sided dice, and displays the resulting sum

Keep the number of dice and dice sides reasonable.


### Roll dice with modifiers
`!roll 1d20 + 10` - rolls 1 20-sided die, adds 10, and displays the result

`!roll 4d6 - 10` - rolls 4 6-sided dice, subtracts 10 from the sum, and displays the result

`!roll 1d4 * 3` - rolls 1 4-sided die, multiples by 3, and displays the result

`!roll 1d100 / 10` - rolls 1 100-sided die, divides by 10, and displays the result

Keep the modifier value reasonable.


### Configuring the Bot
Modify the values in the `config.py` file to match those of your bot,
and the subreddit you wish the Bot to be active in.
