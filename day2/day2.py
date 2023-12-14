'''
Returns the id of the game given the input line as an int.
Ex. game_id('Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green') -> 1
Ex. game_id('Game 100: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green') -> 100
'''
def game_id(line: str) -> int:
    # Set to a list of size 2 where the first element is in the format of "Game X"
    game_and_number = line.split(':', 1)[0]
    # Grab just the number
    return int(game_and_number.split(' ')[1])

'''
Returns a dictionary with three string keys {red, green, blue} where each value is the
number of cubes used for that color in that round.
Ex. cubes_per_color_used_in_round('1 red, 2 green, 6 blue') -> { 'red': 1, 'green': 2, 'blue': 6 }
Ex. cubes_per_color_used_in_round('5 green, 2 blue') -> { 'red': 0, 'green': 5, 'blue': 2 }
'''
def cubes_per_color_used_in_round(line: str) -> dict[str, int]:
    color_dict = {}

    # i in format of 'X color'
    for i in line.split(', '):
        num_value = i.split(' ')[0]
        color_name = i.split(' ')[1]
        color_dict[color_name] = int(num_value)
        
    return color_dict

'''
Returns if a game is possible given the input line and number of each cubes.
Ex. is_game_possible('Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue', 12, 13, 14) -> True
Ex. is_game_possible('Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red', 12, 13, 14) -> False
'''
def is_game_possible(input: str, num_cubes: dict[str, int]) -> bool:
    # Records the maximum number of each color of cube used
    max_cubes_used = { 'red': 0, 'green': 0, 'blue': 0 }

    # Remove 'Game X: ' from input
    rounds = input.split(': ')[1]
    for round in rounds.split('; '):
        for key, value in cubes_per_color_used_in_round(round).items():
            if (max_cubes_used[key] < value):
                max_cubes_used[key] = value
    
    for key in num_cubes:
        if (max_cubes_used[key] > num_cubes[key]):
            return False
    return True

'''
Returns the power of each game. Power is determined by the product of the amount of cubes used for each color.
Ex. game_power('Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green') -> 48
Ex. game_power('Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red') -> 1560
'''
def game_power(input: str) -> int:
    # Records the maximum number of each color of cube used
    max_cubes_used = { 'red': 0, 'green': 0, 'blue': 0 }

    # Remove 'Game X: ' from input
    rounds = input.split(': ')[1]
    for round in rounds.split('; '):
        for key, value in cubes_per_color_used_in_round(round).items():
            if (max_cubes_used[key] < value):
                max_cubes_used[key] = value
    
    power_score = 1
    for key, value in max_cubes_used.items():
        power_score *= value
    return power_score

def main():
    total = 0
    # num_cubes = { 'red': 12, 'green': 13, 'blue': 14 }
    with open('./day2/day2.input.txt', 'r') as input_file:
        for line in input_file:
            # if (is_game_possible(line.strip(), num_cubes)):
            #     total += game_id(line.strip())
            total += game_power(line.strip())

    print(total)
    return total

if __name__ == "__main__":
    main()