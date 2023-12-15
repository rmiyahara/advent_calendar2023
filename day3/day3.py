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

    # Adds currently held number to the total
    def add_to_total(self):
        self.current_sum += self.current_num
        self.current_num = 0
        return

    # Adds parameter to currently held number
    def add_to_sum(self, num: int):
        self.current_num = self.current_num * 10 + num
        return

    def process_square(self, i: int, j: int):
        # Check if current square is a number
        if (self.board.check_square_status(i, j) == TileStatus.DIGIT):
            self.add_to_sum(int(self.board.input[i][j]))
        
        
        # Check above and below square for symbol
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
            self.process_square(self.row_num, i)
        return self.current_sum

            
        

def main():
    with open('./day3/day3_input.txt', 'r') as input_file:
        input_grid = []
        # Set input_grid's values
        for line in input_file:
            input_grid.append(line.strip())
        board = Board(input_grid)
        print("Grand total is:" + str(board.sum_of_part_numbers()))

    return 0

if __name__ == "__main__":
    main()