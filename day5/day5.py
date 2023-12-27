import argparse
from typing import Tuple 

# Creates logs when set to true through cmd line args
debug = False

# Holds the seed start number and the range for the length the sequence continues
class Seed:
    def __init__(self, num, range):
        self.num = num
        self.range = range

# Holds all the input for seeds and every map
class Almanac:
    def __init__(self, input: list[str]):
        self.seeds: list[Seed] = self.parse_seeds(input[0])

        self.maps: list[SourceDestinationMap] = []
        transforming_map_lines = []
        input.append('')
        for line in input[2:]:
            if (line == ''):
                self.maps.append(SourceDestinationMap(transforming_map_lines))
                transforming_map_lines = []
            else:
                transforming_map_lines.append(line)
        
    
    def parse_seeds(self, seed_line: str) -> list[Seed]:
        nums_list = seed_line.split(': ')[-1]
        split_nums = nums_list.split(' ')
        input_seed_list: list[Seed] = []
        if (len(split_nums) % 2 > 0):
            return input_seed_list
        for i in range(0, len(split_nums), 2):
            if (split_nums[i].isdigit() and split_nums[i + 1].isdigit()):
                input_seed_list.append(Seed(split_nums[i], split_nums[i + 1]))

        if (debug):
            print("[DEBUG] Seed numbers: ")
            for seed in input_seed_list:
                print("[DEBUG] Num %s, range %s" % (seed.num, seed.range))
        return input_seed_list
    
    def transform_seeds(self) -> list[Seed]:
        for map in self.maps:
            for seed in self.seeds:
                if (map.find_destination_for_source_in_map):
                # If we find a match
                    # Move seeds in range to a new seed
                    # Add remaining original seeds

        return seed_to_final_destination
    
    def lowest_location(self) -> int:
        num_list = self.transform_seeds()
        lowest = num_list[0]
        for num in num_list:
            if (num < lowest):
                lowest = num
        return lowest
        
    
class SourceDestinationMap:
    def __init__(self, input: list[str]):
        self.source_name = input[0].split('-')[0]
        self.destination_name = input[0].split('-')[2].split(' ')[0]
        self.transformation: list[TransformLine] = []
        for line in input[1:]:
            self.transformation.append(TransformLine((int(line.split(' ')[0]), int(line.split(' ')[1]), int(line.split(' ')[2]))))

    def find_destination_for_source_in_map(self, source):
        for rule in self.transformation:
            destination_num = rule.find_destination_from_source_for_line(source)
            if (destination_num != source):
                return destination_num
        return source

class TransformLine:
    def __init__(self, rules: Tuple[int, int, int]):
        self.destination_start = rules[0]
        self.source_start = rules[1]
        self.range = rules[2]
    
    # Takes in a source seed. Returns a list of Seeds after checking for intersection with the given Seed
    def find_destination_from_source_for_line(self, source: Seed):
        # Upper most source counts for seed and map
        seed_upper_bound = source.num + source.range - 1
        map_upper_bound = self.source_start + self.range - 1
        processed_seeds: list[Seed] = []
        
        # No intersection found
        if (seed_upper_bound < self.source_start or source.num > map_upper_bound):
            processed_seeds.append(source)
        
        # Handle source before hitting the map rule
        if (source.num < self.source_start):
            processed_seeds.append(Seed(source.num, self.source_start - source.num))
        # Handle source after passing map rule
        if (source.num + source.range > self.source_start + self.range):
            processed_seeds.append(Seed(map_upper_bound, seed_upper_bound - self.source_start + self.range)) # Might be a fencepost bug here
        
        if (source.num < self.source_start):
            if (seed_upper_bound > map_upper_bound):
                processed_seeds.append(Seed(self.destination_start, self.range))
            else:
                processed_seeds.append(Seed(self.destination_start, seed_upper_bound - self.source_start))
        else:
            if (source.num + source.range > self.source_start + self.range):
                processed_seeds.append(Seed(self.source_start + self.range - source.num + self.destination_start, self.source_start + self.range - source.num)) # TODO: Transform
            else:
                processed_seeds.append(Seed(source.num, source.range)) # TODO: Transform

        return processed_seeds

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
        file_name = './day5/day5_test_input.txt'
    else:
        file_name = './day5/day5_input.txt'

    with open(file_name, 'r') as input_file:
        input = []
        for line in input_file:
            input.append(line.strip())
        print(Almanac(input).seeds)

    return 0

if __name__ == "__main__":
    main()