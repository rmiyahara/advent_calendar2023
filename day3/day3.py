# Holds the inputted grid
from enum import Enum

# Enum for what possible states a tile can have
class TileStatus(Enum):
    DOT = 1
    DIGIT = 2
    SYMBOL = 3

class Board:
    def __init__(self, input_grid: list[str]):
        self.input = input_grid
        self.height = len(self.input)
        if (self.height < 1):
            self.length = 0
        else:
            self.length = len(self.input[0])

    # Returns the status of the square in the desired location
    def check_square_status(self, i: int, j: int) -> TileStatus:
        # Check for out of bounds
        if (i >= self.height or i < 0 or
            j >= self.length or j < 0 or
            self.input[i][j] == '.'):
            return TileStatus.DOT
        elif (self.input[i][j].isdigit()):
            return TileStatus.DIGIT
        else:
            return TileStatus.SYMBOL
    
    # Returns the sum of the engine parts for the entire board
    def sum_of_part_numbers(self) -> int:
        total = 0
        for i in range(0, self.height):
            # Send a crawler down the row
            total += TileCrawler(i, self).sum_of_row()
        return total
    
    # Assumes gear is above or below i, j
    def num_gear_connections_in_adjacent_row(self, i: int, j: int) -> int:
        if (self.check_square_status(i, j) == TileStatus.DIGIT):
            return 1
        else:
            if (self.check_square_status(i, j - 1) == TileStatus.DIGIT and
                self.check_square_status(i, j + 1) == TileStatus.DIGIT):
                return 2
            elif (self.check_square_status(i, j - 1) == TileStatus.DIGIT or
                self.check_square_status(i, j + 1) == TileStatus.DIGIT):
                return 1
            else:
                return 0
    
    # Only call on a digit square
    def value_going_left(self, i: int, j: int) -> str:
        if (self.check_square_status(i, j) != TileStatus.DIGIT):
            return ''
        else:
            return self.value_going_left(i, j - 1) + self.input[i][j]
        
    def value_going_right(self, i: int, j:int) -> str:
        if (self.check_square_status(i, j) != TileStatus.DIGIT):
            return ''
        else:
            return self.input[i][j] + self.value_going_right(i, j + 1)
    
    # Used to check engine part numbers in the row above or below a gear
    def value_gear_ratio_in_adjacent_row(self, i: int, j: int) -> int:
        left = self.value_going_left(i, j - 1)
        right = self.value_going_right(i, j + 1)
        
        # Case for one number adjacent to gear
        if (self.check_square_status(i, j) == TileStatus.DIGIT):
            return int(left + self.input[i][j] + right)
        else:
            # Case for 2 different numbers adjacent to gear
            if (len(left) > 0 and len(right) > 0):
                return int(left) * int(right)
            # Case for one number to top left of the gear
            elif (len(left) > 0):
                return int(left)
            # Case for one number to top right of the gear
            elif (len(right) > 0):
                return int(right)
            else:
                return 1

    # Returns the sum of the engine parts for the entire board
    def sum_of_gear_ratios(self) -> int:
        total = 0
        for i in range(0, self.height):
            # Send a crawler down the row
            total += TileCrawler(i, self).gear_ratio()
        return total

class TileCrawler:

    def __init__(self, row_num: int,board: Board):
        # Holds the current row and the ones above and below it
        self.board = board
        self.row_num = row_num
        # Holds the current row total
        self.current_sum = 0
        # Holds the current number while travelling down the row valid or not
        self.current_num = 0
        # Set to True when the current number is adjacent to a symbol
        self.is_valid_engine_number = False
        self.current_gear_ratio = 0

    # Adds currently held number to the total
    def add_to_total(self):
        self.current_sum += self.current_num
        self.current_num = 0
        return

    # Adds parameter to currently held number
    def add_to_sum(self, num: int):
        self.current_num = self.current_num * 10 + num
        return
    
    def add_to_gear_ratio(self, num: int):
        self.add_to_gear_ratio = self.current_gear_ratio + num

    # Processes the current square and adds to total if necessary
    def process_square_for_sum(self, i: int, j: int):
        # Check if current square is a number
        if (self.board.check_square_status(i, j) == TileStatus.DIGIT):
            self.add_to_sum(int(self.board.input[i][j]))
        
        
        # Check above and below square for symbol to enter a valid state
        if (self.board.check_square_status(i - 1, j) == TileStatus.SYMBOL or
            self.board.check_square_status(i + 1, j) == TileStatus.SYMBOL):
            self.is_valid_engine_number = True
        
        
        # Current number becomes valid and next one as well
        if ((self.board.check_square_status(i, j) == TileStatus.DOT and self.is_valid_engine_number) or
            (self.board.check_square_status(i, j) == TileStatus.SYMBOL)):
            self.is_valid_engine_number = True
            self.add_to_total()


        # Check if current square is a dot
        if (self.board.check_square_status(i, j) == TileStatus.DOT):
            if (self.board.check_square_status(i - 1, j) != TileStatus.SYMBOL and
                self.board.check_square_status(i + 1, j) != TileStatus.SYMBOL):
                self.is_valid_engine_number = False
                self.current_num = 0
        
        return

    # Returns the sum of the engine parts in the current row
    def sum_of_row(self) -> int:
        for i in range(0, self.board.length + 1):
            self.process_square_for_sum(self.row_num, i)
        return self.current_sum
    
    # Returns the gear ratio at position (i, j)
    def calculate_gear_ratio_for_gear(self, i: int, j: int) -> int:
        # Check for exactly 2 adjacent engine parts
        connected_gear_parts = 0
        if (self.board.check_square_status(i, j - 1) == TileStatus.DIGIT):
            connected_gear_parts += 1
        if (self.board.check_square_status(i, j + 1) == TileStatus.DIGIT):
            connected_gear_parts += 1
        connected_gear_parts += self.board.num_gear_connections_in_adjacent_row(i - 1, j)
        connected_gear_parts += self.board.num_gear_connections_in_adjacent_row(i + 1, j)

        if (connected_gear_parts != 2):
            return 0
        
        gear_ratio = 1
        # Add left and right adjacent values
        left_value = self.board.value_going_left(i, j - 1)
        if (len(left_value) > 0):
            gear_ratio *= int(left_value)
        right_value = self.board.value_going_right(i, j + 1)
        if (len(right_value) > 0):
            gear_ratio *= int(right_value)
        
        # Add values from row above and below
        gear_ratio *= self.board.value_gear_ratio_in_adjacent_row(i - 1, j)
        gear_ratio *= self.board.value_gear_ratio_in_adjacent_row(i + 1, j)
            
        return gear_ratio
    
    # Finds gears in input board and adds their gear ratios
    def gear_ratio(self) -> int:
        for j in range(0, self.board.length):
            if (self.board.check_square_status(self.row_num, j) == TileStatus.SYMBOL and self.board.input[self.row_num][j] == '*'):
                gear_ratio = self.calculate_gear_ratio_for_gear(self.row_num, j)
                self.current_gear_ratio += gear_ratio
        return self.current_gear_ratio

            
        

def main():
    with open('./day3/day3_input.txt', 'r') as input_file:
        input_grid = []
        # Set input_grid's values
        for line in input_file:
            input_grid.append(line.strip())
        board = Board(input_grid)
        # print("Grand total is: " + str(board.sum_of_part_numbers()))
        print ("Gear ratio is: " + str(board.sum_of_gear_ratios()))

    return 0

if __name__ == "__main__":
    main()