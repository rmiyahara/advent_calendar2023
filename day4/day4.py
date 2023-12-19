import argparse

# Creates logs when set to true through cmd line args
debug = False

# Class used to hold the entire input. Can loop through games to get point totals
class GameSet:
    def __init__(self, input: list[str]):
        self.num_games = len(input) + 1
        self.games: dict[int, Game] = {}
        for line in input:
            game_for_line = Game(line)
            self.games[game_for_line.card_num] = game_for_line
    
    def get_point_total(self) -> int:
        total = 0
        for key in self.games:
            if (debug):
                print("[DEBUG] Game: %s has %s points" % (self.games[key].card_num, self.games[key].get_points()))
            total += self.games[key].get_points()
        return total
    
    def get_total_scratch_cards(self) -> int:
        copies: dict[int, int] = {}
        # Account for the current card
        for key in self.games:
            copies[key] = 1

        for i in range(1, self.num_games):
            if (debug):
                print("[DEBUG] Processing card: %d with %d matching numbers" % (i, self.games[i].matching_num_count))
            # Add copies
            if (self.games[i].matching_num_count > 0):
                for j in range(1, self.games[i].matching_num_count + 1):
                    # Make sure the card we're copying exists
                    if (self.games[i + j]):
                        copies[i + j] += copies[i]

        if (debug):
            for key in copies:
                print("[DEBUG] Card: %s has %s copies" % (key, copies[key]))
        total = 0
        for key in copies:
            total += copies[key]
        return total

# Class used to parse each line of a game
class Game:
    def __init__(self, input: list[str]):
        self.card_num = self.parse_card_num(input)
        self.winning_nums = self.parse_winning_nums(input)
        self.nums_owned = self.parse_nums_owned(input)
        self.matching_num_count = self.get_matching_num_count()

    def parse_card_num(self, input_line: str) -> int:
        # In format of 'Card X'
        card = input_line.split(': ')[0]
        return int(card.split(' ')[-1].strip())
    
    # Takes in a string containing numbers and converts them to an int list
    def numbers_in_string_to_int_list(self, nums_as_str: str) -> list[int]:
        nums_list = []
        for num in nums_as_str.split(' '):
            if (num != ''):
                nums_list.append(int(num.strip()))
        return nums_list
    
    # Parses the Game and grabs the list of winning numbers
    def parse_winning_nums(self, input_line: str) -> list[int]:
        if (debug):
            print("[DEBUG] Parsing winning numbers...")

        # Winning numbers are displayed first
        semicolon_index = input_line.find(':')
        vertical_bar_index = input_line.find('|')
        if (semicolon_index < 0 or vertical_bar_index < 0):
            return []
        nums_list = self.numbers_in_string_to_int_list(input_line[semicolon_index + 1:vertical_bar_index].strip())

        if (debug):
            print('[DEBUG] Nums parsed: ' + str(nums_list))
        return nums_list
    
    # Parses the Game and grabs the list of numbers owned by the player
    def parse_nums_owned(self, input_line: str) -> list[int]:
        if (debug):
            print('[DEBUG] Parsing numbers owned...')

        # Owned numbers are displayed second, after the vertical bar
        vertical_bar_index = input_line.find('|')
        if (vertical_bar_index < 0):
            return []
        nums_list = self.numbers_in_string_to_int_list(input_line[vertical_bar_index + 1:].strip())
    
        if (debug):
            print('[DEBUG] Nums parsed: ' + str(nums_list))
        return nums_list
    
    # Returns the number of matching numbers in a game
    def get_matching_num_count(self):
        matching_num_count = 0
        for nums in self.nums_owned:
            if (nums in self.winning_nums):
                matching_num_count += 1

        return matching_num_count

    # Returns the points a card is worth based on the amount of matching numbers
    def get_points(self) -> int:
        if (self.matching_num_count < 1):
            return 0
        return 2 ** (self.matching_num_count - 1)


def main():
    # Command line argument parsing
    parser = argparse.ArgumentParser(description='A script to run day 4 of the advent calendar.')
    parser.add_argument('--test', action = 'store_true', help = 'Run the program with the test data')
    parser.add_argument('--debug', action = 'store_true',  help='Runs code with logging statements for debugging')
    args = parser.parse_args()

    global debug
    debug = args.debug

    file_name = ''
    if (args.test):
        file_name = './day4/day4_test_input.txt'
    else:
        file_name = './day4/day4_input.txt'

    # Parse input and create the GameSet to hold it
    with open(file_name, 'r') as input_file:
        input = []
        # Set input_grid's values
        for line in input_file:
            input.append(line.strip())
        # print("Game total is: " + str(GameSet(input).get_point_total()))
        print("Scratch Card total is: " + str(GameSet(input).get_total_scratch_cards()))

    return 0

if __name__ == "__main__":
    main()
