# Holds the inputted grid
from enum import Enum

class Board:
    def __init__(self, input_grid: list[str]):
        self.input = input_grid
        self.height = len(self.input)
        if (self.height < 1):
            self.length = 0
        else:
            self.length = len(self.input[0])
    
    def sum_of_part_numbers(self) -> int:
        total = 0
        for i in range(0, self.height):
            total = TileCrawler(i, self).sum_of_row()
        return total


# How do I know when to turn validation state off
# BUG: If a symbol is directly above or below, wrong numbers are picked up
class TileCrawler:

    # Enum for what possible states a tile can have
    class TileStatus(Enum):
        DOT = 1
        DIGIT = 2
        SYMBOL = 3

    def __init__(self, row_num: int,board: Board):
        # Holds the current row and the ones above and below it
        self.board = board
        self.row_num = row_num
        self.current_sum = 0
        self.current_num = 0
        self.is_valid_engine_number = False


    # Returns the status of the square in the desired location
    def check_square_status(self, i: int, j: int) -> TileStatus:
        # Check for out of bounds
        if (i < 0 or i >= self.board.length or
            j < 0 or j >= self.board.height or
            self.board.input[i][j] == '.'):
            return self.TileStatus.DOT
        elif (self.board.input[i][j].isdigit()):
            return self.TileStatus.DIGIT
        else:
            return self.TileStatus.SYMBOL

    def process_square(self, i: int, j: int):
        # Check above and below square for symbol
        if (self.check_square_status(i - 1, j) == self.TileStatus.SYMBOL or
            self.check_square_status(i + 1, j) == self.TileStatus.SYMBOL):
            self.is_valid_engine_number(True)
            return
        
        # Check if current square is a symbol
        if (self.check_square_status(i, j) == self.TileStatus.SYMBOL):
            print("Adding: " + str(self.current_num))
            self.current_sum += self.current_num
            self.current_num = 0
            self.is_valid_engine_number(True)
            return
        
        # Check if current square is a number
        if (self.check_square_status(i, j) == self.TileStatus.DIGIT):
            self.current_num = self.current_num * 10 + int(self.board.input[i][j])
            return
        
        # Check if current square is a dot
        if (self.check_square_status(i, j) == self.TileStatus.DOT):
            if (self.is_valid_engine_number):
                print("Adding: " + str(self.current_num))
                self.current_sum += self.current_num
                self.current_num = 0
            else:
                self.current_num = 0
            return
        
        return

    def sum_of_row(self) -> int:
        for i in range(0, self.board.length):
            self.process_square(self.row_num, i)
        return self.current_sum

            
        

def main():
    with open('./day3/day3_test_input.txt', 'r') as input_file:
        input_grid = []
        # Set input_grid's values
        for line in input_file:
            input_grid.append(line.strip())
        board = Board(input_grid)
        print("Grand total is:" + str(board.sum_of_part_numbers()))

    return 0

if __name__ == "__main__":
    main()