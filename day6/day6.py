import argparse

# Creates logs when set to true through cmd line args
debug = False

class Race:
    def __init__(self, time: int, distance: int):
        self.time = time
        self.distance_record = distance
        self.num_solutions = self.find_solutions()
        if (debug):
            print('[DEBUG] Race created with time: %d and distance: %d' % (self.time, self.distance_record))

    def find_solutions(self) -> int:
        num_solutions = 0
        i = self.time / 2
        while (i < self.time):
            if (self.distance_traveled(i) < self.distance_record):
                break
            if (i == self.time / 2 and self.time % 2 < 1):
                num_solutions += 1
            else:
                num_solutions += 2
            i += 1

        return num_solutions

    def distance_traveled(self, time_held: int) -> int:
        return time_held * (self.time - time_held)

class RaceSet:
    def __init__(self, file_input: list[str]):
        self.times: list[int] = self.parse_list(file_input[0])
        self.distances: list[int] = self.parse_list(file_input[1])

        # if (len(self.times) != len(self.distances)):
        #     raise ValueError('[ERROR] The number of times and distances does not match.')
        
        self.races: list[Race] = []
        for i in range(0, len(self.times)):
            self.races.append(Race(self.times[i], self.distances[i]))

    def parse_list(self, line: str) -> list[int]:
        temp_str = ''
        for chars in line.split(' '):
            if (chars.isdigit()):
                temp_str = temp_str + chars
        return [int(temp_str)]
    
    def product_of_solutions(self) -> int:
        product = 1
        for race in self.races:
            product *= race.num_solutions
        return product

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
        file_name = './day6/day6_test_input.txt'
    else:
        file_name = './day6/day6_input.txt'

    # Parse input and create the GameSet to hold it
    with open(file_name, 'r') as input_file:
        input = []
        # Set input_grid's values
        for line in input_file:
            input.append(line.strip())

        if (len(input) != 2):
            print('[ERROR] Invalid input file. File must have only 2 lines, one for time and one for distance.')
        set = RaceSet(input)
        print(set.product_of_solutions())
        
    return 0

if __name__ == "__main__":
    main()
